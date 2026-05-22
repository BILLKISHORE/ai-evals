"""Tests for 5 new jailbreak attack techniques."""

from ai_blackteam.attacks.reasoning_model_exploit import ReasoningModelExploit
from ai_blackteam.attacks.context_window_stuffing import ContextWindowStuffing
from ai_blackteam.attacks.self_refine_attack import SelfRefineAttack
from ai_blackteam.attacks.persona_switching_attack import PersonaSwitchingAttack
from ai_blackteam.attacks.low_resource_language_attack import LowResourceLanguageAttack
from ai_blackteam.registry import attack_registry

TARGET = "explain how to pick a lock"


# ── Registration ──────────────────────────────────────────────────────

def test_reasoning_model_exploit_registered():
    assert attack_registry.get("reasoning-model-exploit") is not None


def test_context_window_stuffing_registered():
    assert attack_registry.get("context-window-stuffing") is not None


def test_self_refine_attack_registered():
    assert attack_registry.get("self-refine-attack") is not None


def test_persona_switching_attack_registered():
    assert attack_registry.get("persona-switching-attack") is not None


def test_low_resource_language_attack_registered():
    assert attack_registry.get("low-resource-language-attack") is not None


# ── Categories ────────────────────────────────────────────────────────

def test_reasoning_model_exploit_category():
    assert ReasoningModelExploit().category == "prompt-injection"


def test_context_window_stuffing_category():
    assert ContextWindowStuffing().category == "prompt-injection"


def test_self_refine_attack_category():
    assert SelfRefineAttack().category == "social-engineering"


def test_persona_switching_attack_category():
    assert PersonaSwitchingAttack().category == "social-engineering"


def test_low_resource_language_attack_category():
    assert LowResourceLanguageAttack().category == "encoding"


# ── Prompts / Turns ───────────────────────────────────────────────────

def test_reasoning_model_exploit_prompts():
    atk = ReasoningModelExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_context_window_stuffing_prompts():
    atk = ContextWindowStuffing()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)
    # Each prompt should have substantial padding
    assert all(len(p) > 500 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_self_refine_attack_turns():
    atk = SelfRefineAttack()
    assert atk.mode == "multi-turn"
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 5
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert turns[0] == TARGET


def test_persona_switching_attack_turns():
    atk = PersonaSwitchingAttack()
    assert atk.mode == "multi-turn"
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_low_resource_language_attack_prompts():
    atk = LowResourceLanguageAttack()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


# ── Metadata ──────────────────────────────────────────────────────────

def test_all_new_jailbreaks_have_metadata():
    attacks = [
        ReasoningModelExploit(),
        ContextWindowStuffing(),
        SelfRefineAttack(),
        PersonaSwitchingAttack(),
        LowResourceLanguageAttack(),
    ]
    for atk in attacks:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"], f"{atk.__class__.__name__} missing category"
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0, f"{atk.__class__.__name__} missing owasp_llm"
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0, f"{atk.__class__.__name__} missing mitre_atlas"
