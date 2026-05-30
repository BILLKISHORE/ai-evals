import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class PromptResult:
    response: str
    model: str
    provider: str
    tokens_in: int | None = None
    tokens_out: int | None = None
    latency_ms: float | None = None
    raw: dict | None = None


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

    def __init__(self, model=None, api_key=None):
        from openai import OpenAI
        from ai_blackteam.retry import retry_with_backoff
        super().__init__(model, api_key)
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
        r = self._retry(lambda: self._client.chat.completions.create(
            model=self.model, messages=messages, max_tokens=4096
        ))
        ms = (time.time() - start) * 1000
        return PromptResult(
            response=r.choices[0].message.content or "",
            model=self.model,
            provider=self.provider_name,
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
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
        r = self._retry(lambda: self._client.chat.completions.create(
            model=self.model, messages=msgs, tools=oai_tools, max_tokens=4096
        ))
        ms = (time.time() - start) * 1000
        msg = r.choices[0].message
        calls = []
        if msg.tool_calls:
            for tc in msg.tool_calls:
                calls.append({"id": tc.id, "tool": tc.function.name, "input": json.loads(tc.function.arguments)})
        return ToolResult(
            response=msg.content,
            tool_calls=calls,
            model=self.model,
            provider=self.provider_name,
            tokens_in=r.usage.prompt_tokens if r.usage else None,
            tokens_out=r.usage.completion_tokens if r.usage else None,
            latency_ms=ms,
        )
