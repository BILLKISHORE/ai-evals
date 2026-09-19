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
        )
