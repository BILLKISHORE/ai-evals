"""AI code security scanner for ai-blackteam.

Detects LLM-specific vulnerabilities in Python and JavaScript/TypeScript code:
- Prompt injection (user input in system prompts)
- Secrets in prompts (API keys, PII)
- Improper output handling (XSS, code execution, SQL injection)
- Excessive agency (unrestricted tools)
- Missing safety controls (no max_tokens, no input validation)

Usage:
    from blackteam.scanner import scan_file, scan_directory

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
        "owasp": "LLM05",
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
        "owasp": "LLM05",
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
        "owasp": "LLM05",
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
        "owasp": "LLM06",
        "description": "Tool/function exposed to LLM has unrestricted shell command execution.",
        "patterns": [
            # @tool decorator + subprocess/os.system
            r'''@tool.*\n(?:.*\n){0,10}.*subprocess\.(?:run|call|Popen)\s*\(.*shell\s*=\s*True''',
            r'''@tool.*\n(?:.*\n){0,10}.*os\.system\s*\(''',
            # Function in tools array with subprocess
            r'''(?:tools|functions)\s*=\s*\[(?:.*\n){0,20}.*subprocess\.(?:run|call|Popen)\s*\(.*shell\s*=\s*True''',
            # LangChain Tool with shell
            r'''class\s+\w+\s*\(\s*(?:BaseTool|Tool)\s*\).*\n(?:.*\n){0,20}.*subprocess.*shell\s*=\s*True''',
        ],
        "file_types": [".py"],
        "message": "Allowlist permitted commands. Never expose unrestricted shell access to an LLM.",
    },
    {
        "id": "BTSC-007",
        "name": "Excessive Agency: Unrestricted File Access",
        "severity": "high",
        "owasp": "LLM06",
        "description": "Tool/function exposed to LLM can read/write arbitrary file paths.",
        "patterns": [
            r'''@tool.*\n(?:.*\n){0,10}.*open\s*\(.*(?:path|file|filename)''',
            r'''@tool.*\n(?:.*\n){0,10}.*(?:read_file|write_file|Path)\s*\(''',
            r'''(?:tools|functions)\s*=\s*\[(?:.*\n){0,20}.*open\s*\(''',
        ],
        "file_types": [".py"],
        "message": "Restrict file access to specific directories. Validate paths against an allowlist.",
    },
    {
        "id": "BTSC-008",
        "name": "Missing max_tokens Limit",
        "severity": "medium",
        "owasp": "LLM10",
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
        "owasp": "LLM07",
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
        "owasp": "LLM08",
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
        compiled.append({**rule, "_compiled": compiled_patterns})
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

    for rule in COMPILED_RULES:
        if ext not in rule["file_types"]:
            continue

        for pattern in rule["_compiled"]:
            for match in pattern.finditer(content):
                # Find line number
                start = match.start()
                line_num = content[:start].count("\n") + 1

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
