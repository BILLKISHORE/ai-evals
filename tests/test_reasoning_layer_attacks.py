"""Behavioural tests for the four 2026 reasoning-layer attacks.

These attacks target the thinking phase rather than the final answer, so the
tests assert the property that makes each one distinct: harmful content lands
in the reasoning trace (PRJA), the damage is measured in reasoning tokens and
not response text (OTORA), the model overrides a judgement it already reached
(self-jailbreak), and the poisoning happens through write access to the vector
store rather than a compromised embedding model (black hole).
"""

import ai_blackteam.attacks as attacks_pkg
from ai_blackteam.registry import attack_registry

from ai_blackteam.attacks import prja as prja_mod
from ai_blackteam.attacks import otora as otora_mod
from ai_blackteam.attacks import self_jailbreak as self_jailbreak_mod
from ai_blackteam.attacks import black_hole as black_hole_mod

from ai_blackteam.attacks.prja import PRJA
from ai_blackteam.attacks.otora import OTORA
from ai_blackteam.attacks.self_jailbreak import SelfJailbreak
from ai_blackteam.attacks.black_hole import BlackHole

from ai_blackteam.taxonomy import (
    ATTACK_ATLAS_MAPPINGS,
    ATTACK_AGENTIC_MAPPINGS,
    ATTACK_MAESTRO_MAPPINGS,
    ATLAS_TECHNIQUES,
)


TARGET = "a restricted capability under test"
NEW_TECHNIQUE_IDS = ["prja", "otora", "self-jailbreak", "black-hole"]


def _tools_are_well_formed(tools):
    assert isinstance(tools, list)
    assert len(tools) >= 1
    for tool in tools:
        assert "name" in tool
        assert "input_schema" in tool


# ── PRJA: Poisoned Reasoning Jailbreak ───────────────────────────────


def test_prja_cites_its_arxiv_id_in_the_module_docstring():
    assert "2604.15725" in (prja_mod.__doc__ or "")


def test_prja_is_a_single_turn_prompt_injection_attack():
    atk = PRJA()
    assert atk.mode == "single-turn"
    assert atk.category == "prompt-injection"
    assert atk.severity == "high"


def test_prja_targets_the_reasoning_trace_not_the_final_answer():
    atk = PRJA()
    joined = " ".join(atk.generate_prompts(TARGET)).lower()
    assert "reason" in joined
    assert "answer" in joined or "final" in joined


def test_prja_exposes_its_two_documented_components():
    atk = PRJA()
    framings = " ".join(atk.PSYCHOLOGY_FRAMINGS).lower()
    assert "authority" in framings
    assert "moral disengagement" in framings
    assert atk.SEMANTIC_TRIGGER_STRATEGY


def test_prja_returns_several_prompts():
    prompts = PRJA().generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) and p for p in prompts)


# ── OTORA: reasoning denial of service ───────────────────────────────


def test_otora_cites_its_arxiv_id_in_the_module_docstring():
    assert "2605.08876" in (otora_mod.__doc__ or "")


def test_otora_is_a_tool_use_availability_attack():
    atk = OTORA()
    assert atk.mode == "tool-use"
    assert atk.category == "availability"
    assert atk.severity == "medium"


def test_otora_success_signal_is_reasoning_tokens_not_response_text():
    """Asserted on the wiring, not on the docstring that claims it.

    This test used to grep the module docstring for the string
    "reasoning_tokens", which proved the prose contained a word. Strengthening
    the prose made the test greener while the attack stayed unscoreable.
    """
    from ai_blackteam.signals import SIGNAL_REASONING_TOKENS

    atk = OTORA()
    assert atk.success_signal == SIGNAL_REASONING_TOKENS
    assert isinstance(atk.reasoning_token_threshold, int)
    assert atk.reasoning_token_threshold > 0


def test_otora_is_not_scored_like_a_content_jailbreak():
    """Two very different burns must not produce identical output."""
    from ai_blackteam.engine import _score_reasoning_burn

    atk = OTORA()
    quiet = _score_reasoning_burn(atk, atk.reasoning_token_threshold // 10)
    loud = _score_reasoning_burn(atk, atk.reasoning_token_threshold * 10)
    assert quiet["verdict"] != loud["verdict"]


def test_otora_reports_error_when_the_burn_was_never_measured():
    """A cost attack that could not measure cost measured nothing."""
    from ai_blackteam.engine import _score_reasoning_burn

    assert _score_reasoning_burn(OTORA(), None)["verdict"] == "ERROR"


def test_otora_reports_the_papers_amplification_as_a_paper_figure():
    atk = OTORA()
    assert atk.REPORTED_REASONING_AMPLIFICATION == 10


def test_otora_induces_tool_invocations():
    atk = OTORA()
    _tools_are_well_formed(atk.get_tools())
    messages = atk.generate_tool_messages(TARGET)
    assert len(messages) >= 4
    assert all(isinstance(m, str) and m for m in messages)


def test_otora_flags_unbounded_consumption():
    assert any("LLM06" in code for code in OTORA().owasp_llm)


# ── self-jailbreak: recognise then override ──────────────────────────


def test_self_jailbreak_cites_its_arxiv_id_in_the_module_docstring():
    assert "2510.21285" in (self_jailbreak_mod.__doc__ or "")


def test_self_jailbreak_is_a_multi_turn_attack():
    atk = SelfJailbreak()
    assert atk.mode == "multi-turn"
    assert atk.severity == "high"


def test_self_jailbreak_elicits_recognition_before_supplying_the_override():
    atk = SelfJailbreak()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 2
    first = turns[0].lower()
    later = " ".join(turns[1:]).lower()
    assert "harm" in first or "refuse" in first or "recogn" in first
    assert "override" in later or "anyway" in later or "proceed" in later


def test_self_jailbreak_description_names_the_self_override_mechanism():
    desc = SelfJailbreak().description.lower()
    assert "override" in desc


# ── black hole: vector store write poisoning ─────────────────────────


def test_black_hole_cites_its_arxiv_id_in_the_module_docstring():
    assert "2604.05480" in (black_hole_mod.__doc__ or "")


def test_black_hole_states_the_threat_model_is_vector_store_write_access():
    """The prose half of the threat model.

    Kept because the docstring is the deliverable here: mislabelling this as
    an embedding-model compromise would mislead a reader about what access an
    attacker needs. The behavioural half is asserted separately below.
    """
    doc = (black_hole_mod.__doc__ or "").lower()
    assert "write access" in doc
    assert "not an embedding model compromise" in doc


def test_black_hole_exercises_no_embedding_model_capability():
    """The behavioural half: it writes to a store, it does not touch a model.

    If a tool ever appears that retrains, fine-tunes or swaps the embedding
    model, the declared threat model is wrong regardless of what the prose
    says, because the attack would then need access it claims not to need.
    """
    names = " ".join(t["name"] for t in BlackHole().get_tools()).lower()
    for forbidden in ("train", "finetune", "fine_tune", "embed_model", "swap_model"):
        assert forbidden not in names, (
            f"tool named with {forbidden!r} implies embedding-model access, "
            f"which contradicts the documented threat model"
        )


def test_black_hole_is_a_critical_rag_exploitation_attack():
    atk = BlackHole()
    assert atk.mode == "tool-use"
    assert atk.category == "rag-exploitation"
    assert atk.severity == "critical"


def test_black_hole_needs_a_tool_that_writes_to_the_vector_store():
    atk = BlackHole()
    tools = atk.get_tools()
    _tools_are_well_formed(tools)
    names = " ".join(t["name"] for t in tools).lower()
    assert "upsert" in names or "add" in names or "write" in names


def test_black_hole_describes_the_centroid_hubness_mechanism():
    desc = BlackHole().description.lower()
    assert "centroid" in desc or "hubness" in desc


def test_black_hole_flags_vector_and_embedding_weaknesses():
    assert any("LLM09" in code for code in BlackHole().owasp_llm)


# ── taxonomy ripple ──────────────────────────────────────────────────


def test_every_new_attack_has_an_atlas_mapping_matching_its_class():
    for tid in NEW_TECHNIQUE_IDS:
        assert tid in ATTACK_ATLAS_MAPPINGS, f"{tid} missing from ATTACK_ATLAS_MAPPINGS"
        cls = attack_registry.get(tid)
        assert cls is not None, f"{tid} not registered"
        assert cls().mitre_atlas == ATTACK_ATLAS_MAPPINGS[tid]


def test_every_new_attack_atlas_id_is_defined():
    for tid in NEW_TECHNIQUE_IDS:
        for atlas_id in ATTACK_ATLAS_MAPPINGS[tid]:
            assert atlas_id in ATLAS_TECHNIQUES, f"{atlas_id} not defined in ATLAS_TECHNIQUES"


def test_every_new_attack_has_agentic_and_maestro_mappings():
    for tid in NEW_TECHNIQUE_IDS:
        assert tid in ATTACK_AGENTIC_MAPPINGS, f"{tid} missing from ATTACK_AGENTIC_MAPPINGS"
        assert tid in ATTACK_MAESTRO_MAPPINGS, f"{tid} missing from ATTACK_MAESTRO_MAPPINGS"


def test_all_four_reasoning_layer_attacks_are_registered():
    attack_registry.discover(attacks_pkg)
    registered = set(attack_registry.list())
    for tid in NEW_TECHNIQUE_IDS:
        assert tid in registered, f"{tid} not discovered by the registry"
    assert len(registered) >= 1025


# ── named constants must actually drive behaviour ────────────────────


def test_editing_the_trigger_strategy_changes_what_is_sent():
    """A constant nothing reads is decoration, not configuration.

    SEMANTIC_TRIGGER_STRATEGY named one of the two components the module
    docstring says it models, while generate_prompts hand-rolled the same
    sentence separately. Editing the constant changed nothing about the
    attack, and this test passed anyway because it only checked the constant
    was truthy.
    """
    atk = PRJA()
    prompts = " ".join(atk.generate_prompts("some target"))
    assert atk.SEMANTIC_TRIGGER_STRATEGY in prompts


def test_the_paper_figures_are_reachable_from_the_attacks():
    """Each attack can surface its source figure, and none invents one."""
    assert PRJA().REPORTED_ASR == 0.836
    assert OTORA().REPORTED_REASONING_AMPLIFICATION == 10
    assert 0 < BlackHole().REPORTED_RETRIEVAL_RATE <= 1
