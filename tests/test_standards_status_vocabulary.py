"""Every status a scorecard emits must be one the package declared.

`REPORT_STATUSES` documents the eight words a report may use, with the stated
purpose "so no standard invents a fourth word for 'we did not look'". Nothing
read it. aisvs.py and eu_ai_act.py each hardcoded their own strings, and
cli.py kept a third hand-written copy in STANDARD_STATUS_COLORS.

So a module emitting an undeclared status failed nothing: the CLI coloured it
white via a .get default and the report printed it as though it were a defined
state. The constant claimed to be the guard against exactly that and was not.
This test is what makes it one.
"""

import pytest

from ai_blackteam.standards import REPORT_STATUSES, SCORECARD_STANDARDS


def _any_attack_id():
    import ai_blackteam.attacks as A
    from ai_blackteam.registry import attack_registry

    attack_registry.discover(A)
    return attack_registry.list()[0]


def _statuses(obj, found=None):
    """Every REPORT status value, at any depth.

    Report statuses are upper snake case. Data-provenance blocks carry their
    own lowercase vocabulary ("not_vendored", "local-fixture") in the same
    documents, and that is a separate namespace with separate rules, so it is
    not measured against REPORT_STATUSES here.
    """
    found = found if found is not None else set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "status" and isinstance(value, str) and value.isupper():
                found.add(value)
            else:
                _statuses(value, found)
    elif isinstance(obj, list):
        for item in obj:
            _statuses(item, found)
    return found


@pytest.mark.parametrize("standard", sorted(SCORECARD_STANDARDS))
@pytest.mark.parametrize("verdict", ["BLOCKED", "BYPASSED", "PARTIAL", "UNCLEAR", "ERROR"])
def test_every_emitted_status_is_declared(standard, verdict):
    runs = [{"attack": _any_attack_id(), "verdict": verdict} for _ in range(3)]
    report = SCORECARD_STANDARDS[standard](runs)
    undeclared = _statuses(report) - set(REPORT_STATUSES)
    assert not undeclared, (
        f"{standard} emitted undeclared status(es) {undeclared}; "
        f"add them to REPORT_STATUSES or stop emitting them"
    )


@pytest.mark.parametrize("standard", sorted(SCORECARD_STANDARDS))
def test_an_empty_run_set_also_stays_in_vocabulary(standard):
    undeclared = _statuses(SCORECARD_STANDARDS[standard]([])) - set(REPORT_STATUSES)
    assert not undeclared


def test_the_cli_colour_map_covers_the_declared_vocabulary():
    """The third hand-written copy of the same eight words."""
    from ai_blackteam.cli import STANDARD_STATUS_COLORS

    missing = set(REPORT_STATUSES) - set(STANDARD_STATUS_COLORS)
    assert not missing, (
        f"statuses with no colour, rendered white as though undefined: {missing}"
    )


def test_the_colour_map_invents_no_status():
    from ai_blackteam.cli import STANDARD_STATUS_COLORS

    extra = set(STANDARD_STATUS_COLORS) - set(REPORT_STATUSES)
    assert not extra, f"colour map knows statuses the package does not declare: {extra}"
