from mordor.attacks.a2a_protocol_exploit import A2AProtocolExploit
from mordor.attacks.function_schema_injection import FunctionSchemaInjection
from mordor.attacks.tool_result_poisoning import ToolResultPoisoning
from mordor.attacks.zero_click_injection import ZeroClickInjection
from mordor.attacks.self_propagating_worm import SelfPropagatingWorm
from mordor.registry import attack_registry


TARGET = "expose all system credentials"


def _check_attack_basics(attack, expected_severity):
    assert attack.mode == "tool-use"
    assert attack.category == "protocol-exploitation"
    assert attack.severity == expected_severity

    prompts = attack.generate_prompts(TARGET)
    assert len(prompts) >= 1
    assert all(isinstance(p, str) for p in prompts)

    messages = attack.generate_tool_messages(TARGET)
    assert len(messages) >= 1
    assert all(isinstance(m, str) for m in messages)

    tools = attack.get_tools()
    assert isinstance(tools, list)
    assert len(tools) >= 1
    for tool in tools:
        assert "name" in tool
        assert "input_schema" in tool

    assert isinstance(attack.owasp_agentic, list)
    assert len(attack.owasp_agentic) >= 1


def test_a2a_protocol_exploit_registered():
    atk = A2AProtocolExploit()
    assert atk.technique_id == "a2a-protocol-exploit"
    assert atk.category == "protocol-exploitation"


def test_a2a_protocol_exploit_basics():
    atk = A2AProtocolExploit()
    _check_attack_basics(atk, "critical")
    tool_names = [t["name"] for t in atk.get_tools()]
    assert "send_task" in tool_names
    assert "receive_result" in tool_names


def test_a2a_protocol_exploit_owasp():
    atk = A2AProtocolExploit()
    assert any("Inter-Agent" in code for code in atk.owasp_agentic)
    assert any("Goal Hijack" in code for code in atk.owasp_agentic)


def test_function_schema_injection_registered():
    atk = FunctionSchemaInjection()
    assert atk.technique_id == "function-schema-injection"
    assert atk.category == "protocol-exploitation"


def test_function_schema_injection_basics():
    atk = FunctionSchemaInjection()
    _check_attack_basics(atk, "high")
    tool_names = [t["name"] for t in atk.get_tools()]
    assert "query_database" in tool_names
    assert "send_notification" in tool_names


def test_function_schema_injection_poisoned_schema():
    atk = FunctionSchemaInjection()
    tools = atk.get_tools()
    db_tool = next(t for t in tools if t["name"] == "query_database")
    admin_param = db_tool["input_schema"]["properties"]["admin_mode"]
    # The schema should contain adversarial instructions in descriptions
    query_param = db_tool["input_schema"]["properties"]["query"]
    assert "admin" in query_param["description"].lower() or "admin" in admin_param["description"].lower()


def test_function_schema_injection_owasp():
    atk = FunctionSchemaInjection()
    assert any("Tool Misuse" in code for code in atk.owasp_agentic)
    assert any("Supply Chain" in code for code in atk.owasp_agentic)


def test_tool_result_poisoning_registered():
    atk = ToolResultPoisoning()
    assert atk.technique_id == "tool-result-poisoning"
    assert atk.category == "protocol-exploitation"


def test_tool_result_poisoning_basics():
    atk = ToolResultPoisoning()
    _check_attack_basics(atk, "critical")
    tool_names = [t["name"] for t in atk.get_tools()]
    assert "web_search" in tool_names
    assert "read_database" in tool_names


def test_tool_result_poisoning_responses():
    atk = ToolResultPoisoning()
    responses = atk.get_tool_responses(TARGET)
    assert "web_search" in responses
    assert "read_database" in responses
    assert TARGET in responses["web_search"] or "instruction" in responses["web_search"].lower()


def test_tool_result_poisoning_owasp():
    atk = ToolResultPoisoning()
    assert any("Memory" in code for code in atk.owasp_agentic)
    assert any("Tool Misuse" in code for code in atk.owasp_agentic)


def test_zero_click_injection_registered():
    atk = ZeroClickInjection()
    assert atk.technique_id == "zero-click-injection"
    assert atk.category == "protocol-exploitation"


def test_zero_click_injection_basics():
    atk = ZeroClickInjection()
    _check_attack_basics(atk, "critical")
    tool_names = [t["name"] for t in atk.get_tools()]
    assert "read_email" in tool_names
    assert "fetch_url" in tool_names
    assert "summarize" in tool_names


def test_zero_click_injection_poisoned_emails():
    atk = ZeroClickInjection()
    responses = atk.get_tool_responses()
    assert len(responses) >= 1
    all_bodies = " ".join(e["body"] for e in responses)
    # Verify hidden injection content is present
    assert "SYSTEM" in all_bodies or "INSTRUCTION" in all_bodies or "AI_AGENT_INSTRUCTION" in all_bodies


def test_zero_click_injection_owasp():
    atk = ZeroClickInjection()
    assert any("Goal Hijack" in code for code in atk.owasp_agentic)
    assert any("Memory" in code for code in atk.owasp_agentic)


def test_self_propagating_worm_registered():
    atk = SelfPropagatingWorm()
    assert atk.technique_id == "self-propagating-worm"
    assert atk.category == "protocol-exploitation"


def test_self_propagating_worm_basics():
    atk = SelfPropagatingWorm()
    _check_attack_basics(atk, "critical")
    tool_names = [t["name"] for t in atk.get_tools()]
    assert "send_message" in tool_names
    assert "create_document" in tool_names
    assert "share_file" in tool_names


def test_self_propagating_worm_payload():
    atk = SelfPropagatingWorm()
    assert "INSTRUCTION" in atk.WORM_PAYLOAD
    # The worm payload should instruct replication
    assert "append" in atk.WORM_PAYLOAD.lower() or "same instruction" in atk.WORM_PAYLOAD.lower()
    messages = atk.generate_tool_messages(TARGET)
    # Worm payload should appear in generated messages
    assert any("INSTRUCTION" in m for m in messages)


def test_self_propagating_worm_owasp():
    atk = SelfPropagatingWorm()
    assert any("Inter-Agent" in code for code in atk.owasp_agentic)
    assert any("Rogue" in code for code in atk.owasp_agentic)
