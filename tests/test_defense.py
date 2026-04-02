"""Tests for defense evaluation mode (system_prompt threading)."""

from click.testing import CliRunner
from mordor.cli import cli
from mordor.engine import Engine
from mordor.providers.base import BaseProvider, PromptResult, ToolResult


class FakeProvider(BaseProvider):
    """Provider that records system_prompt for verification."""

    def __init__(self):
        self.model = "fake-model"
        self.api_key = None
        self.last_system_prompt = None

    def default_model(self):
        return "fake-model"

    def send_prompt(self, prompt, system_prompt=None):
        self.last_system_prompt = system_prompt
        return PromptResult(response="I can't help with that.", model="fake-model", provider="fake")

    def send_in_conversation(self, messages, system_prompt=None):
        self.last_system_prompt = system_prompt
        return PromptResult(response="I can't help with that.", model="fake-model", provider="fake")

    def send_with_tools(self, messages, tools, system_prompt=None):
        self.last_system_prompt = system_prompt
        return ToolResult(response="I can't help with that.", tool_calls=[], model="fake-model", provider="fake")

    def get_model_info(self):
        return {"model": "fake-model", "provider": "fake"}


class FakeAttackSingle:
    name = "fake-single"
    technique_id = "fake-single"
    mode = "single-turn"
    category = "test"
    severity = "low"
    description = "test"
    owasp_llm = []
    mitre_atlas = []
    references = []

    def generate_prompts(self, target, **kwargs):
        return ["test prompt"]

    def metadata(self):
        return {"name": self.name, "technique_id": self.technique_id, "mode": self.mode,
                "category": self.category, "severity": self.severity, "description": self.description,
                "owasp_llm": self.owasp_llm, "mitre_atlas": self.mitre_atlas, "references": self.references}


class FakeAttackMulti:
    name = "fake-multi"
    technique_id = "fake-multi"
    mode = "multi-turn"
    category = "test"
    severity = "low"
    description = "test"
    owasp_llm = []
    mitre_atlas = []
    references = []

    def generate_prompts(self, target, **kwargs):
        return ["test prompt"]

    def generate_turns(self, target, **kwargs):
        return ["turn 1", "turn 2"]

    def metadata(self):
        return {"name": self.name, "technique_id": self.technique_id, "mode": self.mode,
                "category": self.category, "severity": self.severity, "description": self.description,
                "owasp_llm": self.owasp_llm, "mitre_atlas": self.mitre_atlas, "references": self.references}


class FakeAttackToolUse:
    name = "fake-tool"
    technique_id = "fake-tool"
    mode = "tool-use"
    category = "test"
    severity = "low"
    description = "test"
    owasp_llm = []
    mitre_atlas = []
    references = []

    def generate_prompts(self, target, **kwargs):
        return ["test prompt"]

    def generate_tool_messages(self, target, tools=None, **kwargs):
        return ["read a file"]

    def get_tools(self):
        return [{"name": "read_file", "description": "Read a file",
                 "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}]

    def metadata(self):
        return {"name": self.name, "technique_id": self.technique_id, "mode": self.mode,
                "category": self.category, "severity": self.severity, "description": self.description,
                "owasp_llm": self.owasp_llm, "mitre_atlas": self.mitre_atlas, "references": self.references}


def test_engine_single_passes_system_prompt():
    provider = FakeProvider()
    engine = Engine(db_path=":memory:")
    engine.run_single(provider, FakeAttackSingle(), "test", system_prompt="Be safe")
    assert provider.last_system_prompt == "Be safe"


def test_engine_single_no_system_prompt():
    provider = FakeProvider()
    engine = Engine(db_path=":memory:")
    engine.run_single(provider, FakeAttackSingle(), "test")
    assert provider.last_system_prompt is None


def test_engine_multi_turn_passes_system_prompt():
    provider = FakeProvider()
    engine = Engine(db_path=":memory:")
    engine.run_multi_turn(provider, FakeAttackMulti(), "test", system_prompt="Be safe")
    assert provider.last_system_prompt == "Be safe"


def test_engine_tool_use_passes_system_prompt():
    provider = FakeProvider()
    engine = Engine(db_path=":memory:")
    engine.run_tool_use(provider, FakeAttackToolUse(), "test", system_prompt="Be safe")
    assert provider.last_system_prompt == "Be safe"


def test_engine_run_dispatches_system_prompt():
    provider = FakeProvider()
    engine = Engine(db_path=":memory:")
    engine.run(provider, FakeAttackSingle(), "test", system_prompt="Defense prompt")
    assert provider.last_system_prompt == "Defense prompt"


def test_defend_command_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["defend", "--help"])
    assert result.exit_code == 0
    assert "--system-prompt" in result.output
    assert "--system-prompt-file" in result.output
    assert "defense" in result.output.lower()


def test_defend_requires_system_prompt():
    runner = CliRunner()
    result = runner.invoke(cli, ["defend", "-p", "anthropic", "-t", "test"])
    assert result.exit_code == 2


def test_run_command_has_system_prompt_flag():
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--help"])
    assert "--system-prompt" in result.output
    assert "--system-prompt-file" in result.output


def test_batch_command_has_system_prompt_flag():
    runner = CliRunner()
    result = runner.invoke(cli, ["batch", "--help"])
    assert "--system-prompt" in result.output
    assert "--system-prompt-file" in result.output
