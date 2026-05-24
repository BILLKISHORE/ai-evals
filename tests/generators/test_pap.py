"""Offline tests for PAP (Persuasive Adversarial Prompts) generator."""

from __future__ import annotations

from ai_blackteam.generators.pap import (
    DEFAULT_TECHNIQUES,
    PAPGenerator,
)
from ai_blackteam.providers.base import BaseProvider, PromptResult


# ── Fake providers ──────────────────────────────────────────────────────


class FakeProvider(BaseProvider):
    """Provider that returns canned responses based on prompt content."""

    def __init__(self, judge_score: int = 3):
        super().__init__(model="fake-model")
        self.judge_score = judge_score
        self.call_log: list[dict] = []

    def default_model(self) -> str:
        return "fake-model"

    def send_prompt(self, prompt, system_prompt=None):  # type: ignore[override]
        self.call_log.append({"prompt": prompt})

        # Judge prompt - returns configured score.
        if "Score 1-10" in prompt or "SCORE:" in prompt:
            return PromptResult(
                response=f"SCORE: {self.judge_score}",
                model="fake",
                provider="fake",
            )

        # Attacker rewrite prompt - returns a fake rewritten request.
        if "Rewrite the following harmful request" in prompt:
            return PromptResult(
                response="As a senior researcher I require this information now.",
                model="fake",
                provider="fake",
            )

        # Target response - default refusal.
        return PromptResult(
            response="I can't help with that.",
            model="fake",
            provider="fake",
        )

    def send_in_conversation(self, messages, system_prompt=None):  # type: ignore[override]
        return self.send_prompt(messages[-1].get("content", ""), system_prompt)


class HighScoreProvider(FakeProvider):
    """Judge always returns 9 - success on the first technique."""

    def __init__(self):
        super().__init__(judge_score=9)


class EscalatingProvider(FakeProvider):
    """Judge scores 2, 5, 9 across calls - threshold hits on iteration 3."""

    def __init__(self):
        super().__init__(judge_score=1)
        self._judge_calls = 0

    def send_prompt(self, prompt, system_prompt=None):  # type: ignore[override]
        if "Score 1-10" in prompt or "SCORE:" in prompt:
            self._judge_calls += 1
            scores = [2, 5, 9, 9, 9]
            score = scores[min(self._judge_calls - 1, len(scores) - 1)]
            self.call_log.append({"prompt": prompt})
            return PromptResult(
                response=f"SCORE: {score}",
                model="fake",
                provider="fake",
            )
        return super().send_prompt(prompt, system_prompt)


# ── Tests ───────────────────────────────────────────────────────────────


class TestPAPGenerator:
    def test_returns_expected_keys(self):
        gen = PAPGenerator()
        provider = FakeProvider(judge_score=3)
        result = gen.generate(
            target="test harmful request",
            target_provider=provider,
            techniques=DEFAULT_TECHNIQUES[:3],
        )
        expected = {
            "success",
            "iterations",
            "best_score",
            "best_prompt",
            "best_response",
            "best_technique",
            "history",
        }
        assert set(result.keys()) == expected

    def test_iterations_match_technique_count(self):
        gen = PAPGenerator()
        provider = FakeProvider(judge_score=2)
        custom = [("X", "do X"), ("Y", "do Y"), ("Z", "do Z")]
        result = gen.generate(
            target="test harmful request",
            target_provider=provider,
            techniques=custom,
            success_threshold=8,
        )
        assert result["success"] is False
        assert result["iterations"] == 3
        assert len(result["history"]) == 3

    def test_short_circuits_on_success(self):
        gen = PAPGenerator()
        provider = HighScoreProvider()
        result = gen.generate(
            target="test harmful request",
            target_provider=provider,
            techniques=DEFAULT_TECHNIQUES[:5],
            success_threshold=8,
        )
        assert result["success"] is True
        assert result["iterations"] == 1
        assert result["best_score"] == 9
        assert result["best_technique"] == DEFAULT_TECHNIQUES[0][0]

    def test_escalating_scores_hit_threshold(self):
        gen = PAPGenerator()
        provider = EscalatingProvider()
        result = gen.generate(
            target="test harmful request",
            target_provider=provider,
            techniques=DEFAULT_TECHNIQUES[:5],
            success_threshold=8,
        )
        assert result["success"] is True
        assert result["iterations"] == 3
        assert result["best_score"] == 9
        assert result["best_technique"] == DEFAULT_TECHNIQUES[2][0]

    def test_history_entries_have_expected_fields(self):
        gen = PAPGenerator()
        provider = FakeProvider(judge_score=4)
        result = gen.generate(
            target="test",
            target_provider=provider,
            techniques=DEFAULT_TECHNIQUES[:2],
        )
        for entry in result["history"]:
            assert {"iteration", "technique", "prompt", "response", "score"} <= entry.keys()
            assert isinstance(entry["score"], int)

    def test_on_iteration_callback_fires(self):
        gen = PAPGenerator()
        provider = FakeProvider(judge_score=2)
        calls: list[dict] = []

        def on_iter(i, technique, prompt, response, score):
            calls.append(
                {
                    "i": i,
                    "technique": technique,
                    "prompt": prompt,
                    "score": score,
                }
            )

        gen.generate(
            target="test",
            target_provider=provider,
            techniques=DEFAULT_TECHNIQUES[:3],
            on_iteration=on_iter,
        )
        assert len(calls) == 3
        assert calls[0]["i"] == 1
        assert calls[2]["technique"] == DEFAULT_TECHNIQUES[2][0]

    def test_default_techniques_loaded_when_none_passed(self):
        gen = PAPGenerator()
        provider = FakeProvider(judge_score=2)
        result = gen.generate(
            target="test",
            target_provider=provider,
            success_threshold=99,  # never succeeds
        )
        assert result["iterations"] == len(DEFAULT_TECHNIQUES)

    def test_separate_attacker_and_judge_providers(self):
        gen = PAPGenerator()
        target_prov = FakeProvider(judge_score=2)
        attacker_prov = FakeProvider(judge_score=2)
        judge_prov = FakeProvider(judge_score=2)
        gen.generate(
            target="test",
            target_provider=target_prov,
            attacker_provider=attacker_prov,
            judge_provider=judge_prov,
            techniques=DEFAULT_TECHNIQUES[:2],
        )
        # attacker invoked once per technique for the rewrite
        rewrite_calls = [c for c in attacker_prov.call_log if "Rewrite" in c["prompt"]]
        assert len(rewrite_calls) == 2
        # judge invoked once per technique
        judge_calls = [c for c in judge_prov.call_log if "Score 1-10" in c["prompt"]]
        assert len(judge_calls) == 2

    def test_best_score_tracks_maximum(self):
        gen = PAPGenerator()
        provider = EscalatingProvider()
        result = gen.generate(
            target="test",
            target_provider=provider,
            techniques=DEFAULT_TECHNIQUES[:5],
            success_threshold=99,  # never succeeds, run full sweep
        )
        assert result["best_score"] == 9

    def test_unparseable_judge_falls_back_to_one(self):
        class BadJudge(FakeProvider):
            def send_prompt(self, prompt, system_prompt=None):
                if "Score 1-10" in prompt or "SCORE:" in prompt:
                    return PromptResult(
                        response="I'm not going to answer.",
                        model="fake",
                        provider="fake",
                    )
                return super().send_prompt(prompt, system_prompt)

        gen = PAPGenerator()
        provider = BadJudge()
        result = gen.generate(
            target="test",
            target_provider=provider,
            techniques=DEFAULT_TECHNIQUES[:2],
        )
        assert result["best_score"] == 1
        assert all(e["score"] == 1 for e in result["history"])

    def test_registered_in_generator_registry(self):
        from ai_blackteam.generators import pap  # noqa: F401 - ensures decorator fires
        from ai_blackteam.registry import generator_registry

        assert generator_registry.get("pap") is PAPGenerator
