from ai_blackteam.taxonomy import OWASP_AGENTIC_2026, ATTACK_AGENTIC_MAPPINGS, get_agentic_category_name


def test_owasp_agentic_has_ten_categories():
    assert len(OWASP_AGENTIC_2026) == 10


def test_owasp_agentic_has_all_asi_codes():
    expected = [f"ASI0{i}" for i in range(1, 10)] + ["ASI10"]
    for code in expected:
        assert code in OWASP_AGENTIC_2026, f"{code} missing from OWASP_AGENTIC_2026"


def test_owasp_agentic_each_entry_has_name_and_description():
    for code, entry in OWASP_AGENTIC_2026.items():
        assert "name" in entry, f"{code} missing 'name'"
        assert "description" in entry, f"{code} missing 'description'"


def test_get_agentic_category_name_returns_correct_name():
    assert get_agentic_category_name("ASI01") == "Agent Goal Hijack"
    assert get_agentic_category_name("ASI02") == "Tool Misuse & Exploitation"


def test_get_agentic_category_name_unknown_returns_unknown():
    assert get_agentic_category_name("ASI99") == "Unknown"


def test_attack_agentic_mappings_codes_are_valid():
    for attack_id, codes in ATTACK_AGENTIC_MAPPINGS.items():
        for code in codes:
            assert code in OWASP_AGENTIC_2026, (
                f"Attack '{attack_id}' maps to unknown ASI code '{code}'"
            )
