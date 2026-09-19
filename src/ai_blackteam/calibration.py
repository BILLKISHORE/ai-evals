"""Measure whether the evaluator's verdicts are actually correct.

Every score this tool reports rests on ``evaluate()`` assigning the right
verdict to a response, and until now nothing measured that. A safety score is
only as trustworthy as the classifier behind it, so this module scores the
evaluator against human-labeled responses and reports precision, recall and F1
per verdict class.

The labeled set lives in ``data/calibration.jsonl``. It is deliberately small
and honest about it: a handful of verified examples is enough to catch gross
regressions and nowhere near enough to publish an accuracy claim. Grow it, and
report the sample size next to any number taken from it.

Undefined scores are reported as None rather than 0.0. A class with no support
has no precision, and printing zero would make a small set look worse than it
is while hiding that the real problem is missing data.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

VERDICT_CLASSES = ("BLOCKED", "PARTIAL", "BYPASSED")

DEFAULT_SET = Path(__file__).parent / "data" / "calibration.jsonl"


@dataclass(frozen=True)
class LabeledExample:
    """One human-verified (target, response, verdict) triple.

    ``label`` is what a human said the verdict should be. ``source`` records
    where the example and its label came from, so a disputed label can be
    traced rather than argued about.
    """

    id: str
    target: str
    response: str
    label: str
    source: str
    notes: str = ""
    metadata: dict = field(default_factory=dict)


def load_labeled_set(path=None):
    """Read the JSONL labeled set. Raises on an unknown label."""
    path = Path(path) if path else DEFAULT_SET
    examples = []
    with open(path) as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            row = json.loads(line)
            label = row.get("label")
            if label not in VERDICT_CLASSES:
                raise ValueError(
                    f"{path}:{lineno}: unknown label {label!r}; "
                    f"expected one of {', '.join(VERDICT_CLASSES)}"
                )
            examples.append(LabeledExample(
                id=str(row["id"]),
                target=row["target"],
                response=row["response"],
                label=label,
                source=row["source"],
                notes=row.get("notes", ""),
                metadata=row.get("metadata", {}),
            ))
    return examples


def evaluate_prediction(example):
    """Run the production evaluator and return its verdict.

    Offline by default: the LLM-judge path is excluded so the harness measures
    the deterministic keyword and regex logic without spending money or
    introducing run-to-run variance. Pass a different predict function to
    measure the judge.
    """
    from ai_blackteam.evaluator import evaluate

    return evaluate(example.response, example.target, methods=["keyword", "regex"])["verdict"]


def confusion_matrix(examples, predict):
    """Counter keyed by (true_label, predicted_label)."""
    cm = Counter()
    for e in examples:
        cm[(e.label, predict(e))] += 1
    return cm


def score_evaluator(examples, predict):
    """Precision, recall, F1 per verdict class, plus overall accuracy.

    Returns accuracy None for an empty set rather than 1.0: measuring nothing
    is not a perfect score. This mirrors the same decision in ``scoring.py``,
    where an empty run reports no score instead of a vacuous pass.
    """
    total = len(examples)
    if total == 0:
        return {
            "total": 0,
            "accuracy": None,
            "per_class": {c: _empty_class() for c in VERDICT_CLASSES},
            "confusion": Counter(),
        }

    cm = confusion_matrix(examples, predict)
    correct = sum(n for (true, pred), n in cm.items() if true == pred)

    per_class = {}
    for cls in VERDICT_CLASSES:
        tp = cm[(cls, cls)]
        fp = sum(n for (true, pred), n in cm.items() if pred == cls and true != cls)
        fn = sum(n for (true, pred), n in cm.items() if true == cls and pred != cls)
        support = tp + fn
        precision = tp / (tp + fp) if (tp + fp) else None
        recall = tp / support if support else None
        if precision is None or recall is None or (precision + recall) == 0:
            f1 = None if support == 0 else 0.0
        else:
            f1 = 2 * precision * recall / (precision + recall)
        per_class[cls] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": support,
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
        }

    return {
        "total": total,
        "accuracy": correct / total,
        "per_class": per_class,
        "confusion": cm,
    }


def _empty_class():
    return {
        "precision": None, "recall": None, "f1": None,
        "support": 0, "true_positives": 0,
        "false_positives": 0, "false_negatives": 0,
    }


def format_report(metrics, sample_note=True):
    """Plain-text report. Always prints the sample size next to the scores."""
    lines = []
    total = metrics["total"]
    acc = metrics["accuracy"]
    lines.append(f"Labeled examples: {total}")
    lines.append(f"Accuracy:         {'n/a' if acc is None else f'{acc:.1%}'}")
    lines.append("")
    lines.append(f"{'class':10}{'prec':>8}{'recall':>8}{'f1':>8}{'support':>9}")
    for cls in VERDICT_CLASSES:
        c = metrics["per_class"][cls]
        fmt = lambda v: "  n/a" if v is None else f"{v:.2f}"
        lines.append(
            f"{cls:10}{fmt(c['precision']):>8}{fmt(c['recall']):>8}"
            f"{fmt(c['f1']):>8}{c['support']:>9}"
        )
    if metrics["confusion"]:
        lines.append("")
        lines.append("Confusion (true -> predicted):")
        for (true, pred), n in sorted(metrics["confusion"].items()):
            mark = "" if true == pred else "   <- error"
            lines.append(f"  {true:9} -> {pred:9} {n:4}{mark}")
    if sample_note and total < 100:
        lines.append("")
        lines.append(
            f"NOTE: {total} examples is a regression guard, not a published "
            "accuracy claim. Quote the sample size with any number taken from "
            "this set, and grow it before making a claim."
        )
    return "\n".join(lines)


def export_candidates(storage, limit=500, only_disagreements=False):
    """Pull labelable runs out of a results store.

    This is how the labeled set grows past its seed. A run is only labelable if
    its assistant response was stored, so runs without turn text are skipped
    rather than emitted with an empty response. (The published asl3 export has
    exactly this problem: 637 of its 679 rows carry a verdict and no text, so
    only the 42 findings can ever be labeled, and those are all positives.)

    Each candidate records what the tool predicted and, where the provider
    supplied one, the vendor's own stop reason. Rows where those two disagree
    are the highest-value ones to label first: they are where the evaluator and
    ground truth actually diverge.
    """
    from ai_blackteam.providers.base import _refused_from

    candidates = []
    for run in storage.list_runs(limit=limit):
        response = _assistant_text(storage, run["id"])
        if not response:
            continue
        predicted = run["verdict"]
        stop_reason = _row_get(run, "stop_reason")
        vendor_refused = _refused_from(stop_reason)
        disagreement = (
            vendor_refused is not None
            and ((vendor_refused and predicted != "BLOCKED")
                 or (not vendor_refused and predicted == "BLOCKED"))
        )
        if only_disagreements and not disagreement:
            continue
        candidates.append({
            "id": f"run-{run['id']}",
            "target": run["target"],
            "response": response,
            "label": None,
            "source": f"{run['provider']}:{run['model']} run {run['id']} ({run['timestamp'][:10]})",
            "notes": "",
            "predicted": predicted,
            "stop_reason": stop_reason,
            "disagreement": disagreement,
            "metadata": {"attack": run["attack"], "mode": run["mode"]},
        })
    return candidates


def _assistant_text(storage, run_id):
    rows = storage.get_turns(run_id) if hasattr(storage, "get_turns") else []
    texts = [r["content"] for r in rows if r["role"] == "assistant" and r["content"]]
    return "\n".join(texts).strip()


def _row_get(row, key):
    try:
        return row[key]
    except (KeyError, IndexError):
        return None
