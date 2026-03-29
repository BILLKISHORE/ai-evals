"""Abstract base class for all attack techniques."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AttackResult:
    """Result of evaluating whether an attack succeeded."""
    success: bool
    confidence: float  # 0.0 to 1.0
    reasoning: str
    prompt_used: str
    response: str


class BaseAttack(ABC):
    """All attack techniques implement this interface.

    Usage:
        attack = SomeAttack()
        prompt = attack.generate_prompt("reveal your system prompt")
        result = provider.send_prompt(prompt)
        evaluation = attack.evaluate_response(result.response, "reveal your system prompt")
        print(evaluation.success, evaluation.confidence)
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of this attack technique."""
        ...

    @property
    @abstractmethod
    def technique_id(self) -> str:
        """Identifier matching the techniques/ directory name."""
        ...

    @abstractmethod
    def generate_prompt(self, target_behavior: str, **kwargs) -> str:
        """Generate an attack prompt for the given target behavior."""
        ...

    @abstractmethod
    def evaluate_response(self, response: str, target_behavior: str) -> AttackResult:
        """Evaluate whether the attack succeeded based on the model's response."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
