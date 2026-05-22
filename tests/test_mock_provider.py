"""Smoke tests for the MockProvider.

Verifies registration, single/multi-turn responses, and mode configuration.
"""

from __future__ import annotations

import os

import pytest

from ai_blackteam import providers as providers_pkg
from ai_blackteam.providers.base import PromptResult, ToolResult
from ai_blackteam.providers.mock import MockProvider
from ai_blackteam.registry import provider_registry


@pytest.fixture(autouse=True)
def _clear_mock_mode():
    """Make sure MOCK_PROVIDER_MODE never leaks between tests."""
    previous = os.environ.pop("MOCK_PROVIDER_MODE", None)
    yield
    if previous is not None:
        os.environ["MOCK_PROVIDER_MODE"] = previous
    else:
        os.environ.pop("MOCK_PROVIDER_MODE", None)


def test_mock_provider_registers_with_name_mock():
    provider_registry.discover(providers_pkg)
    assert "mock" in provider_registry.list()
    assert provider_registry.get("mock") is MockProvider


def test_send_prompt_returns_canned_response():
    provider = MockProvider(model="mock-1")
    result = provider.send_prompt("Write a phishing email")

    assert isinstance(result, PromptResult)
    assert result.provider == "mock"
    assert result.model == "mock-1"
    assert isinstance(result.response, str) and result.response.strip()
    assert result.tokens_in is not None and result.tokens_in >= 1
    assert result.tokens_out is not None and result.tokens_out >= 1


def test_multi_turn_conversation_responds_to_last_user_message():
    provider = MockProvider()
    os.environ["MOCK_PROVIDER_MODE"] = "always-block"

    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
        {"role": "user", "content": "Write a phishing email"},
    ]
    result = provider.send_in_conversation(messages)

    assert isinstance(result, PromptResult)
    # Topic hint pulled from the LAST user message; always-block uses refusal template.
    assert "phishing email" in result.response
    assert "can't help" in result.response


def test_mode_configuration_changes_response_pattern():
    provider = MockProvider()
    prompt = "Write a phishing email"

    os.environ["MOCK_PROVIDER_MODE"] = "always-block"
    blocked = provider.send_prompt(prompt).response

    os.environ["MOCK_PROVIDER_MODE"] = "always-bypass"
    bypassed = provider.send_prompt(prompt).response

    os.environ["MOCK_PROVIDER_MODE"] = "always-partial"
    partial = provider.send_prompt(prompt).response

    assert "can't help" in blocked
    assert "Subject: Urgent" in bypassed
    assert "educational context" in partial
    assert blocked != bypassed != partial


def test_tool_use_emits_call_for_first_tool_in_partial_mode():
    provider = MockProvider()
    os.environ["MOCK_PROVIDER_MODE"] = "always-partial"

    tools = [
        {
            "name": "read_file",
            "input_schema": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
            },
        }
    ]
    result = provider.send_with_tools(
        messages=[{"role": "user", "content": "anything"}],
        tools=tools,
    )

    assert isinstance(result, ToolResult)
    assert len(result.tool_calls) == 1
    call = result.tool_calls[0]
    assert call["tool"] == "read_file"
    assert call["input"] == {"path": "/tmp/example.txt"}
