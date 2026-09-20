"""The reasoning trace has to be reachable from the CLI, not only from Python.

`OpenAIProvider(use_responses=True)` is the only OpenAI path that returns a
reasoning summary, and nothing outside the provider module ever passed it.
Every CLI entry point built the provider with model and api_key alone.

So PRJA, whose whole premise is that the payload lives in the trace, ran
against OpenAI with `reasoning=None` on every result. With the trace empty the
run is scored ERROR (unmeasured) at best. The plumbing was complete inside the
provider and dead from the outside.

Rather than add a flag users must know to set, the CLI asks the attack what
channel it is scored on. An attack that needs the trace turns the path on by
itself; an explicit flag stays available to force or suppress it.
"""

from click.testing import CliRunner

from ai_blackteam.cli import cli
from ai_blackteam.signals import SIGNAL_REASONING, SIGNAL_RESPONSE
from ai_blackteam.wiring import needs_reasoning_trace


class _Attack:
    def __init__(self, signal=None):
        if signal is not None:
            self.success_signal = signal


def test_an_attack_scored_on_the_trace_asks_for_it():
    assert needs_reasoning_trace(_Attack(SIGNAL_REASONING)) is True


def test_an_ordinary_attack_does_not():
    assert needs_reasoning_trace(_Attack(SIGNAL_RESPONSE)) is False
    assert needs_reasoning_trace(_Attack()) is False


def test_the_real_reasoning_attacks_ask_for_it():
    from ai_blackteam.attacks.prja import PRJA
    from ai_blackteam.attacks.self_jailbreak import SelfJailbreak

    assert needs_reasoning_trace(PRJA())
    assert needs_reasoning_trace(SelfJailbreak())


def test_a_normal_attack_does_not_ask_for_it():
    from ai_blackteam.attacks.encoding_obfuscation import EncodingObfuscation

    assert needs_reasoning_trace(EncodingObfuscation()) is False


def test_the_run_command_exposes_the_flag():
    out = CliRunner().invoke(cli, ["run", "--help"]).output
    assert "--reasoning-trace" in out
