"""The AIVSS composite has to be arithmetic, and it has to refuse guesses.

A scoring system that silently defaults a missing factor to zero reports a
lower score than the evidence supports, and the caller never learns that a
factor was never measured. That is the exact failure this repository keeps
hitting: an absent measurement turning into a clean one. These tests pin the
arithmetic to hand-computed values and pin the refusals to raising, so neither
can be softened into a plausible default later.

They also pin the honesty markers. The factor names in this checkout were
reconstructed rather than read from OWASP's published specification, and the
result object has to keep saying so.
"""

import pytest

from ai_blackteam.standards import aivss
from ai_blackteam.standards.loader import StandardsDataUnavailable


def _eight_factor_keys():
    return sorted(aivss.factors())


def _all_at(value):
    return {key: value for key in _eight_factor_keys()}


# ── the agentic sub-score is a weighted mean scaled to ten ────────────


def test_no_agentic_capability_scores_zero():
    assert aivss.agentic_risk_score(_all_at(0.0)) == 0.0


def test_every_agentic_capability_at_maximum_scores_ten():
    assert aivss.agentic_risk_score(_all_at(1.0)) == 10.0


def test_half_the_factors_at_maximum_scores_five():
    keys = _eight_factor_keys()
    half = len(keys) // 2
    values = {key: (1.0 if i < half else 0.0) for i, key in enumerate(keys)}
    assert aivss.agentic_risk_score(values) == 5.0


def test_uniform_quarter_values_score_two_point_five():
    assert aivss.agentic_risk_score(_all_at(0.25)) == 2.5


def test_weights_actually_weight_the_mean():
    """A weighted spec must move the score, or the weight column is dead wiring."""
    spec = {
        "heavy": {"label": "Heavy", "weight": 3.0},
        "light": {"label": "Light", "weight": 1.0},
    }
    only_heavy = aivss.agentic_risk_score({"heavy": 1.0, "light": 0.0}, factor_spec=spec)
    only_light = aivss.agentic_risk_score({"heavy": 0.0, "light": 1.0}, factor_spec=spec)
    assert only_heavy == 7.5
    assert only_light == 2.5


def test_raising_any_single_factor_raises_the_score():
    """Proves the score is computed from the inputs, not looked up."""
    baseline = aivss.agentic_risk_score(_all_at(0.0))
    for key in _eight_factor_keys():
        values = _all_at(0.0)
        values[key] = 1.0
        assert aivss.agentic_risk_score(values) > baseline, key


def test_sub_score_rounds_up_rather_than_to_nearest():
    """AIVSS composes a CVSS base score, so it follows the CVSS Roundup rule.

    Four factors at 1.0 plus one at 0.48008 gives an exact sub-score of
    5.6001. Rounding to nearest would report 5.6 and understate it.
    """
    keys = _eight_factor_keys()
    values = {key: 0.0 for key in keys}
    for key in keys[:4]:
        values[key] = 1.0
    values[keys[4]] = 0.48008
    assert aivss.agentic_risk_score(values) == 5.7


# ── refusals: an unmeasured factor is not a measured zero ─────────────


def test_a_missing_factor_raises_instead_of_scoring_zero():
    values = _all_at(1.0)
    dropped = values.popitem()[0]
    with pytest.raises(aivss.AivssInputError) as exc:
        aivss.agentic_risk_score(values)
    assert dropped in str(exc.value)


def test_an_unknown_factor_raises_instead_of_being_ignored():
    values = _all_at(0.0)
    values["telepathy"] = 1.0
    with pytest.raises(aivss.AivssInputError) as exc:
        aivss.agentic_risk_score(values)
    assert "telepathy" in str(exc.value)


@pytest.mark.parametrize("bad", [-0.1, 1.1, 2.0])
def test_a_factor_value_outside_zero_to_one_raises(bad):
    values = _all_at(0.0)
    values[_eight_factor_keys()[0]] = bad
    with pytest.raises(aivss.AivssInputError):
        aivss.agentic_risk_score(values)


def test_a_non_numeric_factor_value_raises():
    values = _all_at(0.0)
    values[_eight_factor_keys()[0]] = "high"
    with pytest.raises(aivss.AivssInputError):
        aivss.agentic_risk_score(values)


def test_a_boolean_factor_value_raises():
    """bool is an int in Python; a True must not silently become 1.0."""
    values = _all_at(0.0)
    values[_eight_factor_keys()[0]] = True
    with pytest.raises(aivss.AivssInputError):
        aivss.agentic_risk_score(values)


@pytest.mark.parametrize("bad", [-1.0, 10.1, "9.8"])
def test_a_cvss_base_outside_zero_to_ten_raises(bad):
    with pytest.raises(aivss.AivssInputError):
        aivss.score(bad, _all_at(0.0))


# ── the composite ────────────────────────────────────────────────────


def test_composite_is_the_mean_of_the_cvss_base_and_the_agentic_sub_score():
    keys = _eight_factor_keys()
    values = {key: (1.0 if i < len(keys) // 2 else 0.0) for i, key in enumerate(keys)}
    result = aivss.score(7.0, values)
    assert result["agentic_risk_score"] == 5.0
    assert result["aivss_score"] == 6.0


def test_composite_of_a_high_cvss_and_a_low_agentic_sub_score():
    result = aivss.score(9.5, _all_at(0.25))
    assert result["agentic_risk_score"] == 2.5
    assert result["aivss_score"] == 6.0


def test_composite_echoes_the_inputs_it_scored():
    values = _all_at(0.5)
    result = aivss.score(4.0, values)
    assert result["cvss_base"] == 4.0
    assert result["factors"] == values


def test_a_non_agentic_finding_scores_its_cvss_base_halved():
    """Zero agentic capability must not leave the CVSS base untouched."""
    result = aivss.score(8.0, _all_at(0.0))
    assert result["aivss_score"] == 4.0


# ── severity bands ───────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value,expected",
    [
        (0.0, "None"),
        (0.1, "Low"),
        (3.9, "Low"),
        (4.0, "Medium"),
        (6.9, "Medium"),
        (7.0, "High"),
        (8.9, "High"),
        (9.0, "Critical"),
        (10.0, "Critical"),
    ],
)
def test_severity_band_boundaries(value, expected):
    assert aivss.severity_band(value) == expected


def test_severity_band_rejects_a_score_off_the_scale():
    with pytest.raises(aivss.AivssInputError):
        aivss.severity_band(10.5)


def test_score_reports_the_band_for_its_own_composite():
    result = aivss.score(10.0, _all_at(1.0))
    assert result["aivss_score"] == 10.0
    assert result["severity"] == "Critical"


# ── honesty markers ──────────────────────────────────────────────────


def test_result_says_the_factor_set_is_not_known_to_be_complete():
    result = aivss.score(5.0, _all_at(0.0))
    assert result["factor_set_complete"] is False


def test_result_says_the_factor_names_are_unverified():
    result = aivss.score(5.0, _all_at(0.0))
    assert result["verification"] == "unverified"


def test_result_carries_a_reason_a_reader_can_act_on():
    result = aivss.score(5.0, _all_at(0.0))
    joined = " ".join(result["notes"]).lower()
    assert "unverified" in joined
    assert "owasp" in joined


def test_every_factor_declares_its_verification_state():
    for key, entry in aivss.factors().items():
        assert entry["verification"] == "unverified", key
        assert entry["label"], key
        assert entry["weight"] > 0, key


def test_the_document_does_not_claim_a_verified_source():
    doc = aivss.aivss_document()
    assert doc["source"]["verified_against"] is None
    assert doc["source"]["provenance"] == "local-fixture"


def test_a_document_claiming_verified_without_a_source_is_rejected(tmp_path):
    """The loader is the guard that keeps an unchecked claim out of a report."""
    import json

    doc = json.loads((aivss.AIVSS_DATA_PATH).read_text())
    doc["factor_set"]["factors"]["tool_use"]["verification"] = "verified"
    bad = tmp_path / "aivss-bad.json"
    bad.write_text(json.dumps(doc))

    from ai_blackteam.standards import loader

    with pytest.raises(StandardsDataUnavailable) as exc:
        loader.load_path(bad)
    assert "verified" in str(exc.value)


def test_the_data_file_ships_inside_the_package():
    import ai_blackteam
    from pathlib import Path

    package_root = Path(ai_blackteam.__file__).parent
    assert package_root in aivss.AIVSS_DATA_PATH.parents, (
        "the AIVSS data resolved outside the package, so a wheel would not carry it"
    )


# ── the CLI surface ──────────────────────────────────────────────────


def _invoke(args):
    from click.testing import CliRunner
    from ai_blackteam.cli import cli

    return CliRunner().invoke(cli, args)


def _factor_args(value):
    return [f"--factor={key}={value}" for key in _eight_factor_keys()]


def test_cli_lists_the_factors_it_will_ask_for():
    result = _invoke(["aivss", "--list-factors"])
    assert result.exit_code == 0
    for key in _eight_factor_keys():
        assert key in result.output


def test_cli_scores_a_finding_and_prints_the_composite():
    result = _invoke(["aivss", "--cvss-base", "8.0", *_factor_args(0.0)])
    assert result.exit_code == 0
    assert "4.0" in result.output


def test_cli_prints_the_unverified_warning_beside_the_score():
    result = _invoke(["aivss", "--cvss-base", "8.0", *_factor_args(0.0)])
    assert "UNVERIFIED" in result.output


def test_cli_refuses_to_score_when_a_factor_was_not_supplied():
    result = _invoke(["aivss", "--cvss-base", "8.0", "--factor=tool_use=1.0"])
    assert result.exit_code != 0
    assert "autonomy_of_action" in result.output


def test_cli_refuses_an_unknown_factor():
    result = _invoke(["aivss", "--cvss-base", "8.0", *_factor_args(0.0), "--factor=telepathy=1.0"])
    assert result.exit_code != 0
    assert "telepathy" in result.output


def test_cli_refuses_a_non_numeric_factor_value():
    result = _invoke(["aivss", "--cvss-base", "8.0", "--factor=tool_use=high"])
    assert result.exit_code != 0


def test_cli_requires_a_cvss_base():
    result = _invoke(["aivss", *_factor_args(0.0)])
    assert result.exit_code != 0
    assert "--cvss-base" in result.output


def test_cli_json_output_keeps_the_verification_marker():
    import json

    result = _invoke(["aivss", "--cvss-base", "8.0", "--format", "json", *_factor_args(1.0)])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["aivss_score"] == 9.0
    assert payload["verification"] == "unverified"
    assert payload["factor_set_complete"] is False
