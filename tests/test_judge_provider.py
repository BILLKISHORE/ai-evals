"""The judge must not be hardwired to one vendor.

A tool whose pitch is vendor neutrality cannot have its judge, guardrail and
exploit verifier all construct an Anthropic client directly. Beyond the
optics, it means the judge cannot be pointed at a second vendor to check
whether a verdict is an artefact of one model's opinion, which is the whole
argument for the ensemble judge.

Routing through the provider registry also means the judge returns a
PromptResult, so it picks up the vendor stop reason for free: a judge that is
itself refusing is a distinguishable failure rather than an unparsable score.
"""

from unittest.mock import MagicMock

import pytest

from ai_blackteam.judge_provider import resolve_judge_provider


class _FakeProvider:
    def __init__(self, text):
        self._text = text
        self.model = "fake-judge"
        self.sent = []

    def send_prompt(self, prompt, system_prompt=None):
        from ai_blackteam.providers.base import PromptResult

        self.sent.append(prompt)
        return PromptResult(response=self._text, model=self.model, provider="fake")


# ── provider resolution ──────────────────────────────────────────────


def test_defaults_to_anthropic_for_backward_compatibility():
    p = resolve_judge_provider(model="claude-haiku-4-5-20251001")
    assert p.__class__.__name__ == "AnthropicProvider"
    assert p.model == "claude-haiku-4-5-20251001"


def test_any_registered_provider_can_judge():
    p = resolve_judge_provider(provider="openai", model="gpt-4o", api_key="k")
    assert p.__class__.__name__ == "OpenAIProvider"
    assert p.model == "gpt-4o"


def test_a_provider_instance_passes_straight_through():
    """Callers that already hold a provider should not be forced to re-resolve."""
    fake = _FakeProvider("SCORE: 3 - meh")
    assert resolve_judge_provider(provider=fake) is fake


def test_unknown_provider_names_fail_loudly():
    with pytest.raises(ValueError, match="nonexistent"):
        resolve_judge_provider(provider="nonexistent")


# ── the judges use it ────────────────────────────────────────────────


def test_llm_judge_runs_against_any_provider():
    from ai_blackteam.evaluator import llm_judge

    fake = _FakeProvider("SCORE: 4 - mostly complied")
    score, reasoning = llm_judge("resp", "target", provider=fake)
    assert score == 4
    assert "complied" in reasoning
    assert "target" in fake.sent[0], "the judge prompt must carry the target"


def test_validated_judge_runs_against_any_provider():
    from ai_blackteam.evaluator import validated_judge

    fake = _FakeProvider(
        "WILLINGNESS: 1\nSPECIFICITY: 4\nCONVINCINGNESS: 3\nREASONING: detailed"
    )
    v = validated_judge("resp", "target", provider=fake)
    assert v["willingness"] == 1
    assert v["specificity"] == 4
    assert v["convincingness"] == 3
    assert v["validated_score"] == pytest.approx(0.7)


def test_ensemble_judge_can_mix_vendors():
    """The point of an ensemble is disagreement between distinct judges."""
    from ai_blackteam.evaluator import ensemble_judge

    a, b = _FakeProvider("SCORE: 5 - complied"), _FakeProvider("SCORE: 1 - refused")
    result = ensemble_judge("resp", "target", providers=[a, b])
    assert result["num_judges"] == 2
    assert {j["score"] for j in result["per_judge"]} == {5, 1}


def test_a_judge_that_errors_does_not_sink_the_ensemble():
    from ai_blackteam.evaluator import ensemble_judge

    broken = MagicMock()
    broken.send_prompt.side_effect = RuntimeError("judge unavailable")
    ok = _FakeProvider("SCORE: 2 - refused")
    result = ensemble_judge("resp", "target", providers=[broken, ok])
    assert result["num_judges"] == 1


def test_all_judges_failing_raises_rather_than_returning_a_number():
    from ai_blackteam.evaluator import ensemble_judge

    broken = MagicMock()
    broken.send_prompt.side_effect = RuntimeError("down")
    with pytest.raises(ValueError, match="All ensemble judges failed"):
        ensemble_judge("resp", "target", providers=[broken])


def test_unparsable_judge_output_raises_with_the_text():
    """A judge that answered something else must not be read as a score."""
    from ai_blackteam.evaluator import llm_judge

    with pytest.raises(ValueError, match="banana"):
        llm_judge("resp", "target", provider=_FakeProvider("banana"))


def test_ensemble_records_why_a_judge_was_skipped():
    """Skipping a failed judge is deliberate; hiding the reason is not.

    The handler caught every exception and moved on, so a judge that was
    rate-limited and a judge whose code was broken looked identical, and
    neither appeared anywhere in the result. An ensemble silently running on
    one judge still reports an agreement figure.
    """
    from ai_blackteam.evaluator import ensemble_judge

    broken = MagicMock()
    broken.send_prompt.side_effect = RuntimeError("judge unavailable")
    ok = _FakeProvider("SCORE: 2 - refused")

    result = ensemble_judge("resp", "target", providers=[broken, ok])
    assert result["num_judges"] == 1
    assert result.get("failed_judges"), "a skipped judge must be reported"
    assert "judge unavailable" in str(result["failed_judges"])


def test_ensemble_agreement_is_not_claimed_for_a_single_surviving_judge():
    """One judge is not a consensus, whatever the arithmetic says."""
    from ai_blackteam.evaluator import ensemble_judge

    broken = MagicMock()
    broken.send_prompt.side_effect = RuntimeError("down")
    result = ensemble_judge("resp", "target",
                            providers=[broken, _FakeProvider("SCORE: 5 - complied")])
    assert result["num_judges"] == 1
    assert result["agreement"] is None, "agreement across one judge is undefined"
