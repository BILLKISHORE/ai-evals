"""Build an interactive, paginated, searchable 'All Attacks' explorer.

Mintlify strips arbitrary Tailwind classes and rewrites <table> elements, so
this component lays out a table-style grid using INLINE STYLES (which Mintlify
preserves) on plain <div>s. Client-side pagination keeps only ~25 rows in the
DOM, so the page stays fast. Severity is plain text (no colored badge).

Outputs:
  * docs/snippets/attacks-explorer.jsx   (data + React component)
  * docs/attacks/all-attacks.mdx         (page that renders the component)

Run: python scripts/build_attacks_explorer.py
"""

import json
from pathlib import Path

import ai_blackteam.api  # noqa: F401  forces registration
from ai_blackteam.registry import attack_registry

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SNIPPETS = DOCS / "snippets"
SNIPPETS.mkdir(parents=True, exist_ok=True)


def owasp_codes(values):
    return ", ".join(v.split(":")[0].strip() for v in values) if values else ""


def collect():
    rows = []
    for tid in attack_registry.list():
        m = attack_registry.get(tid)().metadata()
        rows.append({
            "name": m["name"],
            "id": m["technique_id"],
            "category": m["category"],
            "severity": m["severity"],
            "mode": m["mode"],
            "owasp": owasp_codes(m["owasp_llm"]),
            "mitre": ", ".join(m["mitre_atlas"]),
            "desc": m["description"],
        })
    rows.sort(key=lambda r: (r["category"], r["name"]))
    return rows


# __DATA__ is replaced with a JSON array (valid JS) and __COUNT__ with the
# registry count, so the prose never hand-copies a number that can drift.
# Layout uses inline styles only.
COMPONENT = r"""
export const AttacksExplorer = () => {
  const ATTACKS = __DATA__;
  const PER_PAGE = 25;
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");

  const query = q.trim().toLowerCase();
  const filtered = query
    ? ATTACKS.filter((a) =>
        (a.name + " " + a.id + " " + a.category + " " + a.desc + " " + a.owasp + " " + a.mitre)
          .toLowerCase()
          .includes(query)
      )
    : ATTACKS;

  const pages = Math.max(1, Math.ceil(filtered.length / PER_PAGE));
  const cur = Math.min(page, pages);
  const start = (cur - 1) * PER_PAGE;
  const items = filtered.slice(start, start + PER_PAGE);

  const COLS = "1.7fr 1.5fr 0.8fr 0.9fr 0.8fr 1.4fr 3fr";
  const line = "1px solid rgba(128,128,128,0.18)";
  const wrap = { wordBreak: "break-word", overflowWrap: "anywhere" };
  const rowStyle = {
    display: "grid",
    gridTemplateColumns: COLS,
    gap: "14px",
    padding: "10px 0",
    borderBottom: line,
    fontSize: "14px",
    alignItems: "start",
  };
  const headStyle = {
    ...rowStyle,
    padding: "0 0 8px",
    fontSize: "11px",
    fontWeight: 700,
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    color: "#6b7280",
    borderBottom: "1px solid rgba(128,128,128,0.35)",
  };
  const inputStyle = {
    width: "100%",
    padding: "9px 12px",
    borderRadius: "8px",
    border: "1px solid rgba(128,128,128,0.3)",
    background: "transparent",
    fontSize: "14px",
    marginBottom: "12px",
  };
  const btnStyle = (disabled) => ({
    padding: "5px 14px",
    borderRadius: "6px",
    border: "1px solid rgba(128,128,128,0.3)",
    background: "transparent",
    fontSize: "14px",
    cursor: disabled ? "default" : "pointer",
    opacity: disabled ? 0.4 : 1,
  });

  return (
    <div className="not-prose">
      <input
        type="text"
        value={q}
        onChange={(e) => {
          setQ(e.target.value);
          setPage(1);
        }}
        placeholder="Search all __COUNT__ attacks by name, id, category, OWASP, MITRE, or description..."
        style={inputStyle}
      />

      <div style={{ fontSize: "13px", color: "#6b7280", marginBottom: "10px" }}>
        {filtered.length} attack{filtered.length === 1 ? "" : "s"}
        {query ? " match your search" : ""}. Page {cur} of {pages}.
      </div>

      <div style={headStyle}>
        <div>Attack</div>
        <div>Technique ID</div>
        <div>Severity</div>
        <div>Mode</div>
        <div>OWASP</div>
        <div>MITRE</div>
        <div>Description</div>
      </div>

      {items.map((a) => (
        <div key={a.id} style={rowStyle}>
          <div style={{ ...wrap, fontWeight: 600 }}>{a.name}</div>
          <div style={wrap}>
            <code style={{ fontSize: "12px" }}>{a.id}</code>
          </div>
          <div style={wrap}>{a.severity}</div>
          <div style={wrap}>{a.mode}</div>
          <div style={wrap}>{a.owasp || "-"}</div>
          <div style={wrap}>{a.mitre || "-"}</div>
          <div style={{ ...wrap, color: "#6b7280" }}>{a.desc}</div>
        </div>
      ))}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "14px",
          marginTop: "18px",
        }}
      >
        <button style={btnStyle(cur <= 1)} disabled={cur <= 1} onClick={() => setPage(cur - 1)}>
          Previous
        </button>
        <span style={{ fontSize: "13px", color: "#6b7280" }}>
          Page {cur} of {pages}
        </span>
        <button style={btnStyle(cur >= pages)} disabled={cur >= pages} onClick={() => setPage(cur + 1)}>
          Next
        </button>
      </div>
    </div>
  );
};
"""

PAGE = '''---
title: "All Attacks"
description: "Search and page through every attack in ai-blackteam, with OWASP, MITRE, and descriptions."
mode: "wide"
---

import { AttacksExplorer } from "/snippets/attacks-explorer.jsx"

All **__COUNT__ attacks** in one place. Search by name, category, OWASP, MITRE, or
description, and page through the results. Every attack shows its severity,
mode, standards mapping, and full description.

Run any attack below with its technique id (swap the provider and target):

```bash
ai-blackteam run -p anthropic -a <technique-id> -t "your target prompt"
```

<AttacksExplorer />
'''


def main():
    rows = collect()
    data = json.dumps(rows, ensure_ascii=True)
    count = f"{len(rows):,}"
    # Substitute __COUNT__ before __DATA__ so an attack description that happens
    # to contain the placeholder text cannot be rewritten.
    component = COMPONENT.replace("__COUNT__", count).replace("__DATA__", data)
    (SNIPPETS / "attacks-explorer.jsx").write_text(component.lstrip() + "\n")
    (DOCS / "attacks" / "all-attacks.mdx").write_text(PAGE.replace("__COUNT__", count))
    print(f"wrote explorer snippet with {len(rows)} attacks + all-attacks.mdx page")


if __name__ == "__main__":
    main()
