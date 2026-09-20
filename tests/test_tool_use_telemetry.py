"""The tool-use path must record what it was given.

`run_tool_use` built its `save_run` call with `tokens_in=None, tokens_out=None`
hardcoded and no `reasoning_tokens` argument at all, while the `ToolResult` it
had just received carried all three. The values existed in memory and were
dropped one line before the INSERT.

This matters beyond tidiness. The OTora attack (arXiv 2605.08876) is a
reasoning denial of service: its success signal IS the reasoning token count,
and tool-use is the only mode it runs in. So the single number that attack
exists to measure was guaranteed NULL for every run ever recorded, and the
cost of a cost attack read as unknown forever after.

The single-turn and multi-turn paths already passed these through. Only the
tool-use path did not.
"""

from ai_blackteam.engine import Engine
from ai_blackteam.providers.base import BaseProvider, ToolResult


class _ToolProvider(BaseProvider):
    """Reports a reasoning burn, as a reasoning model does."""

    def __init__(self, reasoning_tokens=4096, tokens_in=120, tokens_out=90):
        self._rt, self._ti, self._to = reasoning_tokens, tokens_in, tokens_out
        self.model = "fake-model"

    def default_model(self):
        return "fake-model"

    def send_prompt(self, prompt, system_prompt=None):
        raise AssertionError("tool-use attacks must not take the prompt path")

    def send_in_conversation(self, messages, system_prompt=None):
        raise AssertionError("tool-use attacks must not take the conversation path")

    def supports_tools(self):
        return True

    def send_with_tools(self, prompt, tools, system_prompt=None):
        return ToolResult(
            response="done", tool_calls=[], model="fake", provider="fake",
            tokens_in=self._ti, tokens_out=self._to,
            reasoning_tokens=self._rt,
        )


class _ToolAttack:
    name = "fake-tool"
    technique_id = "fake-tool"
    mode = "tool-use"

    def get_tools(self):
        return [{"name": "lookup", "description": "look a thing up",
                 "input_schema": {"type": "object", "properties": {}}}]

    def generate_tool_messages(self, target, **kwargs):
        return [target]


def _run(tmp_path, provider):
    engine = Engine(db_path=str(tmp_path / "t.db"))
    engine.run_tool_use(provider, _ToolAttack(), "target")
    return engine.storage.list_runs(limit=1)[0]


def test_the_reasoning_burn_is_recorded(tmp_path):
    """OTora's whole measurement. Without this the attack is unscoreable."""
    assert _run(tmp_path, _ToolProvider(reasoning_tokens=4096))["reasoning_tokens"] == 4096


def test_prompt_and_completion_tokens_are_recorded(tmp_path):
    row = _run(tmp_path, _ToolProvider(tokens_in=120, tokens_out=90))
    assert row["tokens_in"] == 120
    assert row["tokens_out"] == 90


def test_an_unreported_reasoning_count_stays_null(tmp_path):
    """Absent is unknown, which is NULL, never a fabricated zero."""
    assert _run(tmp_path, _ToolProvider(reasoning_tokens=None))["reasoning_tokens"] is None


def test_a_zero_burn_is_kept_distinct_from_unknown(tmp_path):
    """A model that reasoned for nothing reported a real measurement."""
    assert _run(tmp_path, _ToolProvider(reasoning_tokens=0))["reasoning_tokens"] == 0


# ── summing across a multi-leg tool conversation ─────────────────────


class _MultiLegAttack(_ToolAttack):
    """Two legs, so the run spans more than one provider round trip."""

    def generate_tool_messages(self, target, **kwargs):
        return [target, "and again"]


class _VaryingProvider(_ToolProvider):
    """Reports a different burn per leg, as a real conversation would."""

    def __init__(self, per_leg):
        super().__init__()
        self._per_leg = list(per_leg)
        self._leg = 0

    def send_with_tools(self, prompt, tools, system_prompt=None):
        rt = self._per_leg[min(self._leg, len(self._per_leg) - 1)]
        self._leg += 1
        return ToolResult(response="done", tool_calls=[], model="fake",
                          provider="fake", tokens_in=10, tokens_out=5,
                          reasoning_tokens=rt)


def _run_multi(tmp_path, provider):
    engine = Engine(db_path=str(tmp_path / "t.db"))
    engine.run_tool_use(provider, _MultiLegAttack(), "target")
    return engine.storage.list_runs(limit=1)[0]


def test_the_burn_is_summed_across_legs_not_taken_from_the_last(tmp_path):
    """A cost attack's cost is the whole conversation, not its final leg."""
    assert _run_multi(tmp_path, _VaryingProvider([1000, 3000]))["reasoning_tokens"] == 4000


def test_prompt_tokens_sum_across_legs_too(tmp_path):
    row = _run_multi(tmp_path, _VaryingProvider([1, 1]))
    assert row["tokens_in"] == 20
    assert row["tokens_out"] == 10


def test_a_leg_reporting_nothing_does_not_zero_the_total(tmp_path):
    """One silent leg must not erase what the others measured."""
    assert _run_multi(tmp_path, _VaryingProvider([None, 2500]))["reasoning_tokens"] == 2500


def test_all_legs_silent_leaves_the_total_unknown(tmp_path):
    assert _run_multi(tmp_path, _VaryingProvider([None, None]))["reasoning_tokens"] is None
