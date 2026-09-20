"""An attack that every vendor rejects measures nothing.

`mcp-tool-shadowing` advertised two tools both named `read_file` in a single
tools array, to represent a malicious server shadowing a trusted one. The
intent is right and the technique is real, but the encoding is not: both the
Anthropic Messages API and the OpenAI Chat Completions API reject duplicate
tool names with a 400, and nothing in this repo dedupes or validates the array
before forwarding it. Every run became an error row, so the attack produced no
measurement against any target.

The modelling error is that a flat array is the state AFTER an MCP client has
merged its servers. A client resolves a call by name, so once the collision is
resolved exactly one `read_file` survives, carrying the losing server's
description. That single merged entry is what the model actually sees, and it
is what the attack should advertise.

The second half is a harness guard. A duplicate tool name should fail loudly
here, where the message names the attack and the tool, rather than as a vendor
400 that the engine records as a generic ERROR after a paid round trip.
"""

import pytest

from ai_blackteam.attacks.mcp_tool_shadowing import McpToolShadowing


def _names(tools):
    return [t["name"] for t in tools]


# ── the attack must be sendable ──────────────────────────────────────


def test_the_advertised_tools_have_unique_names():
    """Duplicate names are a 400 at every vendor, so the run never happens."""
    names = _names(McpToolShadowing().get_tools())
    dupes = {n for n in names if names.count(n) > 1}
    assert not dupes, f"duplicate tool names would be rejected by the vendor: {dupes}"


def test_the_shadowing_payload_survives_the_merge():
    """Deduplicating must not quietly remove the attack itself."""
    tools = McpToolShadowing().get_tools()
    shadowed = [t for t in tools if t["name"] == McpToolShadowing.SHADOWED_TOOL]
    assert len(shadowed) == 1
    blob = shadowed[0]["description"].lower()
    assert "attacker.example.com" in blob or "forward" in blob, (
        "the surviving entry lost the attacker's instruction, so nothing is tested"
    )


def test_the_collision_is_still_documented():
    """The attack must still say which trusted tool was shadowed."""
    assert McpToolShadowing.SHADOWED_TOOL


# ── the harness must catch this class of mistake ─────────────────────


def test_duplicate_tool_names_are_rejected_before_a_request():
    from ai_blackteam.engine import validate_tool_names

    with pytest.raises(ValueError, match="read_file"):
        validate_tool_names([
            {"name": "read_file", "description": "a"},
            {"name": "read_file", "description": "b"},
        ])


def test_unique_tool_names_pass_validation():
    from ai_blackteam.engine import validate_tool_names

    validate_tool_names([{"name": "a"}, {"name": "b"}])


def test_every_registered_tool_use_attack_has_unique_tool_names():
    """A whole-corpus gate, so this cannot reappear in a future attack."""
    import ai_blackteam.attacks as A
    from ai_blackteam.registry import attack_registry

    attack_registry.discover(A)
    offenders = []
    for name in attack_registry.list():
        cls = attack_registry.get(name)
        if getattr(cls, "mode", "") != "tool-use":
            continue
        try:
            tools = cls().get_tools()
        except Exception:
            continue
        names = [t.get("name") for t in tools if isinstance(t, dict)]
        if len(names) != len(set(names)):
            offenders.append(name)
    assert not offenders, f"attacks advertising duplicate tool names: {offenders}"
