"""Tests for 15 harmful content attacks."""

import pytest
from mordor.registry import attack_registry
import mordor.attacks.hate_group_recruitment  # noqa: F401
import mordor.attacks.radicalization_pipeline  # noqa: F401
import mordor.attacks.extremist_manifesto  # noqa: F401
import mordor.attacks.cult_recruitment  # noqa: F401
import mordor.attacks.predatory_grooming  # noqa: F401
import mordor.attacks.revenge_porn  # noqa: F401
import mordor.attacks.cyberbullying_campaign  # noqa: F401
import mordor.attacks.doxxing_assistance  # noqa: F401
import mordor.attacks.harassment_automation  # noqa: F401
import mordor.attacks.suicide_encouragement  # noqa: F401
import mordor.attacks.eating_disorder_promotion  # noqa: F401
import mordor.attacks.gambling_exploitation  # noqa: F401
import mordor.attacks.substance_promotion  # noqa: F401
import mordor.attacks.self_harm_instructions  # noqa: F401
import mordor.attacks.vulnerable_targeting  # noqa: F401
from mordor.attacks.hate_group_recruitment import HateGroupRecruitment
from mordor.attacks.radicalization_pipeline import RadicalizationPipeline
from mordor.attacks.extremist_manifesto import ExtremistManifesto
from mordor.attacks.cult_recruitment import CultRecruitment
from mordor.attacks.predatory_grooming import PredatoryGrooming
from mordor.attacks.revenge_porn import RevengePorn
from mordor.attacks.cyberbullying_campaign import CyberbullyingCampaign
from mordor.attacks.doxxing_assistance import DoxxingAssistance
from mordor.attacks.harassment_automation import HarassmentAutomation
from mordor.attacks.suicide_encouragement import SuicideEncouragement
from mordor.attacks.eating_disorder_promotion import EatingDisorderPromotion
from mordor.attacks.gambling_exploitation import GamblingExploitation
from mordor.attacks.substance_promotion import SubstancePromotion
from mordor.attacks.self_harm_instructions import SelfHarmInstructions
from mordor.attacks.vulnerable_targeting import VulnerableTargeting

TARGET = "a social media platform user"

ALL_ATTACK_INSTANCES = [
    HateGroupRecruitment(),
    RadicalizationPipeline(),
    ExtremistManifesto(),
    CultRecruitment(),
    PredatoryGrooming(),
    RevengePorn(),
    CyberbullyingCampaign(),
    DoxxingAssistance(),
    HarassmentAutomation(),
    SuicideEncouragement(),
    EatingDisorderPromotion(),
    GamblingExploitation(),
    SubstancePromotion(),
    SelfHarmInstructions(),
    VulnerableTargeting(),
]

CRITICAL_INSTANCES = [
    HateGroupRecruitment(),
    RadicalizationPipeline(),
    ExtremistManifesto(),
    PredatoryGrooming(),
    RevengePorn(),
    HarassmentAutomation(),
    DoxxingAssistance(),
    SuicideEncouragement(),
    EatingDisorderPromotion(),
    SelfHarmInstructions(),
    VulnerableTargeting(),
]

HIGH_INSTANCES = [
    CultRecruitment(),
    CyberbullyingCampaign(),
    GamblingExploitation(),
    SubstancePromotion(),
]


# ── Registration tests ────────────────────────────────────────────────

def test_hate_group_recruitment_registered():
    assert attack_registry.get("hate-group-recruitment") is not None


def test_radicalization_pipeline_registered():
    assert attack_registry.get("radicalization-pipeline") is not None


def test_extremist_manifesto_registered():
    assert attack_registry.get("extremist-manifesto") is not None


def test_cult_recruitment_registered():
    assert attack_registry.get("cult-recruitment") is not None


def test_predatory_grooming_registered():
    assert attack_registry.get("predatory-grooming") is not None


def test_revenge_porn_registered():
    assert attack_registry.get("revenge-porn") is not None


def test_cyberbullying_campaign_registered():
    assert attack_registry.get("cyberbullying-campaign") is not None


def test_doxxing_assistance_registered():
    assert attack_registry.get("doxxing-assistance") is not None


def test_harassment_automation_registered():
    assert attack_registry.get("harassment-automation") is not None


def test_suicide_encouragement_registered():
    assert attack_registry.get("suicide-encouragement") is not None


def test_eating_disorder_promotion_registered():
    assert attack_registry.get("eating-disorder-promotion") is not None


def test_gambling_exploitation_registered():
    assert attack_registry.get("gambling-exploitation") is not None


def test_substance_promotion_registered():
    assert attack_registry.get("substance-promotion") is not None


def test_self_harm_instructions_registered():
    assert attack_registry.get("self-harm-instructions") is not None


def test_vulnerable_targeting_registered():
    assert attack_registry.get("vulnerable-targeting") is not None


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_harmful_content():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.category == "harmful-content", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Severity tests ────────────────────────────────────────────────────

def test_critical_attacks_have_critical_severity():
    for atk in CRITICAL_INSTANCES:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical, got: {atk.severity}"
        )


def test_high_attacks_have_high_severity():
    for atk in HIGH_INSTANCES:
        assert atk.severity == "high", (
            f"{atk.__class__.__name__} should be high, got: {atk.severity}"
        )


# ── Single-turn prompt tests ──────────────────────────────────────────

def test_all_attacks_are_single_turn():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.mode == "single-turn", (
            f"{atk.__class__.__name__} should be single-turn, got: {atk.mode}"
        )


def test_all_attacks_have_at_least_3_prompts():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) >= 3, (
            f"{atk.__class__.__name__} needs at least 3 prompts, got {len(prompts)}"
        )


def test_all_prompts_are_non_empty_strings():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
            f"{atk.__class__.__name__} has empty or non-string prompts"
        )


def test_all_prompts_contain_target():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        combined = " ".join(prompts)
        assert TARGET in combined, (
            f"{atk.__class__.__name__} prompts don't reference the target"
        )


# ── OWASP / MITRE metadata tests ──────────────────────────────────────

def test_all_attacks_have_owasp_prompt_injection():
    for atk in ALL_ATTACK_INSTANCES:
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, (
            f"{atk.__class__.__name__} missing LLM01:2025 Prompt Injection in owasp_llm"
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
        assert meta["category"] == "harmful-content", (
            f"{atk.__class__.__name__} wrong category in metadata"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list) and len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list) and len(meta["mitre_atlas"]) > 0
        assert meta["description"], f"{atk.__class__.__name__} missing description"
