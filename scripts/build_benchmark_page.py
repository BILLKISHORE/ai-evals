"""Generate a responsible model-robustness benchmark page from the run datasets.

Publishes AGGREGATE statistics only: model, date, totals, block rate, and a
per-category breakdown. It never reads or emits attack prompts, model outputs,
or conversations. The raw `target` text and the `*_with_conversations` arrays
are deliberately ignored. This is how safety benchmarks are published
responsibly: the numbers and methodology, never the payloads.

Run: python scripts/build_benchmark_page.py
"""

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "research" / "model-robustness.mdx"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Longest-match wins, so "biological-weapons" beats "weapons".
KNOWN_CATS = sorted([
    "system-prompt-leakage", "biological-weapons", "chemical-weapons",
    "radiological-weapons", "nuclear-weapons", "phishing", "malware", "weapons",
    "drugs", "cybercrime", "fraud", "hate-speech", "self-harm", "misinformation",
    "privacy-violation", "harassment", "social-engineering",
], key=len, reverse=True)

BENCHES = [
    {"path": "writeups/haiku-benchmark-dataset.json", "runs_key": "all_runs",
     "title": "Claude Haiku 4.5 (general harm)"},
    {"path": "writeups/asl3-benchmark-dataset.json", "runs_key": "all_runs",
     "title": "Claude Haiku 4.5 (ASL-3 / CBRN focus)"},
    {"path": "experiments/2026-04-03-gpt54-benchmark/gpt54-benchmark-dataset.json",
     "runs_key": "runs", "title": "GPT-5.4 (general harm)"},
]


def detect_cat(attack_label: str) -> str:
    s = (attack_label or "").lower()
    for c in KNOWN_CATS:
        if c in s:
            return c
    return "other"


def load_bench(spec):
    d = json.load(open(ROOT / spec["path"]))
    runs = d.get(spec["runs_key"], [])
    meta = d.get("metadata", d.get("benchmark", {}))
    verdicts = Counter(r.get("verdict", "?") for r in runs)
    by_cat = defaultdict(lambda: Counter())
    for r in runs:
        by_cat[detect_cat(r.get("attack", ""))][r.get("verdict", "?")] += 1
    total = len(runs)
    blocked = verdicts.get("BLOCKED", 0)
    return {
        "title": spec["title"],
        "model": meta.get("model", "unknown"),
        "date": meta.get("date", "unknown"),
        "version": meta.get("framework", "") and meta.get("version", "") or meta.get("version", meta.get("framework", "")),
        "evaluator": meta.get("evaluator", "keyword + regex (automated, self-scored)"),
        "total": total,
        "blocked": blocked,
        "bypassed": verdicts.get("BYPASSED", 0),
        "partial": verdicts.get("PARTIAL", 0),
        "unclear": verdicts.get("UNCLEAR", 0),
        "block_rate": round(100 * blocked / total, 1) if total else 0,
        "by_cat": by_cat,
    }


def cat_table(by_cat):
    lines = ["| Harm category | Tested | Blocked | Block rate | Flagged (unverified) |",
             "|---------------|--------|---------|------------|----------------------|"]
    for cat in sorted(by_cat, key=lambda c: -by_cat[c].get("BLOCKED", 0) - sum(by_cat[c].values())):
        c = by_cat[cat]
        tot = sum(c.values())
        blk = c.get("BLOCKED", 0)
        flagged = c.get("BYPASSED", 0) + c.get("PARTIAL", 0)
        rate = round(100 * blk / tot, 1) if tot else 0
        lines.append(f"| {cat} | {tot} | {blk} | {rate}% | {flagged} |")
    return "\n".join(lines)


def main():
    benches = [load_bench(b) for b in BENCHES]

    fm = (
        "---\n"
        'title: "Model Robustness Benchmarks"\n'
        'description: "Aggregate results from running ai-blackteam against frontier models. Block rates and methodology, no payloads."\n'
        "---\n\n"
    )

    body = []
    body.append(
        "These are aggregate results from running ai-blackteam against frontier "
        "models. The focus is **robustness**: how often each model **blocked** an "
        "attack attempt. We publish the numbers and the methodology. We do not "
        "publish attack prompts or model outputs."
    )
    body.append("")
    body.append("<Warning>")
    body.append(
        "  These verdicts come from the framework's **automated** evaluator "
        "(keyword and regex matching), not human review. Automated scoring has a "
        "high false-positive rate, a response that merely mentions a sensitive "
        "term can be flagged. So the \"flagged\" counts overstate real bypasses; "
        "treat the **block rate** as the reliable signal and the flagged counts as "
        "an upper bound that needs human verification."
    )
    body.append("</Warning>")
    body.append("")

    # cross-model summary
    body.append("## Summary")
    body.append("")
    body.append("| Benchmark | Model | Prompts | Blocked | Flagged (unverified) | Unclear |")
    body.append("|-----------|-------|---------|---------|----------------------|---------|")
    for b in benches:
        flagged = b["bypassed"] + b["partial"]
        body.append(
            f"| {b['title']} | `{b['model']}` | {b['total']} | "
            f"{b['blocked']} ({b['block_rate']}%) | {flagged} | {b['unclear']} |"
        )
    body.append("")
    body.append("<Note>")
    body.append(
        "  Block rate is blocked divided by total prompts. UNCLEAR responses "
        "(neither a clear refusal nor a clear bypass) are counted separately and "
        "are **not** failures. The automated evaluator behaves differently across "
        "runs, so these rates are **not** directly comparable across benchmarks. "
        "Read each as within-benchmark signal, not a cross-model leaderboard."
    )
    body.append("</Note>")
    body.append("")

    for b in benches:
        body.append(f"## {b['title']}")
        body.append("")
        body.append(
            f"Model `{b['model']}`, run on {b['date']}. {b['total']} attack attempts, "
            f"of which **{b['blocked']} were blocked ({b['block_rate']}%)**. "
            f"{b['bypassed']} were flagged as bypassed and {b['partial']} as partial "
            f"by the automated evaluator (unverified)."
            + (f" {b['unclear']} were unclear." if b["unclear"] else "")
        )
        body.append("")
        body.append(cat_table(b["by_cat"]))
        body.append("")

    body.append("## Methodology")
    body.append("")
    body.append(
        "Each attack is a prompt generated by an ai-blackteam technique against a "
        "harm target. The model's response is scored BLOCKED, PARTIAL, BYPASSED, or "
        "UNCLEAR by the automated evaluator. These runs used the keyword and regex "
        "evaluator without the optional LLM judge, so scores are fast but noisy."
    )
    body.append("")
    body.append("## What we do not publish, and why")
    body.append("")
    body.append(
        "We never publish the attack prompts or the model outputs. Publishing "
        "working jailbreaks or harmful content would cause real-world harm and is "
        "the opposite of responsible safety research. Any genuine, verified finding "
        "is reported privately to the model vendor through coordinated disclosure, "
        "never posted publicly. The value here is the aggregate signal, which "
        "models resist which attack families, not a how-to."
    )
    body.append("")

    OUT.write_text(fm + "\n".join(body).rstrip() + "\n")
    print(f"wrote {OUT} from {len(benches)} benchmarks (aggregate only, no payloads)")


if __name__ == "__main__":
    main()
