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
