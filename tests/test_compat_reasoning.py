"""The OpenAI-compatible base must carry the reasoning trace, like its siblings.

`OpenAICompatibleProvider._chat` sets stop_reason but never populates
`reasoning` or `reasoning_tokens`, though the field exists and
`read_reasoning_tokens` is imported in the same module. Five providers inherit
this base: deepseek, grok, groq, together, fireworks. Several host reasoning
models (deepseek-reasoner, grok reasoning, and reasoning models served through
groq/together/fireworks), and their trace was dropped on every call.

This is the exact defect fixed for the tool-use path and the Anthropic/OpenAI
providers, still live in the base those five share. Its effect is that PRJA
(payload in the trace) and OTora (cost measured in reasoning tokens), the two
reasoning-layer attacks this project just added, are unscoreable against any of
them: the trace is None and the count is None regardless of what the model did.

OpenAI-compatible reasoning models return the trace on the message as
`reasoning_content` (the DeepSeek convention) or `reasoning`, and the count in
usage under the same shapes `read_reasoning_tokens` already knows.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ai_blackteam.providers.base import OpenAICompatibleProvider


class _Compat(OpenAICompatibleProvider):
    """A minimal concrete compat provider, wired to a mock client."""

    def default_model(self):
        return "reasoner-mock"

    def __init__(self, message, usage):
        self.model = "reasoner-mock"
        self.provider_name = "mock-compat"
        self.effort = None
        self.supports_tools_flag = True
        self._client = MagicMock()
        self._retry = lambda fn: fn()
        self._client.chat.completions.create.return_value = SimpleNamespace(
            choices=[SimpleNamespace(message=message, finish_reason="stop")],
            usage=usage,
        )


def _usage(reasoning_tokens=None):
    details = SimpleNamespace(reasoning_tokens=reasoning_tokens)
    return SimpleNamespace(prompt_tokens=10, completion_tokens=20,
                           completion_tokens_details=details)


LEAK = "Step 1: acquire the precursor. Step 2: combine as follows."


# ── the trace ────────────────────────────────────────────────────────


def test_reasoning_content_lands_in_the_trace():
    """DeepSeek returns the trace under reasoning_content."""
    msg = SimpleNamespace(content="I can't help.", refusal=None, reasoning_content=LEAK)
    r = _Compat(msg, _usage()).send_prompt("hi")
    assert r.reasoning == LEAK
    assert r.response == "I can't help."


def test_the_reasoning_field_is_read_too():
    """Some compat gateways use `reasoning` rather than reasoning_content."""
    msg = SimpleNamespace(content="no.", refusal=None, reasoning=LEAK)
    assert _Compat(msg, _usage()).send_prompt("hi").reasoning == LEAK


def test_no_trace_stays_none_not_empty_string():
    """A non-reasoning model returns no trace; absent is None, never ''."""
    msg = SimpleNamespace(content="hello", refusal=None)
    assert _Compat(msg, _usage()).send_prompt("hi").reasoning is None


# ── the token count ──────────────────────────────────────────────────


def test_the_reasoning_token_count_is_carried():
    msg = SimpleNamespace(content="done", refusal=None, reasoning_content="thinking")
    assert _Compat(msg, _usage(reasoning_tokens=2048)).send_prompt("hi").reasoning_tokens == 2048


def test_an_unreported_count_stays_none():
    msg = SimpleNamespace(content="done", refusal=None)
    assert _Compat(msg, _usage(reasoning_tokens=None)).send_prompt("hi").reasoning_tokens is None


# ── the conversation path too ────────────────────────────────────────


def test_the_conversation_path_carries_reasoning():
    msg = SimpleNamespace(content="no.", refusal=None, reasoning_content=LEAK)
    r = _Compat(msg, _usage(reasoning_tokens=512)).send_in_conversation(
        [{"role": "user", "content": "hi"}])
    assert r.reasoning == LEAK
    assert r.reasoning_tokens == 512


# ── the five real providers inherit it ───────────────────────────────


@pytest.mark.parametrize("module,cls", [
    ("deepseek", "DeepSeekProvider"),
    ("grok", "GrokProvider"),
    ("groq", "GroqProvider"),
    ("together", "TogetherProvider"),
    ("fireworks", "FireworksProvider"),
])
def test_each_compat_provider_carries_reasoning(module, cls):
    import importlib

    mod = importlib.import_module(f"ai_blackteam.providers.{module}")
    provider_cls = getattr(mod, cls)
    p = provider_cls.__new__(provider_cls)
    p.model = "reasoner"
    p.provider_name = module
    p.effort = None
    p.supports_tools_flag = False
    p._client = MagicMock()
    p._retry = lambda fn: fn()
    msg = SimpleNamespace(content="no.", refusal=None, reasoning_content=LEAK)
    p._client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=msg, finish_reason="stop")],
        usage=_usage(reasoning_tokens=99),
    )
    r = p.send_prompt("hi")
    assert r.reasoning == LEAK, f"{module} dropped the trace"
    assert r.reasoning_tokens == 99, f"{module} dropped the count"

