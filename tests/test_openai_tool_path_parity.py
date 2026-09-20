"""The two OpenAI tool paths must agree about what they observed.

`_respond_with_tools` (Responses) was built carefully: it parses a structured
refusal, sets stop_reason, and keeps the reasoning trace. Its sibling
`_chat_with_tools` (chat.completions, the default) reads `msg.content`
directly and passes no stop_reason at all.

Two consequences on the path almost every run takes. A structured refusal
comes back as `response=None` with `refused` permanently None, so the vendor
saying no outright is indistinguishable from the vendor saying nothing. And a
tool call whose arguments were truncated because the output budget ran out
raises JSONDecodeError out of the provider, which the engine records as a
whole-run ERROR, discarding the tool calls and the reasoning that did arrive
intact in the same payload.

Truncation is not an edge case here: OTora exists to exhaust the output
budget, so the run that most needs its partial evidence kept is the one that
throws it away.
"""

import json
from types import SimpleNamespace
from unittest.mock import MagicMock, patch


def _provider(use_responses=False):
    from ai_blackteam.providers.openai import OpenAIProvider

    with patch("ai_blackteam.providers.openai.OpenAI"):
        p = OpenAIProvider(api_key="test-not-real", model="gpt-test",
                           use_responses=use_responses)
    p._client = MagicMock()
    return p


def _chat_response(message, usage=None):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=message, finish_reason="stop")],
        usage=usage or SimpleNamespace(prompt_tokens=1, completion_tokens=1,
                                       completion_tokens_details=None),
    )


TOOLS = [{"name": "lookup", "description": "d",
          "input_schema": {"type": "object", "properties": {}}}]


# ── a structured refusal must be observable on both paths ────────────


def test_the_chat_tool_path_surfaces_a_structured_refusal():
    p = _provider()
    msg = SimpleNamespace(content=None, refusal="I can't help with that.",
                          tool_calls=None)
    p._client.chat.completions.create.return_value = _chat_response(msg)

    result = p.send_with_tools([{"role": "user", "content": "hi"}], TOOLS)
    assert result.response == "I can't help with that."
    assert result.stop_reason == "refusal"
    assert result.refused is True


def test_a_normal_chat_tool_reply_is_not_marked_refused():
    p = _provider()
    msg = SimpleNamespace(content="here you go", refusal=None, tool_calls=None)
    p._client.chat.completions.create.return_value = _chat_response(msg)

    result = p.send_with_tools([{"role": "user", "content": "hi"}], TOOLS)
    assert result.response == "here you go"
    assert result.refused is not True


# ── truncated tool arguments must not discard the whole run ──────────


def _truncated_tool_call():
    return SimpleNamespace(
        id="call_1",
        function=SimpleNamespace(name="lookup", arguments='{"q": "partia'),
    )


def test_truncated_tool_arguments_do_not_raise():
    """The budget ran out mid-call; the rest of the payload is still evidence."""
    p = _provider()
    msg = SimpleNamespace(content="partial answer", refusal=None,
                          tool_calls=[_truncated_tool_call()])
    p._client.chat.completions.create.return_value = _chat_response(msg)

    result = p.send_with_tools([{"role": "user", "content": "hi"}], TOOLS)
    assert result.response == "partial answer"


def test_a_truncated_call_is_kept_and_marked_rather_than_dropped():
    p = _provider()
    msg = SimpleNamespace(content=None, refusal=None,
                          tool_calls=[_truncated_tool_call()])
    p._client.chat.completions.create.return_value = _chat_response(msg)

    result = p.send_with_tools([{"role": "user", "content": "hi"}], TOOLS)
    assert len(result.tool_calls) == 1
    call = result.tool_calls[0]
    assert call["tool"] == "lookup"
    assert call.get("input_parse_error"), (
        "an unparsable argument blob must be flagged, not silently read as {}"
    )
    assert call["input"] == {}, "unknown arguments are empty, never invented"


def test_well_formed_tool_arguments_are_still_parsed():
    p = _provider()
    good = SimpleNamespace(id="c", function=SimpleNamespace(
        name="lookup", arguments=json.dumps({"q": "hello"})))
    msg = SimpleNamespace(content=None, refusal=None, tool_calls=[good])
    p._client.chat.completions.create.return_value = _chat_response(msg)

    call = p.send_with_tools([{"role": "user", "content": "hi"}], TOOLS).tool_calls[0]
    assert call["input"] == {"q": "hello"}
    assert not call.get("input_parse_error")


def test_null_arguments_do_not_raise():
    p = _provider()
    bad = SimpleNamespace(id="c", function=SimpleNamespace(name="lookup", arguments=None))
    msg = SimpleNamespace(content=None, refusal=None, tool_calls=[bad])
    p._client.chat.completions.create.return_value = _chat_response(msg)

    call = p.send_with_tools([{"role": "user", "content": "hi"}], TOOLS).tool_calls[0]
    assert call["input"] == {}
    assert call.get("input_parse_error")
