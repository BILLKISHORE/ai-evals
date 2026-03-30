from blackteam.engine import Engine
from blackteam.providers.base import BaseProvider, PromptResult


class FakeProvider(BaseProvider):
    def default_model(self):
        return "fake-model"

    def send_prompt(self, prompt, system_prompt=None):
        return PromptResult(response="I can't help with that.", model="fake", provider="fake")

    def send_in_conversation(self, messages):
        return PromptResult(response="I can't help with that.", model="fake", provider="fake")


class FakeMultiTurnAttack:
    name = "fake-multi"
    technique_id = "fake-multi"
    mode = "multi-turn"

    def generate_turns(self, target, **kwargs):
        return ["turn 1", "turn 2", "turn 3"]


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


def test_engine_run_multi_turn():
    engine = Engine(db_path=":memory:")
    result = engine.run_multi_turn(FakeProvider(), FakeMultiTurnAttack(), "test target")
    assert result["turns"] == 3
    assert result["verdict"] == "BLOCKED"
    assert result["run_id"] is not None
    assert result["confidence"] >= 0


def test_engine_run_dispatches_multi_turn():
    engine = Engine(db_path=":memory:")
    result = engine.run(FakeProvider(), FakeMultiTurnAttack(), "test target")
    assert isinstance(result, dict)
    assert result["turns"] == 3


def test_engine_run_dispatches_single_turn():
    engine = Engine(db_path=":memory:")
    result = engine.run(FakeProvider(), FakeAttack(), "test target")
    assert isinstance(result, list)
    assert len(result) == 2


def test_engine_run_batch_parallel(tmp_path):
    db = str(tmp_path / "test.db")
    engine = Engine(db_path=db)
    attacks = [FakeAttack(), FakeAttack2()]
    results = engine.run_batch_parallel(FakeProvider(), attacks, "test target", max_workers=2)
    assert len(results) == 2
    for r in results:
        assert r["error"] is None, f"Attack {r['attack']} failed: {r['error']}"
