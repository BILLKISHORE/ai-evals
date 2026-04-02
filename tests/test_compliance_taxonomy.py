from blackteam.taxonomy import (
    EU_AI_ACT_RISK_LEVELS,
    NIST_AI_RMF_PILLARS,
    HARM_TO_EU_AI_ACT,
    HARM_TO_NIST,
    get_eu_risk_level,
    get_nist_pillar,
)


def test_eu_ai_act_has_four_risk_levels():
    assert len(EU_AI_ACT_RISK_LEVELS) == 4
    for level in ["unacceptable", "high", "limited", "minimal"]:
        assert level in EU_AI_ACT_RISK_LEVELS


def test_eu_ai_act_entries_have_required_fields():
    for level, entry in EU_AI_ACT_RISK_LEVELS.items():
        assert "name" in entry
        assert "description" in entry


def test_nist_has_four_pillars():
    assert len(NIST_AI_RMF_PILLARS) == 4
    for pillar in ["govern", "map", "measure", "manage"]:
        assert pillar in NIST_AI_RMF_PILLARS


def test_nist_entries_have_required_fields():
    for pillar, entry in NIST_AI_RMF_PILLARS.items():
        assert "name" in entry
        assert "description" in entry


def test_harm_to_eu_maps_to_valid_levels():
    valid_levels = set(EU_AI_ACT_RISK_LEVELS.keys())
    for harm, level in HARM_TO_EU_AI_ACT.items():
        assert level in valid_levels, f"{harm} maps to invalid EU level '{level}'"


def test_harm_to_nist_maps_to_valid_pillars():
    valid_pillars = set(NIST_AI_RMF_PILLARS.keys())
    for harm, pillar in HARM_TO_NIST.items():
        assert pillar in valid_pillars, f"{harm} maps to invalid NIST pillar '{pillar}'"


def test_get_eu_risk_level_known():
    assert get_eu_risk_level("weapons") == "unacceptable"
    assert get_eu_risk_level("phishing") == "high"


def test_get_eu_risk_level_unknown():
    assert get_eu_risk_level("nonexistent") == "minimal"


def test_get_nist_pillar_known():
    assert get_nist_pillar("pii-extraction") == "govern"
    assert get_nist_pillar("weapons") == "manage"


def test_get_nist_pillar_unknown():
    assert get_nist_pillar("nonexistent") == "measure"
