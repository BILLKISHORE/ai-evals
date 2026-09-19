"""Vendor termination signals carried through to the result objects.

The evaluator infers refusal by pattern-matching response text. Several vendors
report it directly: Anthropic returns stop_reason "refusal" with a
stop_details policy category, as a normal HTTP 200, and OpenAI-compatible APIs
return finish_reason "content_filter". That is ground truth, and the harness
was discarding it.

`refused` is deliberately tri-state. False means the vendor said it did not
refuse; None means the vendor said nothing, so text inference stays the
fallback rather than being silently overridden by a missing field.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from ai_blackteam.providers.base import PromptResult, ToolResult


# ── the dataclass contract ───────────────────────────────────────────


def test_prompt_result_defaults_to_unknown_not_false():
    r = PromptResult(response="hi", model="m", provider="p")
    assert r.stop_reason is None
    assert r.stop_details is None
    assert r.refused is None, "absence of a signal is unknown, not 'did not refuse'"


def test_tool_result_carries_the_same_signal():
    r = ToolResult(response=None, model="m", provider="p")
    assert r.stop_reason is None
    assert r.refused is None


def test_anthropic_refusal_is_recognised():
    r = PromptResult(
        response="", model="m", provider="anthropic",
        stop_reason="refusal", stop_details={"policy_category": "violence"},
    )
    assert r.refused is True
    assert r.stop_details["policy_category"] == "violence"


def test_openai_content_filter_is_recognised():
    r = PromptResult(response="", model="m", provider="openai", stop_reason="content_filter")
    assert r.refused is True


def test_normal_completion_is_an_explicit_non_refusal():
    for reason in ("end_turn", "stop", "max_tokens", "length", "tool_use"):
        r = PromptResult(response="x", model="m", provider="p", stop_reason=reason)
        assert r.refused is False, f"{reason} should read as a non-refusal"


def test_unrecognised_stop_reason_is_unknown():
    """A new vendor value must not be silently read as 'did not refuse'."""
    r = PromptResult(response="x", model="m", provider="p", stop_reason="some_future_value")
    assert r.refused is None


# ── providers populate it ────────────────────────────────────────────


def test_anthropic_provider_captures_stop_reason_and_details():
    from ai_blackteam.providers.anthropic import AnthropicProvider

    p = AnthropicProvider(api_key="sk-test")
    block = SimpleNamespace(text="nope")
    p._client = MagicMock()
    p._client.messages.create.return_value = SimpleNamespace(
        content=[block],
        usage=SimpleNamespace(input_tokens=1, output_tokens=2),
        stop_reason="refusal",
        stop_details={"policy_category": "weapons"},
    )
    r = p.send_prompt("q")
    assert r.stop_reason == "refusal"
    assert r.stop_details == {"policy_category": "weapons"}
    assert r.refused is True


def test_anthropic_provider_tolerates_an_sdk_without_stop_details():
    """stop_details does not exist on older anthropic SDKs."""
    from ai_blackteam.providers.anthropic import AnthropicProvider

    p = AnthropicProvider(api_key="sk-test")
    p._client = MagicMock()
    p._client.messages.create.return_value = SimpleNamespace(
        content=[SimpleNamespace(text="ok")],
        usage=SimpleNamespace(input_tokens=1, output_tokens=2),
        stop_reason="end_turn",
    )
    r = p.send_prompt("q")
    assert r.stop_reason == "end_turn"
    assert r.stop_details is None
    assert r.refused is False


def test_openai_compatible_provider_captures_finish_reason():
    from ai_blackteam.providers.deepseek import DeepSeekProvider

    p = DeepSeekProvider(api_key="k")
    p._client = MagicMock()
    p._client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(
            message=SimpleNamespace(content="", tool_calls=None),
            finish_reason="content_filter",
        )],
        usage=SimpleNamespace(prompt_tokens=1, completion_tokens=0),
    )
    r = p.send_prompt("q")
    assert r.stop_reason == "content_filter"
    assert r.refused is True
