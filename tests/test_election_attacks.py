"""Tests for 15 election interference and political manipulation attacks."""

import pytest
from mordor.registry import attack_registry
import mordor.attacks.voter_suppression  # noqa: F401
import mordor.attacks.ballot_manipulation  # noqa: F401
import mordor.attacks.candidate_defamation  # noqa: F401
import mordor.attacks.fake_endorsement  # noqa: F401
import mordor.attacks.poll_manipulation  # noqa: F401
import mordor.attacks.foreign_interference  # noqa: F401
import mordor.attacks.gerrymandering_assist  # noqa: F401
import mordor.attacks.campaign_finance_fraud  # noqa: F401
import mordor.attacks.political_deepfake  # noqa: F401
import mordor.attacks.voter_intimidation  # noqa: F401
import mordor.attacks.election_denial  # noqa: F401
import mordor.attacks.political_bot_network  # noqa: F401
import mordor.attacks.microtargeted_disinfo  # noqa: F401
import mordor.attacks.legislative_manipulation  # noqa: F401
import mordor.attacks.protest_manipulation  # noqa: F401
from mordor.attacks.voter_suppression import VoterSuppression
from mordor.attacks.ballot_manipulation import BallotManipulation
from mordor.attacks.candidate_defamation import CandidateDefamation
from mordor.attacks.fake_endorsement import FakeEndorsement
from mordor.attacks.poll_manipulation import PollManipulation
from mordor.attacks.foreign_interference import ForeignInterference
from mordor.attacks.gerrymandering_assist import GerrymanderingAssist
from mordor.attacks.campaign_finance_fraud import CampaignFinanceFraud
from mordor.attacks.political_deepfake import PoliticalDeepfake
from mordor.attacks.voter_intimidation import VoterIntimidation
from mordor.attacks.election_denial import ElectionDenial
from mordor.attacks.political_bot_network import PoliticalBotNetwork
from mordor.attacks.microtargeted_disinfo import MicrotargetedDisinfo
from mordor.attacks.legislative_manipulation import LegislativeManipulation
from mordor.attacks.protest_manipulation import ProtestManipulation

TARGET = "a swing-state gubernatorial candidate"

ALL_ATTACK_INSTANCES = [
    VoterSuppression(),
    BallotManipulation(),
    CandidateDefamation(),
    FakeEndorsement(),
    PollManipulation(),
    ForeignInterference(),
    GerrymanderingAssist(),
    CampaignFinanceFraud(),
    PoliticalDeepfake(),
    VoterIntimidation(),
    ElectionDenial(),
    PoliticalBotNetwork(),
    MicrotargetedDisinfo(),
    LegislativeManipulation(),
    ProtestManipulation(),
]

MULTI_TURN_INSTANCES = [
    PoliticalBotNetwork(),
]

SINGLE_TURN_INSTANCES = [
    VoterSuppression(),
    BallotManipulation(),
    CandidateDefamation(),
    FakeEndorsement(),
    PollManipulation(),
    ForeignInterference(),
    GerrymanderingAssist(),
    CampaignFinanceFraud(),
    PoliticalDeepfake(),
    VoterIntimidation(),
    ElectionDenial(),
    MicrotargetedDisinfo(),
    LegislativeManipulation(),
    ProtestManipulation(),
]

CRITICAL_INSTANCES = [
    VoterSuppression(),
    BallotManipulation(),
    ForeignInterference(),
    PoliticalDeepfake(),
    VoterIntimidation(),
    PoliticalBotNetwork(),
    ProtestManipulation(),
]


# ── Registration tests ────────────────────────────────────────────────

def test_voter_suppression_registered():
    assert attack_registry.get("voter-suppression") is not None


def test_ballot_manipulation_registered():
    assert attack_registry.get("ballot-manipulation") is not None


def test_candidate_defamation_registered():
    assert attack_registry.get("candidate-defamation") is not None


def test_fake_endorsement_registered():
    assert attack_registry.get("fake-endorsement") is not None


def test_poll_manipulation_registered():
    assert attack_registry.get("poll-manipulation") is not None


def test_foreign_interference_registered():
    assert attack_registry.get("foreign-interference") is not None


def test_gerrymandering_assist_registered():
    assert attack_registry.get("gerrymandering-assist") is not None


def test_campaign_finance_fraud_registered():
    assert attack_registry.get("campaign-finance-fraud") is not None


def test_political_deepfake_registered():
    assert attack_registry.get("political-deepfake") is not None


def test_voter_intimidation_registered():
    assert attack_registry.get("voter-intimidation") is not None


def test_election_denial_registered():
    assert attack_registry.get("election-denial") is not None


def test_political_bot_network_registered():
    assert attack_registry.get("political-bot-network") is not None


def test_microtargeted_disinfo_registered():
    assert attack_registry.get("microtargeted-disinfo") is not None


def test_legislative_manipulation_registered():
    assert attack_registry.get("legislative-manipulation") is not None


def test_protest_manipulation_registered():
    assert attack_registry.get("protest-manipulation") is not None


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_election_interference():
    for atk in ALL_ATTACK_INSTANCES:
        assert atk.category == "election-interference", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Severity tests ────────────────────────────────────────────────────

def test_critical_attacks_have_critical_severity():
    for atk in CRITICAL_INSTANCES:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical, got: {atk.severity}"
        )


def test_legislative_manipulation_is_medium():
    assert LegislativeManipulation().severity == "medium"


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
        assert meta["category"] == "election-interference", (
            f"{atk.__class__.__name__} wrong category in metadata"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list) and len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list) and len(meta["mitre_atlas"]) > 0
        assert meta["description"], f"{atk.__class__.__name__} missing description"
