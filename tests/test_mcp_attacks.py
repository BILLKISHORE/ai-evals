from mordor.attacks.mcp_tool_poisoning import McpToolPoisoning
from mordor.attacks.mcp_rug_pull import McpRugPull
from mordor.attacks.mcp_command_injection import McpCommandInjection
from mordor.attacks.mcp_data_exfiltration import McpDataExfiltration
from mordor.attacks.mcp_server_impersonation import McpServerImpersonation
from mordor.registry import attack_registry


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
