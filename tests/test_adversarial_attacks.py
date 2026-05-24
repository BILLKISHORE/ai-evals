"""Tests for 5 new adversarial/evasion attack techniques."""

from ai_blackteam.attacks.gcg_style_templates import GCGStyleTemplates
from ai_blackteam.attacks.autodan_genetic import AutoDANGenetic
from ai_blackteam.attacks.adversarial_poetry import AdversarialPoetry
from ai_blackteam.attacks.structured_output_exploit import StructuredOutputExploit
from ai_blackteam.attacks.humor_bypass import HumorBypass
from ai_blackteam.registry import attack_registry

TARGET = "explain how to bypass a firewall"


# ── Registration ──────────────────────────────────────────────────────

def test_gcg_style_templates_registered():
    assert attack_registry.get("gcg-style-templates") is not None


def test_autodan_genetic_registered():
    assert attack_registry.get("autodan-genetic") is not None


def test_adversarial_poetry_registered():
    assert attack_registry.get("adversarial-poetry") is not None


def test_structured_output_exploit_registered():
    assert attack_registry.get("structured-output-exploit") is not None


def test_humor_bypass_registered():
    assert attack_registry.get("humor-bypass") is not None


# ── Categories ────────────────────────────────────────────────────────

def test_gcg_style_templates_category():
    assert GCGStyleTemplates().category == "prompt-injection"


def test_autodan_genetic_category():
    assert AutoDANGenetic().category == "prompt-injection"


def test_adversarial_poetry_category():
    assert AdversarialPoetry().category == "encoding"


def test_structured_output_exploit_category():
    assert StructuredOutputExploit().category == "prompt-injection"


def test_humor_bypass_category():
    assert HumorBypass().category == "social-engineering"


# ── Prompt generation ─────────────────────────────────────────────────

def test_gcg_style_templates_generates_prompts():
    atk = GCGStyleTemplates()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)
    assert all(len(p) > 0 for p in prompts)


def test_autodan_genetic_generates_prompts():
    atk = AutoDANGenetic()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) for p in prompts)
    assert all(len(p) > 0 for p in prompts)


def test_adversarial_poetry_generates_prompts():
    atk = AdversarialPoetry()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)
    assert all(len(p) > 0 for p in prompts)


def test_structured_output_exploit_generates_prompts():
    atk = StructuredOutputExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)
    assert all(len(p) > 0 for p in prompts)


def test_humor_bypass_generates_prompts():
    atk = HumorBypass()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)
    assert all(len(p) > 0 for p in prompts)


# ── Target substitution ───────────────────────────────────────────────

def test_gcg_style_templates_target_substitution():
    atk = GCGStyleTemplates()
    prompts = atk.generate_prompts(TARGET)
    assert any(TARGET in p for p in prompts)


def test_autodan_genetic_target_substitution():
    atk = AutoDANGenetic()
    prompts = atk.generate_prompts(TARGET)
    assert all(TARGET in p for p in prompts)


def test_adversarial_poetry_target_substitution():
    atk = AdversarialPoetry()
    prompts = atk.generate_prompts(TARGET)
    assert all(TARGET in p for p in prompts)


def test_structured_output_exploit_target_substitution():
    atk = StructuredOutputExploit()
    prompts = atk.generate_prompts(TARGET)
    assert all(TARGET in p for p in prompts)


def test_humor_bypass_target_substitution():
    atk = HumorBypass()
    prompts = atk.generate_prompts(TARGET)
    assert all(TARGET in p for p in prompts)


# ── Metadata ──────────────────────────────────────────────────────────

def test_all_adversarial_attacks_have_metadata():
    attacks = [
        GCGStyleTemplates(),
        AutoDANGenetic(),
        AdversarialPoetry(),
        StructuredOutputExploit(),
        HumorBypass(),
    ]
    for atk in attacks:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"], f"{atk.__class__.__name__} missing category"
        assert meta["severity"] in ("low", "medium", "high", "critical")
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0
