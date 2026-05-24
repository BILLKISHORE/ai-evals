"""Audit dataset loaders by running each end-to-end and counting records.

Runs the nine ai-blackteam dataset loaders against their public sources,
counts how many records each returns, captures the first three samples per
loader, and prints a results table plus a Markdown-friendly summary.

Designed to be safe under flaky network conditions: any loader-level
exception is captured and reported, never crashes the whole run.

Usage:
    python scripts/count_records.py
"""

from __future__ import annotations

import sys
import time
import traceback
from dataclasses import dataclass, field
from typing import Any

from ai_blackteam.datasets.aart import AARTLoader
from ai_blackteam.datasets.advbench import AdvBenchLoader
from ai_blackteam.datasets.agentharm import AgentHarmLoader
from ai_blackteam.datasets.beavertails import BeaverTailsLoader
from ai_blackteam.datasets.do_not_answer import DoNotAnswerLoader
from ai_blackteam.datasets.forbidden_questions import ForbiddenQuestionsLoader
from ai_blackteam.datasets.harmbench import HarmBenchLoader
from ai_blackteam.datasets.jailbreakbench import JailbreakBenchLoader
from ai_blackteam.datasets.jailbreakv import JailbreakV28KLoader
from ai_blackteam.datasets.realtoxicityprompts import RealToxicityPromptsLoader
from ai_blackteam.datasets.redbench import RedBenchLoader
from ai_blackteam.datasets.redteam2k import RedTeam2KLoader
from ai_blackteam.datasets.salad_bench import SaladBenchLoader
from ai_blackteam.datasets.sorry_bench import SorryBenchLoader
from ai_blackteam.datasets.strongreject import StrongREJECTLoader
from ai_blackteam.datasets.wildguard import WildGuardLoader
from ai_blackteam.datasets.wmdp import WMDPBioLoader, WMDPChemLoader, WMDPCyberLoader


@dataclass
class LoaderResult:
    name: str
    license: str
    source_url: str
    count: int = 0
    ok: bool = False
    error: str | None = None
    elapsed_s: float = 0.0
    samples: list[dict[str, Any]] = field(default_factory=list)


# Treat each registered loader class as one row, including the three WMDP variants.
# This matches what end users actually pull via the registry.
LOADERS = [
    HarmBenchLoader,
    AdvBenchLoader,
    JailbreakBenchLoader,
    WMDPBioLoader,
    WMDPCyberLoader,
    WMDPChemLoader,
    DoNotAnswerLoader,
    WildGuardLoader,
    RedBenchLoader,
    SaladBenchLoader,
    SorryBenchLoader,
    StrongREJECTLoader,
    AARTLoader,
    ForbiddenQuestionsLoader,
    BeaverTailsLoader,
    RealToxicityPromptsLoader,
    JailbreakV28KLoader,
    RedTeam2KLoader,
    AgentHarmLoader,
]


def run_loader(cls: type) -> LoaderResult:
    loader = cls()
    result = LoaderResult(
        name=getattr(loader, "name", cls.__name__),
        license=getattr(loader, "license", "unknown"),
        source_url=getattr(loader, "source_url", ""),
    )
    started = time.monotonic()
    try:
        # Bypass the cache: we want a fresh end-to-end count, not stale data.
        items = loader.download()
        result.count = len(items)
        result.ok = True
        result.samples = items[:3]
    except Exception as exc:  # noqa: BLE001
        result.ok = False
        result.error = f"{type(exc).__name__}: {exc}"
    finally:
        result.elapsed_s = time.monotonic() - started
    return result


def print_table(results: list[LoaderResult]) -> None:
    header = f"{'dataset':<18} {'count':>8} {'ok':>4} {'time(s)':>8}  source / error"
    print(header)
    print("-" * len(header))
    for r in results:
        marker = "y" if r.ok else "n"
        right = r.source_url if r.ok else (r.error or "")
        print(f"{r.name:<18} {r.count:>8} {marker:>4} {r.elapsed_s:>8.1f}  {right}")


def print_samples(results: list[LoaderResult]) -> None:
    print("\nsample records (first 3 per loader):")
    for r in results:
        print(f"\n--- {r.name} ---")
        if not r.ok:
            print(f"  (failed: {r.error})")
            continue
        if not r.samples:
            print("  (no samples)")
            continue
        for i, s in enumerate(r.samples, 1):
            prompt = str(s.get("prompt", ""))[:140].replace("\n", " ")
            cat = s.get("category", "?")
            print(f"  [{i}] ({cat}) {prompt}")


def main() -> int:
    print(f"running {len(LOADERS)} loaders end-to-end...\n")
    results: list[LoaderResult] = []
    for cls in LOADERS:
        print(f"  -> {cls.__name__} ...", flush=True)
        results.append(run_loader(cls))
    print()
    print_table(results)
    print_samples(results)

    total = sum(r.count for r in results if r.ok)
    failed = [r for r in results if not r.ok]
    print(f"\ntotal dataset records: {total}")
    print(f"failed loaders: {len(failed)}")
    for r in failed:
        print(f"  - {r.name}: {r.error}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
