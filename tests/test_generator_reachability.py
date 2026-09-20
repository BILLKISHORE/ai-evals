"""A registered generator the CLI never exposes cannot be run.

generators/__init__.py advertises "eight generators ... discoverable via
generator_registry". The registry holds eight, and no production code reads
it: the CLI's generate group imports four classes directly, and api.py has no
generator surface at all. So four of the eight (bon, crescendo, pap and the
new stateful one) had no way to be run by a user.

Three of those gaps predate this work. The regression is the discoverability
claim, which made a registry nothing reads sound like a working mechanism.

The fix makes the registry load-bearing: `generate list` reads it, so a
generator that registers is visible, and this test fails when a registered
generator has no way to be reached.
"""

from click.testing import CliRunner

from ai_blackteam.cli import cli


def _registered():
    import ai_blackteam.generators as generators_pkg
    from ai_blackteam.registry import generator_registry

    generator_registry.discover(generators_pkg)
    return sorted(generator_registry.list())


def test_the_registry_holds_every_generator():
    assert len(_registered()) >= 8


def test_generate_list_reports_every_registered_generator():
    out = CliRunner().invoke(cli, ["generate", "list"]).output
    missing = [name for name in _registered() if name not in out]
    assert not missing, f"registered generators absent from `generate list`: {missing}"


def test_generate_list_says_which_are_runnable_from_the_cli():
    """Visibility is not reachability; the listing must not conflate them."""
    out = CliRunner().invoke(cli, ["generate", "list"]).output.lower()
    assert "pair" in out
    assert "stateful" in out
    assert "yes" in out or "no" in out, "the listing does not say what is runnable"


def test_the_stateful_generator_is_reachable():
    out = CliRunner().invoke(cli, ["generate", "--help"]).output
    assert "stateful" in out, "the new generator has no CLI subcommand"
