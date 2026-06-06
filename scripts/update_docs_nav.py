"""Add the 'How It Works' tab (front door) and the catalog + strategies groups
to docs/docs.json. Idempotent: running twice does not duplicate entries.
Run: python scripts/update_docs_nav.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CFG = DOCS / "docs.json"

LESSON_PAGES = [
    "how-it-works/what-it-is",
    "how-it-works/attack-surface",
    "how-it-works/the-big-picture",
    "how-it-works/the-contracts",
    "how-it-works/the-evaluator",
    "how-it-works/standards-and-reports",
    "how-it-works/extra-tools",
    "how-it-works/usability",
]

HOW_IT_WORKS_TAB = {
    "tab": "How It Works",
    "icon": "graduation-cap",
    "groups": [{"group": "Start Here", "pages": LESSON_PAGES}],
}


def strategy_pages():
    strat = DOCS / "attacks" / "strategies"
    slugs = sorted(p.stem for p in strat.glob("*.mdx") if p.stem != "overview")
    return ["attacks/strategies/overview"] + [f"attacks/strategies/{s}" for s in slugs]


def catalog_pages():
    cat = DOCS / "attacks" / "catalog"
    slugs = sorted(p.stem for p in cat.glob("*.mdx") if p.stem != "overview")
    return [f"attacks/catalog/{s}" for s in slugs]


def main():
    cfg = json.loads(CFG.read_text())
    tabs = cfg["navigation"]["tabs"]

    # 1) Insert "How It Works" as the first tab (idempotent).
    tabs[:] = [t for t in tabs if t.get("tab") != "How It Works"]
    tabs.insert(0, HOW_IT_WORKS_TAB)

    # 2) Augment the Attack Catalog tab with full reference + strategies.
    for tab in tabs:
        if tab.get("tab") != "Attack Catalog":
            continue
        groups = tab["groups"]
        groups[:] = [g for g in groups if g.get("group") not in
                     ("Full Reference", "Attacks by Category", "Attack Strategies")]
        ref_group = {"group": "Full Reference", "pages": ["attacks/all-attacks", "attacks/all-categories", "attacks/catalog/overview"]}
        catalog_group = {"group": "Attacks by Category", "pages": catalog_pages()}
        strat_group = {"group": "Attack Strategies", "pages": strategy_pages()}
        # Full Reference + per-category catalog right after Overview, strategies at the end.
        insert_at = 1 if groups and groups[0].get("group") == "Overview" else 0
        groups.insert(insert_at, ref_group)
        groups.insert(insert_at + 1, catalog_group)
        groups.append(strat_group)

    CFG.write_text(json.dumps(cfg, indent=2) + "\n")
    print("nav updated:")
    print("  + How It Works tab (first):", len(LESSON_PAGES), "lessons")
    print("  + Attack Catalog: Full Reference (2 pages) + Attack Strategies (",
          len(strategy_pages()), "pages)")


if __name__ == "__main__":
    main()
