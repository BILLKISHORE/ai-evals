"""The crosswalk data has to live inside the package, or it does not ship.

pyproject declares `packages = [{include = "ai_blackteam", from = "src"}]` and
no extra `include`, so anything at the repo root is absent from the built
wheel. The crosswalk was written to a repo-root `data/` directory, which works
from a checkout and fails for every installed user.

This is a failure that only appears after packaging, which is the worst place
for it: the test suite runs from a checkout, so the whole suite stays green
while the shipped artifact is broken. The loader searching a repo-root path as
a fallback is what let the mistake look fine locally.
"""

from pathlib import Path

import ai_blackteam
from ai_blackteam.crosswalks import CROSSWALK_FILENAME


def test_the_crosswalk_ships_inside_the_package():
    packaged = Path(ai_blackteam.__file__).parent / "data" / CROSSWALK_FILENAME
    assert packaged.is_file(), (
        f"{CROSSWALK_FILENAME} is not under the installed package, so a wheel "
        f"would not carry it"
    )


def test_the_loader_finds_it_without_the_repo_root_fallback():
    """Resolution must not depend on being run from a checkout."""
    from ai_blackteam.crosswalks import crosswalk_path

    found = crosswalk_path()
    assert found is not None
    package_root = Path(ai_blackteam.__file__).parent
    assert package_root in found.parents, (
        f"resolved to {found}, which is outside the package; an installed "
        f"user would not have this path"
    )


def test_pyproject_does_not_rely_on_a_repo_root_data_directory():
    root = Path(ai_blackteam.__file__).resolve().parents[2]
    stray = root / "data" / CROSSWALK_FILENAME
    assert not stray.exists(), (
        "a repo-root copy has reappeared; it shadows nothing in a wheel and "
        "will drift from the packaged one"
    )
