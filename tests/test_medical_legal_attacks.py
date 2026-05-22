"""Tests for 15 medical and legal malpractice attack techniques."""

import pytest

from ai_blackteam.attacks.dangerous_dosage import DangerousDosage
from ai_blackteam.attacks.drug_interaction import DrugInteraction
from ai_blackteam.attacks.self_surgery import SelfSurgery
from ai_blackteam.attacks.psychiatric_diagnosis import PsychiatricDiagnosis
from ai_blackteam.attacks.alternative_medicine_harm import AlternativeMedicineHarm
from ai_blackteam.attacks.veterinary_malpractice import VeterinaryMalpractice
from ai_blackteam.attacks.child_medical_advice import ChildMedicalAdvice
from ai_blackteam.attacks.pregnancy_harm import PregnancyHarm
from ai_blackteam.attacks.legal_self_representation import LegalSelfRepresentation
from ai_blackteam.attacks.tax_fraud_advice import TaxFraudAdvice
from ai_blackteam.attacks.immigration_fraud import ImmigrationFraud
from ai_blackteam.attacks.contract_manipulation import ContractManipulation
from ai_blackteam.attacks.evidence_tampering import EvidenceTampering
from ai_blackteam.attacks.witness_coaching import WitnessCoaching
from ai_blackteam.attacks.bankruptcy_fraud import BankruptcyFraud

TARGET = "chest pain and shortness of breath"

ALL_ATTACKS = [
    DangerousDosage(),
    DrugInteraction(),
    SelfSurgery(),
    PsychiatricDiagnosis(),
    AlternativeMedicineHarm(),
    VeterinaryMalpractice(),
    ChildMedicalAdvice(),
    PregnancyHarm(),
    LegalSelfRepresentation(),
    TaxFraudAdvice(),
    ImmigrationFraud(),
    ContractManipulation(),
    EvidenceTampering(),
    WitnessCoaching(),
    BankruptcyFraud(),
]


# ── Per-attack prompt generation tests ───────────────────────────────────────

def test_dangerous_dosage_generates_prompts():
    atk = DangerousDosage()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_drug_interaction_generates_prompts():
    atk = DrugInteraction()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_self_surgery_generates_prompts():
    atk = SelfSurgery()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_psychiatric_diagnosis_generates_prompts():
    atk = PsychiatricDiagnosis()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_alternative_medicine_harm_generates_prompts():
    atk = AlternativeMedicineHarm()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_veterinary_malpractice_generates_prompts():
    atk = VeterinaryMalpractice()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_child_medical_advice_generates_prompts():
    atk = ChildMedicalAdvice()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_pregnancy_harm_generates_prompts():
    atk = PregnancyHarm()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_legal_self_representation_generates_prompts():
    atk = LegalSelfRepresentation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_tax_fraud_advice_generates_prompts():
    atk = TaxFraudAdvice()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_immigration_fraud_generates_prompts():
    atk = ImmigrationFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_contract_manipulation_generates_prompts():
    atk = ContractManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_evidence_tampering_generates_prompts():
    atk = EvidenceTampering()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_witness_coaching_generates_prompts():
    atk = WitnessCoaching()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_bankruptcy_fraud_generates_prompts():
    atk = BankruptcyFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


# ── Metadata tests ────────────────────────────────────────────────────────────

def test_all_attacks_have_required_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "unqualified-advice", f"{atk.__class__.__name__} wrong category"
        assert meta["severity"] in ("low", "medium", "high", "critical"), \
            f"{atk.__class__.__name__} invalid severity"
        assert meta["mode"] == "single-turn", f"{atk.__class__.__name__} should be single-turn"
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0, f"{atk.__class__.__name__} missing owasp_llm"
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0, f"{atk.__class__.__name__} missing mitre_atlas"


def test_critical_attacks_are_marked_critical():
    critical_attacks = [
        DangerousDosage(),
        DrugInteraction(),
        SelfSurgery(),
        ChildMedicalAdvice(),
        PregnancyHarm(),
        EvidenceTampering(),
        WitnessCoaching(),
    ]
    for atk in critical_attacks:
        assert atk.severity == "critical", \
            f"{atk.__class__.__name__} should be critical severity"


def test_high_severity_attacks():
    high_attacks = [
        PsychiatricDiagnosis(),
        AlternativeMedicineHarm(),
        VeterinaryMalpractice(),
        LegalSelfRepresentation(),
        TaxFraudAdvice(),
        ImmigrationFraud(),
        ContractManipulation(),
        BankruptcyFraud(),
    ]
    for atk in high_attacks:
        assert atk.severity == "high", \
            f"{atk.__class__.__name__} should be high severity"


def test_owasp_and_mitre_tags():
    for atk in ALL_ATTACKS:
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, \
            f"{atk.__class__.__name__} missing expected owasp_llm tag"
        assert "AML.T0054" in atk.mitre_atlas, \
            f"{atk.__class__.__name__} missing AML.T0054"
        assert "AML.T0068" in atk.mitre_atlas, \
            f"{atk.__class__.__name__} missing AML.T0068"


def test_registry_contains_all_new_attacks():
    from ai_blackteam.registry import attack_registry
    expected_ids = [
        "dangerous-dosage",
        "drug-interaction",
        "self-surgery",
        "psychiatric-diagnosis",
        "alternative-medicine-harm",
        "veterinary-malpractice",
        "child-medical-advice",
        "pregnancy-harm",
        "legal-self-representation",
        "tax-fraud-advice",
        "immigration-fraud",
        "contract-manipulation",
        "evidence-tampering",
        "witness-coaching",
        "bankruptcy-fraud",
    ]
    for tid in expected_ids:
        assert attack_registry.get(tid) is not None, f"Registry missing attack: {tid}"
