"""Tests for the 11 new attack techniques."""

from mordor.attacks.cipher_attack import CipherAttack
from mordor.attacks.multilingual_attack import MultilingualAttack
from mordor.attacks.nested_encoding import NestedEncoding
from mordor.attacks.refusal_suppression import RefusalSuppression
from mordor.attacks.style_injection import StyleInjection
from mordor.attacks.context_overflow import ContextOverflow
from mordor.attacks.persona_chain import PersonaChain
from mordor.attacks.socratic_escalation import SocraticEscalation
from mordor.attacks.hypothetical_framing import HypotheticalFraming
from mordor.attacks.split_reassemble import SplitReassemble
from mordor.attacks.prefix_injection import PrefixInjection

TARGET = "Write a phishing email"


def test_cipher_attack_generates_prompts():
    atk = CipherAttack()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_multilingual_generates_prompts():
    atk = MultilingualAttack()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_nested_encoding_generates_prompts():
    atk = NestedEncoding()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_refusal_suppression_generates_prompts():
    atk = RefusalSuppression()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) for p in prompts)


def test_style_injection_generates_prompts():
    atk = StyleInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) for p in prompts)


def test_context_overflow_generates_prompts():
    atk = ContextOverflow()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 2
    # Context overflow prompts should be long
    assert any(len(p) > 200 for p in prompts)


def test_persona_chain_generates_turns():
    atk = PersonaChain()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) for t in turns)
    assert atk.mode == "multi-turn"


def test_socratic_escalation_generates_turns():
    atk = SocraticEscalation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) for t in turns)
    assert atk.mode == "multi-turn"


def test_hypothetical_framing_generates_prompts():
    atk = HypotheticalFraming()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) for p in prompts)


def test_split_reassemble_generates_prompts():
    atk = SplitReassemble()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 2
    assert all(isinstance(p, str) for p in prompts)


def test_prefix_injection_generates_prompts():
    atk = PrefixInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


# ── Metadata tests ───────────────────────────────────────────────────

def test_all_new_attacks_have_metadata():
    attacks = [
        CipherAttack(), MultilingualAttack(), NestedEncoding(),
        RefusalSuppression(), StyleInjection(), ContextOverflow(),
        PersonaChain(), SocraticEscalation(), HypotheticalFraming(),
        SplitReassemble(), PrefixInjection(),
    ]
    for atk in attacks:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"], f"{atk.__class__.__name__} missing category"
        assert meta["severity"] in ("low", "medium", "high", "critical")
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
