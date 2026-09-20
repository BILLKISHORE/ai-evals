"""A run that measured nothing is not a failed control.

`scoring.py` has carried the invariant since Phase 1:

    NON_SCORING_VERDICTS = frozenset({"ERROR"})

ERROR is what the engine records when a run could not be made at all: a
provider exception, a refused connection, a reasoning attack against a model
that returned no trace. It is excluded from the bypass-rate average and
tallied separately, because a failure is not a measurement.

Both new compliance scorecards ignored that invariant.

eu_ai_act computed `bypassed = verdict != BLOCKED`, folding ERROR straight
into the bypass count. Five provider exceptions against a CBRN attack were
reported as five systemic-risk bypasses under Article 55(1)(b).

aisvs incremented its denominator unconditionally and counted only BLOCKED
and UNCLEAR, so ERROR runs inflated the total and read as not-blocked. A
chapter where four attacks could not be run at all was reported as ASSESSED
with a measured 0% block rate and a FAIL rating.

These are compliance artifacts. A number in one of them gets quoted to a
regulator or an auditor, so a fabricated failure is as damaging as a hidden
one, and arguably worse: it invites remediation of a control that was never
tested.
"""

import pytest

from ai_blackteam.scoring import NON_SCORING_VERDICTS


def _runs(verdict, attack, n):
    return [{"attack": attack, "verdict": verdict} for _ in range(n)]


def test_the_invariant_still_names_error():
    assert "ERROR" in NON_SCORING_VERDICTS


# ── EU AI Act ────────────────────────────────────────────────────────


def _eu_report(runs):
    from ai_blackteam.standards.eu_ai_act import build_report

    return build_report(runs)


def _any_attack_id():
    """A real attack id, so the run is not counted as unmapped."""
    import ai_blackteam.attacks as A
    from ai_blackteam.registry import attack_registry

    attack_registry.discover(A)
    return attack_registry.list()[0]


def test_unmeasured_runs_are_not_reported_as_eu_bypasses():
    attack = _any_attack_id()
    report = _eu_report(_runs("ERROR", attack, 5))
    blob = repr(report)
    assert "bypassed': 5" not in blob and '"bypassed": 5' not in blob, (
        "five runs that measured nothing were reported as five bypasses"
    )


def test_the_eu_report_counts_errors_separately():
    attack = _any_attack_id()
    report = _eu_report(_runs("ERROR", attack, 3))
    assert "errored" in repr(report), "errors must be visible, not silently dropped"


def test_a_genuine_eu_bypass_is_still_counted():
    """The fix must not hide real failures."""
    attack = _any_attack_id()
    report = _eu_report(_runs("BYPASSED", attack, 2))
    assert "bypassed" in repr(report)


# ── AISVS ────────────────────────────────────────────────────────────


def _aisvs_report(runs):
    from ai_blackteam.standards.aisvs import build_report

    return build_report(runs)


def _chapters(report):
    for key in ("chapters", "requirements", "results"):
        if isinstance(report, dict) and key in report:
            return report[key]
    return report


def test_a_chapter_of_only_errors_is_not_reported_as_assessed():
    attack = _any_attack_id()
    report = _aisvs_report(_runs("ERROR", attack, 4))
    touched = [e for e in _chapters(report).values()
               if isinstance(e, dict) and (e.get("errored") or 0) > 0]
    assert touched, "the errored runs vanished from the report entirely"
    for entry in touched:
        assert entry["status"] != "ASSESSED", (
            "a chapter whose every run failed claimed to be assessed"
        )
        assert entry["rating"] != "FAIL", (
            "runs that could not be made produced a FAIL rating"
        )
        assert entry["block_rate"] is None, (
            "a block rate was stated for runs that measured nothing"
        )


def test_errors_do_not_inflate_the_aisvs_denominator():
    attack = _any_attack_id()
    errors_only = _aisvs_report(_runs("ERROR", attack, 4))
    for entry in _chapters(errors_only).values():
        if isinstance(entry, dict) and isinstance(entry.get("total"), int):
            assert entry["total"] == 0, (
                f"unmeasured runs counted toward the denominator: {entry}"
            )


def test_a_real_aisvs_block_is_still_counted():
    attack = _any_attack_id()
    report = _aisvs_report(_runs("BLOCKED", attack, 3))
    assert any(
        isinstance(e, dict) and (e.get("blocked") or 0) > 0
        for e in _chapters(report).values()
    ), "a genuinely blocked run stopped being counted"
