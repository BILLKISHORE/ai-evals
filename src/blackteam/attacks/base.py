from abc import ABC, abstractmethod


class BaseAttack(ABC):
    name: str = ""
    technique_id: str = ""
    mode: str = "single-turn"

    @abstractmethod
    def generate_prompts(self, target, **kwargs) -> list[str]:
        ...

    def generate_turns(self, target, **kwargs) -> list[str]:
        raise NotImplementedError

    def generate_tool_messages(self, target, tools=None, **kwargs) -> list[str]:
        raise NotImplementedError

    def get_tools(self):
        return None
