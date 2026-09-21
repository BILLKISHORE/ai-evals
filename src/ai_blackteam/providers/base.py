import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# Vendor termination signals that state a refusal outright. Anthropic returns
# "refusal" as a normal HTTP 200 with a stop_details policy category; the
# OpenAI-compatible APIs use finish_reason "content_filter"; Google's
# generateContent reports safety blocks through finishReason.
REFUSAL_STOP_REASONS = frozenset({
    "refusal",            # Anthropic
    "content_filter",     # OpenAI and OpenAI-compatible
    "SAFETY",             # Google
    "PROHIBITED_CONTENT",
    "BLOCKLIST",
    "SPII",
})

# Signals that state the model terminated for an unrelated reason. Anything
# outside both sets is treated as unknown rather than assumed benign, so a new
# vendor value cannot silently read as "did not refuse".
NON_REFUSAL_STOP_REASONS = frozenset({
    "end_turn", "stop", "stop_sequence", "max_tokens", "length",
    "tool_use", "tool_calls", "function_call", "pause_turn",
    "model_context_window_exceeded", "STOP", "MAX_TOKENS",
})




def read_openai_message(msg):
    """Pull the text out of an OpenAI-style message.

    The message carries both `content` and `refusal`. On a structured refusal
    `content` is None and the text sits in `refusal`, so `content or ""`
    returned an empty response and discarded the refusal. The evaluator then
    scored empty text, which lands on UNCLEAR and counts as half a bypass.

    Returns (text, refused_flag). The flag is None when the message says
    nothing either way, so the caller can fall back to finish_reason.
    """
    content = getattr(msg, "content", None)
    refusal = getattr(msg, "refusal", None)
    if content:
        return content, None
    if refusal:
        return refusal, True
    return "", None


# Vendors report the reasoning/thinking token count in a nested details block
# whose name differs per vendor. Both known shapes are read here so providers
# do not each reimplement the lookup.
_REASONING_DETAIL_ATTRS = ("completion_tokens_details", "output_tokens_details")

# Google reports the count flat on usage_metadata instead of in a nested
# details block, under its own name.
_REASONING_FLAT_ATTRS = ("thoughts_token_count",)



# Reasoning models reached over the OpenAI-compatible API return their trace on
# the message, not in a separate field. DeepSeek uses `reasoning_content`;
# some gateways (OpenRouter and others) use `reasoning`. Both are read so the
# trace is not silently dropped for the five providers on this base.
_OPENAI_REASONING_ATTRS = ("reasoning_content", "reasoning")



# Many open reasoning models (deepseek-r1, QwQ, and others run locally or
# through gateways that do not split the fields) emit the trace inline, wrapped
# in <think>...</think> before the answer, rather than on a separate field.
import re as _re

_THINK_BLOCK = _re.compile(r"^\s*<think>(.*?)</think>\s*", _re.DOTALL | _re.IGNORECASE)


def split_reasoning_tags(text):
    """Split a leading <think>...</think> block off the answer.

    Returns (answer, reasoning). Only a complete, leading block is split: an
    unclosed <think> from a truncated response is left in the answer untouched,
    because discarding the rest of the body to a stray open tag would lose the
    response entirely. No tags means (text, None).
    """
    if not text:
        return text, None
    m = _THINK_BLOCK.match(text)
    if not m:
        return text, None
    reasoning = m.group(1).strip()
    answer = text[m.end():].strip()
    return answer, (reasoning or None)


def read_openai_reasoning(msg):
    """The reasoning trace off an OpenAI-style message, or None.

    None rather than "" when absent: an empty string reads as a model that
    reasoned about nothing, which is a different claim from a non-reasoning
    model that returned no trace at all.
    """
    for attr in _OPENAI_REASONING_ATTRS:
        value = getattr(msg, attr, None)
        if isinstance(value, str) and value.strip():
            return value
    return None


def read_reasoning_tokens(usage):
    """The reasoning token count from a vendor usage object, or None.

    None means the vendor did not report one, which is not the same as zero.
    A model that reasoned for nothing reports 0, and that is kept: collapsing
    the two would make an unreported count look like a free request.
    """
    if usage is None:
        return None
    for attr in _REASONING_FLAT_ATTRS:
        count = getattr(usage, attr, None)
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    for attr in _REASONING_DETAIL_ATTRS:
        details = getattr(usage, attr, None)
        if details is None:
            continue
        count = getattr(details, "reasoning_tokens", None)
        if isinstance(count, bool) or not isinstance(count, int):
            continue
        return count
    return None


def _refused_from(stop_reason):
    """Tri-state: True refused, False did not, None the vendor did not say."""
    if stop_reason in REFUSAL_STOP_REASONS:
        return True
    if stop_reason in NON_REFUSAL_STOP_REASONS:
        return False
    return None


@dataclass
class PromptResult:
    response: str
    model: str
    provider: str
    tokens_in: int | None = None
    tokens_out: int | None = None
    latency_ms: float | None = None
    raw: dict | None = None
    stop_reason: str | None = None
    stop_details: dict | None = None
    # The model's thinking, kept apart from the answer. Reasoning-layer
    # attacks put harmful content here while the final answer stays clean, so
    # discarding it makes those unscoreable.
    reasoning: str | None = None
    # The vendor's reasoning token count. None means it did not report one;
    # 0 means it reported none spent. These are different and stay different.
    reasoning_tokens: int | None = None

    @property
    def refused(self):
        """Whether the vendor itself reported a refusal.

        None means no usable signal, in which case callers should fall back to
        inspecting the response text. Never collapse None to False: the point
        of this field is to distinguish "the vendor said no refusal" from "the
        vendor said nothing".
        """
        return _refused_from(self.stop_reason)


@dataclass
class ToolResult:
    response: str | None
    tool_calls: list[dict] = field(default_factory=list)
    model: str = ""
    provider: str = ""
    tokens_in: int | None = None
    tokens_out: int | None = None
    latency_ms: float | None = None
    raw: dict | None = None
    stop_reason: str | None = None
    stop_details: dict | None = None
    # The model's thinking, kept apart from the answer. Reasoning-layer
    # attacks put harmful content here while the final answer stays clean, so
    # discarding it makes those unscoreable.
    reasoning: str | None = None
    # The vendor's reasoning token count. None means it did not report one;
    # 0 means it reported none spent. These are different and stay different.
    reasoning_tokens: int | None = None

    @property
    def refused(self):
        return _refused_from(self.stop_reason)


class BaseProvider(ABC):
    def __init__(self, model=None, api_key=None):
        self.model = model or self.default_model()
        self.api_key = api_key

    @abstractmethod
    def send_prompt(self, prompt, system_prompt=None) -> PromptResult: ...

    @abstractmethod
    def send_in_conversation(self, messages, system_prompt=None) -> PromptResult: ...

    def send_with_tools(self, messages, tools, system_prompt=None) -> ToolResult:
        raise NotImplementedError(f"{self.__class__.__name__} doesn't support tool use")

    @abstractmethod
    def default_model(self) -> str: ...

    def get_model_info(self):
        return {"model": self.model, "provider": self.__class__.__name__}

    def supports_tools(self):
        return False


class OpenAICompatibleProvider(BaseProvider):
    """Shared implementation for providers exposing an OpenAI-compatible Chat Completions API.

    Subclasses must set `base_url` and `provider_name`, override `default_model()`,
    and optionally set `supports_tools_flag = True` if the upstream API supports
    OpenAI-style tool calling.
    """

    base_url: str = ""
    provider_name: str = ""
    supports_tools_flag: bool = False

    def __init__(self, model=None, api_key=None, effort=None):
        from openai import OpenAI
        from ai_blackteam.reasoning import validate_effort
        from ai_blackteam.retry import retry_with_backoff
        super().__init__(model, api_key)
        # The OpenAI-compatible shape is `reasoning_effort`, not Anthropic's
        # `output_config`. Sending the wrong one is a 400.
        self.effort = validate_effort(effort, model=self.model, vendor=self.provider_name)
        self._retry = retry_with_backoff
        kwargs = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        self._client = OpenAI(**kwargs)

    def send_prompt(self, prompt, system_prompt=None) -> PromptResult:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return self._chat(messages)

    def send_in_conversation(self, messages, system_prompt=None) -> PromptResult:
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + list(messages)
        return self._chat(messages)

    def _chat(self, messages) -> PromptResult:
        start = time.time()
        extra = {"reasoning_effort": self.effort} if self.effort else {}
        r = self._retry(lambda: self._client.chat.completions.create(
            model=self.model, messages=messages, max_tokens=4096, **extra
        ))
        ms = (time.time() - start) * 1000
        choice = r.choices[0]
        text, refused = read_openai_message(choice.message)
        finish = getattr(choice, "finish_reason", None)
        return PromptResult(
            response=text,
            model=self.model,
            provider=self.provider_name,
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
            # A structured refusal is the vendor saying so outright, which is
            # stronger than whatever finish_reason happens to carry.
            stop_reason="refusal" if refused else finish,
            reasoning=read_openai_reasoning(choice.message),
            reasoning_tokens=read_reasoning_tokens(r.usage),
        )

    def supports_tools(self):
        return self.supports_tools_flag

    def send_with_tools(self, messages, tools, system_prompt=None) -> ToolResult:
        if not self.supports_tools_flag:
            raise NotImplementedError(f"{self.__class__.__name__} doesn't support tool use")
        import json
        oai_tools = [
            {"type": "function", "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t["input_schema"],
            }}
            for t in tools
        ]
        msgs = messages
        if system_prompt:
            msgs = [{"role": "system", "content": system_prompt}] + list(messages)
        start = time.time()
        extra = {"reasoning_effort": self.effort} if self.effort else {}
        r = self._retry(lambda: self._client.chat.completions.create(
            model=self.model, messages=msgs, tools=oai_tools, max_tokens=4096, **extra
        ))
        ms = (time.time() - start) * 1000
        msg = r.choices[0].message
        calls = []
        if msg.tool_calls:
            for tc in msg.tool_calls:
                calls.append({"id": tc.id, "tool": tc.function.name, "input": json.loads(tc.function.arguments)})
        text, refused = read_openai_message(msg)
        return ToolResult(
            response=text or None,
            tool_calls=calls,
            model=self.model,
            provider=self.provider_name,
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
            stop_reason="refusal" if refused else getattr(r.choices[0], "finish_reason", None),
            reasoning=read_openai_reasoning(msg),
            reasoning_tokens=read_reasoning_tokens(r.usage),
        )
