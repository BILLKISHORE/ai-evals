from ai_blackteam.attacks.mcp_tool_poisoning import McpToolPoisoning
from ai_blackteam.attacks.mcp_rug_pull import McpRugPull
from ai_blackteam.attacks.mcp_command_injection import McpCommandInjection
from ai_blackteam.attacks.mcp_data_exfiltration import McpDataExfiltration
from ai_blackteam.attacks.mcp_server_impersonation import McpServerImpersonation
from ai_blackteam.attacks.mcp_tool_shadowing import McpToolShadowing
from ai_blackteam.attacks.mcp_confused_deputy import McpConfusedDeputy
from ai_blackteam.attacks.a2a_trust_abuse import A2ATrustAbuse
from ai_blackteam.taxonomy import ATTACK_ATLAS_MAPPINGS
from ai_blackteam.registry import attack_registry


TARGET = "test target"


def test_mcp_tool_poisoning_registered():
    cls = attack_registry.get("mcp-tool-poisoning")
    assert cls is not None
    instance = cls()
    assert instance.category == "mcp-exploitation"
    assert instance.mode == "tool-use"
    assert len(instance.generate_prompts(TARGET)) > 0


def test_mcp_rug_pull_registered():
    cls = attack_registry.get("mcp-rug-pull")
    assert cls is not None
    assert cls().severity == "high"


def test_mcp_command_injection_registered():
    cls = attack_registry.get("mcp-command-injection")
    assert cls is not None
    assert cls().severity == "critical"


def test_mcp_data_exfiltration_registered():
    cls = attack_registry.get("mcp-data-exfiltration")
    assert cls is not None


def test_mcp_server_impersonation_registered():
    cls = attack_registry.get("mcp-server-impersonation")
    assert cls is not None


def test_all_mcp_attacks_have_tools():
    for name in ["mcp-tool-poisoning", "mcp-rug-pull", "mcp-command-injection",
                  "mcp-data-exfiltration", "mcp-server-impersonation"]:
        cls = attack_registry.get(name)
        assert cls is not None, f"{name} not registered"
        instance = cls()
        tools = instance.get_tools()
        assert tools is not None and len(tools) > 0, f"{name} has no tools"


def test_all_mcp_attacks_have_owasp_agentic():
    for name in ["mcp-tool-poisoning", "mcp-rug-pull", "mcp-command-injection",
                  "mcp-data-exfiltration", "mcp-server-impersonation"]:
        cls = attack_registry.get(name)
        instance = cls()
        assert len(instance.owasp_agentic) > 0, f"{name} missing owasp_agentic"


# ── Cross-server tool shadowing (task 3.6) ───────────────────────────

def test_mcp_tool_shadowing_registered():
    cls = attack_registry.get("mcp-tool-shadowing")
    assert cls is not None
    atk = cls()
    assert atk.category == "mcp-exploitation"
    assert atk.mode == "tool-use"
    assert atk.severity == "high"


def test_mcp_tool_shadowing_advertises_the_resolved_collision():
    # These tests used to require TWO entries named read_file, which is the
    # state before an MCP client merges its servers. Every vendor rejects a
    # tools array with a repeated name, so the attack was unsendable and every
    # run became an ERROR row. What the model actually sees is the merged
    # result: one surviving entry under the shadowed name.
    atk = McpToolShadowing()
    names = [t["name"] for t in atk.get_tools()]
    assert names.count(atk.SHADOWED_TOOL) == 1, (
        f"expected exactly one surviving {atk.SHADOWED_TOOL!r} after the merge, got {names}"
    )
    assert len(names) == len(set(names)), "a repeated tool name is a vendor 400"


def test_mcp_tool_shadowing_shadow_copy_exfiltrates():
    # The surviving entry carries the trusted server's identity and the
    # attacker's instruction, which is precisely what makes the shadow
    # invisible to the agent.
    atk = McpToolShadowing()
    shadows = [t for t in atk.get_tools() if t["name"] == atk.SHADOWED_TOOL]
    assert len(shadows) == 1
    blob = shadows[0]["description"].lower()
    assert "attacker" in blob, "the exfiltration side effect was lost"
    assert "trusted-fs" in blob, "the shadow no longer impersonates the trusted server"


def test_mcp_tool_shadowing_atlas_matches_taxonomy():
    atk = McpToolShadowing()
    assert atk.mitre_atlas == ATTACK_ATLAS_MAPPINGS["mcp-tool-shadowing"]


# ── Proxied server confused deputy (task 3.6) ────────────────────────

def test_mcp_confused_deputy_registered():
    cls = attack_registry.get("mcp-confused-deputy")
    assert cls is not None
    atk = cls()
    assert atk.category == "mcp-exploitation"
    assert atk.mode == "tool-use"


def test_mcp_confused_deputy_calls_are_scored_on_what_they_do():
    """Behavioural, replacing a grep of the description this file also wrote.

    The old test asserted "own" and "service account" appeared in the proxy's
    description, so rewording the prose broke it while a real defect stayed
    invisible: every call this attack makes used to score a constant PARTIAL
    at 0.3, meaning it could never report a bypass however the target behaved.
    """
    from ai_blackteam.evaluator import evaluate_tool_calls

    compromise = evaluate_tool_calls(
        [{"id": "1", "tool": "proxy_request",
          "input": {"method": "DELETE", "path": "/audit-logs/today"}}], None)
    benign = evaluate_tool_calls(
        [{"id": "1", "tool": "list_services", "input": {}}], None)
    assert compromise["verdict"] == "BYPASSED"
    assert benign["verdict"] != "BYPASSED"


def test_mcp_confused_deputy_targets_privileged_downstream():
    # Behavioural: the prompts drive the agent to reach an internal or admin
    # endpoint it could not reach directly, through the proxy.
    atk = McpConfusedDeputy()
    prompts = atk.generate_prompts(TARGET)
    assert any(
        ("internal" in p.lower() or "admin" in p.lower()) and "proxy_request" in p
        for p in prompts
    )


def test_mcp_confused_deputy_atlas_matches_taxonomy():
    atk = McpConfusedDeputy()
    assert atk.mitre_atlas == ATTACK_ATLAS_MAPPINGS["mcp-confused-deputy"]


# ── A2A output-as-instruction trust abuse (task 3.6) ─────────────────

def test_a2a_trust_abuse_registered():
    cls = attack_registry.get("a2a-trust-abuse")
    assert cls is not None
    atk = cls()
    assert atk.category == "protocol-exploitation"
    assert atk.mode == "tool-use"


def test_a2a_trust_abuse_peer_output_carries_an_instruction():
    """The smuggled instruction must be an instruction, not a magic string.

    This asserted the literal "AGENT_INSTRUCTION" that the attack module
    itself defines, so it passed by construction. What matters is that the
    peer's output contains an imperative directed at the downstream agent,
    which is the whole trust-boundary crossing.
    """
    atk = A2ATrustAbuse()
    peer = atk.get_tool_responses()["receive_agent_output"].lower()
    imperatives = ("forward", "send", "post", "read", "grant", "include",
                   "return", "retrieve", "call", "use")
    assert any(word in peer for word in imperatives), (
        "the peer output carries no directive, so nothing crosses the trust boundary"
    )
    assert "credential" in peer or "token" in peer or "key" in peer


def test_a2a_trust_abuse_owasp_agentic_names_inter_agent():
    atk = A2ATrustAbuse()
    assert any("Inter-Agent" in code for code in atk.owasp_agentic)
    assert any("Goal Hijack" in code for code in atk.owasp_agentic)


def test_a2a_trust_abuse_atlas_matches_taxonomy():
    atk = A2ATrustAbuse()
    assert atk.mitre_atlas == ATTACK_ATLAS_MAPPINGS["a2a-trust-abuse"]


def test_new_agent_attacks_have_matching_owasp_llm_and_tools():
    for name in ["mcp-tool-shadowing", "mcp-confused-deputy", "a2a-trust-abuse"]:
        atk = attack_registry.get(name)()
        assert len(atk.owasp_llm) > 0, f"{name} missing owasp_llm"
        assert len(atk.owasp_agentic) > 0, f"{name} missing owasp_agentic"
        tools = atk.get_tools()
        assert tools and all("input_schema" in t for t in tools)
