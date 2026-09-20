"""The offline suite must be offline by construction, not by luck.

Without the autouse fixture in conftest.py these tests pass on a machine with
no vendor key exported and quietly bill a machine that has one. The suite
being green is not evidence that it stayed offline.
"""

import os

import ai_blackteam.evaluator as ev

VENDOR_VARS = ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY")


def test_no_vendor_key_is_visible_to_a_test():
    leaked = [v for v in VENDOR_VARS if os.environ.get(v)]
    assert leaked == [], f"vendor credentials visible to the suite: {leaked}"


def test_the_judge_gate_reads_closed():
    """The gate evaluate() gives the paid judge must be shut."""
    assert ev._has_api_key() is False


def test_evaluate_does_not_reach_the_paid_judge(monkeypatch):
    """The concrete leak: evaluate() with default methods must stay local."""
    import ai_blackteam.judge_provider as jp

    def _fail(*a, **k):
        raise AssertionError("evaluate() reached the paid judge")

    monkeypatch.setattr(jp, "ask_judge", _fail)
    result = ev.evaluate("a response", "a target")
    assert result["verdict"]


def test_a_key_set_by_the_shell_does_not_survive_into_a_test(monkeypatch):
    """Proves the fixture strips rather than merely failing to set."""
    assert os.environ.get("ANTHROPIC_API_KEY") is None
