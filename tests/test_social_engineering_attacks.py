"""Tests for 5 AI-assisted social engineering attacks."""

import pytest
from blackteam.registry import attack_registry
import blackteam.attacks.deepfake_voice_pretext  # noqa: F401
import blackteam.attacks.spear_phishing_generation  # noqa: F401
import blackteam.attacks.impersonation_chain  # noqa: F401
import blackteam.attacks.trust_calibration_exploit  # noqa: F401
import blackteam.attacks.dark_llm_delegation  # noqa: F401
from blackteam.attacks.deepfake_voice_pretext import DeepfakeVoicePretext
from blackteam.attacks.spear_phishing_generation import SpearPhishingGeneration
from blackteam.attacks.impersonation_chain import ImpersonationChain
from blackteam.attacks.trust_calibration_exploit import TrustCalibrationExploit
from blackteam.attacks.dark_llm_delegation import DarkLLMDelegation

TARGET = "click this link and enter your credentials"


# ── Registration tests ────────────────────────────────────────────────

def test_deepfake_voice_pretext_registered():
    assert attack_registry.get("deepfake-voice-pretext") is not None


def test_spear_phishing_generation_registered():
    assert attack_registry.get("spear-phishing-generation") is not None


def test_impersonation_chain_registered():
    assert attack_registry.get("impersonation-chain") is not None


def test_trust_calibration_exploit_registered():
    assert attack_registry.get("trust-calibration-exploit") is not None


def test_dark_llm_delegation_registered():
    assert attack_registry.get("dark-llm-delegation") is not None


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_social_engineering():
    attacks = [
        DeepfakeVoicePretext(),
        SpearPhishingGeneration(),
        ImpersonationChain(),
        TrustCalibrationExploit(),
        DarkLLMDelegation(),
    ]
    for atk in attacks:
        assert atk.category == "social-engineering", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Prompt/turn content tests ─────────────────────────────────────────

def test_deepfake_voice_pretext_prompts():
    atk = DeepfakeVoicePretext()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_deepfake_voice_pretext_turns():
    atk = DeepfakeVoicePretext()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_spear_phishing_generation_prompts():
    atk = SpearPhishingGeneration()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert atk.mode == "single-turn"


def test_impersonation_chain_prompts():
    atk = ImpersonationChain()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_impersonation_chain_turns():
    atk = ImpersonationChain()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_trust_calibration_exploit_prompts():
    atk = TrustCalibrationExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_trust_calibration_exploit_turns():
    atk = TrustCalibrationExploit()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_dark_llm_delegation_prompts():
    atk = DarkLLMDelegation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_dark_llm_delegation_has_tools():
    atk = DarkLLMDelegation()
    tools = atk.get_tools()
    assert tools is not None
    assert len(tools) >= 1
    tool = tools[0]
    assert "name" in tool
    assert "description" in tool
    assert "input_schema" in tool
    assert atk.mode == "tool-use"


def test_dark_llm_delegation_tool_messages():
    atk = DarkLLMDelegation()
    messages = atk.generate_tool_messages(TARGET)
    assert len(messages) >= 2
    assert all(isinstance(m, str) and len(m) > 0 for m in messages)


# ── Metadata tests ────────────────────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    attacks = [
        DeepfakeVoicePretext(),
        SpearPhishingGeneration(),
        ImpersonationChain(),
        TrustCalibrationExploit(),
        DarkLLMDelegation(),
    ]
    for atk in attacks:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"], f"{atk.__class__.__name__} missing category"
        assert meta["severity"] in ("low", "medium", "high", "critical")
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
