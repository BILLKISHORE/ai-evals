from unittest.mock import patch

import pytest

from ai_blackteam import evaluator


def test_ensemble_aggregates_median_and_agreement():
    # Three judges scoring 4, 4, 5 -> median 4, all within 1 -> agreement 1.0
    calls = iter([(4, "r1"), (4, "r2"), (5, "r3")])
    with patch.object(evaluator, "llm_judge", side_effect=lambda *a, **k: next(calls)):
        result = evaluator.ensemble_judge("resp", "target", models=["m1", "m2", "m3"])
    assert result["median_score"] == 4
    assert result["agreement"] == 1.0
    assert result["num_judges"] == 3
    assert len(result["per_judge"]) == 3


def test_ensemble_low_agreement_on_split():
    # Judges 1, 3, 5 -> median 3, only the 3 is within 1 -> agreement 1/3
    calls = iter([(1, "r1"), (3, "r2"), (5, "r3")])
    with patch.object(evaluator, "llm_judge", side_effect=lambda *a, **k: next(calls)):
        result = evaluator.ensemble_judge("resp", "target", models=["m1", "m2", "m3"])
    assert result["median_score"] == 3
    assert result["agreement"] == pytest.approx(1 / 3, abs=0.01)


def test_ensemble_skips_failed_judges():
    def flaky(response, target, model=None):
        if model == "bad":
            raise RuntimeError("judge down")
        return (5, "ok")

    with patch.object(evaluator, "llm_judge", side_effect=flaky):
        result = evaluator.ensemble_judge("resp", "target", models=["good", "bad", "good2"])
    assert result["num_judges"] == 2  # bad one skipped
    assert result["median_score"] == 5


def test_ensemble_raises_when_all_fail():
    with patch.object(evaluator, "llm_judge", side_effect=RuntimeError("down")):
        with pytest.raises(ValueError, match="All ensemble judges failed"):
            evaluator.ensemble_judge("resp", "target", models=["a", "b"])


def test_ensemble_default_models_are_distinct():
    assert len(set(evaluator.ENSEMBLE_JUDGE_MODELS)) == len(evaluator.ENSEMBLE_JUDGE_MODELS)
    assert len(evaluator.ENSEMBLE_JUDGE_MODELS) >= 2
