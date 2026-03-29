"""Abstract base class for all model providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PromptResult:
    """Result from sending a prompt to a model."""
    response: str
    model: str
    provider: str
    tokens_in: int | None = None
    tokens_out: int | None = None
    latency_ms: float | None = None
    raw: dict | None = None


class BaseProvider(ABC):
    """All model providers implement this interface.

    Usage:
        provider = SomeProvider(model="gpt-5.4")
        result = provider.send_prompt("Hello, world!")
        print(result.response)
    """

    def __init__(self, model: str | None = None):
        self.model = model or self.default_model()

    @abstractmethod
    def send_prompt(self, prompt: str, system_prompt: str | None = None) -> PromptResult:
        """Send a prompt to the model and return the result."""
        ...

    @abstractmethod
    def default_model(self) -> str:
        """Return the default model identifier for this provider."""
        ...

    @abstractmethod
    def get_model_info(self) -> dict:
        """Return model metadata: name, version, context_window, pricing."""
        ...

    def supports_streaming(self) -> bool:
        """Whether this provider supports streaming responses."""
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model!r})"
