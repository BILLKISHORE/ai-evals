"""Reproducibility helpers for ai_blackteam evals.

The goal: when a regulator or auditor reruns an ai_blackteam evaluation, they should
get bit-for-bit equivalent attack prompts and (modulo provider determinism)
materially equivalent verdicts. To make that possible we capture:

* ai_blackteam version
* the SHA-256 of the sorted, comma-joined list of registered ``technique_id``
* Python interpreter version
* the seed that was pinned (if any)
* provider/model name + temperature (best-effort, supplied by caller)
* dataset hash (if any)

The manifest is a frozen dataclass with a stable ``to_json()`` serialisation,
so it can be embedded in evidence ZIPs and compared across runs.

Side-effect-free import: numpy and torch are imported lazily inside the
``pinned_seed`` context manager, never at module import time. That keeps
ai_blackteam's import surface light and avoids pulling heavy ML deps into the
backend just to render a manifest.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import sys
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from ai_blackteam.registry import attack_registry

__all__ = [
    "ReproducibilityManifest",
    "compute_attack_registry_hash",
    "pinned_seed",
]


def _ai_blackteam_version() -> str:
    """Best-effort ai_blackteam version lookup. Falls back to ``"unknown"`` so the
    manifest is never blocked by a missing package metadata install."""
    try:
        from importlib.metadata import version as _pkg_version

        return _pkg_version("ai_blackteam")
    except Exception:
        return os.environ.get("AI_BLACKTEAM_VERSION", "unknown")


def compute_attack_registry_hash() -> str:
    """SHA-256 of the registered technique IDs in sorted order.

    Two runs with the same registry hash should expose the same attack
    surface. Plugins (registered via ``ai_blackteam.plugin_sdk``) participate
    automatically, once a plugin is imported, its technique_id is in the
    registry and contributes to the hash.
    """
    ids = sorted(attack_registry.list())
    payload = ",".join(ids).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class ReproducibilityManifest:
    """JSON-serialisable manifest of everything we need to reproduce a run.

    Frozen so a caller can't accidentally mutate it between capture and
    write-to-zip. ``to_json()`` uses ``sort_keys=True`` so two manifests
    with identical fields hash to the same digest byte-for-byte.
    """

    ai_blackteam_version: str
    python_version: str
    attack_registry_hash: str
    attack_count: int
    captured_at: str
    seed: int | None = None
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None
    dataset_hash: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def capture(
        cls,
        *,
        seed: int | None = None,
        provider: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        dataset_hash: str | None = None,
        extra: dict[str, Any] | None = None,
    ) -> "ReproducibilityManifest":
        """Snapshot the current process + registry into a manifest."""
        return cls(
            ai_blackteam_version=_ai_blackteam_version(),
            python_version=sys.version.split()[0],
            attack_registry_hash=compute_attack_registry_hash(),
            attack_count=len(attack_registry.list()),
            captured_at=datetime.now(timezone.utc).isoformat(),
            seed=seed,
            provider=provider,
            model=model,
            temperature=temperature,
            dataset_hash=dataset_hash,
            extra=dict(extra or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        """Stable, sorted JSON. Auditors can sha256 the bytes directly."""
        return json.dumps(self.to_dict(), sort_keys=True, indent=2)


@contextmanager
def pinned_seed(seed: int):
    """Pin RNG state for the duration of the context.

    Always pins Python's ``random`` module. Best-effort pins NumPy and
    PyTorch if they happen to be importable; both are optional. On exit
    the prior RNG state is restored so callers (tests, in particular)
    don't bleed state into the next test.

    Note: this seeds CPU RNGs only. CUDA RNGs and provider-side sampling
    (the actual model's temperature) are not under our control. For
    deterministic provider output, set ``temperature=0`` and capture the
    value via the manifest.
    """
    if not isinstance(seed, int):
        raise TypeError(f"pinned_seed: seed must be int, got {type(seed).__name__}")

    py_state = random.getstate()
    random.seed(seed)

    np_state: Any = None
    try:
        import numpy as _np  # type: ignore[import-not-found]

        np_state = _np.random.get_state()
        _np.random.seed(seed)
    except ImportError:
        _np = None  # type: ignore[assignment]

    torch_state: Any = None
    torch_cuda_state: Any = None
    try:
        import torch as _torch  # type: ignore[import-not-found]

        torch_state = _torch.random.get_rng_state()
        _torch.manual_seed(seed)
        if _torch.cuda.is_available():
            torch_cuda_state = _torch.cuda.get_rng_state_all()
            _torch.cuda.manual_seed_all(seed)
    except ImportError:
        _torch = None  # type: ignore[assignment]

    try:
        yield seed
    finally:
        random.setstate(py_state)
        if np_state is not None:
            try:
                _np.random.set_state(np_state)  # type: ignore[union-attr]
            except Exception:  # pragma: no cover, restore is best-effort
                pass
        if torch_state is not None:
            try:
                _torch.random.set_rng_state(torch_state)  # type: ignore[union-attr]
                if torch_cuda_state is not None:
                    _torch.cuda.set_rng_state_all(torch_cuda_state)  # type: ignore[union-attr]
            except Exception:  # pragma: no cover
                pass
