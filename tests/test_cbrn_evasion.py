"""Tests for the 15 CBRN evasion attack techniques."""

from mordor.attacks.cbrn_academic_framing import CbrnAcademicFraming
from mordor.attacks.cbrn_historical_context import CbrnHistoricalContext
from mordor.attacks.cbrn_fictional_scenario import CbrnFictionalScenario
from mordor.attacks.cbrn_safety_inversion import CbrnSafetyInversion
from mordor.attacks.cbrn_comparative_analysis import CbrnComparativeAnalysis
from mordor.attacks.cbrn_supply_chain import CbrnSupplyChain
from mordor.attacks.cbrn_detection_evasion import CbrnDetectionEvasion
from mordor.attacks.cbrn_dosage_calculation import CbrnDosageCalculation
from mordor.attacks.cbrn_dispersal_optimization import CbrnDispersalOptimization
from mordor.attacks.cbrn_precursor_substitution import CbrnPrecursorSubstitution
from mordor.attacks.cbrn_lab_setup import CbrnLabSetup
from mordor.attacks.cbrn_aerosolization import CbrnAerosolization
from mordor.attacks.cbrn_weaponization import CbrnWeaponization
from mordor.attacks.cbrn_delivery_mechanism import CbrnDeliveryMechanism
from mordor.attacks.cbrn_scale_up import CbrnScaleUp

TARGET = "a dangerous substance"

ALL_ATTACKS = [
    CbrnAcademicFraming(),
    CbrnHistoricalContext(),
    CbrnFictionalScenario(),
    CbrnSafetyInversion(),
    CbrnComparativeAnalysis(),
    CbrnSupplyChain(),
    CbrnDetectionEvasion(),
    CbrnDosageCalculation(),
    CbrnDispersalOptimization(),
    CbrnPrecursorSubstitution(),
    CbrnLabSetup(),
    CbrnAerosolization(),
    CbrnWeaponization(),
    CbrnDeliveryMechanism(),
    CbrnScaleUp(),
]


# ── Per-attack prompt generation tests ────────────────────────────────


def test_cbrn_academic_framing_generates_prompts():
    atk = CbrnAcademicFraming()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_historical_context_generates_prompts():
    atk = CbrnHistoricalContext()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_fictional_scenario_generates_prompts():
    atk = CbrnFictionalScenario()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_safety_inversion_generates_prompts():
    atk = CbrnSafetyInversion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_comparative_analysis_generates_prompts():
    atk = CbrnComparativeAnalysis()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_supply_chain_generates_prompts():
    atk = CbrnSupplyChain()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_detection_evasion_generates_prompts():
    atk = CbrnDetectionEvasion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_dosage_calculation_generates_prompts():
    atk = CbrnDosageCalculation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_dispersal_optimization_generates_prompts():
    atk = CbrnDispersalOptimization()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_precursor_substitution_generates_prompts():
    atk = CbrnPrecursorSubstitution()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_lab_setup_generates_prompts():
    atk = CbrnLabSetup()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_aerosolization_generates_prompts():
    atk = CbrnAerosolization()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_weaponization_generates_prompts():
    atk = CbrnWeaponization()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_delivery_mechanism_generates_prompts():
    atk = CbrnDeliveryMechanism()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cbrn_scale_up_generates_prompts():
    atk = CbrnScaleUp()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


# ── Metadata tests ─────────────────────────────────────────────────────


def test_all_attacks_have_required_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "cbrn-evasion", (
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
        CbrnSupplyChain(),
        CbrnDetectionEvasion(),
        CbrnDosageCalculation(),
        CbrnDispersalOptimization(),
        CbrnPrecursorSubstitution(),
        CbrnLabSetup(),
        CbrnAerosolization(),
        CbrnWeaponization(),
        CbrnDeliveryMechanism(),
        CbrnScaleUp(),
    ]
    for atk in critical_attacks:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical, got {atk.severity}"
        )


def test_high_severity_attacks():
    high_attacks = [
        CbrnAcademicFraming(),
        CbrnHistoricalContext(),
        CbrnFictionalScenario(),
        CbrnSafetyInversion(),
        CbrnComparativeAnalysis(),
    ]
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
    from mordor.registry import attack_registry
    technique_ids = [
        "cbrn-academic-framing",
        "cbrn-historical-context",
        "cbrn-fictional-scenario",
        "cbrn-safety-inversion",
        "cbrn-comparative-analysis",
        "cbrn-supply-chain",
        "cbrn-detection-evasion",
        "cbrn-dosage-calculation",
        "cbrn-dispersal-optimization",
        "cbrn-precursor-substitution",
        "cbrn-lab-setup",
        "cbrn-aerosolization",
        "cbrn-weaponization",
        "cbrn-delivery-mechanism",
        "cbrn-scale-up",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
