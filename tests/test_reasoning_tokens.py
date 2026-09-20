"""A reasoning token count must survive the trip from vendor to database.

The storage column and the engine's write were added together, but nothing
in between carried a value: PromptResult had no such field, so the engine's
`getattr(result, "reasoning_tokens", None)` could only ever resolve to None.
The column read as wired and was structurally guaranteed to stay NULL.

That is the same shape as the other defects found in this codebase: a path
that cannot fail, because it cannot carry anything either. Reasoning tokens
are the cost signal for the 2026 reasoning-layer attacks, where the whole
point is that thinking is expensive, so a silently empty column would hide
exactly the effect those attacks produce.
"""

from types import SimpleNamespace

from ai_blackteam.engine import Engine
from ai_blackteam.providers.base import (
    BaseProvider,
    PromptResult,
    read_reasoning_tokens,
)


def _usage(reasoning=None, present=True):
    """An OpenAI-shaped usage object."""
    details = SimpleNamespace(reasoning_tokens=reasoning) if present else None
    return SimpleNamespace(
        prompt_tokens=10, completion_tokens=20, completion_tokens_details=details
    )


# ── the field exists ─────────────────────────────────────────────────


def test_prompt_result_carries_a_reasoning_token_count():
    r = PromptResult(response="x", model="m", provider="p", reasoning_tokens=512)
    assert r.reasoning_tokens == 512


def test_reasoning_tokens_default_to_none_not_zero():
    """Unknown is not the same as none spent, and zero would be a lie."""
    r = PromptResult(response="x", model="m", provider="p")
    assert r.reasoning_tokens is None


# ── reading it off a vendor usage object ─────────────────────────────


def test_reads_the_openai_reasoning_token_count():
    assert read_reasoning_tokens(_usage(reasoning=384)) == 384


def test_absent_usage_reads_as_unknown():
    assert read_reasoning_tokens(None) is None


def test_usage_without_a_details_block_reads_as_unknown():
    assert read_reasoning_tokens(_usage(present=False)) is None


def test_a_null_count_stays_unknown():
    """A non-reasoning model returns the block with the field set to None."""
    assert read_reasoning_tokens(_usage(reasoning=None)) is None


def test_a_zero_count_is_kept_as_zero():
    """Zero is a real measurement: the model reasoned for nothing."""
    assert read_reasoning_tokens(_usage(reasoning=0)) == 0


def test_a_non_numeric_count_is_not_passed_through():
    assert read_reasoning_tokens(_usage(reasoning="lots")) is None


def test_the_anthropic_shape_is_read_too():
    usage = SimpleNamespace(output_tokens_details=SimpleNamespace(reasoning_tokens=77))
    assert read_reasoning_tokens(usage) == 77


# ── the engine persists it ───────────────────────────────────────────


class _Provider(BaseProvider):
    def __init__(self, reasoning_tokens=None):
        self._rt = reasoning_tokens

    def default_model(self):
        return "fake-model"

    def send_prompt(self, prompt, system_prompt=None):
        return PromptResult(response="no.", model="fake", provider="fake",
                            reasoning_tokens=self._rt)

    def send_in_conversation(self, messages, system_prompt=None):
        return self.send_prompt("")


class _Attack:
    name = "fake"
    technique_id = "fake"
    mode = "single-turn"

    def generate_prompts(self, target, **kwargs):
        return ["one prompt"]


def _run_and_read(tmp_path, provider):
    engine = Engine(db_path=str(tmp_path / "t.db"))
    engine.run_single(provider, _Attack(), "target")
    return engine.storage.list_runs(limit=1)[0]


def test_a_reported_count_reaches_the_database(tmp_path):
    assert _run_and_read(tmp_path, _Provider(reasoning_tokens=256))["reasoning_tokens"] == 256


def test_an_unreported_count_is_stored_as_null(tmp_path):
    assert _run_and_read(tmp_path, _Provider())["reasoning_tokens"] is None
