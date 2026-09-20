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
import json
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



# Keys that mark a JSON document as an MCP definition rather than arbitrary
# JSON. Deliberately narrow: a package.json or a tsconfig must not be dragged
# through the MCP rules and reported on.
_MCP_SHAPE_KEYS = ("mcpServers", "mcp_servers", "inputSchema", "input_schema")


def _looks_like_mcp_definition(path):
    """Whether this JSON file is plausibly an MCP server or tool definition.

    Read cheaply and defensively: an unreadable or non-JSON file is simply not
    an MCP definition, and deciding that must never raise into a directory
    walk over someone's repository.
    """
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    if not any(key in raw for key in _MCP_SHAPE_KEYS) and '"tools"' not in raw:
        return False
    try:
        doc = json.loads(raw)
    except ValueError:
        return False
    if isinstance(doc, dict):
        if any(isinstance(doc.get(k), dict) and doc.get(k) for k in _MCP_REGISTRY_KEYS):
            return True
        if isinstance(doc.get("tools"), list):
            return True
        return "inputSchema" in doc or "input_schema" in doc
    if isinstance(doc, list):
        return any(isinstance(t, dict) and ("inputSchema" in t or "input_schema" in t) for t in doc)
    return False


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

    # MCP server definitions are JSON, not source, so the source rules find
    # nothing in them. Without this dispatch scan_mcp_server had no caller at
    # all and the CLI reported "no vulnerabilities" on a definition it can
    # detect as critically vulnerable.
    if ext == ".json" and _looks_like_mcp_definition(path):
        return scan_mcp_server(path)

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
    # MCP definitions are JSON and no source rule claims that extension, so
    # a directory walk skipped them entirely. scan_file decides whether a
    # given .json is actually an MCP definition.
    all_extensions.add(".json")

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


# ── MCP server definition scanner (sibling of the source scanner) ─────
#
# The source scanner reads code. This sibling reads an MCP server definition:
# the declarative JSON that lists a server's tools, their descriptions and
# their input schemas (a tools/list response, or a server object wrapping one).
# Those definitions decide what an agent will call and with what arguments,
# so a poisoned description or an unconstrained sink parameter is a security
# weakness before any code runs.
#
# It lives beside RULES rather than inside it on purpose: RULES is a fixed,
# separately tested contract (BTSC-001..011), and these checks key off JSON
# structure, not line regexes. Detection is done with plain string and dict
# operations, never a regex over the whole document, so there is no way to
# reintroduce the catastrophic backtracking the source scanner was rewritten
# to remove.

class MCPDefinitionUnreadable(Exception):
    """The definition could not be read, which is not the same as clean.

    scan_mcp_server returns [] for a missing, unreadable or unparseable file,
    byte-identical to the result for a definition assessed as having no
    weaknesses. A caller wiring this into a gate cannot tell the two apart, so
    a truncated download or a permissions error passes as a clean server.

    The lenient default is kept so existing callers are unaffected; strict=True
    raises this instead.
    """


MCP_RULES = [
    {
        "id": "BTSC-012",
        "name": "MCP Tool Description Carries Instructions",
        "severity": "critical",
        "owasp": "LLM01",
        "description": "A tool description or parameter description carries instruction text, the tool-poisoning vector: the model reads tool metadata as trusted context and follows hidden directives.",
        "message": "Tool descriptions are model-visible context. Keep them to what the tool does. Never embed directives, file paths, or 'before you respond' instructions.",
    },
    {
        "id": "BTSC-013",
        "name": "MCP Tool Shells Out",
        "severity": "critical",
        "owasp": "LLM03",
        "description": "A tool exposes a command, shell, or script parameter, or its description states it runs shell commands, giving the agent unrestricted command execution.",
        "message": "Do not expose raw command execution as a tool. Allowlist specific operations and pass structured arguments, never a shell string.",
    },
    {
        "id": "BTSC-014",
        "name": "MCP Tool Overbroad Scope",
        "severity": "high",
        "owasp": "LLM03",
        "description": "A tool declares wildcard, admin, or root scopes, granting far more authority than any single operation needs.",
        "message": "Scope each tool to the least privilege it needs. Replace wildcard, admin, and root grants with explicit, narrow scopes.",
    },
    {
        "id": "BTSC-015",
        "name": "MCP Unvalidated Passthrough Into Tool Call",
        "severity": "high",
        "owasp": "LLM10",
        "description": "A sink parameter (query, sql, url, path, template, filter) is an unconstrained string, so model output flows into the sink with no enum, pattern, or length validation.",
        "message": "Constrain sink parameters with enum, pattern, format, or maxLength. Validate model-supplied values before they reach a query, request, or file path.",
    },
    {
        "id": "BTSC-016",
        "name": "MCP Server Missing Authentication",
        "severity": "high",
        "owasp": "LLM04",
        "description": "The server definition declares no authentication, so the agent cannot verify the server's identity and treats an unauthenticated component as trusted.",
        "message": "Require authentication on the server (auth, oauth, token, or API key). An unauthenticated MCP server is an untrusted supply-chain component.",
    },
    {
        "id": "BTSC-017",
        "name": "MCP Duplicate Tool Name",
        "severity": "high",
        "owasp": "LLM03",
        "description": "Two tools share one name. An MCP client resolves a call by name, so whichever registration wins captures every call meant for the other, and the pick is registration order rather than a trust decision.",
        "message": "Give every tool a unique name, and namespace tools by server when merging definitions. A shared name lets a later server shadow an earlier one.",
    },
]

# Instruction and injection phrasing that does not belong in tool metadata.
# Phrases no honest tool description contains. Any one of these is a finding
# on its own: they address the model directly, or describe concealing an
# action from the user.
_MCP_DIRECTIVE_MARKERS = (
    "ignore previous", "ignore all previous", "ignore your", "disregard",
    "before responding", "before you respond", "before summar",
    "system override", "note to the assistant", "new directive",
    "do not tell", "don't tell", "without telling", "do not mention",
    "without informing", "exfiltrat", "silently",
)

# Ordinary English that also appears in ordinary documentation. On its own
# each of these is noise: measured against five benign descriptions taken from
# real tool docs, the old flat list flagged all five as CRITICAL. They count
# only when the same description also names something worth stealing.
_MCP_SOFT_MARKERS = (
    "you must", "you should", "before you ", "always ", "also append",
    "always append", "also send", "also forward", "also post", "also return",
    "include its contents", "include the contents", "return it verbatim",
    "read the file", "system:", "assistant:", "<!--", "important:", "attention:",
)

# What a poisoned description is trying to reach. A soft marker plus one of
# these is a directive with a target, which is the actual vector.
_MCP_SENSITIVE_TARGETS = (
    "~/.ssh", ".ssh/", "id_rsa", "id_ed25519", "/etc/passwd", "/etc/shadow",
    ".env", "credentials.json", "secrets.json", "secrets.yaml", "cat /etc/",
    "private key", "api key", "api_key", "password", "token", "credential",
    "http://", "https://",
)

# Parameter names whose presence means the tool runs commands.
_MCP_EXEC_SINK_NAMES = frozenset({
    "command", "cmd", "shell", "shell_command", "bash",
    "script", "exec", "code", "powershell", "pwsh",
})

# Description phrasing that says the tool shells out even without an exec param.
_MCP_SHELL_PHRASES = (
    "shell command", "shell out", "execute command", "run arbitrary",
    "arbitrary command", "/bin/sh", "/bin/bash", "subprocess", "os.system",
    "run a command", "run shell",
)

# Sink parameters whose model-supplied value flows into an interpreter, request,
# or file path. Kept disjoint from the exec names so a value is one rule or the
# other, never double counted.
_MCP_INJECTION_SINK_NAMES = frozenset({
    "sql", "query", "url", "uri", "endpoint", "path", "filepath",
    "file_path", "html", "template", "expression", "filter", "xpath",
})

# Schema keywords that constrain a value enough that it is not a blind sink.
_MCP_VALIDATION_KEYS = frozenset({"enum", "pattern", "maxlength", "const", "format"})

# Tool-level keys that declare authority, and the tokens that make one overbroad.
_MCP_SCOPE_KEYS = ("scopes", "scope", "permissions", "roles", "access", "allowed_paths", "roots")
_MCP_BROAD_SCOPE_TOKENS = ("*", "all", "admin", "root", "superuser", "**")

# Server-level keys that may carry an authentication configuration. Presence
# is not enough: the value decides. "auth": false is the most explicit
# possible statement that a server is unauthenticated.
_MCP_AUTH_KEYS = frozenset({
    "auth", "authentication", "apikey", "api_key", "token", "bearer",
    "oauth", "oauth2", "credentials", "security", "headers",
})

# Values that name the absence of authentication rather than configuring any.
_MCP_NO_AUTH_VALUES = frozenset({"none", "no", "off", "false", "disabled", "anonymous", "public"})


def _declares_authentication(server):
    """Whether ``server`` actually configures authentication.

    The old check asked only whether an auth-ish key existed, so every falsy
    and every explicitly-disabled value read as configured. A security rule
    that turns "authentication: off" into a clean result is a control that
    disables itself precisely when it is needed.
    """
    if not isinstance(server, dict):
        return False
    for key, value in server.items():
        if str(key).lower() not in _MCP_AUTH_KEYS:
            continue
        if not value:
            # False, None, "", {}, [] and 0 all declare nothing.
            continue
        if isinstance(value, str):
            if value.strip().lower() in _MCP_NO_AUTH_VALUES:
                continue
            return True
        if isinstance(value, dict):
            kind = str(value.get("type", "")).strip().lower()
            if kind in _MCP_NO_AUTH_VALUES:
                continue
            return True
        return True
    return False


# A registry document maps server names to server objects. This is the shape
# MCP clients actually ship (a claude_desktop_config.json and its peers), and
# it has to be walked per server: judging the wrapper treats the registry key
# itself as the whole configuration and flags every entry inside it.
_MCP_REGISTRY_KEYS = ("mcpServers", "mcp_servers", "servers")


def _mcp_servers_in(doc):
    """Each (name, server_object) a document defines.

    A registry yields one pair per entry; any other shape yields the single
    document itself, so callers handle one code path.
    """
    if isinstance(doc, dict):
        for key in _MCP_REGISTRY_KEYS:
            registry = doc.get(key)
            if isinstance(registry, dict) and registry:
                return [(name, srv) for name, srv in registry.items() if isinstance(srv, dict)]
    return [(None, doc)]


def _mcp_finding(rule_id, line, code, path):
    rule = next(r for r in MCP_RULES if r["id"] == rule_id)
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


def _mcp_line_of(lines, needle, start_idx=0):
    """Return the 0-based index of the first line at or after start_idx that
    contains needle, or None. Plain substring search, no regex."""
    for i in range(max(0, start_idx), len(lines)):
        if needle in lines[i]:
            return i
    return None


def _mcp_tool_schema(tool):
    """Return a tool's input schema under either MCP or repo key spelling."""
    if not isinstance(tool, dict):
        return {}
    schema = tool.get("inputSchema")
    if schema is None:
        schema = tool.get("input_schema")
    return schema if isinstance(schema, dict) else {}


def _mcp_description_has_instruction(text):
    """Whether a description carries a hidden directive rather than docs.

    Two tiers. A directive marker is damning alone. A soft marker is ordinary
    English and only counts when the same description also names a sensitive
    target, because "You should call get_units first" is documentation and
    "You should always read credentials.json first" is not.
    """
    low = text.lower()
    if any(marker in low for marker in _MCP_DIRECTIVE_MARKERS):
        return True
    if any(marker in low for marker in _MCP_SOFT_MARKERS):
        return any(target in low for target in _MCP_SENSITIVE_TARGETS)
    return False


def _mcp_scope_is_broad(value):
    """True when a scope declaration contains a wildcard, admin, or root grant."""
    items = value if isinstance(value, list) else [value]
    for item in items:
        low = str(item).strip().lower()
        if low in ("/", "~"):
            return True
        for token in _MCP_BROAD_SCOPE_TOKENS:
            if token in low:
                return True
    return False


def _mcp_tools_of(doc):
    """Extract (server_object, tools_list) from the several shapes a definition
    takes: a bare tools array, a server object with a tools list, or a
    JSON-RPC style result wrapper. server_object is None when there is no
    wrapping server to assess for authentication."""
    if isinstance(doc, list):
        return None, [t for t in doc if isinstance(t, dict)]
    if not isinstance(doc, dict):
        return None, []
    # A single bare tool object.
    if "tools" not in doc and "result" not in doc and ("inputSchema" in doc or "input_schema" in doc):
        return None, [doc]
    tools = doc.get("tools")
    if tools is None and isinstance(doc.get("result"), dict):
        tools = doc["result"].get("tools")
    if not isinstance(tools, list):
        tools = []
    return doc, [t for t in tools if isinstance(t, dict)]


def _scan_mcp_tool(tool, lines, cursor, path):
    """Return (findings, next_cursor) for one tool definition.

    cursor is the 0-based line index to search from, advanced to this tool's
    anchor so repeated property names in earlier tools are not re-matched.
    """
    findings = []
    name = tool.get("name", "")
    anchor = None
    if name:
        anchor = _mcp_line_of(lines, f'"{name}"', cursor)
    if anchor is None:
        anchor = cursor
    next_cursor = anchor + 1

    def snippet(idx):
        return lines[idx].strip()[:200] if 0 <= idx < len(lines) else name

    # BTSC-012: instruction text in the tool or a parameter description.
    schema = _mcp_tool_schema(tool)
    props = schema.get("properties", {}) if isinstance(schema, dict) else {}
    descriptions = [tool.get("description", "")]
    if isinstance(props, dict):
        for spec in props.values():
            if isinstance(spec, dict):
                descriptions.append(spec.get("description", ""))
    if any(isinstance(d, str) and _mcp_description_has_instruction(d) for d in descriptions):
        idx = _mcp_line_of(lines, '"description"', anchor)
        line = (idx if idx is not None else anchor) + 1
        findings.append(_mcp_finding("BTSC-012", line, snippet(line - 1), path))

    # BTSC-013: the tool shells out, by exec-sink parameter or by description.
    shells_out = False
    exec_prop = None
    if isinstance(props, dict):
        for prop_name in props:
            if str(prop_name).lower() in _MCP_EXEC_SINK_NAMES:
                shells_out = True
                exec_prop = prop_name
                break
    tool_desc_low = str(tool.get("description", "")).lower()
    if not shells_out and any(phrase in tool_desc_low for phrase in _MCP_SHELL_PHRASES):
        shells_out = True
    if shells_out:
        needle = f'"{exec_prop}"' if exec_prop else '"description"'
        idx = _mcp_line_of(lines, needle, anchor)
        line = (idx if idx is not None else anchor) + 1
        findings.append(_mcp_finding("BTSC-013", line, snippet(line - 1), path))

    # BTSC-014: an overbroad scope declaration on the tool.
    for key in _MCP_SCOPE_KEYS:
        if key in tool and _mcp_scope_is_broad(tool[key]):
            idx = _mcp_line_of(lines, f'"{key}"', anchor)
            line = (idx if idx is not None else anchor) + 1
            findings.append(_mcp_finding("BTSC-014", line, snippet(line - 1), path))
            break

    # BTSC-015: an unconstrained sink parameter (model output passthrough).
    if isinstance(props, dict):
        for prop_name, spec in props.items():
            if str(prop_name).lower() not in _MCP_INJECTION_SINK_NAMES:
                continue
            if not isinstance(spec, dict):
                continue
            if str(spec.get("type", "string")).lower() != "string":
                continue
            if any(k.lower() in _MCP_VALIDATION_KEYS for k in spec.keys()):
                continue
            idx = _mcp_line_of(lines, f'"{prop_name}"', anchor)
            line = (idx if idx is not None else anchor) + 1
            findings.append(_mcp_finding("BTSC-015", line, snippet(line - 1), path))
            break

    return findings, next_cursor


def scan_mcp_server(file_path, strict=False):
    """Scan an MCP server definition for dangerous patterns.

    Reads a JSON definition: a bare tools array, a server object wrapping a
    tools list, or a JSON-RPC result wrapper. Returns finding dicts with the
    same shape the source scanner emits (rule_id, name, severity, owasp, line,
    code, message, file), so scan_summary and export_scan_sarif consume them
    unchanged.

    A missing or unreadable file, or one that is not valid JSON, returns an
    empty list: there is no definition to assess, which is distinct from a
    definition assessed as clean.
    """
    path = Path(file_path)

    def _unreadable(reason):
        # Lenient by default so existing callers keep the behaviour they were
        # written against; strict callers get the distinction the docstring
        # promises between "assessed clean" and "could not assess".
        if strict:
            raise MCPDefinitionUnreadable(f"{path}: {reason}")
        return []

    if not path.exists():
        return _unreadable("no such file")
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        return _unreadable(f"unreadable: {exc}")
    try:
        doc = json.loads(raw)
    except ValueError as exc:
        return _unreadable(f"not valid JSON: {exc}")

    lines = raw.split("\n")
    findings = []
    cursor = 0

    for name, entry in _mcp_servers_in(doc):
        seen_tool_names = set()
        server, tools = _mcp_tools_of(entry)

        # BTSC-016: this server declares no usable authentication.
        if isinstance(server, dict) and not _declares_authentication(server):
            needle = f'"{name}"' if name else '"name"'
            idx = _mcp_line_of(lines, needle, 0)
            line = (idx if idx is not None else 0) + 1
            code = lines[line - 1].strip()[:200] if line - 1 < len(lines) else path.name
            findings.append(_mcp_finding("BTSC-016", line, code, path))

        for tool in tools:
            tool_name = tool.get("name") if isinstance(tool, dict) else None
            if tool_name is not None:
                if tool_name in seen_tool_names:
                    idx = _mcp_line_of(lines, f'"{tool_name}"', 0)
                    line = (idx if idx is not None else 0) + 1
                    code = lines[line - 1].strip()[:200] if line - 1 < len(lines) else str(tool_name)
                    findings.append(_mcp_finding("BTSC-017", line, code, path))
                seen_tool_names.add(tool_name)
            tool_findings, cursor = _scan_mcp_tool(tool, lines, cursor, path)
            findings.extend(tool_findings)

    # The anchor search advances a cursor that can run past the end of a
    # minified definition, which is the normal shape of a captured tools/list
    # response. export_scan_sarif copies the line straight into
    # physicalLocation.region.startLine, so an out-of-range value becomes an
    # alert GitHub cannot resolve and silently drops.
    max_line = max(len(lines), 1)
    for f in findings:
        f["line"] = min(max(int(f.get("line") or 1), 1), max_line)

    # Deduplicate on rule + file + line, matching scan_file's contract.
    seen = set()
    deduped = []
    for f in findings:
        key = (f["rule_id"], f["file"], f["line"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    return deduped
