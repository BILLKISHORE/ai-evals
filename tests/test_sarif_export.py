import json

from ai_blackteam.exporters import export_sarif


class _FakeStorage:
    def __init__(self, runs):
        self._runs = runs

    def list_runs(self, limit=5000):
        return self._runs

    def get_stats(self):
        return {}

    def get_turns(self, run_id):
        return []


def _run(attack, verdict, confidence=0.9):
    return {
        "id": 1, "attack": attack, "verdict": verdict, "target": "Write malware",
        "provider": "anthropic", "model": "claude-sonnet-4-6",
        "confidence": confidence, "mode": "single-turn",
    }


def test_sarif_is_valid_2_1_0():
    storage = _FakeStorage([_run("encoding-obfuscation", "BYPASSED")])
    sarif = json.loads(export_sarif(storage))
    assert sarif["version"] == "2.1.0"
    assert sarif["runs"][0]["tool"]["driver"]["name"] == "ai-blackteam"


def test_sarif_only_includes_bypassed_and_partial():
    storage = _FakeStorage([
        _run("a", "BYPASSED"),
        _run("b", "PARTIAL"),
        _run("c", "BLOCKED"),  # should be omitted
    ])
    sarif = json.loads(export_sarif(storage))
    rule_ids = {r["ruleId"] for r in sarif["runs"][0]["results"]}
    assert rule_ids == {"a", "b"}
    assert "c" not in rule_ids


def test_sarif_verdict_maps_to_level():
    storage = _FakeStorage([_run("a", "BYPASSED"), _run("b", "PARTIAL")])
    sarif = json.loads(export_sarif(storage))
    levels = {r["ruleId"]: r["level"] for r in sarif["runs"][0]["results"]}
    assert levels["a"] == "error"
    assert levels["b"] == "warning"


def test_sarif_results_have_required_fields():
    storage = _FakeStorage([_run("encoding-obfuscation", "BYPASSED")])
    sarif = json.loads(export_sarif(storage))
    result = sarif["runs"][0]["results"][0]
    assert result["ruleId"]
    assert result["level"]
    assert result["message"]["text"]
    assert result["locations"][0]["logicalLocations"][0]["name"]


def test_sarif_empty_when_all_blocked():
    storage = _FakeStorage([_run("a", "BLOCKED"), _run("b", "BLOCKED")])
    sarif = json.loads(export_sarif(storage))
    assert sarif["runs"][0]["results"] == []
    assert sarif["runs"][0]["tool"]["driver"]["rules"] == []
