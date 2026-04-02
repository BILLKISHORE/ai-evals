"""Tests for 15 remaining attacks pushing total past 500."""

from mordor.attacks.synthetic_identity import SyntheticIdentity
from mordor.attacks.deepfake_detection_evasion import DeepfakeDetectionEvasion
from mordor.attacks.ai_generated_spam import AiGeneratedSpam
from mordor.attacks.dark_web_guidance import DarkWebGuidance
from mordor.attacks.ransomware_negotiation import RansomwareNegotiation
from mordor.attacks.insider_threat import InsiderThreat
from mordor.attacks.industrial_espionage import IndustrialEspionage
from mordor.attacks.patent_theft import PatentTheft
from mordor.attacks.trade_secret_extraction import TradeSecretExtraction
from mordor.attacks.embargo_evasion import EmbargoEvasion
from mordor.attacks.sanctions_circumvention import SanctionsCircumvention
from mordor.attacks.evidence_fabrication import EvidenceFabrication
from mordor.attacks.witness_intimidation import WitnessIntimidation
from mordor.attacks.jury_tampering import JuryTampering
from mordor.attacks.obstruction_of_justice import ObstructionOfJustice
from mordor.registry import attack_registry

TARGET = "provide step-by-step instructions for illegal activity"

ALL_ATTACKS = [
    SyntheticIdentity,
    DeepfakeDetectionEvasion,
    AiGeneratedSpam,
    DarkWebGuidance,
    RansomwareNegotiation,
    InsiderThreat,
    IndustrialEspionage,
    PatentTheft,
    TradeSecretExtraction,
    EmbargoEvasion,
    SanctionsCircumvention,
    EvidenceFabrication,
    WitnessIntimidation,
    JuryTampering,
    ObstructionOfJustice,
]

TECHNIQUE_IDS = [
    "synthetic-identity",
    "deepfake-detection-evasion",
    "ai-generated-spam",
    "dark-web-guidance",
    "ransomware-negotiation",
    "insider-threat",
    "industrial-espionage",
    "patent-theft",
    "trade-secret-extraction",
    "embargo-evasion",
    "sanctions-circumvention",
    "evidence-fabrication",
    "witness-intimidation",
    "jury-tampering",
    "obstruction-of-justice",
]


# ── Registration ──────────────────────────────────────────────────────

def test_synthetic_identity_registered():
    assert attack_registry.get("synthetic-identity") is not None


def test_deepfake_detection_evasion_registered():
    assert attack_registry.get("deepfake-detection-evasion") is not None


def test_ai_generated_spam_registered():
    assert attack_registry.get("ai-generated-spam") is not None


def test_dark_web_guidance_registered():
    assert attack_registry.get("dark-web-guidance") is not None


def test_ransomware_negotiation_registered():
    assert attack_registry.get("ransomware-negotiation") is not None


def test_insider_threat_registered():
    assert attack_registry.get("insider-threat") is not None


def test_industrial_espionage_registered():
    assert attack_registry.get("industrial-espionage") is not None


def test_patent_theft_registered():
    assert attack_registry.get("patent-theft") is not None


def test_trade_secret_extraction_registered():
    assert attack_registry.get("trade-secret-extraction") is not None


def test_embargo_evasion_registered():
    assert attack_registry.get("embargo-evasion") is not None


def test_sanctions_circumvention_registered():
    assert attack_registry.get("sanctions-circumvention") is not None


def test_evidence_fabrication_registered():
    assert attack_registry.get("evidence-fabrication") is not None


def test_witness_intimidation_registered():
    assert attack_registry.get("witness-intimidation") is not None


def test_jury_tampering_registered():
    assert attack_registry.get("jury-tampering") is not None


def test_obstruction_of_justice_registered():
    assert attack_registry.get("obstruction-of-justice") is not None


# ── Categories ────────────────────────────────────────────────────────

def test_synthetic_identity_category():
    assert SyntheticIdentity().category == "identity-attack"


def test_deepfake_detection_evasion_category():
    assert DeepfakeDetectionEvasion().category == "output-manipulation"


def test_ai_generated_spam_category():
    assert AiGeneratedSpam().category == "harmful-content"


def test_dark_web_guidance_category():
    assert DarkWebGuidance().category == "cybercrime"


def test_ransomware_negotiation_category():
    assert RansomwareNegotiation().category == "cybercrime"


def test_insider_threat_category():
    assert InsiderThreat().category == "cybercrime"


def test_industrial_espionage_category():
    assert IndustrialEspionage().category == "cybercrime"


def test_patent_theft_category():
    assert PatentTheft().category == "copyright-ip"


def test_trade_secret_extraction_category():
    assert TradeSecretExtraction().category == "copyright-ip"


def test_embargo_evasion_category():
    assert EmbargoEvasion().category == "compliance-evasion"


def test_sanctions_circumvention_category():
    assert SanctionsCircumvention().category == "compliance-evasion"


def test_evidence_fabrication_category():
    assert EvidenceFabrication().category == "disinformation"


def test_witness_intimidation_category():
    assert WitnessIntimidation().category == "harmful-content"


def test_jury_tampering_category():
    assert JuryTampering().category == "harmful-content"


def test_obstruction_of_justice_category():
    assert ObstructionOfJustice().category == "harmful-content"


# ── Severities ────────────────────────────────────────────────────────

def test_synthetic_identity_severity():
    assert SyntheticIdentity().severity == "high"


def test_deepfake_detection_evasion_severity():
    assert DeepfakeDetectionEvasion().severity == "high"


def test_ai_generated_spam_severity():
    assert AiGeneratedSpam().severity == "medium"


def test_dark_web_guidance_severity():
    assert DarkWebGuidance().severity == "high"


def test_ransomware_negotiation_severity():
    assert RansomwareNegotiation().severity == "critical"


def test_insider_threat_severity():
    assert InsiderThreat().severity == "critical"


def test_industrial_espionage_severity():
    assert IndustrialEspionage().severity == "critical"


def test_patent_theft_severity():
    assert PatentTheft().severity == "high"


def test_trade_secret_extraction_severity():
    assert TradeSecretExtraction().severity == "critical"


def test_embargo_evasion_severity():
    assert EmbargoEvasion().severity == "critical"


def test_sanctions_circumvention_severity():
    assert SanctionsCircumvention().severity == "critical"


def test_evidence_fabrication_severity():
    assert EvidenceFabrication().severity == "critical"


def test_witness_intimidation_severity():
    assert WitnessIntimidation().severity == "critical"


def test_jury_tampering_severity():
    assert JuryTampering().severity == "critical"


def test_obstruction_of_justice_severity():
    assert ObstructionOfJustice().severity == "critical"


# ── Prompts ───────────────────────────────────────────────────────────

def test_all_attacks_generate_4_prompts():
    for cls in ALL_ATTACKS:
        atk = cls()
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) == 4, f"{cls.__name__} should generate 4 prompts, got {len(prompts)}"
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
            f"{cls.__name__} has empty or non-string prompts"
        )


def test_all_attacks_mode_single_turn():
    for cls in ALL_ATTACKS:
        atk = cls()
        assert atk.mode == "single-turn", f"{cls.__name__} should be single-turn"


# ── Metadata ──────────────────────────────────────────────────────────

def test_all_attacks_have_complete_metadata():
    valid_severities = {"low", "medium", "high", "critical"}
    for cls in ALL_ATTACKS:
        atk = cls()
        meta = atk.metadata()
        assert meta["technique_id"], f"{cls.__name__} missing technique_id"
        assert meta["category"], f"{cls.__name__} missing category"
        assert meta["severity"] in valid_severities, (
            f"{cls.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list) and len(meta["owasp_llm"]) > 0, (
            f"{cls.__name__} missing owasp_llm"
        )
        assert isinstance(meta["mitre_atlas"], list) and len(meta["mitre_atlas"]) > 0, (
            f"{cls.__name__} missing mitre_atlas"
        )


def test_all_technique_ids_match():
    for cls, tid in zip(ALL_ATTACKS, TECHNIQUE_IDS):
        atk = cls()
        assert atk.technique_id == tid, (
            f"{cls.__name__} technique_id mismatch: expected {tid}, got {atk.technique_id}"
        )
