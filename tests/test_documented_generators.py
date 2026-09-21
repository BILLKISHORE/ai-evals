"""The generator roster in the docs must match the registry.

`test_documented_counts.py` gates the generator COUNT, but not the named list
beside it. Writing the feature docs on 2026-09-21 surfaced the gap: the intro
said "8 adaptive generators" (count correct, gated) while the parenthetical
list named only 7, because Stateful was added and the prose was not. A count
that agrees with the code sitting next to a name list that does not is the
worst of both, and nothing failed.

This gates the names too. Each registered generator must appear in the guide
introduction under a recognizable display name, and the prose must not claim a
generator the registry does not have.
"""

from pathlib import Path

import ai_blackteam.generators as _generators
from ai_blackteam.registry import generator_registry

generator_registry.discover(_generators)

REPO = Path(__file__).resolve().parents[1]
INTRO = REPO / "docs" / "guide" / "introduction.mdx"

# Registry name -> the display token the prose uses. Stable, human-facing names.
DISPLAY = {
    "autodan": "AutoDAN",
    "bon": "Best-of-N",
    "crescendo": "Crescendo",
    "fuzzer": "Fuzzer",
    "pair": "PAIR",
    "pap": "PAP",
    "stateful": "Stateful",
    "tap": "TAP",
}


def test_every_registered_generator_has_a_display_name():
    """The map must cover the registry, or the test below is blind to a new one."""
    missing = set(generator_registry.list()) - set(DISPLAY)
    assert not missing, (
        f"generators with no display name in this test: {missing}. "
        f"Add them here and to the docs."
    )


def test_every_generator_is_named_in_the_introduction():
    text = INTRO.read_text()
    absent = [DISPLAY[name] for name in generator_registry.list()
              if DISPLAY[name] not in text]
    assert not absent, (
        f"generators registered but not named in the introduction: {absent}. "
        f"Update docs/guide/introduction.mdx."
    )


def test_the_generator_count_in_prose_matches_the_registry():
    live = len(generator_registry.list())
    text = INTRO.read_text()
    assert f"{live} adaptive generators" in text, (
        f"introduction does not state the live generator count of {live}"
    )
