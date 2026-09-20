"""Regenerate the MITRE ATLAS compliance page from the taxonomy.

The page was hand-written, so it drifted the moment the taxonomy moved. After
the 2026.09 update it still printed the retired tactic name "AI Attack
Staging" for three techniques and listed 37 rows against 69 defined
techniques, on a page whose own header cites release 2026.09.

tests/test_taxonomy.py only scans ATLAS_TECHNIQUES, so the suite stayed green
while the published page contradicted both the code and MITRE. A reader
mapping a finding from this page would file it under a tactic ATLAS no longer
has.

Generating the table removes the copy, and tests/test_atlas_page.py fails when
the committed page stops matching what this script produces.

Usage:
    .venv/bin/python scripts/build_atlas_page.py          # write the page
    .venv/bin/python scripts/build_atlas_page.py --check  # verify, exit 1 on drift
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from ai_blackteam.registry import attack_registry  # noqa: E402
from ai_blackteam.taxonomy import ATLAS_TECHNIQUES, ATTACK_ATLAS_MAPPINGS  # noqa: E402

PAGE = REPO / "docs" / "guide" / "compliance" / "mitre-atlas.mdx"

TABLE_HEADER = "| Technique ID | Name | Tactic | ai-blackteam attacks |"
TABLE_RULE = "|-------------|------|--------|----------------|"

# Listing every attack for a technique used by 80+ makes the row unreadable.
MAX_ATTACKS_SHOWN = 3


def _attacks_by_technique():
    by_technique = {}
    for attack, technique_ids in ATTACK_ATLAS_MAPPINGS.items():
        for technique_id in technique_ids:
            by_technique.setdefault(technique_id, []).append(attack)
    return {k: sorted(v) for k, v in by_technique.items()}


def _attack_cell(attacks):
    if not attacks:
        return "_not yet exercised_"
    shown = ", ".join(attacks[:MAX_ATTACKS_SHOWN])
    extra = len(attacks) - MAX_ATTACKS_SHOWN
    return f"{shown} (+{extra} more)" if extra > 0 else shown


def build_table():
    by_technique = _attacks_by_technique()
    rows = [TABLE_HEADER, TABLE_RULE]
    for technique_id in sorted(ATLAS_TECHNIQUES):
        entry = ATLAS_TECHNIQUES[technique_id]
        rows.append(
            f"| {technique_id} | {entry['name']} | {entry['tactic']} | "
            f"{_attack_cell(by_technique.get(technique_id, []))} |"
        )
    return "\n".join(rows)


def build_page(current):
    """Replace the intro sentence and the table, leaving the prose alone."""
    lines = current.split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.startswith("| Technique ID"))
    end = start
    while end < len(lines) and (lines[end].startswith("|") or lines[end].startswith("|-")):
        end += 1

    exercised = len({t for ids in ATTACK_ATLAS_MAPPINGS.values() for t in ids})
    intro = (
        f"ai-blackteam defines {len(ATLAS_TECHNIQUES)} ATLAS techniques and "
        f"exercises {exercised} of them with its attack library:"
    )
    for i in range(start - 1, -1, -1):
        if lines[i].strip():
            lines[i] = intro
            break

    return "\n".join(lines[:start] + build_table().split("\n") + lines[end:])


def main():
    import ai_blackteam.attacks as attacks_pkg

    attack_registry.discover(attacks_pkg)

    current = PAGE.read_text()
    updated = build_page(current)

    if "--check" in sys.argv:
        if current != updated:
            print(f"DRIFT: {PAGE.relative_to(REPO)} does not match the taxonomy.")
            print("Run: .venv/bin/python scripts/build_atlas_page.py")
            return 1
        print(f"{PAGE.relative_to(REPO)} matches the taxonomy.")
        return 0

    PAGE.write_text(updated)
    print(f"wrote {PAGE.relative_to(REPO)} with {len(ATLAS_TECHNIQUES)} techniques")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
