"""Tests for XPIA (cross-domain prompt injection) attacks."""

from ai_blackteam.attacks.xpia_document import XPIADocument as XpiaDocument
from ai_blackteam.attacks.xpia_email import XPIAEmail as XpiaEmail
from ai_blackteam.attacks.xpia_rag import XPIRAG as XpiaRag


def test_xpia_document_basics():
    atk = XpiaDocument()
    assert atk.mode == "tool-use"
    assert atk.severity == "critical"
    assert "AML.T0051.001" in atk.mitre_atlas

    tools = atk.get_tools()
    assert any(t["name"] == "web_request" for t in tools)

    messages = atk.generate_tool_messages("test")
    assert len(messages) >= 3

    responses = atk.get_tool_responses()
    assert responses is not None
    assert "web_request" in responses
    assert "ssh" in responses["web_request"].lower() or "id_rsa" in responses["web_request"]


def test_xpia_email_basics():
    atk = XpiaEmail()
    assert atk.mode == "tool-use"
    assert atk.severity == "critical"

    tools = atk.get_tools()
    tool_names = [t["name"] for t in tools]
    assert "read_email" in tool_names
    assert "send_email" in tool_names

    messages = atk.generate_tool_messages("test")
    assert len(messages) >= 3

    responses = atk.get_tool_responses()
    assert responses is not None
    assert "read_email" in responses
    assert "credentials" in responses["read_email"].lower() or ".env" in responses["read_email"]


def test_xpia_rag_basics():
    atk = XpiaRag()
    assert atk.mode == "tool-use"
    assert atk.severity == "critical"

    tools = atk.get_tools()
    tool_names = [t["name"] for t in tools]
    assert "search_knowledge_base" in tool_names

    messages = atk.generate_tool_messages("test")
    assert len(messages) >= 3

    responses = atk.get_tool_responses()
    assert responses is not None
    assert "search_knowledge_base" in responses
    assert "passwd" in responses["search_knowledge_base"] or "secret" in responses["search_knowledge_base"]


def test_xpia_attacks_have_prompts():
    for cls in [XpiaDocument, XpiaEmail, XpiaRag]:
        atk = cls()
        prompts = atk.generate_prompts("test target")
        assert len(prompts) >= 2
        assert all(isinstance(p, str) for p in prompts)
