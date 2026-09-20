"""Build per-category attack catalog pages using Mintlify <ResponseField>.

Splits the corpus into one page per category (fast to load) and renders
each attack as a ResponseField so the description shows inline with no
horizontal scrolling. Also writes a light index page.

Outputs under docs/attacks/catalog/:
  * overview.mdx          (index linking to every category page)
  * <category>.mdx        (one page per category, ResponseField per attack)

Run: python scripts/build_catalog_pages.py
"""

from collections import defaultdict
from pathlib import Path

import ai_blackteam.api  # noqa: F401  forces registration
from ai_blackteam.registry import attack_registry

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "attacks" / "catalog"
OUT.mkdir(parents=True, exist_ok=True)

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def mdx_safe(text: str) -> str:
    """Escape characters MDX treats specially in body text."""
    return (text or "").replace("{", "&#123;").replace("}", "&#125;").replace("<", "&lt;")


def attr_safe(text: str) -> str:
    """Make a string safe for an MDX attribute value (double-quoted)."""
    return (text or "").replace('"', "'").replace("\n", " ").strip()


def owasp_codes(values):
    return ", ".join(v.split(":")[0].strip() for v in values) if values else ""


def collect():
    by_cat = defaultdict(list)
    for tid in attack_registry.list():
        m = attack_registry.get(tid)().metadata()
        by_cat[m["category"]].append(m)
    for items in by_cat.values():
        items.sort(key=lambda m: (SEVERITY_ORDER.get(m["severity"], 9), m["name"]))
    return by_cat


def render_field(m) -> str:
    meta_bits = [f"`{m['technique_id']}`", m["mode"]]
    if m["owasp_llm"]:
        meta_bits.append(f"OWASP: {owasp_codes(m['owasp_llm'])}")
    if m["mitre_atlas"]:
        meta_bits.append(f"MITRE: {', '.join(m['mitre_atlas'])}")
    meta_line = " &middot; ".join(meta_bits)
    desc = mdx_safe(m["description"]) or "No description."
    cmd = f'ai-blackteam run -p anthropic -a {m["technique_id"]} -t "your target prompt"'
    return (
        f'<ResponseField name="{attr_safe(m["name"])}" type="{attr_safe(m["severity"])}">\n'
        f"  {mdx_safe(meta_line)}\n\n"
        f"  {desc}\n\n"
        f"  **Run it:**\n\n"
        f"  ```bash\n"
        f"  {cmd}\n"
        f"  ```\n"
        f"</ResponseField>"
    )


def write_category_page(cat, items):
    fm = (
        f"---\n"
        f'title: "{cat}"\n'
        f'description: "All {len(items)} attacks in the {cat} category, with severity, mode, and standards mapping."\n'
        f"---\n\n"
    )
    body = [
        f"There are {len(items)} attacks in the **{cat}** category. "
        f"Each shows its technique id, mode, standards mapping, description, and the "
        f"exact command to run it (swap the provider and target as needed).",
        "",
    ]
    for m in items:
        body.append(render_field(m))
        body.append("")
    (OUT / f"{cat}.mdx").write_text(fm + "\n".join(body).rstrip() + "\n")


def write_overview(by_cat):
    total = sum(len(v) for v in by_cat.values())
    fm = (
        f"---\n"
        f'title: "Attacks by Category"\n'
        f'description: "Browse all {total} ai-blackteam attacks, organized into {len(by_cat)} categories."\n'
        f"---\n\n"
    )
    lines = [
        f"All **{total} attacks** across **{len(by_cat)} categories**. "
        "Pick a category to see every attack in it, with its description inline.",
        "",
        "| Category | Attacks |",
        "|----------|---------|",
    ]
    for cat in sorted(by_cat, key=lambda c: -len(by_cat[c])):
        lines.append(f"| [{cat}](/attacks/catalog/{cat}) | {len(by_cat[cat])} |")
    lines.append("")
    (OUT / "overview.mdx").write_text(fm + "\n".join(lines))


def main():
    by_cat = collect()
    for cat, items in by_cat.items():
        write_category_page(cat, items)
    write_overview(by_cat)
    print(f"wrote {len(by_cat)} category pages + overview into {OUT}")


if __name__ == "__main__":
    main()
