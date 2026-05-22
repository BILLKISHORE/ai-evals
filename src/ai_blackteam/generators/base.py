from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """Base class for adaptive attack generators (PAIR, TAP, GPTFuzzer)."""

    name: str = ""
    description: str = ""

    @abstractmethod
    def generate(self, target, provider, **kwargs):
        """Generate attacks against a target. Returns list of results."""
        ...
