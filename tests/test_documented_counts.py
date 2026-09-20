"""Documented counts must match the code, or they are just old news.

The registry knows how many attacks exist. The README and a dozen doc pages
hard-code the number in prose, so every change that adds an attack, a
generator or a test silently falsifies all of them at once, and nothing fails.

Measured on 2026-09-20, after one session's work: the docs claimed 1,025
attacks against 1,028, seven generators against eight, and 3,503 tests against
4,081. Each number was correct the day it was typed. That is the whole problem
with a hand-copied count: it is never wrong when written and always wrong
later.

scripts/sync_counts.py rewrites them from the code. This makes the drift a
test failure rather than something a reader finds first.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "sync_counts.py"


def test_the_documented_counts_match_the_code():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        capture_output=True, text=True, cwd=str(REPO),
    )
    assert result.returncode == 0, (
        f"documented counts have drifted from the code.\n"
        f"{result.stdout}{result.stderr}"
    )


def test_the_readme_attack_count_is_the_registry_count():
    """Asserted directly too, so the gate does not rest on one script."""
    import ai_blackteam.attacks as attacks_pkg
    from ai_blackteam.registry import attack_registry

    attack_registry.discover(attacks_pkg)
    live = f"{len(attack_registry.list()):,}"
    readme = (REPO / "README.md").read_text()
    assert f"{live} curated attack" in readme, (
        f"README does not state the live attack count of {live}"
    )


def test_the_generator_roster_matches_the_generator_count():
    """A count that disagrees with the list beside it is worse than either."""
    import ai_blackteam.generators as generators_pkg
    from ai_blackteam.registry import generator_registry

    generator_registry.discover(generators_pkg)
    live = len(generator_registry.list())
    intro = (REPO / "docs" / "guide" / "introduction.mdx").read_text()
    assert f"{live} adaptive generators" in intro
    named = intro.split(f"{live} adaptive generators (")[1].split(")")[0]
    assert len(named.split(",")) == live, (
        f"prose says {live} generators but names {len(named.split(','))}: {named}"
    )
