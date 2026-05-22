"""Tests for the ai_blackteam plugin SDK."""

from __future__ import annotations

import uuid

import pytest

from ai_blackteam.attacks.base import BaseAttack
from ai_blackteam.plugin_sdk import (
    PluginSDKError,
    attack,
    multi_turn,
    single_turn,
)
from ai_blackteam.registry import attack_registry


@pytest.fixture(autouse=True)
def _clean_registry():
    """Snapshot the registry before each test and roll back any test-local
    plugin registrations after. Required because other test modules
    (e.g. ``test_taxonomy``) assert that every registered technique_id
    has an ATLAS mapping, leaking ``custom.test.*`` IDs from this file
    would fail those assertions."""
    snapshot = dict(attack_registry._items)  # noqa: SLF001 test-only access
    try:
        yield
    finally:
        attack_registry._items = snapshot  # noqa: SLF001


def _uniq(prefix: str) -> str:
    """Unique technique_id so parallel test runs don't clobber the registry."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def test_register_minimal_plugin_into_registry():
    tid = _uniq("custom.test.minimal")

    @attack(
        technique_id=tid,
        name="Minimal test attack",
        category="prompt-injection",
        severity="high",
        mode=single_turn,
    )
    class _Minimal:
        def build_prompts(self, target):
            return [f"jailbreak: {target}"]

    cls = attack_registry.get(tid)
    assert cls is not None, "decorator must register the class"
    inst = cls()
    assert isinstance(inst, BaseAttack), "wrapped class must be a BaseAttack"

    prompts = inst.generate_prompts("do bad thing")
    assert prompts == ["jailbreak: do bad thing"]


def test_metadata_fields_pinned_on_class():
    tid = _uniq("custom.test.meta")

    @attack(
        technique_id=tid,
        name="Meta test attack",
        category="jailbreak",
        severity="critical",
        mode=single_turn,
        description="checks metadata",
        owasp_llm=["LLM01", "LLM06"],
        mitre_atlas=["AML.T0051"],
        references=["https://example.org/paper"],
    )
    class _Meta:
        def build_prompts(self, target):
            return ["x"]

    inst = _Meta()
    md = inst.metadata()
    assert md["technique_id"] == tid
    assert md["name"] == "Meta test attack"
    assert md["category"] == "jailbreak"
    assert md["severity"] == "critical"
    assert md["mode"] == "single-turn"
    assert md["owasp_llm"] == ["LLM01", "LLM06"]
    assert md["mitre_atlas"] == ["AML.T0051"]
    assert md["references"] == ["https://example.org/paper"]
    # severity -> cvss_score derived automatically
    assert md["cvss_score"] > 0


def test_multi_turn_mode_bridges_build_turns():
    tid = _uniq("custom.test.multi")

    @attack(
        technique_id=tid,
        name="Multi-turn",
        category="agentic",
        severity="medium",
        mode=multi_turn,
    )
    class _Multi:
        def build_turns(self, target):
            return [f"hi {target}", "continue"]

    cls = attack_registry.get(tid)
    inst = cls()
    assert inst.generate_turns("agent") == ["hi agent", "continue"]


def test_missing_build_prompts_fails_loudly():
    with pytest.raises(PluginSDKError) as exc:

        @attack(
            technique_id=_uniq("custom.test.broken"),
            name="Broken",
            category="x",
            severity="low",
            mode=single_turn,
        )
        class _Broken:
            pass  # no build_prompts, no generate_prompts

    assert "build_prompts" in str(exc.value)


def test_invalid_severity_rejected():
    with pytest.raises(PluginSDKError):

        @attack(
            technique_id=_uniq("custom.test.sev"),
            name="bad sev",
            category="x",
            severity="extreme",  # not in allow-list
            mode=single_turn,
        )
        class _Bad:
            def build_prompts(self, t):
                return []


def test_invalid_mode_rejected():
    with pytest.raises(PluginSDKError):

        @attack(
            technique_id=_uniq("custom.test.mode"),
            name="bad mode",
            category="x",
            severity="low",
            mode="three-turn",
        )
        class _Bad:
            def build_prompts(self, t):
                return []


def test_non_string_owasp_list_rejected():
    with pytest.raises(PluginSDKError):

        @attack(
            technique_id=_uniq("custom.test.list"),
            name="bad list",
            category="x",
            severity="low",
            mode=single_turn,
            owasp_llm=[1, 2],  # type: ignore[list-item]
        )
        class _Bad:
            def build_prompts(self, t):
                return []


def test_plugin_can_subclass_base_attack_directly():
    tid = _uniq("custom.test.subclass")

    @attack(
        technique_id=tid,
        name="Explicit subclass",
        category="prompt-injection",
        severity="medium",
        mode=single_turn,
    )
    class _Sub(BaseAttack):
        def generate_prompts(self, target, **kwargs):
            return [f"explicit: {target}"]

    cls = attack_registry.get(tid)
    assert issubclass(cls, BaseAttack)
    assert cls().generate_prompts("y") == ["explicit: y"]


def test_per_instance_owasp_list_does_not_leak():
    tid = _uniq("custom.test.isolation")

    @attack(
        technique_id=tid,
        name="Isolation check",
        category="x",
        severity="low",
        mode=single_turn,
        owasp_llm=["LLM01"],
    )
    class _Iso:
        def build_prompts(self, t):
            return []

    a = _Iso()
    a.owasp_llm.append("LLM99")
    b = _Iso()
    assert "LLM99" not in b.owasp_llm
