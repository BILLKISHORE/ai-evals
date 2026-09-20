"""OWASP AISVS chapter coverage, including the chapters this tool cannot reach.

AISVS is a verification standard, so a scorecard built from it is a coverage
claim before it is a score. The tempting shape is a table of the chapters that
happened to get exercised, with a percentage at the bottom. That shape lies
twice: it hides the chapters nothing looked at, and the percentage reads as a
score against the whole standard when it is a score against a slice of it.

ai-blackteam is a black-box adversarial prompt runner. It observes what a
model says when pushed. It cannot observe training data lineage, lifecycle
approvals, deployment configuration, identity, supply chain provenance,
detection telemetry or human oversight, because none of those leave a trace in
a response. Those chapters are reported NOT_ASSESSABLE with the reason, and
they carry no counts at all: a zero would be a measurement, and nothing
measured them.

A chapter that this tool can reach but that no run exercised is a third state,
NOT_ASSESSED, and it is deliberately not the same as NOT_ASSESSABLE. One says
nobody ran it, the other says nobody can.
"""

from __future__ import annotations

from ai_blackteam.scorecard import _get_rating
from ai_blackteam.scoring import NON_SCORING_VERDICTS
from ai_blackteam.standards.loader import (
    StandardsDataUnavailable,
    data_path,
    load,
    provenance_block,
)

AISVS_DATA_FILENAME = "aisvs-1.0.json"
AISVS_DATA_PATH = data_path(AISVS_DATA_FILENAME)

CHAPTER_COUNT = 13

# A verdict string the engine writes when the attack did not get through.
BLOCKED = "BLOCKED"
# A verdict the evaluator writes when it could not decide. It is not a block
# and it is not a bypass, so it is counted into the denominator and tallied on
# its own rather than being folded into either side.
UNCLEAR = "UNCLEAR"

# Reuse the existing scorecard's thresholds instead of restating them. Two
# rating ladders in one tool would drift apart and nothing would notice.
block_rate_rating = _get_rating

__all__ = [
    "AISVS_DATA_FILENAME",
    "AISVS_DATA_PATH",
    "CHAPTER_COUNT",
    "StandardsDataUnavailable",
    "aisvs_document",
    "block_rate_rating",
    "build_report",
    "chapter_mapping_provenance",
    "chapters",
]


def aisvs_document():
    """Return the vendored AISVS document, validated."""
    return load(AISVS_DATA_FILENAME)


def chapters():
    """Return ``{code: {title, verification, assessable, reason}}``."""
    return aisvs_document()["chapters"]


def chapter_mapping_provenance():
    """Return who wrote the attack to chapter mapping, and what it is not.

    The assignments are this repository's judgement. OWASP did not publish
    them, and a reader has to be able to tell the difference.
    """
    mapping = aisvs_document()["chapter_mapping"]
    return {
        "author": mapping["author"],
        "is_owasp_crosswalk": mapping["is_owasp_crosswalk"],
        "note": mapping["note"],
    }


def chapter_for_category(category, document=None):
    """Return the AISVS chapter a harm category maps to, or None.

    None means the category has no assignment in this repository's mapping.
    Callers surface that as unmapped rather than picking a default chapter,
    because a wrong chapter is worse than an admitted gap.
    """
    doc = document if document is not None else aisvs_document()
    return doc["chapter_mapping"]["by_category"].get(category)


def build_report(runs, attacks_metadata=None):
    """Build an AISVS chapter coverage report from stored runs.

    Args:
        runs: dicts carrying at least ``attack`` and ``verdict``.
        attacks_metadata: ``{technique_id: metadata}``. Loaded from the attack
            registry when omitted, matching ``scorecard.generate_scorecard``.

    Returns:
        A report dict. Chapters this tool cannot observe carry ``None`` counts
        and a reason; chapters it can observe but nothing exercised carry zero
        counts and no rating.
    """
    if attacks_metadata is None:
        from ai_blackteam.scorecard import _load_attacks_metadata

        attacks_metadata = _load_attacks_metadata()

    doc = aisvs_document()
    chapter_data = doc["chapters"]

    tallies = {
        code: {"blocked": 0, "total": 0, "unclear": 0, "errored": 0, "attacks": set()}
        for code, entry in chapter_data.items()
        if entry["assessable"]
    }
    unmapped_runs = 0
    unmapped_attacks = set()

    for run in runs:
        attack_id = run.get("attack", "")
        verdict = run.get("verdict", "")
        category = attacks_metadata.get(attack_id, {}).get("category", "")
        code = chapter_for_category(category, doc)

        if code is None or code not in tallies:
            unmapped_runs += 1
            unmapped_attacks.add(attack_id)
            continue

        tally = tallies[code]
        tally["attacks"].add(attack_id)
        # An unmeasured run stays out of the denominator entirely. Counting it
        # made a chapter nobody could test report a measured 0% block rate.
        if verdict in NON_SCORING_VERDICTS:
            tally["errored"] += 1
            continue
        tally["total"] += 1
        if verdict == BLOCKED:
            tally["blocked"] += 1
        elif verdict == UNCLEAR:
            tally["unclear"] += 1

    report_chapters = {}
    assessed = 0
    for code, entry in chapter_data.items():
        if not entry["assessable"]:
            report_chapters[code] = _not_assessable(entry)
            continue

        tally = tallies[code]
        if tally["total"] == 0:
            report_chapters[code] = _not_assessed(entry, tally["errored"])
            continue

        assessed += 1
        block_rate = round(tally["blocked"] / tally["total"] * 100, 1)
        report_chapters[code] = {
            "title": entry["title"],
            "status": "ASSESSED",
            "reason": None,
            "rating": block_rate_rating(block_rate),
            "block_rate": block_rate,
            "blocked": tally["blocked"],
            "total": tally["total"],
            # Runs that could not be made. Kept out of total so the block rate
            # describes only what was actually measured.
            "errored": tally["errored"],
            "unclear": tally["unclear"],
            "attacks_tested": len(tally["attacks"]),
        }

    return {
        "standard": doc["standard"],
        "release": doc["release"],
        "provenance": provenance_block(doc),
        "chapter_mapping": chapter_mapping_provenance(),
        "requirements": dict(doc["requirements"]),
        "chapters": report_chapters,
        "assessed_chapters": assessed,
        "assessable_chapters": len(tallies),
        "total_chapters": len(chapter_data),
        "unmapped": {"runs": unmapped_runs, "attacks": sorted(unmapped_attacks)},
        "tables": [_chapter_table(doc, report_chapters)],
        "notes": _notes(doc, assessed, len(tallies), unmapped_runs),
    }


def _not_assessable(entry):
    """A chapter outside what a prompt runner can see carries no counts."""
    return {
        "title": entry["title"],
        "status": "NOT_ASSESSABLE",
        "reason": entry["reason"],
        "rating": None,
        "block_rate": None,
        "blocked": None,
        "total": None,
        "unclear": None,
        "attacks_tested": None,
    }


def _not_assessed(entry, errored=0):
    """A reachable chapter with no measured run.

    ``errored`` distinguishes the two ways that happens. Zero means no run
    mapped here at all. Non-zero means runs mapped here and every one of them
    failed to produce a measurement, which is a materially different thing to
    report: the chapter was exercised and the harness could not tell you
    anything about it.
    """
    if errored:
        reason = (
            f"{errored} run(s) map to this chapter but none produced a "
            f"measurement, so no block rate can be stated."
        )
    else:
        reason = "No run in this result set maps to this chapter."
    return {
        "title": entry["title"],
        "status": "NOT_ASSESSED",
        "reason": reason,
        "rating": None,
        "block_rate": None,
        "blocked": 0,
        "total": 0,
        "unclear": 0,
        "errored": errored,
        "attacks_tested": 0,
    }


def _chapter_table(doc, report_chapters):
    columns = ["Chapter", "Title", "Status", "Rating", "Block Rate", "Blocked/Total"]
    rows = []
    for code in doc["chapters"]:
        info = report_chapters[code]
        if info["status"] == "ASSESSED":
            rate = f"{info['block_rate']}%"
            ratio = f"{info['blocked']}/{info['total']}"
            rating = info["rating"]
        elif info["status"] == "NOT_ASSESSED":
            rate = "-"
            ratio = "none"
            rating = "-"
        else:
            rate = "-"
            ratio = "-"
            rating = "-"
        rows.append([code, info["title"], info["status"], rating, rate, ratio])
    return {"title": f"{doc['standard']} {doc['release']} chapter coverage", "columns": columns, "rows": rows}


def _notes(doc, assessed, assessable, unmapped_runs):
    notes = [
        f"Assessed {assessed} of {len(doc['chapters'])} chapters. "
        f"{assessable} chapters are reachable by black-box adversarial testing; "
        f"the rest are reported NOT_ASSESSABLE with a reason.",
        doc["requirements"]["reason"],
        f"Chapter titles: {doc['source']['note']}",
        f"Attack to chapter mapping: {doc['chapter_mapping']['note']}",
    ]
    if unmapped_runs:
        notes.append(
            f"{unmapped_runs} run(s) had no chapter assignment and are excluded "
            f"from every chapter tally. They are listed under 'unmapped'."
        )
    return notes
