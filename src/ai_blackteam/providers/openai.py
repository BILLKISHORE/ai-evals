"""OpenAI requests over two endpoints, because one of them cannot carry thinking.

This provider used chat.completions for everything. That endpoint returns a
single message, and for a reasoning model the thinking is not in it: the
reasoning summary and the reasoning token accounting are exposed only through
the Responses API. Every OpenAI result therefore came back with
``reasoning=None``, which is indistinguishable from a model that did not think,
and the reasoning-layer attacks that turn on what a model reasons while it
decides which tool to call had nothing to score at all.

Switching wholesale would have been the wrong fix, since chat.completions is
what every existing run used. It stays the default and the reasoning path is
opt-in. The cost of two paths is the translation between two payload shapes,
which is where the mistakes live: Responses returns a flat list of output items
rather than one message, and reports termination as a status rather than a
finish_reason.
"""

import json
import os
import time

from openai import OpenAI
from openai import __version__ as openai_sdk_version

from ai_blackteam.reasoning import validate_effort
from ai_blackteam.registry import register_provider
from ai_blackteam.providers.base import read_reasoning_tokens, BaseProvider, PromptResult, ToolResult
from ai_blackteam.providers.base import read_openai_message
from ai_blackteam.retry import retry_with_backoff

OPENAI_VENDOR = "the OpenAI API"

# What the chat path has always sent. Left alone so no existing run shifts.
CHAT_MAX_TOKENS = 4096

# Reasoning tokens are billed against the same output budget as the answer, so
# a 4096 cap can be spent entirely on thinking and return "incomplete" with no
# text at all. Empty text scores as UNCLEAR, which counts as half a bypass, so
# the reasoning path gets room for both.
RESPONSES_MAX_OUTPUT_TOKENS = 32768

# Asking for the summary is what makes the trace come back. Without it the
# reasoning item still arrives, with an empty summary.
REASONING_SUMMARY = "auto"

# The SDK release that introduced client.responses.
RESPONSES_MIN_SDK_VERSION = "1.66.0"

# The Responses API reports termination as a status plus an incomplete reason,
# not the finish_reason vocabulary the rest of the harness reads. These are
# translations, not inventions: a reason that is not listed here stays unknown,
# so a new vendor value cannot quietly read as "the model did not refuse".
RESPONSES_INCOMPLETE_REASONS = {
    "max_output_tokens": "length",
    "content_filter": "content_filter",
}

# The trace was sealed by the vendor. What the model thought is unavailable,
# but that it thought is still signal, so it is recorded rather than dropped.
SEALED_REASONING = "[encrypted reasoning]"


def _require_responses_api(client):
    """Refuse the reasoning path on an SDK that has no such endpoint.

    Falling back to chat.completions would return reasoning=None, which is
    exactly what a model that chose not to think returns. The caller would have
    no way to tell that the trace was never available in the first place.
    """
    if hasattr(client, "responses"):
        return
    raise RuntimeError(
        "this openai SDK has no Responses API, so a reasoning trace cannot be "
        f"requested. Reasoning with tool calls needs openai>={RESPONSES_MIN_SDK_VERSION} "
        f"and the installed version is {openai_sdk_version}. Drop use_responses to stay "
        "on chat.completions, which carries no reasoning trace."
    )


def _summary_text(item):
    """The visible parts of one reasoning item."""
    parts = [getattr(p, "text", "") or "" for p in (getattr(item, "summary", None) or [])]
    visible = [p for p in parts if p]
    if visible:
        return visible
    if getattr(item, "encrypted_content", None):
        return [SEALED_REASONING]
    return []


def _message_text(item):
    """(text, refused) for one output message.

    A refusal arrives as its own content part with the words in ``refusal``, so
    reading only output_text returns an empty string and throws away both the
    refusal text and the fact that it was one.
    """
    text, refused = [], None
    for part in getattr(item, "content", None) or []:
        ptype = getattr(part, "type", None)
        if ptype == "output_text":
            text.append(getattr(part, "text", "") or "")
        elif ptype == "refusal":
            text.append(getattr(part, "refusal", "") or "")
            refused = True
    return "".join(text), refused



def _parse_tool_arguments(raw):
    """A tool call's arguments, and whether they could be read.

    Returns (arguments, error). The vendor sends arguments as a JSON string,
    and it can be truncated mid-token when the output budget runs out, which
    is precisely what a reasoning denial-of-service provokes. Letting
    json.loads raise here discards the whole payload, including the tool
    calls and the reasoning that arrived intact beside it, and the engine
    records the run as ERROR.

    An unreadable blob yields {} plus an error string rather than invented
    arguments, so a caller can tell "no arguments" from "unreadable
    arguments" instead of both looking like an empty call.
    """
    if raw is None:
        return {}, "no arguments returned"
    if isinstance(raw, dict):
        return raw, None
    try:
        parsed = json.loads(raw)
    except (TypeError, ValueError) as exc:
        return {}, f"unparsable arguments: {exc}"
    if not isinstance(parsed, dict):
        return {}, f"arguments were {type(parsed).__name__}, expected object"
    return parsed, None


def _tool_call_entry(call_id, name, raw_arguments):
    """One tool call in the harness's shape, truncation-safe."""
    arguments, error = _parse_tool_arguments(raw_arguments)
    entry = {"id": call_id, "tool": name, "input": arguments}
    if error:
        entry["input_parse_error"] = error
    return entry


def _tool_call(item):
    """One function call in the harness's shape.

    call_id is what a tool result is submitted against; id names the output
    item. Prefer the one the caller would need to reply with.
    """
    return _tool_call_entry(
        getattr(item, "call_id", None) or getattr(item, "id", None),
        getattr(item, "name", None),
        getattr(item, "arguments", None),
    )


def _parse_responses_output(items):
    """Split a Responses payload into (answer, reasoning, tool_calls, refused).

    The payload is a flat list: reasoning summaries, messages and function
    calls sit side by side in whatever order the model produced them. Reading
    item zero picks up the thinking rather than the answer on every reasoning
    model, which is the same defect the Anthropic path had with content[0].

    refused is tri-state. None means the payload said nothing either way.
    """
    answer, thoughts, calls = [], [], []
    refused = None
    for item in items or []:
        itype = getattr(item, "type", None)
        if itype == "reasoning":
            thoughts.extend(_summary_text(item))
        elif itype == "message":
            text, message_refused = _message_text(item)
            answer.append(text)
            if message_refused:
                refused = True
        elif itype == "function_call":
            calls.append(_tool_call(item))
    return "".join(answer), "\n".join(thoughts) or None, calls, refused


def _responses_stop_reason(response, refused, has_tool_calls):
    """Translate a Responses status into the harness's stop_reason vocabulary.

    An untranslated status returns None rather than a guess. None reads as "the
    vendor said nothing usable", which is the honest answer and keeps a new
    status from being scored as a clean, non-refusing completion.
    """
    if refused:
        return "refusal"
    status = getattr(response, "status", None)
    if status == "incomplete":
        details = getattr(response, "incomplete_details", None)
        return RESPONSES_INCOMPLETE_REASONS.get(getattr(details, "reason", None))
    if status == "completed":
        return "tool_calls" if has_tool_calls else "stop"
    return None


def _responses_tokens(usage):
    """(input, output) from a Responses usage block, or (None, None).

    Responses names these input_tokens and output_tokens. Reading the
    chat.completions names off it yields None for both, which would report a
    request that apparently cost nothing.
    """
    if usage is None:
        return None, None
    return getattr(usage, "input_tokens", None), getattr(usage, "output_tokens", None)


@register_provider("openai")
class OpenAIProvider(BaseProvider):
    def __init__(self, model=None, api_key=None, user_id=None, base_url=None,
                 effort=None, use_responses=False):
        super().__init__(model, api_key)
        self.effort = validate_effort(effort, model=self.model, vendor=OPENAI_VENDOR)
        # chat.completions stays the default. Reasoning is what the other
        # endpoint buys, and it costs a second payload shape to parse.
        self.use_responses = bool(use_responses)
        client_kwargs = {}
        if self.api_key:
            client_kwargs["api_key"] = self.api_key
        resolved_base_url = base_url or os.environ.get("OPENAI_BASE_URL")
        if resolved_base_url:
            client_kwargs["base_url"] = resolved_base_url
        self._client = OpenAI(**client_kwargs)
        self._user_id = user_id or "ai_blackteam-safety-eval"
        if self.use_responses:
            _require_responses_api(self._client)

    def default_model(self):
        return "gpt-5.5"

    def supports_tools(self):
        return True

    def send_prompt(self, prompt, system_prompt=None):
        return self._send([{"role": "user", "content": prompt}], system_prompt)

    def send_in_conversation(self, messages, system_prompt=None):
        return self._send(list(messages), system_prompt)

    def send_with_tools(self, messages, tools, system_prompt=None):
        if self.use_responses:
            return self._respond_with_tools(list(messages), tools, system_prompt)
        return self._chat_with_tools(list(messages), tools, system_prompt)

    def _send(self, messages, system_prompt):
        if self.use_responses:
            return self._respond(messages, system_prompt)
        return self._chat(messages, system_prompt)

    # ── chat.completions, the default path ───────────────────────────

    def _chat_kwargs(self, messages, system_prompt):
        msgs = list(messages)
        if system_prompt:
            msgs = [{"role": "system", "content": system_prompt}] + msgs
        kwargs = {"model": self.model, "messages": msgs,
                  "max_completion_tokens": CHAT_MAX_TOKENS, "user": self._user_id}
        if self.effort:
            kwargs["reasoning_effort"] = self.effort
        return kwargs

    def _chat(self, messages, system_prompt):
        kwargs = self._chat_kwargs(messages, system_prompt)
        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat.completions.create(**kwargs))
        ms = (time.time() - start) * 1000

        choice = r.choices[0]
        text, refused = read_openai_message(choice.message)
        return PromptResult(
            response=text,
            model=self.model, provider="openai",
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            reasoning_tokens=read_reasoning_tokens(r.usage),
            latency_ms=ms,
            # A structured refusal is the vendor saying so outright, which
            # is stronger than whatever finish_reason carries.
            stop_reason="refusal" if refused else getattr(choice, "finish_reason", None),
        )

    def _chat_with_tools(self, messages, tools, system_prompt):
        oai_tools = [{"type": "function", "function": {"name": t["name"], "description": t.get("description", ""), "parameters": t["input_schema"]}} for t in tools]
        kwargs = self._chat_kwargs(messages, system_prompt)
        kwargs["tools"] = oai_tools

        start = time.time()
        r = retry_with_backoff(lambda: self._client.chat.completions.create(**kwargs))
        ms = (time.time() - start) * 1000

        choice = r.choices[0]
        msg = choice.message
        # Was reading msg.content directly, so a structured refusal came back
        # as None with no stop_reason and refused stuck at None forever. The
        # Responses sibling has always parsed it; the two paths now agree.
        text, refused = read_openai_message(msg)
        calls = []
        if msg.tool_calls:
            for tc in msg.tool_calls:
                calls.append(_tool_call_entry(
                    tc.id, tc.function.name, getattr(tc.function, "arguments", None)))

        return ToolResult(response=text, tool_calls=calls, model=self.model, provider="openai",
                          tokens_in=r.usage.prompt_tokens if r.usage else None,
                          tokens_out=r.usage.completion_tokens if r.usage else None,
                          reasoning_tokens=read_reasoning_tokens(r.usage), latency_ms=ms,
                          stop_reason="refusal" if refused
                          else getattr(choice, "finish_reason", None))

    # ── the Responses API, opt-in, the only path that carries thinking ─

    def _reasoning_param(self):
        """Ask for the summary always; name an effort only if one was given.

        Omitting the effort leaves the model's own default, which is not the
        same as any level this harness could name for it.
        """
        param = {"summary": REASONING_SUMMARY}
        if self.effort:
            param["effort"] = self.effort
        return param

    def _responses_kwargs(self, messages, system_prompt, tools=None):
        kwargs = {"model": self.model, "input": list(messages),
                  "max_output_tokens": RESPONSES_MAX_OUTPUT_TOKENS,
                  "user": self._user_id, "reasoning": self._reasoning_param()}
        if system_prompt:
            # Responses carries the system prompt beside the input rather than
            # as a message inside it.
            kwargs["instructions"] = system_prompt
        if tools is not None:
            kwargs["tools"] = tools
        return kwargs

    def _responses_call(self, messages, system_prompt, tools=None):
        """One round trip. Returns (response, parsed, latency_ms)."""
        kwargs = self._responses_kwargs(messages, system_prompt, tools)
        start = time.time()
        r = retry_with_backoff(lambda: self._client.responses.create(**kwargs))
        ms = (time.time() - start) * 1000
        return r, _parse_responses_output(getattr(r, "output", None)), ms

    def _respond(self, messages, system_prompt):
        r, (text, reasoning, calls, refused), ms = self._responses_call(messages, system_prompt)
        tokens_in, tokens_out = _responses_tokens(getattr(r, "usage", None))
        return PromptResult(
            response=text,
            model=self.model, provider="openai",
            tokens_in=tokens_in, tokens_out=tokens_out,
            reasoning=reasoning,
            reasoning_tokens=read_reasoning_tokens(getattr(r, "usage", None)),
            latency_ms=ms,
            stop_reason=_responses_stop_reason(r, refused, bool(calls)),
        )

    def _respond_with_tools(self, messages, tools, system_prompt):
        # Responses puts the function's name and schema beside the type; the
        # nested chat.completions shape is rejected.
        responses_tools = [{"type": "function", "name": t["name"],
                            "description": t.get("description", ""),
                            "parameters": t["input_schema"], "strict": False}
                           for t in tools]
        r, (text, reasoning, calls, refused), ms = self._responses_call(
            messages, system_prompt, responses_tools)
        tokens_in, tokens_out = _responses_tokens(getattr(r, "usage", None))
        return ToolResult(
            response=text or None,
            tool_calls=calls,
            model=self.model, provider="openai",
            tokens_in=tokens_in, tokens_out=tokens_out,
            reasoning=reasoning,
            reasoning_tokens=read_reasoning_tokens(getattr(r, "usage", None)),
            latency_ms=ms,
            stop_reason=_responses_stop_reason(r, refused, bool(calls)),
        )
