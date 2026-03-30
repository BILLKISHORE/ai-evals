"""Tests for NIST AI RMF and EU AI Act regulatory framework mappings."""

from blackteam.taxonomy import (
    NIST_AI_RMF, HARM_TO_NIST,
    EU_AI_ACT_RISK, HARM_TO_EU_AI_ACT,
)
from click.testing import CliRunner
from blackteam.cli import cli


def test_nist_has_4_functions():
    assert len(NIST_AI_RMF) == 4
    assert set(NIST_AI_RMF.keys()) == {"govern", "map", "measure", "manage"}


def test_nist_functions_have_fields():
    for func_id, info in NIST_AI_RMF.items():
        assert "name" in info
        assert "description" in info


def test_harm_to_nist_maps_to_valid_functions():
    for harm, func in HARM_TO_NIST.items():
        assert func in NIST_AI_RMF, f"{harm} maps to unknown NIST function {func}"


def test_eu_ai_act_has_4_levels():
    assert len(EU_AI_ACT_RISK) == 4
    assert set(EU_AI_ACT_RISK.keys()) == {"unacceptable", "high", "limited", "minimal"}


def test_eu_ai_act_levels_have_fields():
    for level, info in EU_AI_ACT_RISK.items():
        assert "name" in info
        assert "description" in info


def test_harm_to_eu_maps_to_valid_levels():
    for harm, level in HARM_TO_EU_AI_ACT.items():
        assert level in EU_AI_ACT_RISK, f"{harm} maps to unknown EU AI Act level {level}"


def test_weapons_is_unacceptable_risk():
    assert HARM_TO_EU_AI_ACT["weapons"] == "unacceptable"


def test_child_safety_is_unacceptable_risk():
    assert HARM_TO_EU_AI_ACT["child-safety"] == "unacceptable"


def test_frameworks_command():
    runner = CliRunner()
    result = runner.invoke(cli, ["frameworks"])
    assert result.exit_code == 0
    assert "NIST" in result.output
    assert "EU AI Act" in result.output
    assert "Govern" in result.output
    assert "Unacceptable Risk" in result.output
