"""Tests for the 15 capability elicitation attack techniques."""

from ai_blackteam.attacks.chemical_synthesis import ChemicalSynthesis
from ai_blackteam.attacks.biological_agent import BiologicalAgent
from ai_blackteam.attacks.nuclear_knowledge import NuclearKnowledge
from ai_blackteam.attacks.radiological_dispersal import RadiologicalDispersal
from ai_blackteam.attacks.explosive_synthesis import ExplosiveSynthesis
from ai_blackteam.attacks.drug_synthesis import DrugSynthesis
from ai_blackteam.attacks.poison_preparation import PoisonPreparation
from ai_blackteam.attacks.bioweapon_delivery import BioweaponDelivery
from ai_blackteam.attacks.dual_use_research import DualUseResearch
from ai_blackteam.attacks.gain_of_function import GainOfFunction
from ai_blackteam.attacks.cyber_weapon import CyberWeapon
from ai_blackteam.attacks.autonomous_weapon import AutonomousWeapon
from ai_blackteam.attacks.mass_casualty import MassCasualty
from ai_blackteam.attacks.infrastructure_attack import InfrastructureAttack
from ai_blackteam.attacks.uplift_assessment import UpliftAssessment

TARGET = "a dangerous substance"

ALL_ATTACKS = [
    ChemicalSynthesis(),
    BiologicalAgent(),
    NuclearKnowledge(),
    RadiologicalDispersal(),
    ExplosiveSynthesis(),
    DrugSynthesis(),
    PoisonPreparation(),
    BioweaponDelivery(),
    DualUseResearch(),
    GainOfFunction(),
    CyberWeapon(),
    AutonomousWeapon(),
    MassCasualty(),
    InfrastructureAttack(),
    UpliftAssessment(),
]


def test_chemical_synthesis_generates_prompts():
    atk = ChemicalSynthesis()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_biological_agent_generates_prompts():
    atk = BiologicalAgent()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_nuclear_knowledge_generates_prompts():
    atk = NuclearKnowledge()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_radiological_dispersal_generates_prompts():
    atk = RadiologicalDispersal()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_explosive_synthesis_generates_prompts():
    atk = ExplosiveSynthesis()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_drug_synthesis_generates_prompts():
    atk = DrugSynthesis()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_poison_preparation_generates_prompts():
    atk = PoisonPreparation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_bioweapon_delivery_generates_prompts():
    atk = BioweaponDelivery()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_dual_use_research_generates_prompts():
    atk = DualUseResearch()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_gain_of_function_generates_prompts():
    atk = GainOfFunction()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cyber_weapon_generates_prompts():
    atk = CyberWeapon()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_autonomous_weapon_generates_prompts():
    atk = AutonomousWeapon()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_mass_casualty_generates_prompts():
    atk = MassCasualty()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_infrastructure_attack_generates_prompts():
    atk = InfrastructureAttack()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_uplift_assessment_generates_prompts():
    atk = UpliftAssessment()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


# ── Metadata tests ────────────────────────────────────────────────────


def test_all_attacks_have_required_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "capability-elicitation", (
            f"{atk.__class__.__name__} wrong category: {meta['category']}"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0


def test_critical_attacks_have_critical_severity():
    critical_attacks = [
        ChemicalSynthesis(), BiologicalAgent(), NuclearKnowledge(),
        RadiologicalDispersal(), ExplosiveSynthesis(), DrugSynthesis(),
        PoisonPreparation(), BioweaponDelivery(), GainOfFunction(),
        CyberWeapon(), AutonomousWeapon(), MassCasualty(), InfrastructureAttack(),
    ]
    for atk in critical_attacks:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical, got {atk.severity}"
        )


def test_high_severity_attacks():
    high_attacks = [DualUseResearch(), UpliftAssessment()]
    for atk in high_attacks:
        assert atk.severity == "high", (
            f"{atk.__class__.__name__} should be high, got {atk.severity}"
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
    from ai_blackteam.registry import attack_registry
    technique_ids = [
        "chemical-synthesis", "biological-agent", "nuclear-knowledge",
        "radiological-dispersal", "explosive-synthesis", "drug-synthesis",
        "poison-preparation", "bioweapon-delivery", "dual-use-research",
        "gain-of-function", "cyber-weapon", "autonomous-weapon",
        "mass-casualty", "infrastructure-attack", "uplift-assessment",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
