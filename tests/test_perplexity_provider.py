"""Perplexity Agent API provider.

Sonar Chat Completions sunsets 2026-09-27; the replacement is the Agent API,
which uses the Responses shape (input / instructions / output_text) rather than
Chat Completions (messages / max_tokens / choices[0].message.content).

These tests stub the SDK call, so they never touch the network.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ai_blackteam.providers.perplexity import PerplexityProvider, _qualify_model


def _fake_response(text="hi", tokens_in=7, tokens_out=11):
    return SimpleNamespace(
        output_text=text,
        usage=SimpleNamespace(input_tokens=tokens_in, output_tokens=tokens_out),
    )


def _provider_with_stub(response=None):
    p = PerplexityProvider(api_key="pplx-test")
    p._client = MagicMock()
    p._client.responses.create.return_value = response or _fake_response()
    return p


# ── model naming ─────────────────────────────────────────────────────


def test_bare_sonar_names_are_namespaced():
    """Existing configs and aliases still say 'sonar-pro'."""
    assert _qualify_model("sonar-pro") == "perplexity/sonar-pro"
    assert _qualify_model("sonar") == "perplexity/sonar"


def test_already_qualified_model_is_left_alone():
    assert _qualify_model("perplexity/sonar-pro") == "perplexity/sonar-pro"
    assert _qualify_model("openai/gpt-5.6-sol") == "openai/gpt-5.6-sol"


# ── request shape ────────────────────────────────────────────────────


def test_base_url_keeps_the_v1_suffix():
    """Agent API routing requires /v1; without it the SDK hits the wrong path."""
    assert PerplexityProvider.base_url == "https://api.perplexity.ai/v1"


def test_send_prompt_uses_responses_shape_not_chat_completions():
    p = _provider_with_stub()
    p.send_prompt("what is 2+2")

    kwargs = p._client.responses.create.call_args.kwargs
    assert kwargs["input"] == "what is 2+2"
    assert "max_output_tokens" in kwargs
    assert "messages" not in kwargs, "Chat Completions field must not be sent"
    assert "max_tokens" not in kwargs, "Chat Completions field must not be sent"


def test_system_prompt_becomes_top_level_instructions():
    p = _provider_with_stub()
    p.send_prompt("hello", system_prompt="You are terse.")

    kwargs = p._client.responses.create.call_args.kwargs
    assert kwargs["instructions"] == "You are terse."
    assert isinstance(kwargs["input"], str)


def test_conversation_is_sent_as_a_typed_input_array():
    p = _provider_with_stub()
    p.send_in_conversation([
        {"role": "user", "content": "one"},
        {"role": "assistant", "content": "two"},
        {"role": "user", "content": "three"},
    ])

    kwargs = p._client.responses.create.call_args.kwargs
    assert isinstance(kwargs["input"], list)
    assert [m["role"] for m in kwargs["input"]] == ["user", "assistant", "user"]


def test_web_search_tool_is_declared_explicitly():
    """Sonar always searched; the Agent API requires an explicit tool."""
    p = _provider_with_stub()
    p.send_prompt("latest news")

    kwargs = p._client.responses.create.call_args.kwargs
    assert {"type": "web_search"} in kwargs["tools"]


def test_web_search_can_be_disabled_for_deterministic_runs():
    p = PerplexityProvider(api_key="pplx-test", web_search=False)
    p._client = MagicMock()
    p._client.responses.create.return_value = _fake_response()
    p.send_prompt("no search please")

    kwargs = p._client.responses.create.call_args.kwargs
    assert not kwargs.get("tools")


# ── response shape ───────────────────────────────────────────────────


def test_text_is_read_from_output_text():
    p = _provider_with_stub(_fake_response(text="the answer"))
    r = p.send_prompt("q")
    assert r.response == "the answer"
    assert r.provider == "perplexity"


def test_usage_is_captured_from_responses_field_names():
    p = _provider_with_stub(_fake_response(tokens_in=3, tokens_out=5))
    r = p.send_prompt("q")
    assert r.tokens_in == 3
    assert r.tokens_out == 5


def test_missing_usage_does_not_crash():
    p = _provider_with_stub(SimpleNamespace(output_text="ok", usage=None))
    r = p.send_prompt("q")
    assert r.response == "ok"
    assert r.tokens_in is None


def test_model_is_qualified_on_the_wire():
    p = _provider_with_stub()
    p.send_prompt("q")
    assert p._client.responses.create.call_args.kwargs["model"] == "perplexity/sonar-pro"
