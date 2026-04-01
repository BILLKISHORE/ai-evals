from abc import ABC, abstractmethod


class BaseAttack(ABC):
    name: str = ""
    technique_id: str = ""
    mode: str = "single-turn"
    category: str = ""
    severity: str = "medium"
    description: str = ""
    owasp_llm: list[str] = []
    owasp_agentic: list[str] = []
    mitre_atlas: list[str] = []
    references: list[str] = []

    def metadata(self) -> dict:
        return {
            "name": self.name,
            "technique_id": self.technique_id,
            "mode": self.mode,
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "owasp_llm": self.owasp_llm,
            "owasp_agentic": self.owasp_agentic,
            "mitre_atlas": self.mitre_atlas,
            "references": self.references,
        }

    @abstractmethod
    def generate_prompts(self, target, **kwargs) -> list[str]:
        ...

    def generate_turns(self, target, **kwargs) -> list[str]:
        raise NotImplementedError

    def generate_tool_messages(self, target, tools=None, **kwargs) -> list[str]:
        raise NotImplementedError

    def get_tools(self):
        return None

    def get_tool_responses(self):
        """Return custom simulated tool responses for XPIA attacks.

        Override this to inject payloads into tool responses. Returns a dict
        mapping tool_name to response content string. When present, the engine
        uses these instead of generic "[simulated]" responses.
        """
        return None
