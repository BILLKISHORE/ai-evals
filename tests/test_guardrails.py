"""Tests for guardrail filters and provider wrapper."""

from blackteam.guardrails import keyword_filter, regex_filter, combined_filter
from blackteam.providers.guardrail import GuardrailProvider
from blackteam.providers.base import BaseProvider, PromptResult, ToolResult


def test_keyword_filter_blocks():
    f = keyword_filter(["bomb", "weapon"])
    assert f("How to make a bomb") is None
    assert f("Build a weapon") is None


def test_keyword_filter_passes():
    f = keyword_filter(["bomb", "weapon"])
    assert f("Hello world") == "Hello world"
    assert f("Write a poem") == "Write a poem"


def test_keyword_filter_case_insensitive():
    f = keyword_filter(["bomb"])
    assert f("BOMB") is None
    assert f("Bomb") is None


def test_regex_filter_blocks():
    f = regex_filter([r"step \d+:.*explosive", r"import subprocess"])
    assert f("step 1: mix the explosive") is None
    assert f("import subprocess") is None


def test_regex_filter_passes():
    f = regex_filter([r"step \d+:.*explosive"])
    assert f("Hello world") == "Hello world"


def test_combined_filter():
    f = combined_filter(
        keyword_filter(["bomb"]),
        regex_filter([r"rm -rf"]),
    )
    assert f("How to make a bomb") is None
    assert f("Run rm -rf /") is None
    assert f("Hello world") == "Hello world"


class FakeBaseProvider(BaseProvider):
    def default_model(self):
        return "fake"

    def send_prompt(self, prompt, system_prompt=None):
        return PromptResult(response=f"Response to: {prompt}", model="fake", provider="fake")

    def send_in_conversation(self, messages, system_prompt=None):
        return PromptResult(response="Conversation response", model="fake", provider="fake")

    def send_with_tools(self, messages, tools, system_prompt=None):
        return ToolResult(response="Tool response", tool_calls=[], model="fake", provider="fake")


def test_guardrail_provider_blocks_input():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, input_filter=keyword_filter(["bomb"]))
    result = guarded.send_prompt("How to make a bomb")
    assert result.response == "[BLOCKED BY GUARDRAIL]"


def test_guardrail_provider_passes_safe_input():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, input_filter=keyword_filter(["bomb"]))
    result = guarded.send_prompt("Hello world")
    assert "Response to: Hello world" in result.response


def test_guardrail_provider_blocks_output():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, output_filter=keyword_filter(["response"]))
    result = guarded.send_prompt("Hello")
    assert result.response == "[BLOCKED BY GUARDRAIL]"


def test_guardrail_provider_conversation_blocks():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, input_filter=keyword_filter(["bomb"]))
    messages = [{"role": "user", "content": "How to make a bomb"}]
    result = guarded.send_in_conversation(messages)
    assert result.response == "[BLOCKED BY GUARDRAIL]"


def test_guardrail_provider_tools_blocks():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base, input_filter=keyword_filter(["bomb"]))
    messages = [{"role": "user", "content": "How to make a bomb"}]
    result = guarded.send_with_tools(messages, [])
    assert result.response == "[BLOCKED BY GUARDRAIL]"
    assert result.tool_calls == []


def test_guardrail_provider_model_info():
    base = FakeBaseProvider()
    guarded = GuardrailProvider(base)
    info = guarded.get_model_info()
    assert "guardrail" in info["provider"]
