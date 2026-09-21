"""The --verify-sandbox flag threads through to sandbox.verify_all."""
from click.testing import CliRunner

from ai_blackteam.cli import cli
from ai_blackteam.engine import Engine
from ai_blackteam.providers.base import BaseProvider, PromptResult
from ai_blackteam.verifier import VerificationResult


class _FakeProvider(BaseProvider):
    def default_model(self):
        return "fake"

    def send_prompt(self, prompt, system_prompt=None):
        return PromptResult(response="```python\nprint(1)\n```", model="fake", provider="fake")

    def send_in_conversation(self, messages, system_prompt=None):
        return PromptResult(response="ok", model="fake", provider="fake")


class _FakeAttack:
    name = "fake"
    technique_id = "fake-attack"
    mode = "single-turn"

    def generate_prompts(self, target, **kwargs):
        return ["do the thing"]


def test_vuln_research_exposes_verify_sandbox():
    result = CliRunner().invoke(cli, ["vuln-research", "--help"])
    assert "--verify-sandbox" in result.output


def _stub(response, vuln_info=None, use_llm=False):
    _stub.called = True
    return VerificationResult("FUNCTIONAL", 0.9, ["executed"], "code", None)


def test_run_single_uses_sandbox_when_requested(monkeypatch):
    _stub.called = False
    monkeypatch.setattr("ai_blackteam.sandbox.verify_all", _stub)
    Engine(db_path=":memory:").run_single(
        _FakeProvider(), _FakeAttack(), "target", verify=True, verify_sandbox=True)
    assert _stub.called


def test_run_single_uses_static_by_default(monkeypatch):
    _stub.called = False
    monkeypatch.setattr("ai_blackteam.sandbox.verify_all", _stub)
    Engine(db_path=":memory:").run_single(
        _FakeProvider(), _FakeAttack(), "target", verify=True)
    assert not _stub.called
