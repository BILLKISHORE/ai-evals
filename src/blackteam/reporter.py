import json
from datetime import datetime
from blackteam.storage.sqlite import Storage


def generate_markdown(storage):
    stats = storage.get_stats()
    runs = storage.list_runs(limit=500)

    lines = [
        "# AI Blackteam -- Security Report",
        f"\nGenerated: {datetime.now().isoformat()}",
        f"\n## Summary",
        f"- Total runs: {stats['total_runs']}",
        f"- Bypassed: {stats['bypassed']}",
        f"- Blocked: {stats['blocked']}",
        f"- Models tested: {stats['models_tested']}",
        f"- Attacks used: {stats['attacks_used']}",
        "",
        "## Results",
        "",
        "| # | Model | Attack | Verdict | Confidence |",
        "|---|-------|--------|---------|------------|",
    ]

    for run in reversed(runs):
        lines.append(
            f"| {run['id']} | {run['model']} | {run['attack']} | "
            f"{run['verdict']} | {run['confidence']:.2f} |"
        )

    return "\n".join(lines) + "\n"


def generate_json(storage):
    runs = storage.list_runs(limit=500)
    stats = storage.get_stats()
    return json.dumps({"stats": stats, "runs": runs}, indent=2, default=str)
