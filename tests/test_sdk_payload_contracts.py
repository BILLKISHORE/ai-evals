"""Validate built payloads against the real vendor types, not against mocks.

Every provider test in this suite asserts the harness's own dict back to
itself through a MagicMock. That proves the code builds the dict it meant to
build; it proves nothing about whether the vendor accepts it. A misspelled or
removed field name passes every one of those tests and fails on the first
real request.

This was not hypothetical. The checked-out virtualenv had google-genai 1.2.0,
whose ThinkingConfig accepts only include_thoughts and sets extra='forbid',
while pyproject and poetry.lock both require 2.24.0. Building a thinking
config against the installed SDK raised a pydantic ValidationError before any
HTTP call, and the entire suite stayed green because nothing ever handed a
payload to a real vendor type.

These tests construct the genuine SDK model. They make no network request:
pydantic validation is local. They fail loudly when the installed SDK and the
code disagree, which is the gap the mocks leave open.
"""

import pytest

from ai_blackteam.reasoning import EFFORT_LEVELS


# ── Google ───────────────────────────────────────────────────────────


@pytest.mark.parametrize("effort", EFFORT_LEVELS)
def test_google_thinking_config_is_accepted_by_the_real_sdk_type(effort):
    """The built config must validate against types.GenerateContentConfig."""
    types = pytest.importorskip("google.genai.types")
    from ai_blackteam.reasoning import google_thinking_config

    cfg = google_thinking_config(effort, "gemini-2.5-pro")
    if cfg is None:
        pytest.skip(f"no thinking config produced for effort={effort}")
    # Raises pydantic.ValidationError if a field name is wrong or unknown.
    built = types.GenerateContentConfig(thinking_config=cfg)
    assert built.thinking_config is not None


def test_every_google_thinking_field_exists_on_the_installed_sdk():
    """Catches a field the code sends that the pinned SDK does not define."""
    types = pytest.importorskip("google.genai.types")
    from ai_blackteam.reasoning import google_thinking_config

    known = set(types.ThinkingConfig.model_fields)
    sent = set()
    for effort in EFFORT_LEVELS:
        cfg = google_thinking_config(effort, "gemini-2.5-pro") or {}
        sent |= set(cfg)
        cfg = google_thinking_config(effort, "gemini-3.5-flash") or {}
        sent |= set(cfg)
    unknown = sent - known
    assert not unknown, f"fields the installed google-genai does not accept: {unknown}"


# ── OpenAI ───────────────────────────────────────────────────────────


def test_openai_reasoning_effort_values_match_the_sdk_literal():
    """The vendor constrains reasoning_effort to a fixed set of strings.

    If the SDK narrows that set, a level this tool offers becomes a 400 that
    only appears at run time.
    """
    pytest.importorskip("openai")
    import typing

    try:
        from openai.types.shared.reasoning_effort import ReasoningEffort
    except ImportError:
        pytest.skip("installed openai SDK does not expose ReasoningEffort")

    allowed = set()
    for arg in typing.get_args(ReasoningEffort):
        if isinstance(arg, str):
            allowed.add(arg)
        else:
            allowed |= {a for a in typing.get_args(arg) if isinstance(a, str)}
    if not allowed:
        pytest.skip("could not introspect the ReasoningEffort literal")

    from ai_blackteam.reasoning import EFFORT_LEVELS as levels
    unsupported = {lv for lv in levels if lv not in allowed}
    assert not unsupported, (
        f"effort levels the installed openai SDK rejects: {sorted(unsupported)}; "
        f"SDK allows {sorted(allowed)}"
    )


def test_the_installed_openai_sdk_has_the_responses_api():
    """The Responses path is the only one carrying a reasoning summary."""
    pytest.importorskip("openai")
    from openai import OpenAI

    client = OpenAI(api_key="test-not-real")
    assert hasattr(client, "responses"), (
        "the pinned openai SDK has no Responses API; the reasoning-trace path "
        "cannot work against it"
    )
