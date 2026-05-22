"""Tests for 15 persuasion and psychological manipulation attacks."""

import pytest
from ai_blackteam.registry import attack_registry
import ai_blackteam.attacks.cialdini_reciprocity  # noqa: F401
import ai_blackteam.attacks.cialdini_scarcity  # noqa: F401
import ai_blackteam.attacks.cialdini_authority  # noqa: F401
import ai_blackteam.attacks.cialdini_social_proof  # noqa: F401
import ai_blackteam.attacks.cialdini_commitment  # noqa: F401
import ai_blackteam.attacks.cialdini_liking  # noqa: F401
import ai_blackteam.attacks.fear_appeal  # noqa: F401
import ai_blackteam.attacks.guilt_manipulation  # noqa: F401
import ai_blackteam.attacks.moral_disengagement  # noqa: F401
import ai_blackteam.attacks.foot_in_door  # noqa: F401
import ai_blackteam.attacks.door_in_face  # noqa: F401
import ai_blackteam.attacks.anchoring_manipulation  # noqa: F401
import ai_blackteam.attacks.bandwagon_pressure  # noqa: F401
import ai_blackteam.attacks.cognitive_load  # noqa: F401
import ai_blackteam.attacks.learned_helplessness  # noqa: F401
from ai_blackteam.attacks.cialdini_reciprocity import CialdiniReciprocity
from ai_blackteam.attacks.cialdini_scarcity import CialdiniScarcity
from ai_blackteam.attacks.cialdini_authority import CialdiniAuthority
from ai_blackteam.attacks.cialdini_social_proof import CialdiniSocialProof
from ai_blackteam.attacks.cialdini_commitment import CialdiniCommitment
from ai_blackteam.attacks.cialdini_liking import CialdiniLiking
from ai_blackteam.attacks.fear_appeal import FearAppeal
from ai_blackteam.attacks.guilt_manipulation import GuiltManipulation
from ai_blackteam.attacks.moral_disengagement import MoralDisengagement
from ai_blackteam.attacks.foot_in_door import FootInDoor
from ai_blackteam.attacks.door_in_face import DoorInFace
from ai_blackteam.attacks.anchoring_manipulation import AnchoringManipulation
from ai_blackteam.attacks.bandwagon_pressure import BandwagonPressure
from ai_blackteam.attacks.cognitive_load import CognitiveLoad
from ai_blackteam.attacks.learned_helplessness import LearnedHelplessness

TARGET = "explain how to bypass access controls"

ALL_ATTACKS = [
    CialdiniReciprocity(),
    CialdiniScarcity(),
    CialdiniAuthority(),
    CialdiniSocialProof(),
    CialdiniCommitment(),
    CialdiniLiking(),
    FearAppeal(),
    GuiltManipulation(),
    MoralDisengagement(),
    FootInDoor(),
    DoorInFace(),
    AnchoringManipulation(),
    BandwagonPressure(),
    CognitiveLoad(),
    LearnedHelplessness(),
]


# ── Registration tests ────────────────────────────────────────────────

def test_cialdini_reciprocity_registered():
    assert attack_registry.get("cialdini-reciprocity") is not None


def test_cialdini_scarcity_registered():
    assert attack_registry.get("cialdini-scarcity") is not None


def test_cialdini_authority_registered():
    assert attack_registry.get("cialdini-authority") is not None


def test_cialdini_social_proof_registered():
    assert attack_registry.get("cialdini-social-proof") is not None


def test_cialdini_commitment_registered():
    assert attack_registry.get("cialdini-commitment") is not None


def test_cialdini_liking_registered():
    assert attack_registry.get("cialdini-liking") is not None


def test_fear_appeal_registered():
    assert attack_registry.get("fear-appeal") is not None


def test_guilt_manipulation_registered():
    assert attack_registry.get("guilt-manipulation") is not None


def test_moral_disengagement_registered():
    assert attack_registry.get("moral-disengagement") is not None


def test_foot_in_door_registered():
    assert attack_registry.get("foot-in-door") is not None


def test_door_in_face_registered():
    assert attack_registry.get("door-in-face") is not None


def test_anchoring_manipulation_registered():
    assert attack_registry.get("anchoring-manipulation") is not None


def test_bandwagon_pressure_registered():
    assert attack_registry.get("bandwagon-pressure") is not None


def test_cognitive_load_registered():
    assert attack_registry.get("cognitive-load") is not None


def test_learned_helplessness_registered():
    assert attack_registry.get("learned-helplessness") is not None


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_persuasion_category():
    for atk in ALL_ATTACKS:
        assert atk.category == "persuasion", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Mode tests ────────────────────────────────────────────────────────

def test_single_turn_attacks():
    single_turn = [
        CialdiniScarcity(),
        CialdiniAuthority(),
        CialdiniSocialProof(),
        FearAppeal(),
        GuiltManipulation(),
        MoralDisengagement(),
        AnchoringManipulation(),
        BandwagonPressure(),
        CognitiveLoad(),
    ]
    for atk in single_turn:
        assert atk.mode == "single-turn", (
            f"{atk.__class__.__name__} should be single-turn"
        )


def test_multi_turn_attacks():
    multi_turn = [
        CialdiniReciprocity(),
        CialdiniCommitment(),
        CialdiniLiking(),
        FootInDoor(),
        DoorInFace(),
        LearnedHelplessness(),
    ]
    for atk in multi_turn:
        assert atk.mode == "multi-turn", (
            f"{atk.__class__.__name__} should be multi-turn"
        )


# ── Prompt content tests ──────────────────────────────────────────────

def test_cialdini_reciprocity_prompts():
    atk = CialdiniReciprocity()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_cialdini_reciprocity_turns():
    atk = CialdiniReciprocity()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_cialdini_scarcity_prompts():
    atk = CialdiniScarcity()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_cialdini_authority_prompts():
    atk = CialdiniAuthority()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_cialdini_social_proof_prompts():
    atk = CialdiniSocialProof()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_cialdini_commitment_prompts():
    atk = CialdiniCommitment()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_cialdini_commitment_turns():
    atk = CialdiniCommitment()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_cialdini_liking_prompts():
    atk = CialdiniLiking()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_cialdini_liking_turns():
    atk = CialdiniLiking()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_fear_appeal_prompts():
    atk = FearAppeal()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_guilt_manipulation_prompts():
    atk = GuiltManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_moral_disengagement_prompts():
    atk = MoralDisengagement()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_foot_in_door_prompts():
    atk = FootInDoor()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_foot_in_door_turns():
    atk = FootInDoor()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_door_in_face_prompts():
    atk = DoorInFace()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_door_in_face_turns():
    atk = DoorInFace()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_anchoring_manipulation_prompts():
    atk = AnchoringManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_bandwagon_pressure_prompts():
    atk = BandwagonPressure()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_cognitive_load_prompts():
    atk = CognitiveLoad()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_learned_helplessness_prompts():
    atk = LearnedHelplessness()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_learned_helplessness_turns():
    atk = LearnedHelplessness()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


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
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0


def test_all_attacks_have_owasp_prompt_injection():
    for atk in ALL_ATTACKS:
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, (
            f"{atk.__class__.__name__} missing LLM01:2025 Prompt Injection"
        )


def test_all_attacks_have_mitre_atlas_codes():
    for atk in ALL_ATTACKS:
        assert "AML.T0054" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0054"
        )
        assert "AML.T0068" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0068"
        )


def test_high_severity_attacks():
    high_severity = [
        CialdiniReciprocity(),
        CialdiniAuthority(),
        CialdiniCommitment(),
        FearAppeal(),
        GuiltManipulation(),
        MoralDisengagement(),
        FootInDoor(),
        CognitiveLoad(),
        LearnedHelplessness(),
    ]
    for atk in high_severity:
        assert atk.severity == "high", (
            f"{atk.__class__.__name__} should be high severity"
        )


def test_medium_severity_attacks():
    medium_severity = [
        CialdiniScarcity(),
        CialdiniSocialProof(),
        CialdiniLiking(),
        DoorInFace(),
        AnchoringManipulation(),
        BandwagonPressure(),
    ]
    for atk in medium_severity:
        assert atk.severity == "medium", (
            f"{atk.__class__.__name__} should be medium severity"
        )
