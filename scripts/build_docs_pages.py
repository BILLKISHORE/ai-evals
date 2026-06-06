"""Convert the generated attack-catalog Markdown into Mintlify .mdx pages.

Produces, under docs/attacks/:
  * all-attacks.mdx            (from attack-catalog/ATTACKS-CATALOG.md)
  * all-categories.mdx         (from attack-catalog/CATEGORIES.md)
  * strategies/overview.mdx    (index of the 61 strategy pages)
  * strategies/<category>.mdx  (one per attack-catalog/strategies/<category>.md)

Frontmatter (title + description) is derived from the source. The body H1 is
stripped so Mintlify does not render a duplicate title. No emojis are emitted.
Run: python scripts/build_docs_pages.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "attack-catalog"
DOCS_ATTACKS = ROOT / "docs" / "attacks"
STRAT_OUT = DOCS_ATTACKS / "strategies"
STRAT_OUT.mkdir(parents=True, exist_ok=True)


def yaml_escape(text: str) -> str:
    text = text.replace('"', "'").strip()
    return text[:155]


def strip_h1(body: str):
    lines = body.splitlines()
    title = ""
    out = []
    dropped = False
    for ln in lines:
        if not dropped and ln.startswith("# "):
            title = ln[2:].strip()
            dropped = True
            continue
        out.append(ln)
    return title, "\n".join(out).lstrip("\n")


def first_what_is(body: str) -> str:
    m = re.search(r"\*\*What it is:\*\*\s*(.+)", body)
    if m:
        return re.sub(r"[*`()]", "", m.group(1)).strip()
    # fall back to first non-empty, non-heading line
    for ln in body.splitlines():
        s = ln.strip()
        if s and not s.startswith("#") and not s.startswith("|"):
            return re.sub(r"[*`()]", "", s).strip()
    return ""


def write_mdx(path: Path, title: str, description: str, body: str):
    fm = f'---\ntitle: "{yaml_escape(title)}"\ndescription: "{yaml_escape(description)}"\n---\n\n'
    path.write_text(fm + body.rstrip() + "\n")


def convert_strategies():
    cats = []
    for md in sorted((SRC / "strategies").glob("*.md")):
        raw = md.read_text()
        title, body = strip_h1(raw)
        desc = first_what_is(raw)
        title = title or f"{md.stem} strategy"
        write_mdx(STRAT_OUT / f"{md.stem}.mdx", title, desc, body)
        cats.append((md.stem, title, desc))
    return cats


def write_strategies_overview(cats):
    lines = [
        "Plain-English strategy guides for every attack family in ai-blackteam.",
        "Each page explains what the attacks do, how they work, real examples,",
        "why a model might fall for them, and how to defend.",
        "",
        "| Category | Focus |",
        "|----------|-------|",
    ]
    for slug, title, desc in cats:
        name = title.replace(": Attack Strategy", "")
        lines.append(f"| [{name}](/attacks/strategies/{slug}) | {desc[:90]} |")
    lines.append("")
    write_mdx(
        STRAT_OUT / "overview.mdx",
        "Attack Strategies",
        "Plain-English strategy guides for all 61 attack categories.",
        "\n".join(lines),
    )


def convert_catalog():
    cat_md = SRC / "ATTACKS-CATALOG.md"
    title, body = strip_h1(cat_md.read_text())
    write_mdx(
        DOCS_ATTACKS / "all-attacks.mdx",
        "All Attacks",
        "Every attack technique registered in ai-blackteam, grouped by category.",
        body,
    )

    catg_md = SRC / "CATEGORIES.md"
    title2, body2 = strip_h1(catg_md.read_text())
    write_mdx(
        DOCS_ATTACKS / "all-categories.mdx",
        "All Categories",
        "Every attack category in ai-blackteam with counts and example techniques.",
        body2,
    )


def main():
    cats = convert_strategies()
    write_strategies_overview(cats)
    convert_catalog()
    print(f"wrote {len(cats)} strategy pages + overview + all-attacks + all-categories")
    print(f"into {STRAT_OUT} and {DOCS_ATTACKS}")


if __name__ == "__main__":
    main()
