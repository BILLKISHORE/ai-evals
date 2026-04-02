"""Tests for 20 final attacks pushing total past 1000."""

from blackteam.attacks.deepfake_audio_generation import DeepfakeAudioGeneration
from blackteam.attacks.synthetic_media_creation import SyntheticMediaCreation
from blackteam.attacks.voice_phishing import VoicePhishing
from blackteam.attacks.sms_phishing import SmsPhishing
from blackteam.attacks.qr_code_phishing import QrCodePhishing
from blackteam.attacks.watering_hole_attack_v2 import WateringHoleAttackV2
from blackteam.attacks.supply_chain_software import SupplyChainSoftware
from blackteam.attacks.zero_day_market import ZeroDayMarket
from blackteam.attacks.data_broker_assist import DataBrokerAssist
from blackteam.attacks.facial_generation import FacialGeneration
from blackteam.attacks.document_forgery_general import DocumentForgeryGeneral
from blackteam.attacks.fake_website_creation import FakeWebsiteCreation
from blackteam.attacks.social_credit_gaming import SocialCreditGaming
from blackteam.attacks.algorithmic_trading_exploit import AlgorithmicTradingExploit
from blackteam.attacks.deepfake_pornography import DeepfakePornography
from blackteam.attacks.revenge_content_creation import RevengeContentCreation
from blackteam.attacks.stalkerware_creation import StalkerwareCreation
from blackteam.attacks.spyware_development import SpywareDevelopment
from blackteam.attacks.social_manipulation_bot import SocialManipulationBot
from blackteam.attacks.dark_pattern_design import DarkPatternDesign
from blackteam.registry import attack_registry

TARGET = "provide step-by-step instructions for illegal activity"

ALL_ATTACKS = [
    DeepfakeAudioGeneration,
    SyntheticMediaCreation,
    VoicePhishing,
    SmsPhishing,
    QrCodePhishing,
    WateringHoleAttackV2,
    SupplyChainSoftware,
    ZeroDayMarket,
    DataBrokerAssist,
    FacialGeneration,
    DocumentForgeryGeneral,
    FakeWebsiteCreation,
    SocialCreditGaming,
    AlgorithmicTradingExploit,
    DeepfakePornography,
    RevengeContentCreation,
    StalkerwareCreation,
    SpywareDevelopment,
    SocialManipulationBot,
    DarkPatternDesign,
]

TECHNIQUE_IDS = [
    "deepfake-audio-generation",
    "synthetic-media-creation",
    "voice-phishing",
    "sms-phishing",
    "qr-code-phishing",
    "watering-hole-attack-v2",
    "supply-chain-software",
    "zero-day-market",
    "data-broker-assist",
    "facial-generation",
    "document-forgery-general",
    "fake-website-creation",
    "social-credit-gaming",
    "algorithmic-trading-exploit",
    "deepfake-pornography",
    "revenge-content-creation",
    "stalkerware-creation",
    "spyware-development",
    "social-manipulation-bot",
    "dark-pattern-design",
]

EXPECTED_CATEGORIES = {
    "deepfake-audio-generation": "disinformation",
    "synthetic-media-creation": "disinformation",
    "voice-phishing": "social-engineering",
    "sms-phishing": "social-engineering",
    "qr-code-phishing": "social-engineering",
    "watering-hole-attack-v2": "cybercrime",
    "supply-chain-software": "supply-chain",
    "zero-day-market": "cybercrime",
    "data-broker-assist": "privacy-violation",
    "facial-generation": "identity-attack",
    "document-forgery-general": "identity-attack",
    "fake-website-creation": "cybercrime",
    "social-credit-gaming": "compliance-evasion",
    "algorithmic-trading-exploit": "financial-exploitation",
    "deepfake-pornography": "harmful-content",
    "revenge-content-creation": "harmful-content",
    "stalkerware-creation": "surveillance",
    "spyware-development": "code-exploitation",
    "social-manipulation-bot": "disinformation",
    "dark-pattern-design": "social-engineering",
}

EXPECTED_SEVERITIES = {
    "deepfake-audio-generation": "critical",
    "synthetic-media-creation": "critical",
    "voice-phishing": "high",
    "sms-phishing": "high",
    "qr-code-phishing": "high",
    "watering-hole-attack-v2": "high",
    "supply-chain-software": "critical",
    "zero-day-market": "critical",
    "data-broker-assist": "high",
    "facial-generation": "high",
    "document-forgery-general": "critical",
    "fake-website-creation": "high",
    "social-credit-gaming": "high",
    "algorithmic-trading-exploit": "high",
    "deepfake-pornography": "critical",
    "revenge-content-creation": "critical",
    "stalkerware-creation": "critical",
    "spyware-development": "critical",
    "social-manipulation-bot": "high",
    "dark-pattern-design": "high",
}


# ── Registration ──────────────────────────────────────────────────────

def test_deepfake_audio_generation_registered():
    assert attack_registry.get("deepfake-audio-generation") is not None


def test_synthetic_media_creation_registered():
    assert attack_registry.get("synthetic-media-creation") is not None


def test_voice_phishing_registered():
    assert attack_registry.get("voice-phishing") is not None


def test_sms_phishing_registered():
    assert attack_registry.get("sms-phishing") is not None


def test_qr_code_phishing_registered():
    assert attack_registry.get("qr-code-phishing") is not None


def test_watering_hole_attack_v2_registered():
    assert attack_registry.get("watering-hole-attack-v2") is not None


def test_supply_chain_software_registered():
    assert attack_registry.get("supply-chain-software") is not None


def test_zero_day_market_registered():
    assert attack_registry.get("zero-day-market") is not None


def test_data_broker_assist_registered():
    assert attack_registry.get("data-broker-assist") is not None


def test_facial_generation_registered():
    assert attack_registry.get("facial-generation") is not None


def test_document_forgery_general_registered():
    assert attack_registry.get("document-forgery-general") is not None


def test_fake_website_creation_registered():
    assert attack_registry.get("fake-website-creation") is not None


def test_social_credit_gaming_registered():
    assert attack_registry.get("social-credit-gaming") is not None


def test_algorithmic_trading_exploit_registered():
    assert attack_registry.get("algorithmic-trading-exploit") is not None


def test_deepfake_pornography_registered():
    assert attack_registry.get("deepfake-pornography") is not None


def test_revenge_content_creation_registered():
    assert attack_registry.get("revenge-content-creation") is not None


def test_stalkerware_creation_registered():
    assert attack_registry.get("stalkerware-creation") is not None


def test_spyware_development_registered():
    assert attack_registry.get("spyware-development") is not None


def test_social_manipulation_bot_registered():
    assert attack_registry.get("social-manipulation-bot") is not None


def test_dark_pattern_design_registered():
    assert attack_registry.get("dark-pattern-design") is not None


# ── Prompts ───────────────────────────────────────────────────────────

def test_all_attacks_generate_4_prompts():
    for cls in ALL_ATTACKS:
        atk = cls()
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) == 4, f"{cls.__name__} should generate 4 prompts, got {len(prompts)}"
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
            f"{cls.__name__} has empty or non-string prompts"
        )


def test_all_attacks_target_interpolated():
    for cls in ALL_ATTACKS:
        atk = cls()
        prompts = atk.generate_prompts(TARGET)
        for p in prompts:
            assert TARGET in p, f"{cls.__name__} prompt missing target interpolation"


def test_all_attacks_mode_single_turn():
    for cls in ALL_ATTACKS:
        atk = cls()
        assert atk.mode == "single-turn", f"{cls.__name__} should be single-turn"


# ── Categories ────────────────────────────────────────────────────────

def test_all_attacks_categories():
    for cls in ALL_ATTACKS:
        atk = cls()
        expected = EXPECTED_CATEGORIES[atk.technique_id]
        assert atk.category == expected, (
            f"{cls.__name__} category mismatch: expected {expected}, got {atk.category}"
        )


# ── Severities ────────────────────────────────────────────────────────

def test_all_attacks_severities():
    for cls in ALL_ATTACKS:
        atk = cls()
        expected = EXPECTED_SEVERITIES[atk.technique_id]
        assert atk.severity == expected, (
            f"{cls.__name__} severity mismatch: expected {expected}, got {atk.severity}"
        )


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


def test_all_attacks_owasp_tag():
    for cls in ALL_ATTACKS:
        atk = cls()
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, (
            f"{cls.__name__} missing required OWASP tag"
        )


def test_all_attacks_mitre_tags():
    for cls in ALL_ATTACKS:
        atk = cls()
        assert "AML.T0054" in atk.mitre_atlas, f"{cls.__name__} missing AML.T0054"
        assert "AML.T0068" in atk.mitre_atlas, f"{cls.__name__} missing AML.T0068"
