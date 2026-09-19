"""Reasoning effort as a red-team dimension.

Every current frontier model reasons before answering, and how much it reasons
is now a request parameter. That matters here for a specific reason: effort
governs all output tokens including thinking, so the same attack can land
differently at `low` than at `max`. A harness that cannot set it can only ever
test one point on that curve, and silently at that, since the vendor default
is `high`.

The vendor shapes differ and are not interchangeable. Anthropic takes
`output_config.effort`; the OpenAI-compatible APIs take `reasoning_effort`.
Sending the wrong one, or sending either to a model that does not accept it, is
a 400 rather than a graceful degradation, so the wiring is worth pinning.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ai_blackteam.providers.anthropic import AnthropicProvider
from ai_blackteam.providers.deepseek import DeepSeekProvider


def _anthropic(**kw):
    p = AnthropicProvider(api_key="sk-test", **kw)
    p._client = MagicMock()
    p._client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(text="ok")],
        usage=SimpleNamespace(input_tokens=1, output_tokens=1),
        stop_reason="end_turn",
    )
    return p


def _openai_compatible(**kw):
    p = DeepSeekProvider(api_key="k", **kw)
    p._client = MagicMock()
    p._client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(
            message=SimpleNamespace(content="ok", tool_calls=None), finish_reason="stop")],
        usage=SimpleNamespace(prompt_tokens=1, completion_tokens=1),
    )
    return p


# ── Anthropic: output_config.effort ──────────────────────────────────


def test_effort_is_sent_as_output_config():
    p = _anthropic(model="claude-opus-5", effort="low")
    p.send_prompt("q")
    kwargs = p._client.messages.create.call_args.kwargs
    assert kwargs["output_config"] == {"effort": "low"}


def test_no_effort_means_no_parameter_at_all():
    """Omitting it is not the same as sending high on every model."""
    p = _anthropic(model="claude-opus-5")
    p.send_prompt("q")
    assert "output_config" not in p._client.messages.create.call_args.kwargs


def test_effort_applies_to_conversations_and_tool_use_too():
    p = _anthropic(model="claude-opus-5", effort="max")
    p.send_in_conversation([{"role": "user", "content": "q"}])
    assert p._client.messages.create.call_args.kwargs["output_config"] == {"effort": "max"}

    p2 = _anthropic(model="claude-opus-5", effort="max")
    p2._client.messages.create.return_value = SimpleNamespace(
        content=[], usage=SimpleNamespace(input_tokens=1, output_tokens=1), stop_reason="end_turn")
    p2.send_with_tools([{"role": "user", "content": "q"}], [])
    assert p2._client.messages.create.call_args.kwargs["output_config"] == {"effort": "max"}


@pytest.mark.parametrize("level", ["low", "medium", "high", "xhigh", "max"])
def test_every_documented_level_is_accepted(level):
    p = _anthropic(model="claude-opus-5", effort=level)
    p.send_prompt("q")
    assert p._client.messages.create.call_args.kwargs["output_config"] == {"effort": level}


def test_adaptive_is_rejected_as_an_effort_level():
    """`adaptive` is a thinking mode, not an effort level.

    The docs call this out explicitly, and it is an easy confusion because both
    are ways of talking about how much the model thinks.
    """
    with pytest.raises(ValueError, match="adaptive"):
        AnthropicProvider(api_key="sk-test", model="claude-opus-5", effort="adaptive")


def test_an_invented_level_is_rejected_before_the_request():
    with pytest.raises(ValueError, match="turbo"):
        AnthropicProvider(api_key="sk-test", model="claude-opus-5", effort="turbo")


def test_effort_on_a_model_that_does_not_support_it_fails_loudly():
    """Haiku 4.5 is absent from the supported list; the API answers 400.

    Failing at construction turns a mid-sweep API error into an immediate,
    readable one.
    """
    with pytest.raises(ValueError, match="haiku"):
        AnthropicProvider(api_key="sk-test", model="claude-haiku-4-5", effort="low")


def test_an_unknown_model_is_allowed_through():
    """The supported list will go stale; a new model must not be pre-blocked.

    Being wrong in this direction costs one clear API error. Being wrong the
    other way makes the tool refuse to test a model that works.
    """
    p = _anthropic(model="claude-some-future-model", effort="low")
    p.send_prompt("q")
    assert p._client.messages.create.call_args.kwargs["output_config"] == {"effort": "low"}


# ── OpenAI-compatible: reasoning_effort ──────────────────────────────


def test_openai_compatible_uses_reasoning_effort_not_output_config():
    p = _openai_compatible(effort="medium")
    p.send_prompt("q")
    kwargs = p._client.chat.completions.create.call_args.kwargs
    assert kwargs["reasoning_effort"] == "medium"
    assert "output_config" not in kwargs, "that is the Anthropic shape"


def test_openai_compatible_omits_the_parameter_when_unset():
    p = _openai_compatible()
    p.send_prompt("q")
    assert "reasoning_effort" not in p._client.chat.completions.create.call_args.kwargs
