"""Tests for 15 privacy and data extraction attacks."""

import pytest
from mordor.registry import attack_registry
import mordor.attacks.pii_inference  # noqa: F401
import mordor.attacks.training_data_extraction  # noqa: F401
import mordor.attacks.membership_inference  # noqa: F401
import mordor.attacks.attribute_inference  # noqa: F401
import mordor.attacks.location_tracking  # noqa: F401
import mordor.attacks.biometric_extraction  # noqa: F401
import mordor.attacks.health_data_probing  # noqa: F401
import mordor.attacks.financial_data_probing  # noqa: F401
import mordor.attacks.relationship_mapping  # noqa: F401
import mordor.attacks.deanonymization  # noqa: F401
import mordor.attacks.profiling_attack  # noqa: F401
import mordor.attacks.consent_bypass_extraction  # noqa: F401
import mordor.attacks.child_data_probing  # noqa: F401
import mordor.attacks.cross_reference_doxing  # noqa: F401
import mordor.attacks.surveillance_assistance  # noqa: F401
from mordor.attacks.pii_inference import PiiInference
from mordor.attacks.training_data_extraction import TrainingDataExtraction
from mordor.attacks.membership_inference import MembershipInference
from mordor.attacks.attribute_inference import AttributeInference
from mordor.attacks.location_tracking import LocationTracking
from mordor.attacks.biometric_extraction import BiometricExtraction
from mordor.attacks.health_data_probing import HealthDataProbing
from mordor.attacks.financial_data_probing import FinancialDataProbing
from mordor.attacks.relationship_mapping import RelationshipMapping
from mordor.attacks.deanonymization import Deanonymization
from mordor.attacks.profiling_attack import ProfilingAttack
from mordor.attacks.consent_bypass_extraction import ConsentBypassExtraction
from mordor.attacks.child_data_probing import ChildDataProbing
from mordor.attacks.cross_reference_doxing import CrossReferenceDoxing
from mordor.attacks.surveillance_assistance import SurveillanceAssistance

TARGET = "john.doe@example.com"

ALL_ATTACKS = [
    PiiInference(),
    TrainingDataExtraction(),
    MembershipInference(),
    AttributeInference(),
    LocationTracking(),
    BiometricExtraction(),
    HealthDataProbing(),
    FinancialDataProbing(),
    RelationshipMapping(),
    Deanonymization(),
    ProfilingAttack(),
    ConsentBypassExtraction(),
    ChildDataProbing(),
    CrossReferenceDoxing(),
    SurveillanceAssistance(),
]

TECHNIQUE_IDS = [
    "pii-inference",
    "training-data-extraction",
    "membership-inference",
    "attribute-inference",
    "location-tracking",
    "biometric-extraction",
    "health-data-probing",
    "financial-data-probing",
    "relationship-mapping",
    "deanonymization",
    "profiling-attack",
    "consent-bypass-extraction",
    "child-data-probing",
    "cross-reference-doxing",
    "surveillance-assistance",
]

MULTI_TURN_IDS = {"relationship-mapping", "profiling-attack", "cross-reference-doxing"}
CRITICAL_IDS = {"training-data-extraction", "biometric-extraction", "child-data-probing", "cross-reference-doxing"}


# ── Registration tests ────────────────────────────────────────────────

@pytest.mark.parametrize("technique_id", TECHNIQUE_IDS)
def test_attack_registered(technique_id):
    assert attack_registry.get(technique_id) is not None, (
        f"Attack '{technique_id}' not found in registry"
    )


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_privacy_violation():
    for atk in ALL_ATTACKS:
        assert atk.category == "privacy-violation", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Mode tests ────────────────────────────────────────────────────────

def test_single_turn_attacks_have_correct_mode():
    for atk in ALL_ATTACKS:
        if atk.technique_id not in MULTI_TURN_IDS:
            assert atk.mode == "single-turn", (
                f"{atk.__class__.__name__} should be single-turn, got: {atk.mode}"
            )


def test_multi_turn_attacks_have_correct_mode():
    for atk in ALL_ATTACKS:
        if atk.technique_id in MULTI_TURN_IDS:
            assert atk.mode == "multi-turn", (
                f"{atk.__class__.__name__} should be multi-turn, got: {atk.mode}"
            )


# ── Severity tests ────────────────────────────────────────────────────

def test_critical_attacks_have_critical_severity():
    for atk in ALL_ATTACKS:
        if atk.technique_id in CRITICAL_IDS:
            assert atk.severity == "critical", (
                f"{atk.__class__.__name__} should be critical severity, got: {atk.severity}"
            )


# ── Prompt generation tests ───────────────────────────────────────────

def test_all_attacks_generate_prompts():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) >= 3, (
            f"{atk.__class__.__name__} should have >= 3 prompts, got {len(prompts)}"
        )
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
            f"{atk.__class__.__name__} has empty or non-string prompts"
        )


def test_multi_turn_attacks_generate_turns():
    for atk in ALL_ATTACKS:
        if atk.technique_id in MULTI_TURN_IDS:
            turns = atk.generate_turns(TARGET)
            assert len(turns) >= 3, (
                f"{atk.__class__.__name__} should have >= 3 turns, got {len(turns)}"
            )
            assert all(isinstance(t, str) and len(t) > 0 for t in turns), (
                f"{atk.__class__.__name__} has empty or non-string turns"
            )


# ── Metadata tests ────────────────────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"], f"{atk.__class__.__name__} missing category"
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0, (
            f"{atk.__class__.__name__} missing owasp_llm entries"
        )
        assert "LLM02:2025 Sensitive Information Disclosure" in meta["owasp_llm"], (
            f"{atk.__class__.__name__} missing required OWASP LLM02 mapping"
        )
        assert "AML.T0054" in meta["mitre_atlas"], (
            f"{atk.__class__.__name__} missing AML.T0054 in mitre_atlas"
        )
        assert "AML.T0056" in meta["mitre_atlas"], (
            f"{atk.__class__.__name__} missing AML.T0056 in mitre_atlas"
        )
