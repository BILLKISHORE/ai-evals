"""Generate the attack catalog docs straight from the live registry.

Produces ground-truth Markdown in ``attack-catalog/``:
  * ATTACKS-CATALOG.md     -- every registered attack, grouped by category
  * CATEGORIES.md          -- one row per category with counts
  * ATTACK-SURFACE-163M.md -- the full 163M expansion breakdown

Run: python scripts/generate_attack_catalog.py
Re-run any time attacks change; the numbers come from the code, not by hand.
"""

from collections import defaultdict
from pathlib import Path

import ai_blackteam.api  # noqa: F401  (forces full registration)
from ai_blackteam.registry import attack_registry
from ai_blackteam.expander import expand_summary
from ai_blackteam.mutations import (
    ENCODING_MUTATIONS,
    FRAMING_TEMPLATES,
    DIFFICULTY_TEMPLATES,
    LANGUAGE_TEMPLATES,
)

OUT = Path(__file__).resolve().parent.parent / "attack-catalog"
OUT.mkdir(exist_ok=True)

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def collect():
    """Return a list of metadata dicts for every registered attack."""
    rows = []
    for tid in attack_registry.list():
        rows.append(attack_registry.get(tid)().metadata())
    rows.sort(key=lambda m: (m["category"], SEVERITY_ORDER.get(m["severity"], 9), m["name"]))
    return rows


def _join(values):
    return ", ".join(values) if values else "-"


def _cell(text):
    """Make a string safe for a Markdown table cell."""
    text = (text or "").replace("|", "\\|").replace("\n", " ").strip()
    return text or "-"


def _owasp_codes(values):
    """Short OWASP codes only (e.g. 'LLM01'), so the table stays narrow."""
    if not values:
        return "-"
    return ", ".join(v.split(":")[0].strip() for v in values)


def write_catalog(rows):
    by_cat = defaultdict(list)
    for m in rows:
        by_cat[m["category"]].append(m)

    lines = [
        "# Attack Catalog",
        "",
        f"Every attack registered in ai-blackteam, generated directly from the code.",
        "",
        f"- **Total attacks:** {len(rows)}",
        f"- **Categories:** {len(by_cat)}",
        "- **Source of truth:** the live `attack_registry` (not hand-typed)",
        "",
        "Each attack lists its technique id, severity, mode, and standards mapping.",
        "",
        "---",
        "",
    ]

    for cat in sorted(by_cat):
        items = by_cat[cat]
        lines.append(f"## {cat} ({len(items)})")
        lines.append("")
        lines.append("| Attack | Technique ID | Severity | Mode | OWASP | MITRE ATLAS | Description |")
        lines.append("|--------|--------------|----------|------|-------|-------------|-------------|")
        for m in items:
            lines.append(
                f"| {m['name']} | `{m['technique_id']}` | {m['severity']} | "
                f"{m['mode']} | {_owasp_codes(m['owasp_llm'])} | {_join(m['mitre_atlas'])} | {_cell(m['description'])} |"
            )
        lines.append("")
    (OUT / "ATTACKS-CATALOG.md").write_text("\n".join(lines))


def write_categories(rows):
    by_cat = defaultdict(list)
    for m in rows:
        by_cat[m["category"]].append(m)

    lines = [
        "# Attack Categories",
        "",
        f"ai-blackteam groups its {len(rows)} attacks into {len(by_cat)} categories.",
        "",
        "| Category | Attacks | Top severity | Modes | Example techniques |",
        "|----------|---------|--------------|-------|--------------------|",
    ]
    for cat in sorted(by_cat, key=lambda c: -len(by_cat[c])):
        items = by_cat[cat]
        sev = sorted({m["severity"] for m in items}, key=lambda s: SEVERITY_ORDER.get(s, 9))
        modes = sorted({m["mode"] for m in items})
        examples = ", ".join(f"`{m['technique_id']}`" for m in items[:3])
        lines.append(
            f"| {cat} | {len(items)} | {sev[0]} | {_join(modes)} | {examples} |"
        )
    lines.append("")
    (OUT / "CATEGORIES.md").write_text("\n".join(lines))


def write_surface():
    s = expand_summary()
    lines = [
        "# The 163 Million Attack Surface (full breakdown)",
        "",
        "This number is real and computed by the code. It is **not** 163 million",
        "hand-written attacks. It is a combinatorial space built by mixing a small",
        "set of building blocks across five axes.",
        "",
        "## Building blocks (the real, hand-built pieces)",
        "",
        f"- **{s['techniques']:,} attack techniques** (the recipes)",
        f"- **{s['dataset_prompts']:,} dataset prompts** (from 19 public benchmarks)",
        f"- Of the techniques, **{s['single_turn_techniques']:,}** are single-turn "
        "(used in the dataset expansion)",
        "",
        "## The five mixing axes",
        "",
        f"### 1. Harm categories ({s['categories']})",
        "",
        ", ".join(f"`{c}`" for c in s["category_names"]),
        "",
        f"### 2. Difficulty levels ({len(DIFFICULTY_TEMPLATES)})",
        "",
        ", ".join(f"`{d}`" for d in DIFFICULTY_TEMPLATES),
        "",
        f"### 3. Mutations ({s['mutations']} = "
        f"{len(ENCODING_MUTATIONS)} encoding + {len(FRAMING_TEMPLATES)} framing + "
        f"{len(DIFFICULTY_TEMPLATES)} difficulty)",
        "",
        f"- **Encoding ({len(ENCODING_MUTATIONS)}):** "
        + ", ".join(f"`{x}`" for x in ENCODING_MUTATIONS),
        f"- **Framing ({len(FRAMING_TEMPLATES)}):** "
        + ", ".join(f"`{x}`" for x in FRAMING_TEMPLATES),
        f"- **Difficulty ({len(DIFFICULTY_TEMPLATES)}):** "
        + ", ".join(f"`{x}`" for x in DIFFICULTY_TEMPLATES),
        "",
        f"### 4. Languages ({s['languages']})",
        "",
        ", ".join(f"`{x}`" for x in LANGUAGE_TEMPLATES),
        "",
        "### 5. Which technique is applied",
        "",
        f"Any of the {s['techniques']:,} techniques can be paired with a dataset prompt.",
        "",
        "## The math (step by step)",
        "",
        "```",
        "Part 1 -- technique expansion:",
        f"  {s['techniques']:,} techniques x {s['categories']} categories "
        f"x {s['difficulties']} difficulties = {s['base_expanded']:,}",
        f"  {s['base_expanded']:,} x (1 original + {s['mutations']} mutations "
        f"+ {s['languages']} languages) = {s['full_expansion']:,}",
        "",
        "Part 2 -- dataset expansion:",
        f"  {s['dataset_prompts']:,} dataset prompts x {s['mutations']} mutations "
        f"x {s['single_turn_techniques']:,} single-turn techniques = {s['dataset_with_mutations']:,}",
        "",
        "Total:",
        f"  {s['full_expansion']:,} + {s['dataset_with_mutations']:,} "
        f"= {s['total_attack_surface']:,}",
        "```",
        "",
        f"## Final number: **{s['total_attack_surface']:,}**",
        "",
        "You never run all of them. You **sample** from this space. The point is the",
        "diversity of the search space, not a fixed list of prompts.",
        "",
    ]
    (OUT / "ATTACK-SURFACE-163M.md").write_text("\n".join(lines))


def write_readme(rows):
    by_cat = defaultdict(list)
    for m in rows:
        by_cat[m["category"]].append(m)
    lines = [
        "# Attack Catalog (generated)",
        "",
        "These files are generated from the live code by",
        "`scripts/generate_attack_catalog.py`. Re-run it to refresh.",
        "",
        "| File | What it contains |",
        "|------|------------------|",
        f"| `ATTACKS-CATALOG.md` | All {len(rows)} attacks, grouped by category |",
        f"| `CATEGORIES.md` | All {len(by_cat)} categories with counts |",
        "| `ATTACK-SURFACE-163M.md` | Full breakdown of the 163M attack surface |",
        "",
        f"_Totals: {len(rows)} attacks across {len(by_cat)} categories._",
        "",
    ]
    (OUT / "README.md").write_text("\n".join(lines))


def main():
    rows = collect()
    write_catalog(rows)
    write_categories(rows)
    write_surface()
    write_readme(rows)
    cats = {m["category"] for m in rows}
    print(f"Generated {len(rows)} attacks across {len(cats)} categories into {OUT}")


if __name__ == "__main__":
    main()
