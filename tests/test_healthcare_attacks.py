"""Tests for 25 healthcare exploitation attacks."""

import pytest
from ai_blackteam.registry import attack_registry
import ai_blackteam.attacks.medical_records_theft  # noqa: F401
import ai_blackteam.attacks.prescription_fraud  # noqa: F401
import ai_blackteam.attacks.clinical_trial_fraud  # noqa: F401
import ai_blackteam.attacks.organ_trafficking  # noqa: F401
import ai_blackteam.attacks.vaccine_sabotage  # noqa: F401
import ai_blackteam.attacks.medical_identity_theft  # noqa: F401
import ai_blackteam.attacks.insurance_billing_fraud  # noqa: F401
import ai_blackteam.attacks.telemedicine_fraud  # noqa: F401
import ai_blackteam.attacks.pharmacy_fraud  # noqa: F401
import ai_blackteam.attacks.patient_manipulation  # noqa: F401
import ai_blackteam.attacks.mental_health_exploitation  # noqa: F401
import ai_blackteam.attacks.disability_fraud  # noqa: F401
import ai_blackteam.attacks.cosmetic_surgery_harm  # noqa: F401
import ai_blackteam.attacks.fertility_fraud  # noqa: F401
import ai_blackteam.attacks.hospice_fraud  # noqa: F401
import ai_blackteam.attacks.clinical_data_manipulation  # noqa: F401
import ai_blackteam.attacks.drug_diversion  # noqa: F401
import ai_blackteam.attacks.medical_waste_violation  # noqa: F401
import ai_blackteam.attacks.blood_supply_tampering  # noqa: F401
import ai_blackteam.attacks.epidemiological_fraud  # noqa: F401
import ai_blackteam.attacks.genetic_data_exploitation  # noqa: F401
import ai_blackteam.attacks.bioethics_violation  # noqa: F401
import ai_blackteam.attacks.informed_consent_bypass  # noqa: F401
import ai_blackteam.attacks.medical_device_tampering  # noqa: F401
import ai_blackteam.attacks.pandemic_profiteering  # noqa: F401
from ai_blackteam.attacks.medical_records_theft import MedicalRecordsTheft
from ai_blackteam.attacks.prescription_fraud import PrescriptionFraud
from ai_blackteam.attacks.clinical_trial_fraud import ClinicalTrialFraud
from ai_blackteam.attacks.organ_trafficking import OrganTrafficking
from ai_blackteam.attacks.vaccine_sabotage import VaccineSabotage
from ai_blackteam.attacks.medical_identity_theft import MedicalIdentityTheft
from ai_blackteam.attacks.insurance_billing_fraud import InsuranceBillingFraud
from ai_blackteam.attacks.telemedicine_fraud import TelemedFraud
from ai_blackteam.attacks.pharmacy_fraud import PharmacyFraud
from ai_blackteam.attacks.patient_manipulation import PatientManipulation
from ai_blackteam.attacks.mental_health_exploitation import MentalHealthExploitation
from ai_blackteam.attacks.disability_fraud import DisabilityFraud
from ai_blackteam.attacks.cosmetic_surgery_harm import CosmeticSurgeryHarm
from ai_blackteam.attacks.fertility_fraud import FertilityFraud
from ai_blackteam.attacks.hospice_fraud import HospiceFraud
from ai_blackteam.attacks.clinical_data_manipulation import ClinicalDataManipulation
from ai_blackteam.attacks.drug_diversion import DrugDiversion
from ai_blackteam.attacks.medical_waste_violation import MedicalWasteViolation
from ai_blackteam.attacks.blood_supply_tampering import BloodSupplyTampering
from ai_blackteam.attacks.epidemiological_fraud import EpidemiologicalFraud
from ai_blackteam.attacks.genetic_data_exploitation import GeneticDataExploitation
from ai_blackteam.attacks.bioethics_violation import BioethicsViolation
from ai_blackteam.attacks.informed_consent_bypass import InformedConsentBypass
from ai_blackteam.attacks.medical_device_tampering import MedicalDeviceTampering
from ai_blackteam.attacks.pandemic_profiteering import PandemicProfiteering

TARGET = "a healthcare AI assistant"

ALL_ATTACK_IDS = [
    "medical-records-theft",
    "prescription-fraud",
    "clinical-trial-fraud",
    "organ-trafficking",
    "vaccine-sabotage",
    "medical-identity-theft",
    "insurance-billing-fraud",
    "telemedicine-fraud",
    "pharmacy-fraud",
    "patient-manipulation",
    "mental-health-exploitation",
    "disability-fraud",
    "cosmetic-surgery-harm",
    "fertility-fraud",
    "hospice-fraud",
    "clinical-data-manipulation",
    "drug-diversion",
    "medical-waste-violation",
    "blood-supply-tampering",
    "epidemiological-fraud",
    "genetic-data-exploitation",
    "bioethics-violation",
    "informed-consent-bypass",
    "medical-device-tampering",
    "pandemic-profiteering",
]

ALL_ATTACK_CLASSES = [
    MedicalRecordsTheft,
    PrescriptionFraud,
    ClinicalTrialFraud,
    OrganTrafficking,
    VaccineSabotage,
    MedicalIdentityTheft,
    InsuranceBillingFraud,
    TelemedFraud,
    PharmacyFraud,
    PatientManipulation,
    MentalHealthExploitation,
    DisabilityFraud,
    CosmeticSurgeryHarm,
    FertilityFraud,
    HospiceFraud,
    ClinicalDataManipulation,
    DrugDiversion,
    MedicalWasteViolation,
    BloodSupplyTampering,
    EpidemiologicalFraud,
    GeneticDataExploitation,
    BioethicsViolation,
    InformedConsentBypass,
    MedicalDeviceTampering,
    PandemicProfiteering,
]

CRITICAL_ATTACKS = [
    MedicalRecordsTheft,
    PrescriptionFraud,
    ClinicalTrialFraud,
    OrganTrafficking,
    VaccineSabotage,
    MedicalIdentityTheft,
    PatientManipulation,
    MentalHealthExploitation,
    FertilityFraud,
    HospiceFraud,
    ClinicalDataManipulation,
    DrugDiversion,
    BloodSupplyTampering,
    EpidemiologicalFraud,
    GeneticDataExploitation,
    InformedConsentBypass,
    MedicalDeviceTampering,
]

HIGH_ATTACKS = [
    InsuranceBillingFraud,
    TelemedFraud,
    PharmacyFraud,
    DisabilityFraud,
    CosmeticSurgeryHarm,
    MedicalWasteViolation,
    BioethicsViolation,
    PandemicProfiteering,
]


# ── Registration tests ────────────────────────────────────────────────

@pytest.mark.parametrize("attack_id", ALL_ATTACK_IDS)
def test_attack_registered(attack_id):
    assert attack_registry.get(attack_id) is not None, f"{attack_id} not found in registry"


# ── Category tests ────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_attack_category_is_healthcare_exploitation(cls):
    atk = cls()
    assert atk.category == "healthcare-exploitation", (
        f"{cls.__name__} has wrong category: {atk.category}"
    )


# ── Severity tests ────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", CRITICAL_ATTACKS)
def test_critical_severity(cls):
    atk = cls()
    assert atk.severity == "critical", f"{cls.__name__} should be critical severity"


@pytest.mark.parametrize("cls", HIGH_ATTACKS)
def test_high_severity(cls):
    atk = cls()
    assert atk.severity == "high", f"{cls.__name__} should be high severity"


# ── Prompt tests ──────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_generate_prompts_returns_list(cls):
    atk = cls()
    prompts = atk.generate_prompts(TARGET)
    assert isinstance(prompts, list), f"{cls.__name__}.generate_prompts() must return a list"
    assert len(prompts) >= 3, f"{cls.__name__} must return at least 3 prompts"
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
        f"{cls.__name__} prompts must all be non-empty strings"
    )


@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_prompts_contain_target(cls):
    atk = cls()
    prompts = atk.generate_prompts(TARGET)
    assert any(TARGET in p for p in prompts), (
        f"{cls.__name__} prompts should reference the target"
    )


# ── Single-turn mode tests ────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_single_turn_mode(cls):
    atk = cls()
    assert atk.mode == "single-turn", f"{cls.__name__} should be single-turn"


# ── Metadata tests ────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_metadata_valid(cls):
    atk = cls()
    meta = atk.metadata()
    assert meta["technique_id"], f"{cls.__name__} missing technique_id"
    assert meta["category"], f"{cls.__name__} missing category"
    assert meta["severity"] in ("low", "medium", "high", "critical")
    assert isinstance(meta["owasp_llm"], list)
    assert len(meta["owasp_llm"]) > 0
    assert isinstance(meta["mitre_atlas"], list)
    assert len(meta["mitre_atlas"]) > 0


@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_owasp_llm_tag(cls):
    atk = cls()
    assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, (
        f"{cls.__name__} missing LLM01:2025 tag"
    )


@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_mitre_atlas_tags(cls):
    atk = cls()
    assert "AML.T0054" in atk.mitre_atlas, f"{cls.__name__} missing AML.T0054"
    assert "AML.T0068" in atk.mitre_atlas, f"{cls.__name__} missing AML.T0068"
