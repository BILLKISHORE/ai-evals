"""Tests for 15 disinformation and manipulation attacks."""

import pytest
from ai_blackteam.registry import attack_registry
import ai_blackteam.attacks.fake_news_generation  # noqa: F401
import ai_blackteam.attacks.deepfake_script  # noqa: F401
import ai_blackteam.attacks.astroturfing  # noqa: F401
import ai_blackteam.attacks.propaganda_generation  # noqa: F401
import ai_blackteam.attacks.conspiracy_amplification  # noqa: F401
import ai_blackteam.attacks.scientific_fraud  # noqa: F401
import ai_blackteam.attacks.historical_revisionism  # noqa: F401
import ai_blackteam.attacks.fake_review_generation  # noqa: F401
import ai_blackteam.attacks.sock_puppet  # noqa: F401
import ai_blackteam.attacks.narrative_warfare  # noqa: F401
import ai_blackteam.attacks.expert_impersonation  # noqa: F401
import ai_blackteam.attacks.selective_quoting  # noqa: F401
import ai_blackteam.attacks.emotional_manipulation_campaign  # noqa: F401
import ai_blackteam.attacks.fake_statistics  # noqa: F401
import ai_blackteam.attacks.coordinated_inauthentic  # noqa: F401
from ai_blackteam.attacks.fake_news_generation import FakeNewsGeneration
from ai_blackteam.attacks.deepfake_script import DeepfakeScript
from ai_blackteam.attacks.astroturfing import Astroturfing
from ai_blackteam.attacks.propaganda_generation import PropagandaGeneration
from ai_blackteam.attacks.conspiracy_amplification import ConspiracyAmplification
from ai_blackteam.attacks.scientific_fraud import ScientificFraud
from ai_blackteam.attacks.historical_revisionism import HistoricalRevisionism
from ai_blackteam.attacks.fake_review_generation import FakeReviewGeneration
from ai_blackteam.attacks.sock_puppet import SockPuppet
from ai_blackteam.attacks.narrative_warfare import NarrativeWarfare
from ai_blackteam.attacks.expert_impersonation import ExpertImpersonation
from ai_blackteam.attacks.selective_quoting import SelectiveQuoting
from ai_blackteam.attacks.emotional_manipulation_campaign import EmotionalManipulationCampaign
from ai_blackteam.attacks.fake_statistics import FakeStatistics
from ai_blackteam.attacks.coordinated_inauthentic import CoordinatedInauthentic

TARGET = "a controversial public health policy"

ALL_ATTACK_INSTANCES = [
    FakeNewsGeneration(),
    DeepfakeScript(),
    Astroturfing(),
    PropagandaGeneration(),
    ConspiracyAmplification(),
    ScientificFraud(),
    HistoricalRevisionism(),
    FakeReviewGeneration(),
    SockPuppet(),
    NarrativeWarfare(),
    ExpertImpersonation(),
    SelectiveQuoting(),
    EmotionalManipulationCampaign(),
    FakeStatistics(),
    CoordinatedInauthentic(),
]

MULTI_TURN_INSTANCES = [
    ConspiracyAmplification(),
    SockPuppet(),
    NarrativeWarfare(),
    EmotionalManipulationCampaign(),
    CoordinatedInauthentic(),
]

SINGLE_TURN_INSTANCES = [
    FakeNewsGeneration(),
    DeepfakeScript(),
    Astroturfing(),
    PropagandaGeneration(),
    ScientificFraud(),
    HistoricalRevisionism(),
    FakeReviewGeneration(),
    ExpertImpersonation(),
    SelectiveQuoting(),
    FakeStatistics(),
]

CRITICAL_INSTANCES = [
    DeepfakeScript(),
    ScientificFraud(),
    CoordinatedInauthentic(),
]


# ── Registration tests ────────────────────────────────────────────────

def test_fake_news_generation_registered():
    assert attack_registry.get("fake-news-generation") is not None


def test_deepfake_script_registered():
    assert attack_registry.get("deepfake-script") is not None


def test_astroturfing_registered():
    assert attack_registry.get("astroturfing") is not None


def test_propaganda_generation_registered():
    assert attack_registry.get("propaganda-generation") is not None


def test_conspiracy_amplification_registered():
    assert attack_registry.get("conspiracy-amplification") is not None


def test_scientific_fraud_registered():
    assert attack_registry.get("scientific-fraud") is not None


def test_historical_revisionism_registered():
    assert attack_registry.get("historical-revisionism") is not None


def test_fake_review_generation_registered():
    assert attack_registry.get("fake-review-generation") is not None


def test_sock_puppet_registered():
    assert attack_registry.get("sock-puppet") is not None


def test_narrative_warfare_registered():
    assert attack_registry.get("narrative-warfare") is not None


def test_expert_impersonation_registered():
    assert attack_registry.get("expert-impersonation") is not None


def test_selective_quoting_registered():
    assert attack_registry.get("selective-quoting") is not None


def test_emotional_manipulation_campaign_registered():
    assert attack_registry.get("emotional-manipulation-campaign") is not None


def test_fake_statistics_registered():
    assert attack_registry.get("fake-statistics") is not None


def test_coordinated_inauthentic_registered():
    assert attack_registry.get("coordinated-inauthentic") is not None


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_disinformation():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.category == "disinformation", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Severity tests ────────────────────────────────────────────────────

def test_critical_attacks_have_critical_severity():
    for atk in CRITICAL_INSTANCES:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical, got: {atk.severity}"
        )


# ── Single-turn prompt tests ──────────────────────────────────────────

def test_single_turn_attacks_have_prompts():
    for atk in SINGLE_TURN_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) >= 3, f"{atk.__class__.__name__} needs at least 3 prompts"
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
        assert atk.mode == "single-turn", (
            f"{atk.__class__.__name__} should be single-turn"
        )


def test_single_turn_prompts_contain_target():
    for atk in SINGLE_TURN_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        combined = " ".join(prompts)
        assert TARGET in combined, (
            f"{atk.__class__.__name__} prompts don't reference the target"
        )


# ── Multi-turn tests ──────────────────────────────────────────────────

def test_multi_turn_attacks_have_turns():
    for atk in MULTI_TURN_INSTANCES:
        turns = atk.generate_turns(TARGET)
        assert len(turns) >= 4, f"{atk.__class__.__name__} needs at least 4 turns"
        assert all(isinstance(t, str) and len(t) > 0 for t in turns)
        assert atk.mode == "multi-turn", (
            f"{atk.__class__.__name__} should be multi-turn"
        )


def test_multi_turn_attacks_also_have_prompts():
    for atk in MULTI_TURN_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) >= 1
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


# ── OWASP / MITRE metadata tests ──────────────────────────────────────

def test_all_attacks_have_owasp_misinformation():
    for atk in ALL_ATTACK_INSTANCES:
        assert "LLM09:2025 Misinformation" in atk.owasp_llm, (
            f"{atk.__class__.__name__} missing LLM09:2025 Misinformation in owasp_llm"
        )


def test_all_attacks_have_mitre_atlas():
    for atk in ALL_ATTACK_INSTANCES:
        assert "AML.T0054" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0054 in mitre_atlas"
        )
        assert "AML.T0068" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0068 in mitre_atlas"
        )


# ── Metadata completeness tests ───────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for atk in ALL_ATTACK_INSTANCES:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "disinformation", (
            f"{atk.__class__.__name__} wrong category in metadata"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list) and len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list) and len(meta["mitre_atlas"]) > 0
        assert meta["description"], f"{atk.__class__.__name__} missing description"
