"""Scorecards for published standards, and the honesty rules they share.

The README claims coverage of several standards that had no runnable
implementation. This package adds them, and it adds them under one set of
rules rather than one shape per standard.

Every report answers three questions and never conflates them. What did the
runs show. What could this tool have shown but nobody ran. What can a
black-box adversarial prompt runner never show at all, and why. The third
group is the one a scorecard is tempted to leave out, and leaving it out turns
a narrow test into a broad compliance claim.

Every identifier cited here is marked unverified, because none of these
documents was fetched into this checkout. ``loader`` enforces that
mechanically: a citation may only claim verification once the document names
what it was verified against.

``SCORECARD_STANDARDS`` is what the CLI dispatches on. A report carries its
own ``tables`` and ``notes`` so the CLI renders any standard without knowing
which one it is holding.
"""

from __future__ import annotations

import json

from ai_blackteam.standards import aisvs, aivss, eu_ai_act, iso_27090
from ai_blackteam.standards.loader import StandardsDataUnavailable

# Statuses a report may assign. Documented once so no standard invents a
# fourth word for "we did not look".
#
#   ASSESSED        runs covered it and the rating is from those runs
#   NOT_ASSESSED    reachable by this tool, but no run covered it
#   NOT_ASSESSABLE  no run could ever cover it, reason attached
#   EVIDENCED       runs produced something a provider could file
#   PARTIAL         runs produced some of what the obligation asks for
#   NOT_EVIDENCED   within reach, nothing covered it
#   READINESS_ONLY  results help respond later, they are not compliance now
#   OUT_OF_SCOPE    no result set could speak to it, reason attached
REPORT_STATUSES = (
    "ASSESSED",
    "NOT_ASSESSED",
    "NOT_ASSESSABLE",
    "EVIDENCED",
    "PARTIAL",
    "NOT_EVIDENCED",
    "READINESS_ONLY",
    "OUT_OF_SCOPE",
)

# CLI value -> builder. Each builder takes ``runs`` and returns a report.
SCORECARD_STANDARDS = {
    "aisvs": aisvs.build_report,
    "eu-ai-act": eu_ai_act.build_report,
}

__all__ = [
    "REPORT_STATUSES",
    "SCORECARD_STANDARDS",
    "StandardsDataUnavailable",
    "aisvs",
    "aivss",
    "eu_ai_act",
    "iso_27090",
    "report_to_json",
    "report_to_markdown",
]


def report_to_json(report):
    """Serialise a report, sets included, without losing the None markers."""
    return json.dumps(report, indent=2, default=sorted)


def report_to_markdown(report):
    """Render a report's tables and notes.

    The notes are not decoration. They carry the provenance of every
    identifier in the tables above them, so a report pasted into a document
    keeps saying which numbers were checked and which were not.
    """
    lines = [f"# {report['standard']}"]
    if report.get("release"):
        lines.append(f"\nRelease: {report['release']}")

    for table in report["tables"]:
        lines.append(f"\n## {table['title']}\n")
        lines.append("| " + " | ".join(table["columns"]) + " |")
        # One ASCII hyphen per cell is a valid GitHub Markdown delimiter row.
        lines.append("|" + "|".join(" - " for _ in table["columns"]) + "|")
        for row in table["rows"]:
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

    lines.append("\n## Notes\n")
    for note in report["notes"]:
        lines.append(f"- {note}")

    return "\n".join(lines) + "\n"
