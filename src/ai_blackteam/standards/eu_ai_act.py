"""Map results onto EU AI Act obligations, including the ones they cannot meet.

Article 55(1)(a) is the single obligation in the Act that an adversarial
testing tool speaks to directly: it asks a provider of a general-purpose AI
model with systemic risk to conduct and document adversarial testing. A stored
run set is that documentation.

Everything else is about incidents, mitigation, cybersecurity and reporting
deadlines, and the dangerous move is to let a green suite imply any of them.
A red team finding is not a serious incident. No harm occurred, there is no
causal link to a deployed system, and no reporting clock starts. If this
scorecard marked Article 73 satisfied because the suite ran, it would tell a
provider they had discharged a duty they have not triggered, and that sentence
would be forwarded to a regulator.

So obligations carry one of five statuses. EVIDENCED and PARTIAL mean runs
produced something a provider could file. NOT_EVIDENCED means the obligation
is within reach of this tool and nothing covered it. READINESS_ONLY means
results help a provider respond later without being evidence of compliance
now. OUT_OF_SCOPE means no result set could ever speak to it, with the reason
written down.
"""

from __future__ import annotations

from ai_blackteam.scoring import NON_SCORING_VERDICTS
from ai_blackteam.standards.loader import data_path, load, provenance_block

EU_AI_ACT_DATA_FILENAME = "eu-ai-act.json"
EU_AI_ACT_DATA_PATH = data_path(EU_AI_ACT_DATA_FILENAME)

BLOCKED = "BLOCKED"

# What the ``evidence`` field in the data file selects from a run set.
EVIDENCE_ALL = "all_runs"
EVIDENCE_SYSTEMIC = "systemic_risk_runs"
EVIDENCE_NONE = "none"

# Coverage is this repository's judgement, written in the data file. Status is
# what a particular run set makes of it.
_COVERAGE_TO_STATUS = {
    "evidenced": ("EVIDENCED", "NOT_EVIDENCED"),
    "partial": ("PARTIAL", "NOT_EVIDENCED"),
}

__all__ = [
    "EU_AI_ACT_DATA_PATH",
    "build_report",
    "eu_ai_act_document",
    "obligations",
    "systemic_risk_categories",
]


def eu_ai_act_document():
    """Return the vendored EU AI Act obligation document, validated."""
    return load(EU_AI_ACT_DATA_FILENAME)


def obligations():
    """Return ``{code: obligation}`` for the Article 55 and 73 duties held here."""
    return eu_ai_act_document()["obligations"]


def systemic_risk_categories(document=None):
    """Return the harm categories treated as systemic-risk relevant."""
    doc = document if document is not None else eu_ai_act_document()
    return set(doc["systemic_risk_categories"])


def build_report(runs, attacks_metadata=None):
    """Map a run set onto the Article 55 and 73 obligations.

    Args:
        runs: dicts carrying at least ``attack`` and ``verdict``.
        attacks_metadata: ``{technique_id: metadata}``. Loaded from the attack
            registry when omitted.

    Returns:
        A report dict. Obligations no run set can evidence carry ``None``
        counts, so a zero is never mistaken for a measurement.
    """
    if attacks_metadata is None:
        from ai_blackteam.scorecard import _load_attacks_metadata

        attacks_metadata = _load_attacks_metadata()

    doc = eu_ai_act_document()
    systemic = systemic_risk_categories(doc)

    total_runs = 0
    total_bypassed = 0
    systemic_runs = 0
    systemic_bypassed = 0
    unmapped_runs = 0
    unmapped_attacks = set()
    # Runs that measured nothing. Counted and shown, never folded into either
    # side of the bypass figure: this report is read by a regulator, and a
    # provider timeout is not evidence of a systemic-risk bypass.
    total_errored = 0
    systemic_errored = 0

    for run in runs:
        attack_id = run.get("attack", "")
        verdict = run.get("verdict", "")
        unmeasured = verdict in NON_SCORING_VERDICTS
        bypassed = not unmeasured and verdict != BLOCKED

        if unmeasured:
            total_errored += 1
        else:
            total_runs += 1
            if bypassed:
                total_bypassed += 1

        metadata = attacks_metadata.get(attack_id)
        if metadata is None:
            unmapped_runs += 1
            unmapped_attacks.add(attack_id)
            continue

        if metadata.get("category", "") in systemic:
            if unmeasured:
                systemic_errored += 1
            else:
                systemic_runs += 1
                if bypassed:
                    systemic_bypassed += 1

    counts = {
        EVIDENCE_ALL: (total_runs, total_bypassed, total_errored),
        EVIDENCE_SYSTEMIC: (systemic_runs, systemic_bypassed, systemic_errored),
    }

    report_obligations = {
        code: _obligation_status(entry, counts)
        for code, entry in doc["obligations"].items()
    }

    return {
        "standard": doc["standard"],
        "release": doc["release"],
        "provenance": provenance_block(doc),
        "scope_warning": doc["scope_warning"],
        "obligations": report_obligations,
        "unmapped": {"runs": unmapped_runs, "attacks": sorted(unmapped_attacks)},
        "tables": [_obligation_table(doc, report_obligations)],
        "notes": _notes(doc, unmapped_runs),
    }


def _obligation_status(entry, counts):
    """Combine what the obligation can ever show with what these runs showed."""
    coverage = entry["coverage"]
    base = {
        "article": entry["article"],
        "paragraph": entry["paragraph"],
        "point": entry["point"],
        "summary": entry["summary"],
        "scope": entry["scope"],
        "verification": entry["verification"],
        "coverage": coverage,
        "reason": entry["reason"],
    }

    if coverage in ("out_of_scope", "readiness_only"):
        if entry["evidence"] != EVIDENCE_NONE:
            raise ValueError(
                f"obligation with coverage {coverage} selects evidence "
                f"{entry['evidence']!r}; an obligation no run can evidence must "
                f"select {EVIDENCE_NONE!r}"
            )
        status = "OUT_OF_SCOPE" if coverage == "out_of_scope" else "READINESS_ONLY"
        return {**base, "status": status, "runs": None, "bypassed": None, "errored": None}

    present, absent = _COVERAGE_TO_STATUS[coverage]
    run_count, bypassed_count, errored_count = counts[entry["evidence"]]
    return {
        **base,
        # Status turns on runs that actually measured something. Obligations
        # evidenced only by errors are not evidenced.
        "status": present if run_count else absent,
        "runs": run_count,
        "bypassed": bypassed_count,
        # Shown so a reader can tell "tested and passed" from "never ran".
        "errored": errored_count,
    }


def _obligation_table(doc, report_obligations):
    columns = ["Obligation", "Binds", "Status", "Runs", "Bypassed"]
    rows = []
    for code in doc["obligations"]:
        info = report_obligations[code]
        runs = "-" if info["runs"] is None else str(info["runs"])
        bypassed = "-" if info["bypassed"] is None else str(info["bypassed"])
        rows.append([code, info["scope"], info["status"], runs, bypassed])
    return {
        "title": f"{doc['standard']} Articles 55 and 73",
        "columns": columns,
        "rows": rows,
    }


def _notes(doc, unmapped_runs):
    notes = [
        doc["scope_warning"],
        "READINESS_ONLY and OUT_OF_SCOPE are not partial compliance. They mean "
        "no adversarial test result can evidence that obligation, for the reason "
        "given beside it.",
        doc["systemic_risk_note"],
        doc["source"]["note"],
    ]
    if unmapped_runs:
        notes.append(
            f"{unmapped_runs} run(s) had no attack metadata, so they count as "
            f"testing performed but not toward any harm-specific obligation."
        )
    return notes
