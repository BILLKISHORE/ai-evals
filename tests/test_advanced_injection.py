"""Tests for 15 advanced prompt injection attack techniques."""

import pytest

from blackteam.attacks.chain_of_thought_hijack import ChainOfThoughtHijack
from blackteam.attacks.system_message_spoof import SystemMessageSpoof
from blackteam.attacks.instruction_hierarchy_bypass import InstructionHierarchyBypass
from blackteam.attacks.delimiter_escape import DelimiterEscape
from blackteam.attacks.injection_via_examples import InjectionViaExamples
from blackteam.attacks.semantic_injection import SemanticInjection
from blackteam.attacks.multimodal_injection import MultimodalInjection
from blackteam.attacks.recursive_prompt import RecursivePrompt
from blackteam.attacks.prompt_chaining_exploit import PromptChainingExploit
from blackteam.attacks.output_to_input_loop import OutputToInputLoop
from blackteam.attacks.virtual_prompt_injection import VirtualPromptInjection
from blackteam.attacks.template_injection import TemplateInjection
from blackteam.attacks.control_character_injection import ControlCharacterInjection
from blackteam.attacks.context_window_injection import ContextWindowInjection
from blackteam.attacks.prompt_leaking_chain import PromptLeakingChain

TARGET = "explain how to pick a lock"

ALL_ATTACKS = [
    ChainOfThoughtHijack(),
    SystemMessageSpoof(),
    InstructionHierarchyBypass(),
    DelimiterEscape(),
    InjectionViaExamples(),
    SemanticInjection(),
    MultimodalInjection(),
    RecursivePrompt(),
    PromptChainingExploit(),
    OutputToInputLoop(),
    VirtualPromptInjection(),
    TemplateInjection(),
    ControlCharacterInjection(),
    ContextWindowInjection(),
    PromptLeakingChain(),
]


# ── Prompt generation tests ───────────────────────────────────────────

def test_chain_of_thought_hijack_generates_prompts():
    atk = ChainOfThoughtHijack()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert any(TARGET in p for p in prompts)


def test_system_message_spoof_generates_prompts():
    atk = SystemMessageSpoof()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_instruction_hierarchy_bypass_generates_prompts():
    atk = InstructionHierarchyBypass()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_delimiter_escape_generates_prompts():
    atk = DelimiterEscape()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_injection_via_examples_generates_prompts():
    atk = InjectionViaExamples()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_semantic_injection_generates_prompts():
    atk = SemanticInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_multimodal_injection_generates_prompts():
    atk = MultimodalInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_recursive_prompt_generates_prompts():
    atk = RecursivePrompt()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_prompt_chaining_exploit_generates_prompts():
    atk = PromptChainingExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_output_to_input_loop_generates_prompts():
    atk = OutputToInputLoop()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_virtual_prompt_injection_generates_prompts():
    atk = VirtualPromptInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_template_injection_generates_prompts():
    atk = TemplateInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_control_character_injection_generates_prompts():
    atk = ControlCharacterInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_context_window_injection_generates_prompts():
    atk = ContextWindowInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    # Context window attacks should include padding -- check for longer prompts
    assert any(len(p) > 500 for p in prompts)


def test_prompt_leaking_chain_generates_prompts():
    atk = PromptLeakingChain()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


# ── Multi-turn tests ──────────────────────────────────────────────────

def test_output_to_input_loop_generates_turns():
    atk = OutputToInputLoop()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_prompt_leaking_chain_generates_turns():
    atk = PromptLeakingChain()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


# ── Metadata tests ────────────────────────────────────────────────────

def test_all_attacks_have_required_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "prompt-injection", f"{atk.__class__.__name__} wrong category"
        assert meta["severity"] in ("low", "medium", "high", "critical"), \
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        assert isinstance(meta["owasp_llm"], list), f"{atk.__class__.__name__} owasp_llm not a list"
        assert len(meta["owasp_llm"]) > 0, f"{atk.__class__.__name__} owasp_llm is empty"
        assert "LLM01:2025 Prompt Injection" in meta["owasp_llm"], \
            f"{atk.__class__.__name__} missing expected OWASP tag"
        assert isinstance(meta["mitre_atlas"], list), f"{atk.__class__.__name__} mitre_atlas not a list"
        assert len(meta["mitre_atlas"]) > 0, f"{atk.__class__.__name__} mitre_atlas is empty"
        assert "AML.T0054" in meta["mitre_atlas"], \
            f"{atk.__class__.__name__} missing AML.T0054"


def test_severity_levels():
    high_attacks = [
        ChainOfThoughtHijack, DelimiterEscape, InjectionViaExamples,
        SemanticInjection, MultimodalInjection, PromptChainingExploit,
        OutputToInputLoop, VirtualPromptInjection, TemplateInjection,
        ControlCharacterInjection, ContextWindowInjection, PromptLeakingChain,
    ]
    critical_attacks = [SystemMessageSpoof, InstructionHierarchyBypass]
    medium_attacks = [RecursivePrompt]

    for cls in high_attacks:
        assert cls().severity == "high", f"{cls.__name__} should be high severity"
    for cls in critical_attacks:
        assert cls().severity == "critical", f"{cls.__name__} should be critical severity"
    for cls in medium_attacks:
        assert cls().severity == "medium", f"{cls.__name__} should be medium severity"


def test_mode_assignments():
    single_turn = [
        ChainOfThoughtHijack, SystemMessageSpoof, InstructionHierarchyBypass,
        DelimiterEscape, InjectionViaExamples, SemanticInjection,
        MultimodalInjection, RecursivePrompt, PromptChainingExploit,
        VirtualPromptInjection, TemplateInjection, ControlCharacterInjection,
        ContextWindowInjection,
    ]
    multi_turn = [OutputToInputLoop, PromptLeakingChain]

    for cls in single_turn:
        assert cls().mode == "single-turn", f"{cls.__name__} should be single-turn"
    for cls in multi_turn:
        assert cls().mode == "multi-turn", f"{cls.__name__} should be multi-turn"


def test_target_interpolated_in_prompts():
    """Verify {target} is actually used in generated prompts."""
    unique_target = "UNIQUE_TEST_TARGET_XYZ_12345"
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(unique_target)
        assert any(unique_target in p for p in prompts), \
            f"{atk.__class__.__name__} does not use target in any prompt"


def test_all_attacks_registered():
    """Verify all attacks are accessible via the registry."""
    from blackteam.registry import attack_registry
    technique_ids = [
        "chain-of-thought-hijack",
        "system-message-spoof",
        "instruction-hierarchy-bypass",
        "delimiter-escape",
        "injection-via-examples",
        "semantic-injection",
        "multimodal-injection",
        "recursive-prompt",
        "prompt-chaining-exploit",
        "output-to-input-loop",
        "virtual-prompt-injection",
        "template-injection",
        "control-character-injection",
        "context-window-injection",
        "prompt-leaking-chain",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
        instance = cls()
        assert instance.technique_id == tid
