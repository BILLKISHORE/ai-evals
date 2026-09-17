from ai_blackteam.taxonomy import (
    ATLAS_TECHNIQUES,
    ATTACK_ATLAS_MAPPINGS,
    MLCOMMONS_HAZARDS,
    HARM_TO_MLCOMMONS,
    get_mlcommons_category,
    get_mlcommons_name,
    get_atlas_names,
)
from ai_blackteam.registry import attack_registry


def test_all_attacks_have_atlas_mappings():
    registered = set(attack_registry.list())
    mapped = set(ATTACK_ATLAS_MAPPINGS.keys())
    missing = registered - mapped
    assert not missing, f"Attacks missing ATLAS mappings: {missing}"


def test_all_atlas_ids_are_defined():
    all_ids = set()
    for ids in ATTACK_ATLAS_MAPPINGS.values():
        all_ids.update(ids)
    undefined = all_ids - set(ATLAS_TECHNIQUES.keys())
    assert not undefined, f"ATLAS IDs used but not defined: {undefined}"


def test_no_generic_only_mappings():
    for attack_id, ids in ATTACK_ATLAS_MAPPINGS.items():
        assert ids != ["AML.T0051.000"], (
            f"{attack_id} still has only generic AML.T0051.000"
        )


def test_attack_classes_match_taxonomy():
    for name in attack_registry.list():
        cls = attack_registry.get(name)
        attack = cls()
        expected = ATTACK_ATLAS_MAPPINGS.get(name)
        assert expected is not None, f"{name} not in ATTACK_ATLAS_MAPPINGS"
        assert attack.mitre_atlas == expected, (
            f"{name}: class has {attack.mitre_atlas}, taxonomy has {expected}"
        )


def test_mlcommons_has_12_categories():
    assert len(MLCOMMONS_HAZARDS) == 12


def test_mlcommons_required_codes():
    required = {"vcr", "ncr", "src", "cse", "ssh", "iwp", "hte", "dfm", "ipv", "prv", "spc", "sxc"}
    assert set(MLCOMMONS_HAZARDS.keys()) == required


def test_all_harm_categories_map_to_valid_mlcommons():
    for harm, code in HARM_TO_MLCOMMONS.items():
        assert code in MLCOMMONS_HAZARDS, f"{harm} maps to unknown code {code}"


def test_get_mlcommons_category():
    assert get_mlcommons_category("phishing") == "ncr"
    assert get_mlcommons_category("weapons") == "iwp"
    assert get_mlcommons_category("self-harm") == "ssh"
    assert get_mlcommons_category("nonexistent") is None


def test_get_mlcommons_name():
    assert get_mlcommons_name("phishing") == "Non-Violent Crimes"
    assert get_mlcommons_name("weapons") == "Indiscriminate Weapons (CBRNE)"
    assert get_mlcommons_name("hate-speech") == "Hate"
    assert get_mlcommons_name("nonexistent") is None


def test_get_atlas_names():
    names = get_atlas_names(["AML.T0054", "AML.T0051.000"])
    assert "LLM Jailbreak" in names
    assert "LLM Prompt Injection: Direct" in names


def test_get_atlas_names_ignores_unknown():
    names = get_atlas_names(["AML.T0054", "AML.T9999"])
    assert len(names) == 1
    assert "LLM Jailbreak" in names


def test_atlas_techniques_have_required_fields():
    for tid, info in ATLAS_TECHNIQUES.items():
        assert "name" in info, f"{tid} missing name"
        assert "tactic" in info, f"{tid} missing tactic"
        assert "description" in info, f"{tid} missing description"


def test_mlcommons_hazards_have_required_fields():
    for code, info in MLCOMMONS_HAZARDS.items():
        assert "name" in info, f"{code} missing name"
        assert "description" in info, f"{code} missing description"


# ── ATLAS tactic names must be valid for the pinned version ──────────
#
# MITRE ATLAS renames tactics between releases (v2026.09 renamed AML.TA0001
# from "AI Attack Staging" to "AI Attack Adaptation"). A technique carrying a
# tactic string that no longer exists is a silent staleness bug: nothing else
# validates it. This list is the full tactic set for the version the taxonomy
# claims to track; bump both together.

ATLAS_2026_09_TACTICS = frozenset({
    "AI Model Access",
    "AI Attack Adaptation",   # was "AI Attack Staging" before v2026.09
    "Reconnaissance",
    "Resource Development",
    "Initial Access",
    "Execution",
    "Persistence",
    "Defense Evasion",
    "Discovery",
    "Collection",
    "Exfiltration",
    "Impact",
    "Privilege Escalation",
    "Credential Access",
    "Command and Control",
    "Lateral Movement",
})


def test_every_technique_tactic_is_a_valid_2026_09_tactic():
    from ai_blackteam.taxonomy import ATLAS_TECHNIQUES
    for tid, info in ATLAS_TECHNIQUES.items():
        assert info["tactic"] in ATLAS_2026_09_TACTICS, (
            f"{tid} has tactic {info['tactic']!r}, not a valid ATLAS v2026.09 tactic"
        )


def test_retired_tactic_name_is_gone():
    from ai_blackteam.taxonomy import ATLAS_TECHNIQUES
    stale = [t for t, i in ATLAS_TECHNIQUES.items() if i["tactic"] == "AI Attack Staging"]
    assert not stale, f"techniques still use the retired tactic name: {stale}"


def test_taxonomy_module_declares_the_current_atlas_version():
    import ai_blackteam.taxonomy as tax
    assert "2026.09" in (tax.__doc__ or ""), "module docstring should name the tracked ATLAS version"
