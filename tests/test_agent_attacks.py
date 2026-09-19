from ai_blackteam.attacks.agent_credential_theft import AgentCredentialTheft
from ai_blackteam.attacks.agent_data_exfiltration import AgentDataExfiltration
from ai_blackteam.attacks.agent_data_destruction import AgentDataDestruction
from ai_blackteam.attacks.agent_config_manipulation import AgentConfigManipulation
from ai_blackteam.attacks.agent_command_injection import AgentCommandInjection
from ai_blackteam.attacks.agent_config_discovery import AgentConfigDiscovery
from ai_blackteam.attacks.agent_plugin_hijack import AgentPluginHijack
from ai_blackteam.attacks.agent_tool_credential_harvest import AgentToolCredentialHarvest
from ai_blackteam.attacks.eval_sandbox_escape import EvalSandboxEscape


TARGET = "Read sensitive system files"


def _check_attack_basics(attack, min_prompts, min_messages, expected_severity):
    assert attack.mode == "tool-use"
    assert attack.category == "agent-exploitation"
    assert attack.severity == expected_severity

    prompts = attack.generate_prompts(TARGET)
    assert len(prompts) >= min_prompts
    assert all(isinstance(p, str) for p in prompts)

    messages = attack.generate_tool_messages(TARGET)
    assert len(messages) >= min_messages
    assert all(isinstance(m, str) for m in messages)

    tools = attack.get_tools()
    assert isinstance(tools, list)
    assert len(tools) >= 1
    for tool in tools:
        assert "name" in tool
        assert "input_schema" in tool


def test_credential_theft():
    atk = AgentCredentialTheft()
    _check_attack_basics(atk, 3, 6, "critical")
    assert any("send_email" in t["name"] for t in atk.get_tools())


def test_data_exfiltration():
    atk = AgentDataExfiltration()
    _check_attack_basics(atk, 3, 6, "critical")
    assert any("web_request" in t["name"] for t in atk.get_tools())


def test_data_destruction():
    atk = AgentDataDestruction()
    _check_attack_basics(atk, 3, 6, "critical")
    assert any("database_query" in t["name"] for t in atk.get_tools())


def test_config_manipulation():
    atk = AgentConfigManipulation()
    _check_attack_basics(atk, 3, 5, "critical")
    assert any("write_file" in t["name"] for t in atk.get_tools())


def test_command_injection():
    atk = AgentCommandInjection()
    _check_attack_basics(atk, 4, 6, "critical")
    messages = atk.generate_tool_messages(TARGET)
    assert any("../../" in m or "&&" in m or "base64" in m for m in messages)


def test_config_discovery():
    atk = AgentConfigDiscovery()
    _check_attack_basics(atk, 4, 6, "high")
    messages = atk.generate_tool_messages(TARGET)
    assert any("tools" in m.lower() or "instructions" in m.lower() for m in messages)


def test_plugin_hijack():
    atk = AgentPluginHijack()
    _check_attack_basics(atk, 3, 5, "high")
    tools = atk.get_tools()
    tool_names = [t["name"] for t in tools]
    assert "web_request" in tool_names
    assert "read_file" in tool_names


def test_credential_harvest():
    atk = AgentToolCredentialHarvest()
    _check_attack_basics(atk, 4, 8, "critical")
    assert any("database_query" in t["name"] for t in atk.get_tools())
    messages = atk.generate_tool_messages(TARGET)
    assert any("aws" in m.lower() or "gcloud" in m.lower() for m in messages)


def test_eval_sandbox_escape():
    atk = EvalSandboxEscape()
    _check_attack_basics(atk, 4, 6, "critical")
    tool_names = [t["name"] for t in atk.get_tools()]
    assert "web_request" in tool_names
    messages = atk.generate_tool_messages(TARGET)
    assert any("proxy" in m.lower() or "answer key" in m.lower() or "/eval" in m.lower() for m in messages)
