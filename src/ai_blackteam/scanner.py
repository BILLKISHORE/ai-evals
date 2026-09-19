"""AI code security scanner for ai_blackteam.

Detects LLM-specific vulnerabilities in Python and JavaScript/TypeScript code:
- Prompt injection (user input in system prompts)
- Secrets in prompts (API keys, PII)
- Improper output handling (XSS, code execution, SQL injection)
- Excessive agency (unrestricted tools)
- Missing safety controls (no max_tokens, no input validation)

Usage:
    from ai_blackteam.scanner import scan_file, scan_directory

    findings = scan_file("app.py")
    findings = scan_directory("src/")
"""

import re
import os
from pathlib import Path


# Each rule: id, name, severity, owasp, description, patterns (list of compiled regex),
# file_types (list of extensions to scan), message (what to tell the user)

RULES = [
    {
        "id": "BTSC-001",
        "name": "Prompt Injection: User Input in System Prompt",
        "severity": "critical",
        "owasp": "LLM01",
        "description": "User-controlled input is interpolated into a system/developer role message, enabling prompt injection.",
        "patterns": [
            # Python f-string in system role content (same dict)
            r'''["']role["']\s*:\s*["']system["']\s*,\s*["']content["']\s*:\s*f["']''',
            # f-string with variable in system content (same line or next)
            r'''["']role["']\s*:\s*["']system["']\s*,\s*["']content["']\s*:\s*f?["'][^"']*\{[^}]+\}''',
            # String concatenation in system content (same dict)
            r'''["']role["']\s*:\s*["']system["']\s*,\s*["']content["']\s*:.*?\+\s*\w+''',
            # .format() in system content
            r'''["']role["']\s*:\s*["']system["']\s*,\s*["']content["']\s*:.*?\.format\(''',
        ],
        "file_types": [".py", ".js", ".ts", ".tsx", ".jsx"],
        "message": "User input should only go into role:'user' messages. System prompts must be static strings.",
    },
    {
        "id": "BTSC-002",
        "name": "Secrets in Prompt Templates",
        "severity": "high",
        "owasp": "LLM02",
        "description": "API keys, passwords, or secrets are embedded in prompt templates sent to the LLM.",
        "patterns": [
            # API key patterns in strings likely to be prompts
            r'''(?:prompt|system|instruction|message).*?(?:sk-[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[a-zA-Z0-9]{36})''',
            # Environment variable in prompt content
            r'''(?:system_prompt|instructions|preamble).*?os\.environ\[''',
            r'''(?:system_prompt|instructions|preamble).*?config\.get\(.*?(?:key|secret|token|password)''',
            # Direct password/key reference in prompt
            r'''(?:prompt|system|content).*?(?:password|api_key|secret_key|access_token)\s*[:=]''',
        ],
        "file_types": [".py", ".js", ".ts", ".tsx", ".jsx"],
        "message": "Never embed secrets in LLM prompts. Call APIs server-side and pass results to the LLM.",
    },
    {
        "id": "BTSC-003",
        "name": "LLM Output Executed as Code",
        "severity": "critical",
        "owasp": "LLM10",
        "description": "LLM response is passed to exec(), eval(), or subprocess without sandboxing.",
        "patterns": [
            # Python exec/eval with LLM response variable
            r'''exec\s*\(.*?(?:response|completion|output|result|content|message|text|answer)''',
            r'''eval\s*\(.*?(?:response|completion|output|result|content|message|text|answer)''',
            # subprocess with LLM output
            r'''subprocess\.(?:run|call|Popen|check_output)\s*\(.*?(?:response|completion|output|result|content)''',
            r'''os\.system\s*\(.*?(?:response|completion|output|result|content)''',
            # JavaScript eval/Function
            r'''eval\s*\(.*?(?:response|completion|output|result|content)''',
            r'''new\s+Function\s*\(.*?(?:response|completion|output|result|content)''',
        ],
        "file_types": [".py", ".js", ".ts", ".tsx", ".jsx"],
        "message": "Never execute LLM output directly. Use a sandboxed environment or parse structured output instead.",
    },
    {
        "id": "BTSC-004",
        "name": "LLM Output Rendered as HTML (XSS)",
        "severity": "high",
        "owasp": "LLM10",
        "description": "LLM response is rendered as raw HTML without sanitization, enabling XSS attacks.",
        "patterns": [
            # innerHTML assignment
            r'''\.innerHTML\s*=.*?(?:response|completion|output|result|content|message|text)''',
            # dangerouslySetInnerHTML in React
            r'''dangerouslySetInnerHTML\s*=\s*\{\{.*?__html\s*:.*?(?:response|completion|output|result|content)''',
            # Python render_template_string with LLM output
            r'''render_template_string\s*\(.*?(?:response|completion|output|result|content)''',
            # v-html in Vue
            r'''v-html\s*=.*?(?:response|completion|output|result|content)''',
        ],
        "file_types": [".py", ".js", ".ts", ".tsx", ".jsx", ".vue", ".html"],
        "message": "Use .textContent instead of .innerHTML. Sanitize with DOMPurify. Apply CSP headers.",
    },
    {
        "id": "BTSC-005",
        "name": "LLM Output in SQL Query",
        "severity": "critical",
        "owasp": "LLM10",
        "description": "LLM-generated text is used directly in SQL queries without parameterization.",
        "patterns": [
            r'''(?:cursor|conn|db|connection)\.execute\s*\(.*?(?:response|completion|output|result|content|generated|llm|sql|query)''',
            r'''(?:cursor|conn|db|connection)\.execute\s*\(\s*f["']''',
            r'''\.raw\s*\(.*?(?:response|completion|output|result|content|generated|sql|query)''',
        ],
        "file_types": [".py", ".js", ".ts"],
        "message": "Use parameterized queries. Never pass LLM output directly to SQL execute.",
    },
    {
        "id": "BTSC-006",
        "name": "Excessive Agency: Unrestricted Shell Access",
        "severity": "critical",
        "owasp": "LLM03",
        "description": "Tool/function exposed to LLM has unrestricted shell command execution.",
        # Single-line patterns plus a context requirement. The previous form,
        # `@tool.*\n(?:.*\n){0,10}.*X`, nests a quantified group around `.*`
        # and backtracked for minutes on ordinary files, turning a real scan
        # into an empty result and giving a tool pointed at untrusted code a
        # denial-of-service surface.
        "requires_context": r"@tool|BaseTool|\btools\s*=|\bfunctions\s*=",
        "context_window": 20,
        "patterns": [
            r"""subprocess\.(?:run|call|Popen)\s*\([^\n]*shell\s*=\s*True""",
            r"""os\.system\s*\(""",
        ],
        "file_types": [".py"],
        "message": "Allowlist permitted commands. Never expose unrestricted shell access to an LLM.",
    },
    {
        "id": "BTSC-007",
        "name": "Excessive Agency: Unrestricted File Access",
        "severity": "high",
        "owasp": "LLM03",
        "description": "Tool/function exposed to LLM can read/write arbitrary file paths.",
        # Single-line patterns plus a context requirement. The previous form,
        # `@tool.*\n(?:.*\n){0,10}.*X`, nests a quantified group around `.*`
        # and backtracked for minutes on ordinary files, turning a real scan
        # into an empty result and giving a tool pointed at untrusted code a
        # denial-of-service surface.
        "requires_context": r"@tool|BaseTool|\btools\s*=|\bfunctions\s*=",
        "context_window": 20,
        "patterns": [
            r"""open\s*\([^\n]*(?:path|file|filename)""",
            r"""(?:read_file|write_file|Path)\s*\(""",
        ],
        "file_types": [".py"],
        "message": "Restrict file access to specific directories. Validate paths against an allowlist.",
    },
    {
        "id": "BTSC-008",
        "name": "Missing max_tokens Limit",
        "severity": "medium",
        "owasp": "LLM06",
        "description": "LLM API call does not set max_tokens, risking unbounded token consumption.",
        "patterns": [
            # OpenAI without max_tokens
            r'''(?:openai|client)\.(?:chat\.completions|completions)\.create\s*\([^)]*\)(?!.*max_tokens)''',
            # Anthropic without max_tokens
            r'''(?:anthropic|client)\.messages\.create\s*\([^)]*\)(?!.*max_tokens)''',
            # General pattern - LLM call without max_tokens nearby
            r'''\.(?:generate|complete|chat)\s*\([^)]{50,}\)(?!.*max_tokens)''',
        ],
        "file_types": [".py", ".js", ".ts"],
        "message": "Always set max_tokens with a server-side cap to prevent unbounded consumption.",
    },
    {
        "id": "BTSC-009",
        "name": "Hardcoded System Prompt with Sensitive Content",
        "severity": "medium",
        "owasp": "LLM08",
        "description": "Long system prompt contains potentially sensitive business logic, URLs, or instructions that could be extracted.",
        "patterns": [
            # Long system prompt strings (>200 chars) with sensitive keywords
            r'''(?:system_prompt|system_message|instructions|preamble)\s*=\s*(?:f?["\']{3}|f?["\']).{200,}''',
        ],
        "file_types": [".py", ".js", ".ts"],
        "message": "Treat system prompts as public. Keep business logic server-side. Never embed secrets or internal URLs.",
    },
    {
        "id": "BTSC-010",
        "name": "No Input Validation Before LLM Call",
        "severity": "medium",
        "owasp": "LLM01",
        "description": "User input flows directly from HTTP request to LLM API call with no validation.",
        "patterns": [
            # Flask request directly to LLM
            r'''request\.(?:json|form|args|data).*?(?:openai|anthropic|client)\.(?:chat|messages|completions)\.create''',
            # Express req.body directly to LLM
            r'''req\.body.*?(?:openai|anthropic|client)\.(?:chat|messages|completions)\.create''',
        ],
        "file_types": [".py", ".js", ".ts"],
        "message": "Validate input length, character set, and encoding before passing to LLM. Apply rate limiting.",
    },
    {
        "id": "BTSC-011",
        "name": "RAG Retrieval Without Access Control",
        "severity": "high",
        "owasp": "LLM09",
        "description": "Vector database query does not include user-level access filtering.",
        "patterns": [
            # Pinecone/Chroma/Weaviate query without filter
            r'''\.(?:query|similarity_search|search)\s*\([^)]*\)(?!.*(?:filter|where|metadata))''',
            # Direct embedding search without RBAC
            r'''(?:pinecone|chroma|weaviate|qdrant|milvus).*?\.query\s*\([^)]*\)(?!.*filter)''',
        ],
        "file_types": [".py", ".js", ".ts"],
        "message": "Apply RBAC/ABAC before retrieval. Filter by user permissions in metadata.",
    },
]


def _compile_rules():
    """Pre-compile all regex patterns for performance."""
    compiled = []
    for rule in RULES:
        compiled_patterns = []
        for pattern in rule["patterns"]:
            try:
                compiled_patterns.append(re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL))
            except re.error:
                pass
        entry = {**rule, "_compiled": compiled_patterns}
        # DOTALL makes `.` match newlines, which is what turned the old
        # multi-line windows into exponential backtracking. Context is matched
        # against a bounded slice of lines instead of inside the pattern.
        if rule.get("requires_context"):
            entry["_context_compiled"] = re.compile(
                rule["requires_context"], re.IGNORECASE | re.MULTILINE
            )
        compiled.append(entry)
    return compiled


COMPILED_RULES = _compile_rules()


def scan_file(file_path):
    """Scan a single file for AI security vulnerabilities.

    Args:
        file_path: path to the file to scan

    Returns:
        list of finding dicts with: rule_id, name, severity, owasp, line, code, message, file
    """
    path = Path(file_path)
    if not path.exists():
        return []

    ext = path.suffix.lower()
    findings = []

    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    lines = content.split("\n")

    # Python gets a parse-tree pass for the two rules that need to follow a
    # value across lines. Their line-regexes still run for .js/.ts, where there
    # is no parser here.
    ast_rules = set()
    if ext == ".py":
        findings.extend(_analyse_python(content, path))
        ast_rules = {"BTSC-001", "BTSC-002"}

    for rule in COMPILED_RULES:
        if ext not in rule["file_types"] or rule["id"] in ast_rules:
            continue

        ctx_re = rule.get("_context_compiled")
        window = rule.get("context_window", 20)

        for pattern in rule["_compiled"]:
            for match in pattern.finditer(content):
                # Find line number
                start = match.start()
                line_num = content[:start].count("\n") + 1

                # Context requirement replaces the old multi-line regex window:
                # the dangerous call only matters when it sits inside something
                # exposed to the model. Checking a bounded slice of lines is
                # linear, where the regex form was exponential.
                if ctx_re is not None:
                    above = "\n".join(lines[max(0, line_num - 1 - window):line_num])
                    if not ctx_re.search(above):
                        continue

                # Get the matched code snippet (the line + context)
                line_start = max(0, line_num - 1)
                line_end = min(len(lines), line_num + 2)
                code_snippet = "\n".join(lines[line_start:line_end])

                findings.append({
                    "rule_id": rule["id"],
                    "name": rule["name"],
                    "severity": rule["severity"],
                    "owasp": rule["owasp"],
                    "line": line_num,
                    "code": code_snippet[:200],
                    "message": rule["message"],
                    "file": str(path),
                })

    # Deduplicate: same rule + same line = one finding
    seen = set()
    deduped = []
    for f in findings:
        key = (f["rule_id"], f["file"], f["line"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)

    return deduped


def scan_directory(dir_path, exclude_dirs=None):
    """Scan a directory recursively for AI security vulnerabilities.

    Args:
        dir_path: path to directory to scan
        exclude_dirs: list of directory names to skip (default: common non-source dirs)

    Returns:
        list of finding dicts
    """
    if exclude_dirs is None:
        exclude_dirs = {
            "node_modules", ".git", "__pycache__", "venv", ".venv",
            "dist", "build", ".next", ".nuxt", "env", ".env",
        }

    all_extensions = set()
    for rule in RULES:
        all_extensions.update(rule["file_types"])

    findings = []
    dir_path = Path(dir_path)

    for root, dirs, files in os.walk(dir_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in all_extensions:
                findings.extend(scan_file(file_path))

    return findings


def scan_summary(findings):
    """Generate a summary of scan findings.

    Returns:
        dict with total, by_severity, by_rule, by_owasp, files_affected
    """
    by_severity = {}
    by_rule = {}
    by_owasp = {}
    files = set()

    for f in findings:
        by_severity[f["severity"]] = by_severity.get(f["severity"], 0) + 1
        by_rule[f["rule_id"]] = by_rule.get(f["rule_id"], 0) + 1
        by_owasp[f["owasp"]] = by_owasp.get(f["owasp"], 0) + 1
        files.add(f["file"])

    return {
        "total": len(findings),
        "by_severity": by_severity,
        "by_rule": by_rule,
        "by_owasp": by_owasp,
        "files_affected": len(files),
    }


# ── AST analysis for Python sources ──────────────────────────────────
#
# BTSC-001 and BTSC-002 were single-line regexes with systematic blind spots.
# BTSC-001 required the literal {"role": "system", "content": ...} dict on one
# line, so it missed the common shape of building the prompt into a variable
# first. BTSC-002 required a word like "prompt" on the same line as the key and
# used a character class that excluded hyphens, so it could not match the
# sk-proj- format. Parsing the file gives the variable tracking that neither
# could do with a line at a time.

import ast as _ast

# Names that indicate an attacker-influenced value.
#
# Deliberately narrow. An earlier version included "prompt", "message", "user"
# and "system", which made every provider method taking a `system_prompt`
# pass-through parameter look tainted and produced 13 false criticals on this
# project alone. A library forwarding the caller's own system prompt is not
# interpolating user input, and flagging it buries the real findings.
_TAINT_SOURCES = (
    "user_input", "user_query", "user_message", "user_prompt", "user_data",
    "user_content", "client_input", "untrusted", "external_input",
    "request", "req_", "form_data", "payload", "argv", "raw_input",
)

# Attribute reads that are attacker-controlled regardless of the variable name,
# e.g. request.json, req.body, request.args.
_TAINT_ATTRS = ("json", "body", "form", "args", "params", "query", "data", "values")

_SECRET_PATTERNS = [
    # Hyphens are part of modern key formats (sk-proj-, sk-ant-api03-), which
    # is precisely what the old [a-zA-Z0-9] class could not match.
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{30,}"),
]

# Documentation and templates are full of fake keys. Flagging those teaches
# people to ignore the rule, which is worse than missing one real key.
_PLACEHOLDER_HINTS = ("xxxx", "...", "your", "<", "changeme", "placeholder")


def _is_placeholder(value):
    low = value.lower()
    return any(h in low for h in _PLACEHOLDER_HINTS)


def _refs_tainted(node, tainted):
    """True when the expression reads a tainted name."""
    for sub in _ast.walk(node):
        if isinstance(sub, _ast.Name) and (sub.id in tainted or _looks_tainted(sub.id)):
            return True
        if isinstance(sub, _ast.Attribute):
            base = sub.value
            base_name = base.id if isinstance(base, _ast.Name) else ""
            if sub.attr in _TAINT_ATTRS and _looks_tainted(base_name):
                return True
            if _looks_tainted(sub.attr):
                return True
    return False


def _looks_tainted(name):
    low = (name or "").lower()
    return any(src in low for src in _TAINT_SOURCES)


def _builds_string_from(node, tainted):
    """True when node builds a string out of a tainted value."""
    if isinstance(node, _ast.JoinedStr):
        return any(
            isinstance(v, _ast.FormattedValue) and _refs_tainted(v.value, tainted)
            for v in node.values
        )
    if isinstance(node, _ast.BinOp) and isinstance(node.op, _ast.Add):
        return _refs_tainted(node, tainted)
    if isinstance(node, _ast.Call):
        func = node.func
        if isinstance(func, _ast.Attribute) and func.attr in ("format", "join", "replace"):
            return any(_refs_tainted(a, tainted) for a in node.args)
    return False


def _analyse_python(content, path):
    """Return BTSC-001 and BTSC-002 findings from the parse tree."""
    try:
        tree = _ast.parse(content)
    except SyntaxError:
        return []

    findings = []
    lines = content.split("\n")

    def snippet(lineno):
        return "\n".join(lines[max(0, lineno - 1):lineno + 2])[:200]

    # Parameters are attacker-controlled at a handler boundary.
    tainted = set()
    for node in _ast.walk(tree):
        if isinstance(node, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
            for arg in list(node.args.args) + list(node.args.kwonlyargs):
                if _looks_tainted(arg.arg):
                    tainted.add(arg.arg)

    # Propagate to variables built from those values.
    for _ in range(3):  # a few passes settle simple chains
        for node in _ast.walk(tree):
            if isinstance(node, _ast.Assign) and _builds_string_from(node.value, tainted):
                for target in node.targets:
                    if isinstance(target, _ast.Name):
                        tainted.add(target.id)

    # BTSC-001: a system-role message whose content carries tainted data.
    for node in _ast.walk(tree):
        if not isinstance(node, _ast.Dict):
            continue
        role = content_node = None
        for key, value in zip(node.keys, node.values):
            if not isinstance(key, _ast.Constant):
                continue
            if key.value == "role" and isinstance(value, _ast.Constant):
                role = value.value
            elif key.value == "content":
                content_node = value
        if role != "system" or content_node is None:
            continue
        flows = (
            (isinstance(content_node, _ast.Name) and content_node.id in tainted)
            or _builds_string_from(content_node, tainted)
        )
        if flows:
            findings.append(_finding("BTSC-001", node.lineno, snippet(node.lineno), path))

    # BTSC-002: a credential written as a literal.
    for node in _ast.walk(tree):
        if not isinstance(node, _ast.Constant) or not isinstance(node.value, str):
            continue
        if _is_placeholder(node.value):
            continue
        if any(p.search(node.value) for p in _SECRET_PATTERNS):
            findings.append(_finding("BTSC-002", node.lineno, snippet(node.lineno), path))

    return findings


def _finding(rule_id, line, code, path):
    rule = next(r for r in RULES if r["id"] == rule_id)
    return {
        "rule_id": rule["id"],
        "name": rule["name"],
        "severity": rule["severity"],
        "owasp": rule["owasp"],
        "line": line,
        "code": code,
        "message": rule["message"],
        "file": str(path),
    }
