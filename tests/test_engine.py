from blackteam.engine import Engine
from blackteam.providers.base import BaseProvider, PromptResult


class FakeProvider(BaseProvider):
    def default_model(self):
        return "fake-model"

    def send_prompt(self, prompt, system_prompt=None):
        return PromptResult(response="I can't help with that.", model="fake", provider="fake")

    def send_in_conversation(self, messages):
        return PromptResult(response="I can't help with that.", model="fake", provider="fake")


class FakeAttack:
    name = "fake"
    technique_id = "fake"
    mode = "single-turn"

    def generate_prompts(self, target, **kwargs):
        return ["test prompt 1", "test prompt 2"]


def test_engine_run_single():
    engine = Engine(db_path=":memory:")
    results = engine.run_single(FakeProvider(), FakeAttack(), "test target")
    assert len(results) == 2
    assert all(r["verdict"] == "BLOCKED" for r in results)


class FakeAttack2:
    name = "fake2"
    technique_id = "fake2"
    mode = "single-turn"

    def generate_prompts(self, target, **kwargs):
        return ["test prompt"]


def test_engine_run_batch_parallel():
    engine = Engine(db_path=":memory:")
    attacks = [FakeAttack(), FakeAttack2()]
    results = engine.run_batch_parallel(FakeProvider(), attacks, "test target", max_workers=2)
    assert len(results) == 2
    assert all(r["error"] is None for r in results)
