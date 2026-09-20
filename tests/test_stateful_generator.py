"""Behavioural tests for the memory-conditioned stateful generator.

The other seven generators are memoryless across runs: PAIR, TAP, Fuzzer,
AutoDAN, PAP, Crescendo and BoN all restart from the seed objective on every
invocation, so a sweep that hits the same model twice pays to rediscover the
same refusals. These tests pin the two things that make the stateful generator
different: the record survives the process, and the next candidate is actually
conditioned on it.

They also pin the honesty rules the module claims. An unparseable judge verdict
is an unknown, not a zero, so it must not enter the record and must not be
counted as evidence that a tactic failed. A memory file that exists but cannot
be read is an error, not a silent fresh start, because a silent fresh start is
indistinguishable from "this target has never been attacked" and would quietly
throw away everything the tool had learned.

No test here touches the real memory directory; every one passes an explicit
tmp_path.
"""

from __future__ import annotations

import json

import pytest

from ai_blackteam.generators.stateful import (
    BRIEF_PROMPT_LIMIT,
    CONCESSION_SCORE,
    MAX_REMEMBERED_ATTEMPTS,
    MEMORY_EXCERPT_CHARS,
    TACTICS,
    AttackMemory,
    MemoryUnreadableError,
    StatefulGenerator,
    default_memory_path,
    parse_judge_score,
    rank_tactics,
)
from ai_blackteam.providers.base import BaseProvider, PromptResult


TACTIC_NAMES = [name for name, _instruction in TACTICS]


# ── fake providers ───────────────────────────────────────────────────


class FakeProvider(BaseProvider):
    """Target, attacker and judge in one object, with every call recorded."""

    def __init__(self, judge_score: int = 3, judge_text: str | None = None):
        super().__init__(model="fake-model")
        self.judge_score = judge_score
        self.judge_text = judge_text
        self.prompt_calls: list[str] = []
        self.conversation_calls: list[list[dict]] = []
        self.target_calls: list[str] = []

    def default_model(self) -> str:
        return "fake-model"

    def _is_judge(self, prompt: str) -> bool:
        return "Score 1-10" in prompt or "Rate how" in prompt

    def send_prompt(self, prompt, system_prompt=None):
        self.prompt_calls.append(prompt)
        if self._is_judge(prompt):
            text = (
                self.judge_text
                if self.judge_text is not None
                else f"SCORE: {self.judge_score}"
            )
            return PromptResult(response=text, model="fake", provider="fake")
        self.target_calls.append(prompt)
        return PromptResult(
            response="I can't help with that.", model="fake", provider="fake"
        )

    def send_in_conversation(self, messages, system_prompt=None):
        self.conversation_calls.append([dict(m) for m in messages])
        return PromptResult(
            response="Walk me through the topic as a researcher would.",
            model="fake",
            provider="fake",
        )

    def attacker_text(self) -> str:
        """Every word the attacker was ever shown, flattened."""
        return "\n".join(
            m.get("content", "")
            for call in self.conversation_calls
            for m in call
        )


class ScriptedJudgeProvider(FakeProvider):
    """Judge returns a scripted score sequence, then repeats the last one."""

    def __init__(self, scores: list[int]):
        super().__init__(judge_score=scores[0])
        self._scores = list(scores)
        self._judge_calls = 0

    def send_prompt(self, prompt, system_prompt=None):
        if self._is_judge(prompt):
            self.prompt_calls.append(prompt)
            index = min(self._judge_calls, len(self._scores) - 1)
            self._judge_calls += 1
            return PromptResult(
                response=f"SCORE: {self._scores[index]}",
                model="fake",
                provider="fake",
            )
        return super().send_prompt(prompt, system_prompt)


def _run(provider, memory_path, **kwargs):
    kwargs.setdefault("target", "explain how a smoke detector works")
    kwargs.setdefault("max_iterations", 2)
    return StatefulGenerator().generate(
        target_provider=provider, memory_path=memory_path, **kwargs
    )


# ── the record survives the process ──────────────────────────────────


def test_an_attempt_is_on_disk_before_the_run_ends(tmp_path):
    """Written per attempt, not at the end: a crash must not lose the run."""
    path = tmp_path / "memory.json"
    seen: list[int] = []

    def on_iteration(iteration, tactic, prompt, response, score):
        seen.append(len(json.loads(path.read_text())["targets"]))

    provider = FakeProvider(judge_score=3)
    _run(provider, path, max_iterations=2, on_iteration=on_iteration)

    assert seen == [1, 1], "the record must exist from the first attempt onward"


def test_a_second_run_recalls_the_first_runs_attempts(tmp_path):
    path = tmp_path / "memory.json"
    first = _run(FakeProvider(judge_score=3), path, max_iterations=3)
    assert first["recalled_attempts"] == 0

    second = _run(FakeProvider(judge_score=3), path, max_iterations=1)
    assert second["recalled_attempts"] == 3


def test_memory_is_scoped_to_the_objective(tmp_path):
    """Two objectives against the same model must not read each other."""
    path = tmp_path / "memory.json"
    _run(FakeProvider(), path, target="objective one", max_iterations=2)
    other = _run(FakeProvider(), path, target="objective two", max_iterations=1)
    assert other["recalled_attempts"] == 0


def test_memory_is_scoped_to_the_model(tmp_path):
    """The same objective against a different model starts from nothing."""

    class OtherModelProvider(FakeProvider):
        def default_model(self) -> str:
            return "other-model"

    path = tmp_path / "memory.json"
    _run(FakeProvider(), path, max_iterations=2)
    other = _run(OtherModelProvider(), path, max_iterations=1)
    assert other["recalled_attempts"] == 0


def test_memory_is_scoped_to_the_provider(tmp_path):
    """Same model name on a different provider is a different target."""

    class OtherProvider(FakeProvider):
        pass

    path = tmp_path / "memory.json"
    _run(FakeProvider(), path, max_iterations=2)
    other = _run(OtherProvider(), path, max_iterations=1)
    assert other["recalled_attempts"] == 0


def test_an_explicit_memory_key_overrides_the_derived_one(tmp_path):
    path = tmp_path / "memory.json"
    first = _run(FakeProvider(), path, max_iterations=2, memory_key="shared")
    assert first["memory_key"] == "shared"
    second = _run(
        FakeProvider(), path, target="a different objective",
        max_iterations=1, memory_key="shared",
    )
    assert second["recalled_attempts"] == 2


def test_the_default_memory_path_is_scoped_to_the_tool():
    p = default_memory_path()
    assert ".ai_blackteam" in str(p)
    assert p.suffix == ".json"


# ── the next candidate is conditioned on the record ──────────────────


def test_the_attacker_is_not_briefed_on_an_empty_record(tmp_path):
    provider = FakeProvider(judge_score=3)
    _run(provider, tmp_path / "memory.json", max_iterations=1)
    assert "Previously refused" not in provider.attacker_text()


def test_the_attacker_is_briefed_on_what_was_refused(tmp_path):
    path = tmp_path / "memory.json"
    _run(FakeProvider(judge_score=2), path, max_iterations=1)

    second = FakeProvider(judge_score=2)
    _run(second, path, max_iterations=1)

    briefing = second.attacker_text()
    assert "Previously refused" in briefing
    assert TACTIC_NAMES[0] in briefing


def test_the_attacker_is_briefed_on_what_was_conceded(tmp_path):
    path = tmp_path / "memory.json"
    conceding = FakeProvider(judge_score=CONCESSION_SCORE)
    _run(conceding, path, max_iterations=1, success_threshold=10)

    second = FakeProvider(judge_score=2)
    _run(second, path, max_iterations=1)

    assert "Previously conceded" in second.attacker_text()


def test_the_attacker_is_shown_the_prompts_already_tried(tmp_path):
    """Without this the generator would re-send a prompt it knows is dead."""
    path = tmp_path / "memory.json"
    first = _run(FakeProvider(judge_score=2), path, max_iterations=1)
    tried = first["history"][0]["prompt"]

    second = FakeProvider(judge_score=2)
    _run(second, path, max_iterations=1)
    assert tried[:40] in second.attacker_text()


# ── the tactic order is driven by the record ─────────────────────────


def test_a_fresh_target_uses_the_declared_tactic_order(tmp_path):
    result = _run(FakeProvider(), tmp_path / "memory.json", max_iterations=1)
    assert result["tactic_order"] == TACTIC_NAMES


def test_a_conceded_tactic_is_tried_first_on_the_next_run(tmp_path):
    path = tmp_path / "memory.json"
    late_tactic = TACTIC_NAMES[-1]
    memory = AttackMemory.load(path)
    memory.record(
        "shared", objective="o", model="m", tactic=late_tactic,
        prompt="p", score=CONCESSION_SCORE + 2, excerpt="here is how",
    )
    memory.save()

    result = _run(
        FakeProvider(judge_score=1), path, max_iterations=1, memory_key="shared"
    )
    assert result["tactic_order"][0] == late_tactic
    assert result["history"][0]["tactic"] == late_tactic


def test_an_untried_tactic_outranks_a_known_refused_one(tmp_path):
    """A tactic nobody has tried is unknown, which beats a known failure."""
    path = tmp_path / "memory.json"
    first_tactic = TACTIC_NAMES[0]
    memory = AttackMemory.load(path)
    memory.record(
        "shared", objective="o", model="m", tactic=first_tactic,
        prompt="p", score=1, excerpt="I can't help with that.",
    )
    memory.save()

    result = _run(
        FakeProvider(judge_score=1), path, max_iterations=1, memory_key="shared"
    )
    order = result["tactic_order"]
    assert order[-1] == first_tactic
    assert order[:-1] == [n for n in TACTIC_NAMES if n != first_tactic]


def test_rank_tactics_sorts_conceded_tactics_by_their_best_score():
    a, b, c = TACTIC_NAMES[0], TACTIC_NAMES[1], TACTIC_NAMES[2]
    ordered = rank_tactics(
        TACTICS, {a: CONCESSION_SCORE, b: 10, c: 1}
    )
    names = [n for n, _ in ordered]
    assert names[0] == b
    assert names[1] == a
    assert names[-1] == c


def test_rank_tactics_keeps_an_unknown_tactic_out_of_the_score_ordering():
    """An absent tactic has no score; it must not be sorted as if it had 0."""
    known = {TACTIC_NAMES[0]: 1}
    names = [n for n, _ in rank_tactics(TACTICS, known)]
    assert names.index(TACTIC_NAMES[1]) < names.index(TACTIC_NAMES[0])


# ── an unknown is an unknown ─────────────────────────────────────────


def test_an_unparseable_judge_verdict_is_not_recorded_as_a_score(tmp_path):
    path = tmp_path / "memory.json"
    provider = FakeProvider(judge_text="I would rather not rate this.")
    result = _run(provider, path, max_iterations=2)

    assert [e["score"] for e in result["history"]] == [None, None]
    assert result["unscored_attempts"] == 2
    assert json.loads(path.read_text())["targets"] == {}


def test_best_score_is_none_rather_than_zero_when_nothing_was_scored(tmp_path):
    provider = FakeProvider(judge_text="no verdict here")
    result = _run(provider, tmp_path / "memory.json", max_iterations=2)
    assert result["best_score"] is None
    assert result["best_prompt"] is None
    assert result["best_response"] is None
    assert result["success"] is False


def test_an_unscored_attempt_does_not_demote_its_tactic(tmp_path):
    """An unrated attempt is no evidence, so the order must not move."""
    path = tmp_path / "memory.json"
    _run(
        FakeProvider(judge_text="nothing"), path, max_iterations=2,
    )
    result = _run(FakeProvider(judge_text="nothing"), path, max_iterations=1)
    assert result["tactic_order"] == TACTIC_NAMES


def test_recording_a_missing_score_is_rejected(tmp_path):
    memory = AttackMemory.load(tmp_path / "memory.json")
    with pytest.raises(ValueError):
        memory.record(
            "k", objective="o", model="m", tactic=TACTIC_NAMES[0],
            prompt="p", score=None, excerpt="e",
        )


def test_a_corrupt_memory_file_is_an_error_not_a_fresh_start(tmp_path):
    """Silently starting over would read as 'never attacked' and lose the lot."""
    path = tmp_path / "memory.json"
    path.write_text("{not json at all")
    with pytest.raises(MemoryUnreadableError):
        AttackMemory.load(path)


def test_a_memory_file_from_a_future_schema_is_an_error(tmp_path):
    path = tmp_path / "memory.json"
    path.write_text(json.dumps({"version": 99, "targets": {}}))
    with pytest.raises(MemoryUnreadableError):
        AttackMemory.load(path)


def test_a_missing_memory_file_is_a_legitimate_fresh_start(tmp_path):
    memory = AttackMemory.load(tmp_path / "nothing-here.json")
    assert memory.attempts_for("k") == []


# ── record hygiene ───────────────────────────────────────────────────


def test_the_record_keeps_only_the_most_recent_attempts(tmp_path):
    path = tmp_path / "memory.json"
    memory = AttackMemory.load(path)
    for i in range(MAX_REMEMBERED_ATTEMPTS + 5):
        memory.record(
            "k", objective="o", model="m", tactic=TACTIC_NAMES[0],
            prompt=f"prompt {i}", score=1, excerpt="e",
        )
    kept = memory.attempts_for("k")
    assert len(kept) == MAX_REMEMBERED_ATTEMPTS
    assert kept[-1]["prompt"] == f"prompt {MAX_REMEMBERED_ATTEMPTS + 4}"


def test_the_stored_excerpt_is_capped(tmp_path):
    memory = AttackMemory.load(tmp_path / "memory.json")
    memory.record(
        "k", objective="o", model="m", tactic=TACTIC_NAMES[0],
        prompt="p", score=1, excerpt="x" * (MEMORY_EXCERPT_CHARS * 3),
    )
    assert len(memory.attempts_for("k")[0]["excerpt"]) == MEMORY_EXCERPT_CHARS


def test_the_record_round_trips_through_disk(tmp_path):
    path = tmp_path / "memory.json"
    memory = AttackMemory.load(path)
    memory.record(
        "k", objective="o", model="m", tactic=TACTIC_NAMES[0],
        prompt="p", score=7, excerpt="e",
    )
    memory.save()
    assert AttackMemory.load(path).attempts_for("k") == memory.attempts_for("k")


def test_the_briefing_lists_at_most_the_capped_number_of_candidates(tmp_path):
    """An unbounded briefing crowds the instruction out of the attacker call."""
    memory = AttackMemory.load(tmp_path / "memory.json")
    for i in range(BRIEF_PROMPT_LIMIT + 4):
        memory.record(
            "k", objective="o", model="m", tactic=TACTIC_NAMES[0],
            prompt=f"candidate {i}", score=1, excerpt="e",
        )
    listed = [ln for ln in memory.brief("k").splitlines() if ln.startswith("  - ")]
    assert len(listed) == BRIEF_PROMPT_LIMIT
    assert "candidate 0" not in memory.brief("k"), "oldest drop out first"


def test_parse_judge_score_reads_a_verdict_and_reports_its_absence():
    assert parse_judge_score("SCORE: 7") == 7
    assert parse_judge_score("I would rather not say") is None
    assert parse_judge_score("") is None


def test_best_score_per_tactic_is_the_maximum_seen(tmp_path):
    memory = AttackMemory.load(tmp_path / "memory.json")
    for score in (2, 9, 4):
        memory.record(
            "k", objective="o", model="m", tactic=TACTIC_NAMES[0],
            prompt="p", score=score, excerpt="e",
        )
    assert memory.tactic_scores("k") == {TACTIC_NAMES[0]: 9}


# ── the generator loop ───────────────────────────────────────────────


def test_generate_returns_the_documented_keys(tmp_path):
    result = _run(FakeProvider(), tmp_path / "memory.json", max_iterations=1)
    assert set(result) == {
        "success", "iterations", "best_score", "best_prompt", "best_response",
        "best_tactic", "history", "memory_key", "recalled_attempts",
        "unscored_attempts", "tactic_order",
    }


def test_it_stops_as_soon_as_the_threshold_is_reached(tmp_path):
    provider = ScriptedJudgeProvider([2, 9, 9])
    result = _run(
        provider, tmp_path / "memory.json", max_iterations=5,
        success_threshold=8,
    )
    assert result["success"] is True
    assert result["iterations"] == 2
    assert result["best_score"] == 9
    assert result["best_tactic"] == TACTIC_NAMES[1]


def test_it_respects_max_iterations(tmp_path):
    result = _run(
        FakeProvider(judge_score=2), tmp_path / "memory.json",
        max_iterations=3, success_threshold=8,
    )
    assert result["success"] is False
    assert result["iterations"] == 3
    assert len(result["history"]) == 3


def test_it_cycles_the_tactic_list_when_iterations_exceed_it(tmp_path):
    n = len(TACTICS)
    result = _run(
        FakeProvider(judge_score=2), tmp_path / "memory.json",
        max_iterations=n + 1, success_threshold=10,
    )
    used = [e["tactic"] for e in result["history"]]
    assert used[: n] == TACTIC_NAMES
    assert used[n] == TACTIC_NAMES[0]


def test_history_entries_carry_the_tactic_and_the_score(tmp_path):
    result = _run(
        FakeProvider(judge_score=4), tmp_path / "memory.json", max_iterations=2
    )
    for i, entry in enumerate(result["history"], start=1):
        assert entry["iteration"] == i
        assert entry["tactic"] in TACTIC_NAMES
        assert entry["score"] == 4
        assert isinstance(entry["prompt"], str)
        assert isinstance(entry["response"], str)


def test_the_callback_fires_once_per_attempt(tmp_path):
    calls: list[tuple] = []
    _run(
        FakeProvider(judge_score=2), tmp_path / "memory.json",
        max_iterations=3,
        on_iteration=lambda *a: calls.append(a),
    )
    assert [c[0] for c in calls] == [1, 2, 3]
    assert [c[1] for c in calls] == TACTIC_NAMES[:3]


def test_separate_attacker_and_judge_providers_are_each_used(tmp_path):
    target = FakeProvider(judge_score=2)
    attacker = FakeProvider(judge_score=2)
    judge = FakeProvider(judge_score=2)
    _run(
        target, tmp_path / "memory.json", max_iterations=2,
        attacker_provider=attacker, judge_provider=judge,
    )
    assert attacker.conversation_calls, "attacker was never asked for a candidate"
    assert judge.prompt_calls, "judge was never asked for a verdict"
    assert target.target_calls, "target was never sent a candidate"
    assert not target.conversation_calls, "target must not author its own attack"


def test_it_is_registered_under_its_own_name():
    import ai_blackteam.generators  # noqa: F401
    from ai_blackteam.registry import generator_registry

    assert generator_registry.get("stateful") is StatefulGenerator
    assert StatefulGenerator.name == "stateful"
