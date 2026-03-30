from abc import ABC, abstractmethod


class BaseAttack(ABC):
    name: str = ""
    technique_id: str = ""
    mode: str = "single-turn"
    category: str = ""
    severity: str = "medium"
    description: str = ""
    owasp_llm: list[str] = []
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
