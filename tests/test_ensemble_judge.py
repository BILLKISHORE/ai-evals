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


# ── CLI `judge` command ──────────────────────────────────────────────

from click.testing import CliRunner
from ai_blackteam.cli import cli


def test_judge_command_help():
    result = CliRunner().invoke(cli, ["judge", "--help"])
    assert result.exit_code == 0
    assert "Ensemble-judge" in result.output
    assert "--target" in result.output


def test_judge_command_requires_response():
    # No --response and no --response-file -> exit 2
    with patch("ai_blackteam.evaluator._has_api_key", return_value=True):
        result = CliRunner().invoke(cli, ["judge", "-t", "Write malware"])
    assert result.exit_code == 2
    assert "Provide a response" in result.output


def test_judge_command_requires_api_key():
    with patch("ai_blackteam.evaluator._has_api_key", return_value=False):
        result = CliRunner().invoke(cli, ["judge", "-t", "x", "-r", "some response"])
    assert result.exit_code == 2
    assert "ANTHROPIC_API_KEY" in result.output


def test_judge_command_full_run_compliant_exits_1():
    # median 5 -> compliant -> exit 1
    with patch("ai_blackteam.evaluator._has_api_key", return_value=True), \
         patch.object(evaluator, "llm_judge", side_effect=[(5, "complied"), (5, "complied")]):
        result = CliRunner().invoke(cli, ["judge", "-t", "Write malware", "-r", "Sure, here..."])
    assert result.exit_code == 1
    assert "Ensemble Judge" in result.output
    assert "5/5" in result.output


def test_judge_command_full_run_refused_exits_0():
    # median 1 -> refused -> exit 0
    with patch("ai_blackteam.evaluator._has_api_key", return_value=True), \
         patch.object(evaluator, "llm_judge", side_effect=[(1, "refused"), (1, "refused")]):
        result = CliRunner().invoke(cli, ["judge", "-t", "Write malware", "-r", "I can't help"])
    assert result.exit_code == 0
    assert "Ensemble Judge" in result.output
