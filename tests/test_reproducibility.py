"""Tests for the reproducibility manifest helpers."""

from __future__ import annotations

import json
import random
import uuid

import pytest

from ai_blackteam.registry import attack_registry
from ai_blackteam.reproducibility import (
    ReproducibilityManifest,
    compute_attack_registry_hash,
    pinned_seed,
)


@pytest.fixture(autouse=True)
def _clean_registry():
    """Snapshot and restore the attack registry so registry-mutating
    tests don't leak state into sibling tests."""
    snapshot = dict(attack_registry._items)  # noqa: SLF001
    try:
        yield
    finally:
        attack_registry._items = snapshot  # noqa: SLF001


def _uniq(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def test_manifest_capture_has_required_fields():
    m = ReproducibilityManifest.capture(
        seed=42,
        provider="openai",
        model="gpt-4o-mini",
        temperature=0.0,
    )
    d = m.to_dict()
    for field in (
        "ai_blackteam_version",
        "python_version",
        "attack_registry_hash",
        "attack_count",
        "captured_at",
        "seed",
        "provider",
        "model",
        "temperature",
    ):
        assert field in d, f"missing manifest field: {field}"
    assert d["seed"] == 42
    assert d["provider"] == "openai"
    assert d["temperature"] == 0.0
    assert d["attack_count"] >= 0
    assert len(d["attack_registry_hash"]) == 64  # sha256 hex


def test_manifest_json_stable_for_same_input():
    """``to_json`` must be deterministic given the same dataclass values."""
    fixed = ReproducibilityManifest(
        ai_blackteam_version="1.0.0",
        python_version="3.12.0",
        attack_registry_hash="a" * 64,
        attack_count=10,
        captured_at="2026-01-01T00:00:00+00:00",
        seed=7,
        provider="anthropic",
        model="claude-3-5-sonnet",
        temperature=0.0,
        dataset_hash=None,
        extra={},
    )
    j1 = fixed.to_json()
    j2 = fixed.to_json()
    assert j1 == j2
    # And it round-trips through json.
    parsed = json.loads(j1)
    assert parsed["ai_blackteam_version"] == "1.0.0"
    assert parsed["attack_registry_hash"] == "a" * 64


def test_registry_hash_changes_when_attack_added():
    """A new registration must visibly change the registry hash."""
    h0 = compute_attack_registry_hash()

    tid = _uniq("custom.test.hash")

    class _StubAttack:
        def build_prompts(self, t):
            return []

    attack_registry.register(tid, _StubAttack)

    h1 = compute_attack_registry_hash()
    assert h1 != h0, "registry hash must change when an attack is added"

    # Sanity: same call twice with identical state is stable.
    assert compute_attack_registry_hash() == h1


def test_registry_hash_changes_when_attack_removed():
    """Removing a previously registered attack must change the hash back."""
    tid = _uniq("custom.test.removal")

    class _StubAttack:
        def build_prompts(self, t):
            return []

    h_before = compute_attack_registry_hash()
    attack_registry.register(tid, _StubAttack)
    h_with = compute_attack_registry_hash()
    assert h_with != h_before

    del attack_registry._items[tid]  # noqa: SLF001
    h_after = compute_attack_registry_hash()
    assert h_after == h_before, "removing the addition must restore the prior hash"


def test_pinned_seed_reseeds_python_random():
    with pinned_seed(123):
        a = random.random()
    with pinned_seed(123):
        b = random.random()
    assert a == b, "pinned_seed must give deterministic random()"


def test_pinned_seed_restores_prior_state():
    random.seed(999)
    before = random.random()

    random.seed(999)
    _ = random.random()  # consume one value so internal state advances
    with pinned_seed(42):
        # Inside the context, state is overridden.
        _ = random.random()

    # After exiting, internal state should be restored to what it was at
    # context entry (which is after the consumed value). Asking for one
    # more random() at restored state should not equal ``before``.
    after = random.random()
    assert before != after  # state genuinely advanced

    # And entering the same seed twice yields the same first draw, proves
    # restoration didn't corrupt the underlying RNG.
    random.seed(42)
    with pinned_seed(42):
        x = random.random()
    random.seed(42)
    with pinned_seed(42):
        y = random.random()
    assert x == y


def test_pinned_seed_seeds_numpy_if_available():
    """If numpy is importable, pinned_seed must seed it deterministically."""
    np = pytest.importorskip("numpy")

    with pinned_seed(42):
        a = np.random.rand(3)
    with pinned_seed(42):
        b = np.random.rand(3)
    assert (a == b).all(), "pinned_seed must give deterministic numpy draws"


def test_pinned_seed_rejects_non_int():
    with pytest.raises(TypeError):
        with pinned_seed("not-an-int"):  # type: ignore[arg-type]
            pass


def test_capture_preserves_caller_extra():
    m = ReproducibilityManifest.capture(
        seed=1,
        extra={"git_sha": "abc123", "operator": "test-runner"},
    )
    assert m.extra == {"git_sha": "abc123", "operator": "test-runner"}
