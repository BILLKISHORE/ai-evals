"""Offline tests for Crescendo multi-turn escalation generator."""

from __future__ import annotations

from ai_blackteam.generators.crescendo import CrescendoGenerator
from ai_blackteam.providers.base import BaseProvider, PromptResult


# ── Fake providers ──────────────────────────────────────────────────────


class FakeProvider(BaseProvider):
    """Provider whose responses depend on a heuristic over the prompt."""

    def __init__(self, judge_score: int = 3):
        super().__init__(model="fake-model")
        self.judge_score = judge_score
        self.prompt_calls: list[str] = []
        self.conversation_calls: list[list[dict]] = []

    def default_model(self) -> str:
        return "fake-model"

    def send_prompt(self, prompt, system_prompt=None):  # type: ignore[override]
        self.prompt_calls.append(prompt)
        if "Score 1-10" in prompt or "SCORE:" in prompt:
            return PromptResult(
                response=f"SCORE: {self.judge_score}",
                model="fake",
                provider="fake",
            )
        return PromptResult(
            response="I can't help with that.",
            model="fake",
            provider="fake",
        )

    def send_in_conversation(self, messages, system_prompt=None):  # type: ignore[override]
        self.conversation_calls.append(list(messages))
        last = messages[-1].get("content", "") if messages else ""
        # Attacker is asked to author next turn.
        if "Generate turn" in last or "Conversation so far" in last:
            return PromptResult(
                response="Could you walk me through the topic from a research angle?",
                model="fake",
                provider="fake",
            )
        # Target multi-turn: keep refusing by default.
        return PromptResult(
            response="I can't help with that.",
            model="fake",
            provider="fake",
        )


class HighScoreProvider(FakeProvider):
    def __init__(self):
        super().__init__(judge_score=9)


class EscalatingProvider(FakeProvider):
    """Judge yields 2, 4, 6, 9 - threshold crossed on turn 4."""

    def __init__(self):
        super().__init__(judge_score=1)
        self._judge_calls = 0

    def send_prompt(self, prompt, system_prompt=None):  # type: ignore[override]
        if "Score 1-10" in prompt or "SCORE:" in prompt:
            self._judge_calls += 1
            scores = [2, 4, 6, 9, 9, 9]
            score = scores[min(self._judge_calls - 1, len(scores) - 1)]
            self.prompt_calls.append(prompt)
            return PromptResult(
                response=f"SCORE: {score}",
                model="fake",
                provider="fake",
            )
        return super().send_prompt(prompt, system_prompt)


class SingleTurnOnlyProvider(FakeProvider):
    """Target only supports single-turn; conversation must be folded."""

    def send_in_conversation(self, messages, system_prompt=None):  # type: ignore[override]
        raise NotImplementedError("single turn only")


# ── Tests ───────────────────────────────────────────────────────────────


class TestCrescendoGenerator:
    def test_returns_expected_keys(self):
        gen = CrescendoGenerator()
        provider = FakeProvider(judge_score=2)
        result = gen.generate(
            target="test request",
            target_provider=provider,
            max_turns=3,
        )
        expected = {
            "success",
            "iterations",
            "best_score",
            "best_prompt",
            "best_response",
            "best_turn",
            "history",
        }
        assert set(result.keys()) == expected

    def test_runs_full_max_turns_when_no_success(self):
        gen = CrescendoGenerator()
        provider = FakeProvider(judge_score=2)
        result = gen.generate(
            target="test",
            target_provider=provider,
            max_turns=5,
            success_threshold=8,
        )
        assert result["success"] is False
        assert result["iterations"] == 5
        assert len(result["history"]) == 5

    def test_short_circuits_on_success(self):
        gen = CrescendoGenerator()
        provider = HighScoreProvider()
        result = gen.generate(
            target="test",
            target_provider=provider,
            max_turns=10,
            success_threshold=8,
        )
        assert result["success"] is True
        assert result["iterations"] == 1
        assert result["best_turn"] == 1
        assert result["best_score"] == 9

    def test_escalating_provider_succeeds_on_correct_turn(self):
        gen = CrescendoGenerator()
        provider = EscalatingProvider()
        result = gen.generate(
            target="test",
            target_provider=provider,
            max_turns=10,
            success_threshold=8,
        )
        assert result["success"] is True
        assert result["iterations"] == 4
        assert result["best_score"] == 9
        assert result["best_turn"] == 4

    def test_history_entries_have_expected_fields(self):
        gen = CrescendoGenerator()
        provider = FakeProvider(judge_score=3)
        result = gen.generate(
            target="test",
            target_provider=provider,
            max_turns=2,
        )
        for entry in result["history"]:
            assert {"turn", "prompt", "response", "score"} <= entry.keys()
            assert isinstance(entry["turn"], int)
            assert isinstance(entry["score"], int)

    def test_on_iteration_callback_fires_per_turn(self):
        gen = CrescendoGenerator()
        provider = FakeProvider(judge_score=2)
        calls: list[dict] = []

        def on_iter(turn, prompt, response, score):
            calls.append(
                {"turn": turn, "prompt": prompt, "score": score}
            )

        gen.generate(
            target="test",
            target_provider=provider,
            max_turns=3,
            on_iteration=on_iter,
        )
        assert len(calls) == 3
        assert calls[0]["turn"] == 1
        assert calls[2]["turn"] == 3

    def test_conversation_grows_each_turn(self):
        """Each turn should send a strictly longer conversation to the target."""
        gen = CrescendoGenerator()
        provider = FakeProvider(judge_score=2)
        gen.generate(
            target="test",
            target_provider=provider,
            max_turns=3,
        )
        target_calls = [
            c
            for c in provider.conversation_calls
            if c and c[-1].get("role") == "user" and "Generate turn" not in c[-1].get("content", "")
        ]
        # Multi-turn conversations sent to the target grow by 2 messages each round.
        assert len(target_calls) == 3
        lengths = [len(c) for c in target_calls]
        assert lengths == sorted(lengths)
        assert lengths[-1] > lengths[0]

    def test_falls_back_to_single_turn_when_provider_only_single_turn(self):
        gen = CrescendoGenerator()
        target_prov = SingleTurnOnlyProvider(judge_score=2)
        attacker_prov = FakeProvider(judge_score=2)
        judge_prov = FakeProvider(judge_score=2)
        result = gen.generate(
            target="test",
            target_provider=target_prov,
            attacker_provider=attacker_prov,
            judge_provider=judge_prov,
            max_turns=2,
        )
        assert result["iterations"] == 2
        # Target's send_prompt should have received folded transcripts with role markers.
        folded = [p for p in target_prov.prompt_calls if "USER:" in p]
        assert len(folded) == 2

    def test_separate_providers_each_invoked(self):
        gen = CrescendoGenerator()
        target_prov = FakeProvider(judge_score=2)
        attacker_prov = FakeProvider(judge_score=2)
        judge_prov = FakeProvider(judge_score=2)
        gen.generate(
            target="test",
            target_provider=target_prov,
            attacker_provider=attacker_prov,
            judge_provider=judge_prov,
            max_turns=2,
        )
        # attacker called once per turn for the next prompt
        attacker_authors = [
            c for c in attacker_prov.conversation_calls
            if c and "Generate turn" in c[-1].get("content", "")
        ]
        assert len(attacker_authors) == 2
        judge_calls = [p for p in judge_prov.prompt_calls if "Score 1-10" in p]
        assert len(judge_calls) == 2

    def test_unparseable_judge_falls_back_to_one(self):
        class BadJudge(FakeProvider):
            def send_prompt(self, prompt, system_prompt=None):
                if "Score 1-10" in prompt or "SCORE:" in prompt:
                    return PromptResult(
                        response="dunno",
                        model="fake",
                        provider="fake",
                    )
                return super().send_prompt(prompt, system_prompt)

        gen = CrescendoGenerator()
        provider = BadJudge()
        result = gen.generate(
            target="test",
            target_provider=provider,
            max_turns=2,
        )
        assert result["best_score"] == 1
        assert all(e["score"] == 1 for e in result["history"])

    def test_registered_in_generator_registry(self):
        from ai_blackteam.generators import crescendo  # noqa: F401
        from ai_blackteam.registry import generator_registry

        assert generator_registry.get("crescendo") is CrescendoGenerator
