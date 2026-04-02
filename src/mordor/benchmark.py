"""Benchmark runner for mordor.

Runs all attacks against a curated set of harmful targets
and produces a safety score.
"""

from pathlib import Path

import yaml

from mordor.registry import attack_registry
from mordor.scoring import score_results

BENCHMARK_FILE = Path(__file__).parent / "data" / "benchmark.yaml"


def load_benchmark(categories=None):
    """Load benchmark targets from YAML.

    Args:
        categories: optional list of category names to filter

    Returns:
        dict mapping category -> list of target dicts
    """
    data = yaml.safe_load(BENCHMARK_FILE.read_text())
    if categories:
        data = {k: v for k, v in data.items() if k in categories}
    return data


def get_attacks_metadata():
    """Build a dict mapping attack_id -> metadata for scoring."""
    metadata = {}
    for name in attack_registry.list():
        cls = attack_registry.get(name)
        attack = cls()
        metadata[name] = attack.metadata()
    return metadata


def run_benchmark(engine, provider, attacks=None, categories=None, max_workers=5, on_progress=None):
    """Run the full benchmark and return scored results.

    Args:
        engine: Engine instance
        provider: Provider instance
        attacks: optional list of attack names (defaults to all)
        categories: optional list of benchmark categories to test
        max_workers: parallel workers
        on_progress: callback(attack_name, target, result) called after each run

    Returns:
        dict with scores, per-target results, and metadata
    """
    benchmark = load_benchmark(categories)
    attack_names = attacks or attack_registry.list()

    attack_objects = []
    for name in attack_names:
        cls = attack_registry.get(name)
        if cls:
            attack_objects.append(cls())

    attacks_metadata = get_attacks_metadata()

    all_results = []
    target_results = []

    for category, targets in benchmark.items():
        for target_info in targets:
            target = target_info["target"]
            difficulty = target_info.get("difficulty", "medium")

            # Run all attacks against this target
            batch_results = engine.run_batch_parallel(
                provider, attack_objects, target, max_workers=max_workers
            )

            for entry in batch_results:
                attack_id = entry["attack"]
                results = entry["results"]
                error = entry.get("error")

                if error:
                    verdict = "UNCLEAR"
                elif isinstance(results, list):
                    # Single-turn: worst verdict across variants
                    verdicts = [r["verdict"] for r in results]
                    if "BYPASSED" in verdicts:
                        verdict = "BYPASSED"
                    elif "PARTIAL" in verdicts:
                        verdict = "PARTIAL"
                    else:
                        verdict = "BLOCKED"
                elif isinstance(results, dict):
                    verdict = results.get("verdict", "UNCLEAR")
                else:
                    verdict = "UNCLEAR"

                all_results.append({
                    "attack": attack_id,
                    "verdict": verdict,
                    "target_category": category,
                    "target": target[:80],
                    "difficulty": difficulty,
                    "mlcommons": target_info.get("mlcommons"),
                })

                if on_progress:
                    on_progress(attack_id, target, verdict)

            target_results.append({
                "category": category,
                "target": target[:80],
                "difficulty": difficulty,
                "mlcommons": target_info.get("mlcommons"),
                "attacks_run": len(batch_results),
                "bypassed": sum(1 for r in batch_results if _get_verdict(r) == "BYPASSED"),
                "blocked": sum(1 for r in batch_results if _get_verdict(r) == "BLOCKED"),
            })

    scores = score_results(all_results, attacks_metadata)
    scores["model"] = provider.model
    scores["provider"] = provider.get_model_info()["provider"]
    scores["targets_tested"] = len(target_results)
    scores["attacks_per_target"] = len(attack_objects)
    scores["target_results"] = target_results

    return scores


def _get_verdict(entry):
    results = entry.get("results")
    if entry.get("error"):
        return "UNCLEAR"
    if isinstance(results, list):
        verdicts = [r["verdict"] for r in results]
        if "BYPASSED" in verdicts:
            return "BYPASSED"
        if "PARTIAL" in verdicts:
            return "PARTIAL"
        return "BLOCKED"
    if isinstance(results, dict):
        return results.get("verdict", "UNCLEAR")
    return "UNCLEAR"
