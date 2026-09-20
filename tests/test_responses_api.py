"""A reasoning trace and a tool call cannot both arrive over chat.completions.

`openai.py` used chat.completions everywhere. That endpoint returns one
message, and for a reasoning model the thinking is not in it: the reasoning
summary and the reasoning token accounting are only exposed through the
Responses API. So every OpenAI result came back with `reasoning=None`, which is
indistinguishable from a model that did not think, and the agentic attacks that
turn on what a model reasons while it decides which tool to call had nothing to
score.

Switching wholesale would have been the wrong fix. chat.completions is what
every existing run used, so it stays the default and the Responses path is
opt-in. The two return different payload shapes and the translation between
them is where the mistakes live: Responses returns a flat list of output items,
so reading item zero picks up the thinking rather than the answer, and it
reports termination as a status rather than a finish_reason, so a status nobody
translated would read as "did not refuse".
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from ai_blackteam.providers.openai import OpenAIProvider

TOOLS = [{"name": "lookup", "description": "look something up",
          "input_schema": {"type": "object", "properties": {}}}]


def reasoning_item(*summaries, encrypted=None):
    return SimpleNamespace(
        type="reasoning",
        summary=[SimpleNamespace(type="summary_text", text=s) for s in summaries],
        encrypted_content=encrypted,
    )


def message_item(text=None, refusal=None):
    content = []
    if text is not None:
        content.append(SimpleNamespace(type="output_text", text=text))
    if refusal is not None:
        content.append(SimpleNamespace(type="refusal", refusal=refusal))
    return SimpleNamespace(type="message", content=content)


def call_item(name="lookup", arguments='{"q": "x"}', call_id="call_1"):
    return SimpleNamespace(type="function_call", name=name, arguments=arguments,
                           call_id=call_id, id="fc_1", status="completed")


def response(*items, status="completed", reasoning_tokens=64, incomplete_reason=None):
    details = SimpleNamespace(reason=incomplete_reason) if incomplete_reason else None
    return SimpleNamespace(
        output=list(items),
        status=status,
        incomplete_details=details,
        usage=SimpleNamespace(
            input_tokens=11, output_tokens=22,
            output_tokens_details=SimpleNamespace(reasoning_tokens=reasoning_tokens),
        ),
    )


def wired(payload, **kw):
    """A provider on the Responses path with its SDK client replaced."""
    p = OpenAIProvider(api_key="test-not-real", use_responses=True, **kw)
    p._client = MagicMock()
    p._client.responses.create.return_value = payload
    return p


def chat_wired(**kw):
    p = OpenAIProvider(api_key="test-not-real", **kw)
    p._client = MagicMock()
    p._client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(
            message=SimpleNamespace(content="ok", refusal=None, tool_calls=None),
            finish_reason="stop")],
        usage=SimpleNamespace(prompt_tokens=1, completion_tokens=1),
    )
    return p


def sent(p):
    return p._client.responses.create.call_args.kwargs


# ── chat.completions stays the default ───────────────────────────────


def test_chat_completions_is_still_the_default_path():
    """Every existing run used it; opting in is what changes the endpoint."""
    p = chat_wired()
    p.send_prompt("q")
    assert p._client.chat.completions.create.called
    assert not p._client.responses.create.called


def test_the_responses_path_is_taken_only_when_it_was_asked_for():
    p = wired(response(message_item(text="ok")))
    p.send_prompt("q")
    assert p._client.responses.create.called
    assert not p._client.chat.completions.create.called


def test_the_default_path_still_carries_the_effort_in_the_chat_shape():
    p = chat_wired(effort="medium")
    p.send_prompt("q")
    kwargs = p._client.chat.completions.create.call_args.kwargs
    assert kwargs["reasoning_effort"] == "medium"


def test_the_default_path_omits_the_effort_when_none_was_asked_for():
    p = chat_wired()
    p.send_prompt("q")
    assert "reasoning_effort" not in p._client.chat.completions.create.call_args.kwargs


# ── the trace lands in the result ────────────────────────────────────


def test_the_reasoning_summary_lands_in_the_reasoning_field():
    p = wired(response(reasoning_item("Weighing the request."), message_item(text="The answer.")))
    assert p.send_prompt("q").reasoning == "Weighing the request."


def test_the_answer_is_read_past_a_leading_reasoning_item():
    """Item zero is the thinking, so taking the first item loses the answer."""
    p = wired(response(reasoning_item("Thinking."), message_item(text="The answer.")))
    assert p.send_prompt("q").response == "The answer."


def test_several_summary_parts_are_joined_rather_than_truncated():
    p = wired(response(reasoning_item("Part one.", "Part two."), message_item(text="a")))
    trace = p.send_prompt("q").reasoning
    assert "Part one." in trace and "Part two." in trace


def test_a_response_with_no_reasoning_reports_none_not_an_empty_string():
    """Empty would say the model thought and said nothing. It did not think."""
    p = wired(response(message_item(text="The answer.")))
    assert p.send_prompt("q").reasoning is None


def test_a_sealed_trace_is_recorded_rather_than_dropped():
    """The content is encrypted, but that the model thought is still signal."""
    p = wired(response(reasoning_item(encrypted="hidden"), message_item(text="a")))
    assert p.send_prompt("q").reasoning


def test_the_reasoning_token_count_is_read_from_the_responses_usage():
    p = wired(response(reasoning_item("t"), message_item(text="a"), reasoning_tokens=512))
    assert p.send_prompt("q").reasoning_tokens == 512


def test_an_unreported_reasoning_token_count_stays_unknown():
    """Unknown is not zero, and zero would read as a free request."""
    payload = response(message_item(text="a"))
    payload.usage.output_tokens_details = None
    assert wired(payload).send_prompt("q").reasoning_tokens is None


def test_the_responses_token_counts_are_read_from_their_own_field_names():
    """Responses says input_tokens, not prompt_tokens; the wrong name is None."""
    r = wired(response(message_item(text="a"))).send_prompt("q")
    assert (r.tokens_in, r.tokens_out) == (11, 22)


def test_conversations_take_the_responses_path_too():
    p = wired(response(reasoning_item("t"), message_item(text="a")))
    assert p.send_in_conversation([{"role": "user", "content": "q"}]).reasoning == "t"


# ── reasoning alongside tool calls, which is the point ───────────────


def test_a_tool_call_and_a_reasoning_trace_come_back_together():
    p = wired(response(reasoning_item("I should look this up."), call_item()))
    r = p.send_with_tools([{"role": "user", "content": "q"}], TOOLS)
    assert r.tool_calls == [{"id": "call_1", "tool": "lookup", "input": {"q": "x"}}]
    assert r.reasoning == "I should look this up."


def test_a_tool_call_carries_the_reasoning_token_count():
    p = wired(response(reasoning_item("t"), call_item(), reasoning_tokens=77))
    r = p.send_with_tools([{"role": "user", "content": "q"}], TOOLS)
    assert r.reasoning_tokens == 77


def test_tools_are_sent_in_the_flat_responses_shape():
    """Responses puts the name beside the type; the nested chat shape is a 400."""
    p = wired(response(call_item()))
    p.send_with_tools([{"role": "user", "content": "q"}], TOOLS)
    tool = sent(p)["tools"][0]
    assert tool["type"] == "function"
    assert tool["name"] == "lookup"
    assert "function" not in tool, "that is the chat.completions shape"


def test_a_tool_free_request_sends_no_tools_key():
    p = wired(response(message_item(text="a")))
    p.send_prompt("q")
    assert "tools" not in sent(p)


def test_text_alongside_a_tool_call_is_kept():
    p = wired(response(message_item(text="Looking that up."), call_item()))
    r = p.send_with_tools([{"role": "user", "content": "q"}], TOOLS)
    assert r.response == "Looking that up."
    assert r.tool_calls


def test_no_text_alongside_a_tool_call_reads_as_none_not_empty():
    p = wired(response(call_item()))
    assert p.send_with_tools([{"role": "user", "content": "q"}], TOOLS).response is None


# ── what the request carries ─────────────────────────────────────────


def test_the_effort_is_sent_in_the_responses_reasoning_shape():
    p = wired(response(message_item(text="a")), effort="xhigh")
    p.send_prompt("q")
    assert sent(p)["reasoning"]["effort"] == "xhigh"
    assert "reasoning_effort" not in sent(p), "that is the chat.completions shape"


def test_a_summary_is_requested_even_when_no_effort_level_was_given():
    """The trace only comes back if it was asked for, effort or not."""
    p = wired(response(message_item(text="a")))
    p.send_prompt("q")
    assert sent(p)["reasoning"]["summary"]


def test_no_effort_level_means_no_effort_key_in_the_reasoning_block():
    p = wired(response(message_item(text="a")))
    p.send_prompt("q")
    assert "effort" not in sent(p)["reasoning"]


def test_the_system_prompt_becomes_instructions_not_a_message():
    p = wired(response(message_item(text="a")))
    p.send_prompt("q", system_prompt="be careful")
    kwargs = sent(p)
    assert kwargs["instructions"] == "be careful"
    assert all(m["role"] != "system" for m in kwargs["input"])


def test_the_prompt_is_sent_as_the_input():
    p = wired(response(message_item(text="a")))
    p.send_prompt("the question")
    assert sent(p)["input"] == [{"role": "user", "content": "the question"}]


def test_the_output_budget_leaves_room_for_thinking_and_an_answer():
    """Reasoning tokens are billed against the same cap as the answer.

    A cap small enough to be spent entirely on thinking returns no text, and
    empty text scores as UNCLEAR, which counts as half a bypass.
    """
    p = wired(response(message_item(text="a")))
    p.send_prompt("q")
    assert sent(p)["max_output_tokens"] > 4096


def test_the_caller_message_list_is_not_mutated_by_the_system_prompt():
    p = wired(response(message_item(text="a")))
    messages = [{"role": "user", "content": "q"}]
    p.send_in_conversation(messages, system_prompt="be careful")
    assert messages == [{"role": "user", "content": "q"}]


# ── termination signals, translated rather than invented ─────────────


def test_a_completed_answer_reports_that_it_did_not_refuse():
    assert wired(response(message_item(text="a"))).send_prompt("q").refused is False


def test_a_refusal_part_is_kept_as_the_response_text():
    """Reading only output_text returns empty and throws the refusal away."""
    p = wired(response(message_item(refusal="I can't help with that.")))
    assert p.send_prompt("q").response == "I can't help with that."


def test_a_refusal_is_reported_as_a_refusal():
    p = wired(response(message_item(refusal="I can't help with that.")))
    assert p.send_prompt("q").refused is True


def test_a_tool_path_refusal_is_reported_too():
    p = wired(response(reasoning_item("t"), message_item(refusal="No.")))
    r = p.send_with_tools([{"role": "user", "content": "q"}], TOOLS)
    assert r.response == "No."
    assert r.refused is True


def test_running_out_of_output_room_is_not_a_refusal():
    p = wired(response(reasoning_item("t"), status="incomplete",
                       incomplete_reason="max_output_tokens"))
    assert p.send_prompt("q").refused is False


def test_a_content_filter_stop_is_a_refusal():
    p = wired(response(status="incomplete", incomplete_reason="content_filter"))
    assert p.send_prompt("q").refused is True


def test_an_untranslated_status_stays_unknown_rather_than_reading_as_safe():
    """A new vendor status must not silently mean the model did not refuse."""
    p = wired(response(message_item(text="a"), status="some_new_status"))
    assert p.send_prompt("q").refused is None


def test_an_untranslated_incomplete_reason_stays_unknown():
    p = wired(response(status="incomplete", incomplete_reason="some_new_reason"))
    assert p.send_prompt("q").refused is None


# ── an SDK without the endpoint ──────────────────────────────────────


def test_an_sdk_without_the_responses_api_fails_at_construction():
    """Falling back to chat.completions would hand back reasoning=None, which
    reads exactly like a model that chose not to think."""
    without_responses = MagicMock(spec=["chat"])
    with patch("ai_blackteam.providers.openai.OpenAI", return_value=without_responses), \
            pytest.raises(RuntimeError) as excinfo:
        OpenAIProvider(api_key="test-not-real", use_responses=True)
    assert "1.66.0" in str(excinfo.value), "the error has to name the version needed"


def test_such_an_sdk_is_still_fine_on_the_default_path():
    without_responses = MagicMock(spec=["chat"])
    with patch("ai_blackteam.providers.openai.OpenAI", return_value=without_responses):
        p = OpenAIProvider(api_key="test-not-real")
    assert p.use_responses is False


def test_an_invented_effort_level_is_rejected_before_any_client_is_built():
    with pytest.raises(ValueError, match="turbo"):
        OpenAIProvider(api_key="test-not-real", effort="turbo")
