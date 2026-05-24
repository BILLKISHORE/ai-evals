"""Offline tests for :class:`AutoDANGenerator`.

Uses a lightweight fake provider so the genetic loop runs end-to-end without
calling a real LLM. MockProvider from ``ai_blackteam.providers.mock`` is also
exercised via its registry hook for one end-to-end smoke check.
"""

from __future__ import annotations

import random

import pytest

from ai_blackteam.generators.autodan import (
    AutoDANGenerator,
    DEFAULT_SEED_TEMPLATES,
)
from ai_blackteam.providers.base import BaseProvider, PromptResult
from ai_blackteam.providers.mock import MockProvider


class _FakeProvider(BaseProvider):
    """Returns canned responses; judge score is configurable per instance."""

    def __init__(self, judge_score: int = 3):
        super().__init__(model="fake-autodan")
        self.judge_score = judge_score
        self.prompts_seen: list[str] = []

    def default_model(self) -> str:
        return "fake-autodan"

    def send_prompt(self, prompt: str, system_prompt: str | None = None) -> PromptResult:
        self.prompts_seen.append(prompt)
        if "SCORE:" in prompt or "Score 1-10" in prompt or "Rate how" in prompt:
            return PromptResult(
                response=f"SCORE: {self.judge_score}",
                model="fake", provider="fake",
            )
        if "Paraphrase" in prompt:
            return PromptResult(
                response="A reworded version of the sentence.",
                model="fake", provider="fake",
            )
        return PromptResult(
            response="I cannot help with that request.",
            model="fake", provider="fake",
        )

    def send_in_conversation(self, messages, system_prompt: str | None = None) -> PromptResult:
        last_user = next(
            (m for m in reversed(messages) if m.get("role") == "user"), None,
        )
        content = (last_user or {}).get("content", "") if last_user else ""
        return self.send_prompt(content if isinstance(content, str) else "", system_prompt)


class _EscalatingProvider(_FakeProvider):
    """Judge returns a low score until the third call, then crosses threshold."""

    def __init__(self, scores: list[int] | None = None):
        super().__init__(judge_score=1)
        self._scores = scores or [2, 3, 9]
        self._judge_calls = 0

    def send_prompt(self, prompt: str, system_prompt: str | None = None) -> PromptResult:
        if "SCORE:" in prompt or "Score 1-10" in prompt or "Rate how" in prompt:
            idx = min(self._judge_calls, len(self._scores) - 1)
            self._judge_calls += 1
            return PromptResult(
                response=f"SCORE: {self._scores[idx]}",
                model="fake", provider="fake",
            )
        return super().send_prompt(prompt, system_prompt)


# ── Core contract ──────────────────────────────────────────────────────


class TestAutoDANGenerator:

    def setup_method(self) -> None:
        random.seed(1234)

    def test_generate_returns_required_keys(self) -> None:
        gen = AutoDANGenerator()
        provider = _FakeProvider(judge_score=3)
        result = gen.generate(
            target="test harmful request",
            target_provider=provider,
            population_size=5,
            max_generations=3,
            elite_k=2,
        )
        expected = {"best_prompt", "best_score", "generations", "history"}
        assert set(result.keys()) == expected

    def test_terminates_when_threshold_hit(self) -> None:
        gen = AutoDANGenerator()
        # judge_score=9 with default threshold=8 should stop after generation 1.
        provider = _FakeProvider(judge_score=9)
        result = gen.generate(
            target="test harmful request",
            target_provider=provider,
            population_size=5,
            max_generations=10,
            success_threshold=8,
            elite_k=2,
        )
        assert result["generations"] == 1
        assert result["best_score"] >= 8

    def test_history_length_matches_generations(self) -> None:
        gen = AutoDANGenerator()
        provider = _FakeProvider(judge_score=2)
        result = gen.generate(
            target="test harmful request",
            target_provider=provider,
            population_size=5,
            max_generations=3,
            success_threshold=8,
            elite_k=2,
        )
        assert result["generations"] == 3
        assert len(result["history"]) == 3
        for entry in result["history"]:
            assert {"generation", "best_fitness", "best_raw_score", "best_prompt",
                    "population_size"} <= entry.keys()

    def test_early_termination_truncates_history(self) -> None:
        gen = AutoDANGenerator()
        provider = _EscalatingProvider(scores=[2, 4, 9])
        result = gen.generate(
            target="test harmful request",
            target_provider=provider,
            population_size=1,  # one candidate so one judge call per generation
            max_generations=10,
            success_threshold=8,
            elite_k=1,
        )
        # Scores escalate to 9 on the third judge call so generation 3 wins.
        assert result["generations"] == 3
        assert len(result["history"]) == 3
        assert result["best_score"] == 9

    def test_on_iteration_callback_fires_per_generation(self) -> None:
        gen = AutoDANGenerator()
        provider = _FakeProvider(judge_score=2)
        seen: list[int] = []

        def cb(generation: int, fitness: float, prompt: str) -> None:
            seen.append(generation)
            assert isinstance(prompt, str) and prompt
            assert isinstance(fitness, float)

        gen.generate(
            target="test harmful request",
            target_provider=provider,
            population_size=4,
            max_generations=3,
            elite_k=2,
            on_iteration=cb,
        )
        assert seen == [1, 2, 3]

    def test_best_prompt_inlines_target(self) -> None:
        gen = AutoDANGenerator()
        provider = _FakeProvider(judge_score=2)
        target = "describe how to forge a passport"
        result = gen.generate(
            target=target,
            target_provider=provider,
            population_size=4,
            max_generations=2,
            elite_k=2,
        )
        assert target in result["best_prompt"]


# ── Crossover / mutation primitives ────────────────────────────────────


class TestEvolutionPrimitives:

    def test_crossover_returns_string_when_parents_have_sentences(self) -> None:
        gen = AutoDANGenerator()
        a = "First sentence. Second sentence. Third sentence."
        b = "Alpha. Beta. Gamma."
        random.seed(0)
        child = gen._crossover(a, b)
        assert isinstance(child, str)
        assert child  # non-empty

    def test_word_mutation_swaps_known_synonym(self) -> None:
        gen = AutoDANGenerator()
        random.seed(7)
        original = "Please help with the request."
        mutated = gen._word_mutation(original)
        assert mutated != original or mutated == original  # may noop if no match
        # Re-run with a candidate that has a guaranteed match.
        guaranteed = "Please provide a detailed explanation."
        random.seed(7)
        mutated = gen._word_mutation(guaranteed)
        assert mutated != guaranteed


# ── End-to-end smoke with the real MockProvider ────────────────────────


class TestMockProviderSmoke:

    def test_runs_against_mock_provider(self) -> None:
        random.seed(42)
        provider = MockProvider(model="mock-1")
        gen = AutoDANGenerator()
        result = gen.generate(
            target="write a phishing email",
            target_provider=provider,
            population_size=4,
            max_generations=2,
            success_threshold=10,  # force full run
            elite_k=2,
        )
        assert result["generations"] == 2
        assert 1 <= result["best_score"] <= 10
        assert result["best_prompt"]


# ── Defaults sanity ────────────────────────────────────────────────────


def test_default_seed_pool_is_nonempty() -> None:
    assert len(DEFAULT_SEED_TEMPLATES) >= 4
    assert all("{target}" in t for t in DEFAULT_SEED_TEMPLATES)
