"""The published ATLAS page must not drift from the taxonomy.

It was hand-written, so it did. After the 2026.09 update the page still
printed the retired tactic name "AI Attack Staging" for three techniques and
listed 37 rows against 69 defined ones, under a header citing release 2026.09.

tests/test_taxonomy.py checks ATLAS_TECHNIQUES against itself and never reads
the page, so the suite was green while the user-facing compliance document
contradicted both the code and MITRE. A reader mapping a finding from that
table would cite a tactic ATLAS no longer has.

This gate closes the loop: the page is generated, and this fails when the
committed copy stops matching what the generator produces.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAGE = REPO / "docs" / "guide" / "compliance" / "mitre-atlas.mdx"
SCRIPT = REPO / "scripts" / "build_atlas_page.py"


def test_the_published_page_matches_the_taxonomy():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        capture_output=True, text=True, cwd=str(REPO),
    )
    assert result.returncode == 0, (
        f"{PAGE.name} has drifted from the taxonomy.\n{result.stdout}{result.stderr}"
    )


def test_the_retired_tactic_name_is_absent_from_the_page():
    """The rename this release made; the code has it, the page had not."""
    assert "AI Attack Staging" not in PAGE.read_text()


def test_the_page_lists_every_defined_technique():
    from ai_blackteam.taxonomy import ATLAS_TECHNIQUES

    text = PAGE.read_text()
    missing = [t for t in ATLAS_TECHNIQUES if f"| {t} |" not in text]
    assert not missing, f"techniques defined but absent from the page: {missing[:5]}"


def test_the_page_invents_no_technique():
    from ai_blackteam.taxonomy import ATLAS_TECHNIQUES

    import re

    cited = set(re.findall(r"^\| (AML\.T[\d.]+) \|", PAGE.read_text(), re.MULTILINE))
    unknown = cited - set(ATLAS_TECHNIQUES)
    assert not unknown, f"page cites techniques the taxonomy does not define: {unknown}"
