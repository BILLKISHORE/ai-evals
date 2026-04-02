"""Tests for the 15 weapons evasion attack techniques."""

import importlib

from blackteam.attacks.firearm_modification import FirearmModification
from blackteam.attacks.ghost_gun import GhostGun
from blackteam.attacks.improvised_weapon import ImprovisedWeapon
from blackteam.attacks.arson_techniques import ArsonTechniques
from blackteam.attacks.bomb_threat import BombThreat
from blackteam.attacks.hostage_tactics import HostageTactics
from blackteam.attacks.assassination_planning import AssassinationPlanning
from blackteam.attacks.torture_methods import TortureMethods
from blackteam.attacks.school_attack_planning import SchoolAttackPlanning
from blackteam.attacks.stalking_escalation import StalkingEscalation
from blackteam.attacks.domestic_violence_assist import DomesticViolenceAssist
from blackteam.attacks.trafficking_assistance import TraffickingAssistance
from blackteam.attacks.militia_organization import MilitiaOrganization
from blackteam.attacks.swatting_assist import SwattingAssist

_mod_3d = importlib.import_module("blackteam.attacks.3d_printed_weapon")
ThreeDPrintedWeapon = _mod_3d.ThreeDPrintedWeapon

TARGET = "a test target"

ALL_ATTACKS = [
    FirearmModification(),
    GhostGun(),
    ThreeDPrintedWeapon(),
    ImprovisedWeapon(),
    ArsonTechniques(),
    BombThreat(),
    HostageTactics(),
    AssassinationPlanning(),
    TortureMethods(),
    SchoolAttackPlanning(),
    StalkingEscalation(),
    DomesticViolenceAssist(),
    TraffickingAssistance(),
    MilitiaOrganization(),
    SwattingAssist(),
]


# ── Per-attack prompt generation tests ────────────────────────────────


def test_firearm_modification_generates_prompts():
    atk = FirearmModification()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_ghost_gun_generates_prompts():
    atk = GhostGun()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_3d_printed_weapon_generates_prompts():
    atk = ThreeDPrintedWeapon()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_improvised_weapon_generates_prompts():
    atk = ImprovisedWeapon()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_arson_techniques_generates_prompts():
    atk = ArsonTechniques()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_bomb_threat_generates_prompts():
    atk = BombThreat()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_hostage_tactics_generates_prompts():
    atk = HostageTactics()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_assassination_planning_generates_prompts():
    atk = AssassinationPlanning()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_torture_methods_generates_prompts():
    atk = TortureMethods()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_school_attack_planning_generates_prompts():
    atk = SchoolAttackPlanning()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_stalking_escalation_generates_prompts():
    atk = StalkingEscalation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_domestic_violence_assist_generates_prompts():
    atk = DomesticViolenceAssist()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_trafficking_assistance_generates_prompts():
    atk = TraffickingAssistance()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_militia_organization_generates_prompts():
    atk = MilitiaOrganization()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_swatting_assist_generates_prompts():
    atk = SwattingAssist()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


# ── Metadata tests ─────────────────────────────────────────────────────


def test_all_attacks_have_required_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "weapons-evasion", (
            f"{atk.__class__.__name__} wrong category: {meta['category']}"
        )
        assert meta["severity"] == "critical", (
            f"{atk.__class__.__name__} should be critical, got {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0


def test_all_attacks_are_critical_severity():
    for atk in ALL_ATTACKS:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical, got {atk.severity}"
        )


def test_all_attacks_have_mitre_atlas_tags():
    for atk in ALL_ATTACKS:
        assert "AML.T0054" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0054"
        )
        assert "AML.T0068" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0068"
        )


def test_all_attacks_have_owasp_llm01():
    for atk in ALL_ATTACKS:
        assert any("LLM01" in tag for tag in atk.owasp_llm), (
            f"{atk.__class__.__name__} missing LLM01 owasp tag"
        )


def test_all_attacks_are_single_turn():
    for atk in ALL_ATTACKS:
        assert atk.mode == "single-turn", (
            f"{atk.__class__.__name__} should be single-turn, got {atk.mode}"
        )


def test_prompts_contain_target():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), (
            f"{atk.__class__.__name__} prompts do not contain target"
        )


def test_all_attacks_registered_in_registry():
    from blackteam.registry import attack_registry
    technique_ids = [
        "firearm-modification",
        "ghost-gun",
        "3d-printed-weapon",
        "improvised-weapon",
        "arson-techniques",
        "bomb-threat",
        "hostage-tactics",
        "assassination-planning",
        "torture-methods",
        "school-attack-planning",
        "stalking-escalation",
        "domestic-violence-assist",
        "trafficking-assistance",
        "militia-organization",
        "swatting-assist",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
