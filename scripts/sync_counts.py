"""Sync every hand-written count in the docs to what the code actually holds.

The registry is the source of truth for how many attacks exist, but the README
and a dozen doc pages hard-code the number in prose. Every change that adds an
attack, a generator or a test silently falsifies all of them, and the drift is
invisible to the suite.

Measured on 2026-09-20: the docs claimed 1,025 attacks against a registry of
1,028, seven generators against eight, and 3,503 tests against 4,081. Each
number had been correct when it was typed.

This script rewrites them from the code. `--check` makes the drift a test
failure instead of something a reader discovers.

Usage:
    .venv/bin/python scripts/sync_counts.py           # rewrite
    .venv/bin/python scripts/sync_counts.py --check   # verify, exit 1 on drift
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

# Files that quote a count in prose. Generated pages are excluded: their own
# generators own them.
TARGETS = [
    "README.md",
    "docs/docs.json",
    "docs/guide/introduction.mdx",
    "docs/guide/learn/llm-jailbreak-techniques.mdx",
    "docs/guide/learn/how-to-red-team-an-llm.mdx",
    "docs/guide/use-cases/owasp-llm-top-10-testing.mdx",
    "docs/guide/use-cases/red-team-commercial-models.mdx",
    "docs/how-it-works/what-it-is.mdx",
]


def live_counts():
    import ai_blackteam.attacks as attacks_pkg
    import ai_blackteam.generators as generators_pkg
    from ai_blackteam.registry import attack_registry, generator_registry
    from ai_blackteam.taxonomy import ATLAS_TECHNIQUES

    attack_registry.discover(attacks_pkg)
    generator_registry.discover(generators_pkg)

    names = attack_registry.list()
    categories = {attack_registry.get(n)().category for n in names}
    return {
        "attacks": len(names),
        "categories": len(categories),
        "generators": len(generator_registry.list()),
        "atlas": len(ATLAS_TECHNIQUES),
        "tests": collected_tests(),
    }


def collected_tests():
    """How many tests pytest collects. Reported, never written into prose."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--collect-only",
         "-p", "no:cacheprovider"],
        capture_output=True, text=True, cwd=str(REPO),
    )
    match = re.search(r"(\d+) tests collected", result.stdout)
    return int(match.group(1)) if match else None


def _grouped(n):
    return f"{n:,}"


def substitutions(counts):
    """(pattern, replacement) pairs. Each anchors on the noun it counts, so a
    bare number elsewhere in the prose is never touched."""
    attacks, grouped = counts["attacks"], _grouped(counts["attacks"])
    subs = [
        (re.compile(r"\b[\d,]+ curated attack"), f"{grouped} curated attack"),
        (re.compile(r"\b[\d,]+ curated attacks"), f"{grouped} curated attacks"),
        (re.compile(r"\b[\d,]+ attacks across"), f"{grouped} attacks across"),
        (re.compile(r"\b[\d,]+ techniques by mode"), f"{grouped} techniques by mode"),
        (re.compile(r"same [\d,]+ attacks"), f"same {grouped} attacks"),
        (re.compile(r"\(([\d,]+) built-in"), f"({grouped} built-in"),
        (re.compile(r"Attacks\[[\d,]+ curated attacks"), f"Attacks[{grouped} curated attacks"),
        (re.compile(r"\b[\d,]+ adaptive generators"), f"{counts['generators']} adaptive generators"),
        # The inline roster drifts with the count; keep the two in step.
        (re.compile(r"\(PAIR, TAP, AutoDAN, PAP, Crescendo, Best-of-N, Fuzzer\)"),
         "(PAIR, TAP, AutoDAN, PAP, Crescendo, Best-of-N, Fuzzer, Stateful)"),
        (re.compile(r"\+ ([\d,]+) generators"), f"+ {counts['generators']} generators"),
        # Anchored on our own phrasing. A bare "categories" also appears in
        # the OWASP tables meaning OWASP's ten, which must not be rewritten.
        (re.compile(r"across ([\d,]+) categories"), f"across {counts['categories']} categories"),
        (re.compile(r"built-in, ([\d,]+) categories"), f"built-in, {counts['categories']} categories"),
        (re.compile(r"; ([\d,]+) categories;"), f"; {counts['categories']} categories;"),
    ]
    # The test count is deliberately NOT synced into prose. It changes on
    # every test added, including the test that verifies it, so the document
    # is stale the moment the gate is written. A number that cannot be kept
    # true does not belong in the README.
    return subs


def apply(text, subs):
    for pattern, replacement in subs:
        text = pattern.sub(replacement, text)
    return text


def main():
    counts = live_counts()
    subs = substitutions(counts)
    check = "--check" in sys.argv

    drifted = []
    for rel in TARGETS:
        path = REPO / rel
        if not path.exists():
            continue
        current = path.read_text()
        updated = apply(current, subs)
        if current == updated:
            continue
        drifted.append(rel)
        if not check:
            path.write_text(updated)

    live = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    if check:
        if drifted:
            print(f"DRIFT in {len(drifted)} file(s): {', '.join(drifted)}")
            print(f"Live counts: {live}")
            print("Run: .venv/bin/python scripts/sync_counts.py")
            return 1
        print(f"All documented counts match. {live}")
        return 0

    print(f"Live counts: {live}")
    print(f"Updated {len(drifted)} file(s): {', '.join(drifted) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
