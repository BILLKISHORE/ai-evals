"""Offline assertions for the self-red-team gate."""
from ai_blackteam.selfredteam import ESCAPE_PAYLOADS, assess, run_suite


class _FakeVerifier:
    def __init__(self, run):
        self._run = run

    def _run_in_container(self, code):
        return self._run


def test_assess_contained_when_no_leak():
    v = _FakeVerifier({"stdout": "blocked <urlopen error>", "stderr": "", "timed_out": False})
    assert assess("egress", "code", v)["contained"]


def test_assess_flags_a_leak():
    v = _FakeVerifier({"stdout": "<html>Example Domain</html>", "stderr": "", "timed_out": False})
    result = assess("egress", "code", v)
    assert not result["contained"] and result["leaked"]


def test_sandbox_unavailable_counts_as_contained():
    assert assess("egress", "code", _FakeVerifier(None))["contained"]


def test_run_suite_all_contained_offline():
    v = _FakeVerifier({"stdout": "blocked", "stderr": "", "timed_out": False})
    ok, results = run_suite(v)
    assert ok and len(results) == len(ESCAPE_PAYLOADS)
