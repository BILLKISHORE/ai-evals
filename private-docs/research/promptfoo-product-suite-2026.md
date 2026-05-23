# Promptfoo Product Suite - Deep Research (March 2026)

**Status**: Acquired by OpenAI (announced March 9, 2026, closing pending)
**GitHub**: 18.8k stars, MIT license, v0.121.3, 7,850 commits, 96.9% TypeScript
**Users**: 350,000+ developers, 130,000 monthly active, 127 of Fortune 500
**Team**: 23 people, founded 2024, investors: Insight Partners, a16z
**Open source commitment**: Will remain open source and MIT licensed post-acquisition

---

## 1. Red Teaming

The flagship product. Generates adversarial attacks against LLM applications using agentic attack strategies.

### Scale
- **135 plugins** across 6 categories
- **40+ strategies** across 5 categories
- **80+ provider integrations**
- **50+ vulnerability types** tested
- Free tier: 10,000 probes/month

### Plugin Categories (135 total)

| Category | Count | Examples |
|----------|-------|---------|
| Brand | 14 | Competitor endorsement, financial hallucination, goal misalignment, imitation, political opinions |
| Compliance & Legal | 48 | COPPA, FERPA, TCPA, fair housing, pharmacy, telecom, insurance, billing misinformation, copyright |
| Dataset | 11 | Aegis, BeaverTails, CyberSecEval, DoNotAnswer, HarmBench, Pliny, ToxicChat, UnsafeBench, XSTest |
| Security & Access Control | 41 | ASCII smuggling, cross-session leak, SQL injection, SSRF, prompt extraction, RAG poisoning, shell injection, BOLA, BFLA |
| Trust & Safety | 19 | Age/disability/gender/race bias, child exploitation, graphic content, harassment, hate speech, self-harm |
| Custom | 2 | Custom prompts (intent), custom topic (policy) |

### Strategy Categories (40+ total)

| Category | Count | Key Strategies |
|----------|-------|---------------|
| Static | 14 | Base64, hex, ROT13, homoglyph, leetspeak (deterministic, low-resource) |
| Dynamic | 13 | Jailbreak, composite jailbreaks, GCG, tree-based, citation (LLM-powered, higher success) |
| Multi-turn | 4 | Crescendo (gradual escalation), GOAT (generative offensive agent), Hydra (adaptive branching), Mischievous User |
| Regression | 1 | Retry (re-tests previously failed cases) |
| Custom | 2 | JavaScript or natural language defined |

Strategies improve detection rates by 20-90%.

### Compliance Framework Mappings
- OWASP LLM Top 10 (owasp:llm:01 through 10)
- OWASP API Security Top 10 (owasp:api:01 through 10)
- NIST AI RMF (nist:ai:measure with sub-items)
- MITRE ATLAS (tactics: reconnaissance, initial-access, etc.)
- EU AI Act (eu:ai-act)
- ISO/IEC 42001 (iso:42001)
- GDPR
- DoD AI Ethics (dod:ai:ethics)

### Agentic Red Teaming (Advanced)
Three-layer testing methodology for LLM agents:

1. **Black-box testing** - End-to-end testing as a user would interact
2. **Component testing** - Isolate individual agent steps via custom Python providers
3. **Trace-based testing** - OpenTelemetry integration creating adversarial feedback loops where trace data informs the next attack iteration

Agent-specific attack types:
- Memory poisoning (inject into conversation history)
- Multi-stage attack chains (sequential tool exploitation)
- Tool/API manipulation (database, email, file, auth, payment)
- Privilege escalation (RBAC/BOLA/BFLA)
- RAG document exfiltration
- Tool discovery

### Configuration
YAML-based with support for:
- Multi-language test generation (any language)
- Custom test generation instructions
- Per-plugin severity levels (low/medium/high/critical)
- Custom grader examples and guidance
- Context-aware testing (different user states/roles)
- Custom policies

---

## 2. Guardrails

Real-time protection layer that blocks attacks at inference time. Enterprise/paid product.

### Architecture
- **Feedback loop design**: Red team tests generate attacks -> vulnerabilities found -> guardrail policies auto-update -> attacks blocked
- **Two policy types**: Automated (generated from red team failures, updated on regen) and Manual (user-defined, persistent)
- **Processing pipeline**: Fast filters (regex pre-filtering for PII/credit cards/SSNs) -> LLM-based policy evaluation (if no fast filter matches)
- **API endpoint**: `POST /api/v1/guardrails/{ID}/evaluate` with bearer token auth

### Placement Types (4)
1. `INPUT` - Filter user input before it reaches the LLM
2. `OUTPUT` - Filter LLM response before it reaches the user
3. `TOOL_CALL_INPUT` - Validate tool arguments before execution
4. `TOOL_CALL_OUTPUT` - Validate tool results before returning

### Performance
- Sequential execution: Guardrail runs before LLM (prevents malicious requests from reaching model, adds latency)
- Parallel execution: Guardrail runs alongside LLM (minimizes TTFT, but wastes LLM cost on blocked prompts)
- Only policy text sent at runtime - no raw examples, keeping latency low

### Scale Thresholds
- 500 examples max per vulnerability for policy generation
- 300 jailbreak examples for content generation
- 50 examples max per validation
- Auto map-reduce at >20 examples (batch size 25)

### Key Limitation
Can only block patterns similar to discovered vulnerabilities. Novel attacks require new red team runs to update policies. This is the core value proposition of the red-team-to-guardrail feedback loop.

### Pricing
Enterprise only. Not available in the free/community tier.

---

## 3. Model Security

End-to-end security from model files to deployed instances. Three pillars:

### Pillar 1: Model File Security (Static Analysis)
- Scans model files before deployment for malicious code, backdoors, risky configs, suspicious operations
- Supported formats: PyTorch, TensorFlow, Keras, Pickle, JSON/YAML
- Think of it as antivirus for model files

### Pillar 2: Behavioral Testing
- Tests model behavior against jailbreaks, injection attacks, stress conditions
- Works with both foundation and fine-tuned models
- Overlaps with Red Teaming but positioned as continuous monitoring

### Pillar 3: Compliance Mapping
- Generates compliance reports mapped to OWASP Top 10, NIST AI RMF, EU AI Act, MITRE ATLAS
- Custom policy creation

### How It Differs from Red Teaming
- Red Teaming = proactive vulnerability discovery (offense)
- Model Security = lifecycle protection (defense) including file-level scanning, behavioral monitoring, and compliance reporting
- Model Security includes the model file scanning capability that Red Teaming doesn't
- Model Security is more about continuous monitoring; Red Teaming is about point-in-time testing

---

## 4. MCP Proxy

Secure proxy for Model Context Protocol communications. Targets organizations using AI applications with MCP tool integrations.

### Core Functions
- **Whitelist-based access control**: Only approved MCP servers allowed, preventing unauthorized tool access
- **Granular permissions**: Per-application and per-user MCP server access
- **Centralized policy management**: Single dashboard for all MCP policies

### Monitoring & Alerting
- Real-time monitoring of MCP interactions with focus on PII/sensitive data exposure
- Alerts for suspicious activity, policy violations, unauthorized access attempts
- Detailed logging of all MCP requests
- Centralized audit logs

### Positioning
- Relatively new product (added to lineup recently)
- Targets enterprise security teams worried about uncontrolled MCP tool access
- Solves the problem of developers connecting AI assistants to arbitrary MCP servers

---

## 5. Code Scanning

SAST-like tool purpose-built for LLM/AI vulnerabilities in application code.

### 6 Vulnerability Categories Detected

1. **Prompt Injection** - Untrusted input reaching LLM prompts without sanitization
2. **Data Exfiltration** - Indirect prompt injection vectors extracting data through agent tools
3. **PII Exposure** - Code leaking sensitive user data to LLMs or logging confidential info
4. **Improper Output Handling** - LLM outputs used in dangerous contexts (SQL queries, shell commands)
5. **Excessive Agency** - LLMs with overly broad tool access or missing approval gates
6. **Jailbreak Risks** - Weak system prompts and guardrail bypasses

### How It Works
- AI agents trace data flows across the codebase (not surface-level pattern matching)
- Cross-file analysis, not just single-file rules
- High signal, low noise (not a generic SAST tool)

### IDE Integration
- VS Code extension
- Real-time scanning as developers write code
- Inline diagnostics with severity indicators
- One-click quick fixes
- AI-assisted remediation prompts
- Scan-on-save or on-demand

### CI/CD Integration
- PR comments with security findings and inline suggested fixes
- Severity-based blocking (fail builds on critical findings)
- GitHub integration
- Jenkins, GitLab, CircleCI support
- JSON output for automation
- Configurable severity thresholds

### Positioning vs Traditional SAST
- Claims general SAST tools miss LLM-specific vulnerabilities
- Purpose-built for AI application security
- Detects issues that only exist in AI codebases (prompt injection, excessive agency, etc.)

---

## 6. Evaluations

The original product - an open-source eval framework for testing prompts, models, and RAG pipelines.

### Core Capabilities
- Matrix evaluation: test every combination of prompts x providers x test cases
- Side-by-side model comparison (60+ providers)
- RAG pipeline evaluation with context-based metrics
- Web UI for result visualization
- CLI + YAML configuration

### Assertion Types (54+ total)

**Deterministic (26+)**:
equals, contains, icontains, regex, starts-with, contains-any, contains-all, icontains-any, icontains-all, is-json, contains-json, contains-html, is-html, is-sql, contains-sql, is-xml, contains-xml, is-refusal, javascript, python, webhook, rouge-n, bleu, gleu, levenshtein, latency, meteor, perplexity, cost, is-valid-function-call, is-valid-openai-tools-call, trace-span-count, trace-span-duration, guardrails

**Model-Assisted (13+)**:
similar, classifier, llm-rubric, g-eval, answer-relevance, context-faithfulness, context-recall, context-relevance, conversation-relevance, trajectory:goal-success, factuality, model-graded-closedqa, pi, select-best

All can be negated with "not-" prefix.

### RAG-Specific Metrics
- **Context Adherence (Faithfulness)**: Does the output rely on provided context?
- **Context Recall**: Does the context contain the info needed to answer?
- **Context Relevance**: How much of the context is necessary for the answer?
- **Answer Relevance**: Does the response directly address the question?
- **Factuality**: Are outputs based on ground truth?
- Cross-lingual support with concept-based metrics

### Configuration Features
- YAML-based with modular imports
- Variable loading from YAML, JSON, CSV, JavaScript, Python, PDFs
- Nunjucks templating
- Dynamic context loading via Python scripts (query vector DBs per test case)
- Transform functions for pre/post-processing
- Google Sheets as data source
- Tool/function calling support
- Extended thinking (Claude) support
- defaultTest for shared assertions across all cases

### Provider Support (80+)
OpenAI, Anthropic, Google/Vertex, AWS Bedrock, Azure OpenAI, Mistral, Cohere, Groq, DeepSeek, Cloudflare AI Gateway, Vercel AI Gateway, LiteLLM (400+ models), Ollama, vLLM, llama.cpp, custom via JavaScript/Python/Go/Ruby, HTTP/WebSocket/Shell

---

## Pricing Summary

| Feature | Community (Free) | Enterprise | On-Premise |
|---------|-----------------|------------|------------|
| All eval features | Yes | Yes | Yes |
| All model providers | Yes | Yes | Yes |
| Red team probes | 10k/month | Custom limits | Custom limits |
| Vulnerability scanning | Yes | Advanced | Advanced |
| CI/CD integration | Yes | Yes | Yes |
| Guardrails | No | Yes | Yes |
| Continuous monitoring | No | Yes | Yes |
| Team sharing | No | Yes | Yes |
| Compliance dashboard | No | Yes | Yes |
| SSO/permissions | No | Yes | Yes |
| API access | No | Yes | Yes |
| Managed cloud | No | Yes | No |
| Custom attack profiles | No | Yes | Yes |
| Webhooks | No | Yes | Yes |
| Data isolation | No | No | Yes |
| Dedicated runner | No | No | Yes |
| Deployment engineer | No | No | Yes |

---

## Competitive Implications for ai-blackteam

### What Promptfoo Has That We Don't
1. **Guardrails** - Real-time inference protection with red-team feedback loop
2. **Code Scanning** - SAST for AI code (IDE + CI/CD)
3. **MCP Proxy** - MCP server access control and monitoring
4. **Model File Scanning** - Static analysis of model files (PyTorch, TF, Pickle)
5. **Evaluations Framework** - Full eval suite with 54+ assertion types
6. **Compliance Dashboards** - Enterprise compliance reporting (OWASP, NIST, EU AI Act, MITRE ATLAS, ISO 42001, GDPR, DoD)
7. **Trace-based Testing** - OpenTelemetry integration for glass-box agent testing
8. **Scale** - 135 plugins, 40+ strategies, 80+ providers
9. **Enterprise Features** - SSO, team sharing, webhooks, managed cloud, on-prem

### What We Have That They Don't
1. Independent (not owned by a model provider - OpenAI conflict of interest)
2. Python-native (their tool is TypeScript)
3. Focus on actual offensive security research (CBRN, ASL3, WMDP)
4. Lighter weight, faster to run
5. No vendor lock-in concerns

### Product Gaps to Consider Building
1. **Guardrails/runtime protection** - Biggest gap. Their feedback loop from red team to guardrails is their core moat.
2. **Code scanning** - Novel product category. No other AI security tool does this. Low effort to add basic rules.
3. **MCP security** - Growing attack surface. MCP adoption is exploding.
4. **Compliance reporting** - Enterprise buyers need OWASP/NIST/EU AI Act mappings. We have some, they have more.
5. **Eval framework integration** - Their eval framework is the foundation everything else builds on.
6. **Model file scanning** - Interesting niche. Pickle deserialization attacks are real.

### OpenAI Acquisition Risk
- Promptfoo is now an OpenAI property
- Potential conflict of interest: OpenAI testing OpenAI models
- Enterprise customers may want independent testing (our opportunity)
- Open source may stagnate or diverge from enterprise version
- 18.8k stars community will watch closely for any rug-pull
