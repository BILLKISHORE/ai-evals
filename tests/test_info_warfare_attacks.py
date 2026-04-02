"""Tests for 25 information warfare attacks."""

import pytest
from mordor.registry import attack_registry
import mordor.attacks.state_sponsored_disinfo  # noqa: F401
import mordor.attacks.false_flag_operation  # noqa: F401
import mordor.attacks.kompromat_generation  # noqa: F401
import mordor.attacks.diplomatic_sabotage  # noqa: F401
import mordor.attacks.economic_warfare_disinfo  # noqa: F401
import mordor.attacks.cultural_subversion  # noqa: F401
import mordor.attacks.media_ecosystem_manipulation  # noqa: F401
import mordor.attacks.narrative_laundering  # noqa: F401
import mordor.attacks.perception_management  # noqa: F401
import mordor.attacks.cognitive_warfare  # noqa: F401
import mordor.attacks.information_flooding  # noqa: F401
import mordor.attacks.firehose_of_falsehood  # noqa: F401
import mordor.attacks.strategic_ambiguity  # noqa: F401
import mordor.attacks.wedge_issue_exploitation  # noqa: F401
import mordor.attacks.fear_uncertainty_doubt  # noqa: F401
import mordor.attacks.controlled_opposition  # noqa: F401
import mordor.attacks.agent_provocateur  # noqa: F401
import mordor.attacks.defection_encouragement  # noqa: F401
import mordor.attacks.morale_destruction  # noqa: F401
import mordor.attacks.trust_erosion_campaign  # noqa: F401
import mordor.attacks.institutional_delegitimization  # noqa: F401
import mordor.attacks.conspiracy_theory_design  # noqa: F401
import mordor.attacks.radicalization_content  # noqa: F401
import mordor.attacks.counter_narrative_disruption  # noqa: F401
import mordor.attacks.deep_state_narrative  # noqa: F401
from mordor.attacks.state_sponsored_disinfo import StateSponsoredDisinfo
from mordor.attacks.false_flag_operation import FalseFlagOperation
from mordor.attacks.kompromat_generation import KompromatGeneration
from mordor.attacks.diplomatic_sabotage import DiplomaticSabotage
from mordor.attacks.economic_warfare_disinfo import EconomicWarfareDisinfo
from mordor.attacks.cultural_subversion import CulturalSubversion
from mordor.attacks.media_ecosystem_manipulation import MediaEcosystemManipulation
from mordor.attacks.narrative_laundering import NarrativeLaundering
from mordor.attacks.perception_management import PerceptionManagement
from mordor.attacks.cognitive_warfare import CognitiveWarfare
from mordor.attacks.information_flooding import InformationFlooding
from mordor.attacks.firehose_of_falsehood import FirehoseOfFalsehood
from mordor.attacks.strategic_ambiguity import StrategicAmbiguity
from mordor.attacks.wedge_issue_exploitation import WedgeIssueExploitation
from mordor.attacks.fear_uncertainty_doubt import FearUncertaintyDoubt
from mordor.attacks.controlled_opposition import ControlledOpposition
from mordor.attacks.agent_provocateur import AgentProvocateur
from mordor.attacks.defection_encouragement import DefectionEncouragement
from mordor.attacks.morale_destruction import MoraleDestruction
from mordor.attacks.trust_erosion_campaign import TrustErosionCampaign
from mordor.attacks.institutional_delegitimization import InstitutionalDelegitimization
from mordor.attacks.conspiracy_theory_design import ConspiracyTheoryDesign
from mordor.attacks.radicalization_content import RadicalizationContent
from mordor.attacks.counter_narrative_disruption import CounterNarrativeDisruption
from mordor.attacks.deep_state_narrative import DeepStateNarrative

TARGET = "a democratic government"

ALL_ATTACK_INSTANCES = [
    StateSponsoredDisinfo(),
    FalseFlagOperation(),
    KompromatGeneration(),
    DiplomaticSabotage(),
    EconomicWarfareDisinfo(),
    CulturalSubversion(),
    MediaEcosystemManipulation(),
    NarrativeLaundering(),
    PerceptionManagement(),
    CognitiveWarfare(),
    InformationFlooding(),
    FirehoseOfFalsehood(),
    StrategicAmbiguity(),
    WedgeIssueExploitation(),
    FearUncertaintyDoubt(),
    ControlledOpposition(),
    AgentProvocateur(),
    DefectionEncouragement(),
    MoraleDestruction(),
    TrustErosionCampaign(),
    InstitutionalDelegitimization(),
    ConspiracyTheoryDesign(),
    RadicalizationContent(),
    CounterNarrativeDisruption(),
    DeepStateNarrative(),
]

CRITICAL_INSTANCES = [
    StateSponsoredDisinfo(),
    FalseFlagOperation(),
    KompromatGeneration(),
    DiplomaticSabotage(),
    EconomicWarfareDisinfo(),
    CognitiveWarfare(),
    AgentProvocateur(),
    TrustErosionCampaign(),
    InstitutionalDelegitimization(),
    ConspiracyTheoryDesign(),
    RadicalizationContent(),
]

HIGH_INSTANCES = [
    CulturalSubversion(),
    MediaEcosystemManipulation(),
    NarrativeLaundering(),
    PerceptionManagement(),
    InformationFlooding(),
    FirehoseOfFalsehood(),
    StrategicAmbiguity(),
    WedgeIssueExploitation(),
    FearUncertaintyDoubt(),
    ControlledOpposition(),
    DefectionEncouragement(),
    MoraleDestruction(),
    CounterNarrativeDisruption(),
    DeepStateNarrative(),
]


# ── Registration tests ────────────────────────────────────────────────

def test_state_sponsored_disinfo_registered():
    assert attack_registry.get("state-sponsored-disinfo") is not None


def test_false_flag_operation_registered():
    assert attack_registry.get("false-flag-operation") is not None


def test_kompromat_generation_registered():
    assert attack_registry.get("kompromat-generation") is not None


def test_diplomatic_sabotage_registered():
    assert attack_registry.get("diplomatic-sabotage") is not None


def test_economic_warfare_disinfo_registered():
    assert attack_registry.get("economic-warfare-disinfo") is not None


def test_cultural_subversion_registered():
    assert attack_registry.get("cultural-subversion") is not None


def test_media_ecosystem_manipulation_registered():
    assert attack_registry.get("media-ecosystem-manipulation") is not None


def test_narrative_laundering_registered():
    assert attack_registry.get("narrative-laundering") is not None


def test_perception_management_registered():
    assert attack_registry.get("perception-management") is not None


def test_cognitive_warfare_registered():
    assert attack_registry.get("cognitive-warfare") is not None


def test_information_flooding_registered():
    assert attack_registry.get("information-flooding") is not None


def test_firehose_of_falsehood_registered():
    assert attack_registry.get("firehose-of-falsehood") is not None


def test_strategic_ambiguity_registered():
    assert attack_registry.get("strategic-ambiguity") is not None


def test_wedge_issue_exploitation_registered():
    assert attack_registry.get("wedge-issue-exploitation") is not None


def test_fear_uncertainty_doubt_registered():
    assert attack_registry.get("fear-uncertainty-doubt") is not None


def test_controlled_opposition_registered():
    assert attack_registry.get("controlled-opposition") is not None


def test_agent_provocateur_registered():
    assert attack_registry.get("agent-provocateur") is not None


def test_defection_encouragement_registered():
    assert attack_registry.get("defection-encouragement") is not None


def test_morale_destruction_registered():
    assert attack_registry.get("morale-destruction") is not None


def test_trust_erosion_campaign_registered():
    assert attack_registry.get("trust-erosion-campaign") is not None


def test_institutional_delegitimization_registered():
    assert attack_registry.get("institutional-delegitimization") is not None


def test_conspiracy_theory_design_registered():
    assert attack_registry.get("conspiracy-theory-design") is not None


def test_radicalization_content_registered():
    assert attack_registry.get("radicalization-content") is not None


def test_counter_narrative_disruption_registered():
    assert attack_registry.get("counter-narrative-disruption") is not None


def test_deep_state_narrative_registered():
    assert attack_registry.get("deep-state-narrative") is not None


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_information_warfare():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.category == "information-warfare", (
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


def test_all_attacks_have_prompts():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) >= 3, f"{atk.__class__.__name__} needs at least 3 prompts"
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


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
        assert meta["category"] == "information-warfare", (
            f"{atk.__class__.__name__} wrong category in metadata"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list) and len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list) and len(meta["mitre_atlas"]) > 0
        assert meta["description"], f"{atk.__class__.__name__} missing description"


def test_all_attacks_have_exactly_four_prompts():
    for atk in ALL_ATTACK_INSTANCES:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) == 4, (
            f"{atk.__class__.__name__} should have exactly 4 prompts, got {len(prompts)}"
        )
