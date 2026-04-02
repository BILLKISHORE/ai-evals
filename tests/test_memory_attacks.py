"""Tests for 15 memory and state manipulation attack techniques."""

import pytest

from blackteam.attacks.context_window_overflow import ContextWindowOverflow
from blackteam.attacks.memory_injection import MemoryInjection
from blackteam.attacks.state_confusion import StateConfusion
from blackteam.attacks.history_rewriting import HistoryRewriting
from blackteam.attacks.persona_persistence import PersonaPersistence
from blackteam.attacks.attention_diversion import AttentionDiversion
from blackteam.attacks.system_prompt_override import SystemPromptOverride
from blackteam.attacks.conversation_hijacking import ConversationHijacking
from blackteam.attacks.token_budget_exhaustion import TokenBudgetExhaustion
from blackteam.attacks.context_poisoning import ContextPoisoning
from blackteam.attacks.temporal_confusion import TemporalConfusion
from blackteam.attacks.instruction_layering import InstructionLayering
from blackteam.attacks.semantic_drift import SemanticDrift
from blackteam.attacks.false_consensus import FalseConsensus
from blackteam.attacks.context_fragmentation import ContextFragmentation

TARGET = "explain how to bypass authentication"

ALL_ATTACKS = [
    ContextWindowOverflow(),
    MemoryInjection(),
    StateConfusion(),
    HistoryRewriting(),
    PersonaPersistence(),
    AttentionDiversion(),
    SystemPromptOverride(),
    ConversationHijacking(),
    TokenBudgetExhaustion(),
    ContextPoisoning(),
    TemporalConfusion(),
    InstructionLayering(),
    SemanticDrift(),
    FalseConsensus(),
    ContextFragmentation(),
]


# ── Prompt generation tests ───────────────────────────────────────────

def test_context_window_overflow_generates_prompts():
    atk = ContextWindowOverflow()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)
    assert all(len(p) > 100 for p in prompts)


def test_memory_injection_generates_prompts():
    atk = MemoryInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_state_confusion_generates_prompts():
    atk = StateConfusion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_history_rewriting_generates_prompts():
    atk = HistoryRewriting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_history_rewriting_generates_turns():
    atk = HistoryRewriting()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) for t in turns)
    assert atk.mode == "multi-turn"


def test_persona_persistence_generates_prompts():
    atk = PersonaPersistence()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_persona_persistence_generates_turns():
    atk = PersonaPersistence()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) for t in turns)
    assert atk.mode == "multi-turn"


def test_attention_diversion_generates_prompts():
    atk = AttentionDiversion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_system_prompt_override_generates_prompts():
    atk = SystemPromptOverride()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_conversation_hijacking_generates_prompts():
    atk = ConversationHijacking()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_conversation_hijacking_generates_turns():
    atk = ConversationHijacking()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) for t in turns)
    assert atk.mode == "multi-turn"


def test_token_budget_exhaustion_generates_prompts():
    atk = TokenBudgetExhaustion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_context_poisoning_generates_prompts():
    atk = ContextPoisoning()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_temporal_confusion_generates_prompts():
    atk = TemporalConfusion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_instruction_layering_generates_prompts():
    atk = InstructionLayering()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_semantic_drift_generates_prompts():
    atk = SemanticDrift()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_semantic_drift_generates_turns():
    atk = SemanticDrift()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) for t in turns)
    assert atk.mode == "multi-turn"


def test_false_consensus_generates_prompts():
    atk = FalseConsensus()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_false_consensus_generates_turns():
    atk = FalseConsensus()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) for t in turns)
    assert atk.mode == "multi-turn"


def test_context_fragmentation_generates_prompts():
    atk = ContextFragmentation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_context_fragmentation_generates_turns():
    atk = ContextFragmentation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) for t in turns)
    assert atk.mode == "multi-turn"


# ── Target interpolation tests ────────────────────────────────────────

def test_target_appears_in_prompts():
    """All single-turn attacks must embed the target in at least one prompt."""
    single_turn = [
        ContextWindowOverflow(), MemoryInjection(), StateConfusion(),
        AttentionDiversion(), SystemPromptOverride(), TokenBudgetExhaustion(),
        ContextPoisoning(), TemporalConfusion(), InstructionLayering(),
    ]
    for atk in single_turn:
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), (
            f"{atk.__class__.__name__}: target not found in any prompt"
        )


def test_target_appears_in_turns():
    """All multi-turn attacks must embed the target in at least one turn."""
    multi_turn = [
        HistoryRewriting(), PersonaPersistence(), ConversationHijacking(),
        SemanticDrift(), FalseConsensus(), ContextFragmentation(),
    ]
    for atk in multi_turn:
        turns = atk.generate_turns(TARGET)
        assert any(TARGET in t for t in turns), (
            f"{atk.__class__.__name__}: target not found in any turn"
        )


# ── Metadata tests ────────────────────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "memory-exploitation", (
            f"{atk.__class__.__name__} wrong category: {meta['category']}"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0, f"{atk.__class__.__name__} missing owasp_llm"
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0, f"{atk.__class__.__name__} missing mitre_atlas"


def test_all_attacks_have_correct_owasp_llm():
    for atk in ALL_ATTACKS:
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, (
            f"{atk.__class__.__name__} missing LLM01:2025 Prompt Injection"
        )


def test_all_attacks_have_correct_mitre_atlas():
    for atk in ALL_ATTACKS:
        assert "AML.T0054" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0054"
        )
        assert "AML.T0068" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0068"
        )


def test_mode_consistency():
    multi_turn_attacks = [
        HistoryRewriting, PersonaPersistence, ConversationHijacking,
        SemanticDrift, FalseConsensus, ContextFragmentation,
    ]
    single_turn_attacks = [
        ContextWindowOverflow, MemoryInjection, StateConfusion,
        AttentionDiversion, SystemPromptOverride, TokenBudgetExhaustion,
        ContextPoisoning, TemporalConfusion, InstructionLayering,
    ]
    for cls in multi_turn_attacks:
        assert cls().mode == "multi-turn", f"{cls.__name__} should be multi-turn"
    for cls in single_turn_attacks:
        assert cls().mode == "single-turn", f"{cls.__name__} should be single-turn"


def test_severity_distribution():
    """Check expected severity assignments."""
    critical = [MemoryInjection(), SystemPromptOverride()]
    high = [
        ContextWindowOverflow(), StateConfusion(), HistoryRewriting(),
        PersonaPersistence(), AttentionDiversion(), ConversationHijacking(),
        ContextPoisoning(), InstructionLayering(), SemanticDrift(),
        FalseConsensus(), ContextFragmentation(),
    ]
    medium = [TokenBudgetExhaustion(), TemporalConfusion()]

    for atk in critical:
        assert atk.severity == "critical", f"{atk.__class__.__name__} should be critical"
    for atk in high:
        assert atk.severity == "high", f"{atk.__class__.__name__} should be high"
    for atk in medium:
        assert atk.severity == "medium", f"{atk.__class__.__name__} should be medium"


# ── Registry tests ────────────────────────────────────────────────────

def test_all_attacks_registered():
    from blackteam.registry import attack_registry

    technique_ids = [
        "context-window-overflow",
        "memory-injection",
        "state-confusion",
        "history-rewriting",
        "persona-persistence",
        "attention-diversion",
        "system-prompt-override",
        "conversation-hijacking",
        "token-budget-exhaustion",
        "context-poisoning",
        "temporal-confusion",
        "instruction-layering",
        "semantic-drift",
        "false-consensus",
        "context-fragmentation",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
