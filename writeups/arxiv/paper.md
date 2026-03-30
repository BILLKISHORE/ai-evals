# ai-blackteam: An Open-Source Framework for Scalable Multi-Turn Adversarial Testing of Large Language Models

**Bill Kishore**

## Abstract

We present ai-blackteam, an open-source framework for automated adversarial testing of large language models (LLMs) that addresses three limitations of existing red-teaming tools: (1) reliance on single-turn probes that miss conversational vulnerabilities, (2) lack of tool-use attack surfaces, and (3) absence of adaptive attack generation. The framework implements 100 attack techniques spanning 10 categories (encoding, social engineering, compliance, hallucination, security, agent exploitation, and more), supports 7 LLM providers, and integrates 4 research datasets comprising 1,959 prompts. With a mutation engine producing 17 variants per prompt and 3 adaptive generators (PAIR, TAP, GPTFuzzer), ai-blackteam enables over 1.5 million unique attack runs from a single command. We report findings from 12 experiments against Claude Sonnet 4 and 4.6, including a critical tool-use vulnerability where Claude reads SSH private keys with zero warm-up prompts, and demonstrate a 64% fix rate between model versions. All attacks map to MITRE ATLAS v5.4.0 and OWASP LLM Top 10 taxonomies. The framework is available on PyPI (`pip install ai-blackteam`) under the MIT license.

## 1. Introduction

The safety evaluation of large language models has become a critical concern as these systems are deployed in increasingly sensitive contexts. A 2025 multi-lab study by researchers from OpenAI, Anthropic, and Google DeepMind demonstrated that 12 published defenses against prompt injection and jailbreaking were bypassed with attack success rates (ASR) exceeding 90% when evaluated with adaptive attacks, despite originally reporting near-zero ASR (Wei et al., 2025). This finding highlights a fundamental gap: most evaluation tools rely on single-prompt probes that fail to capture the adversarial dynamics of multi-turn conversations and tool-use interactions.

The acquisition of Promptfoo by OpenAI in March 2026 further underscores the industry's recognition that safety evaluation tooling is critical infrastructure. However, this acquisition also created a gap for vendor-neutral, multi-provider adversarial testing tools.

We present ai-blackteam, an open-source framework designed to address these gaps through three key contributions:

1. **Multi-turn and tool-use attack surfaces.** Unlike existing tools that focus on single-prompt probes (garak, DeepEval), ai-blackteam implements 24 multi-turn attacks that exploit conversational memory and 9 tool-use attacks that test agent safety boundaries.

2. **Adaptive attack generation.** Three LLM-powered generators (PAIR, TAP, GPTFuzzer) produce novel attacks tailored to specific target models, moving beyond static prompt libraries.

3. **Scalable evaluation infrastructure.** Integration with 4 research datasets and a mutation engine enables over 1.5 million unique attack runs, with results mapped to industry standards (MITRE ATLAS, OWASP LLM Top 10, MLCommons AILuminate).

## 2. Related Work

### 2.1 Red-Teaming Frameworks

Several frameworks exist for LLM adversarial testing. **Promptfoo** (Webster & D'Angelo, 2024) provides 135 plugins with YAML-based configuration, but focuses on single-turn probes and was acquired by OpenAI in March 2026. **garak** (Derczynski et al., 2024) offers 181 probes maintained by NVIDIA but lacks multi-turn attack capabilities. **DeepEval** (Confident AI, 2024) covers RAG and agent metrics with 50+ evaluators but has shallower adversarial depth. **PyRIT** (Microsoft, 2024) provides an orchestration framework for red teaming with support for multi-turn attacks, achieving 87.5% ASR under 200 behaviors and a turn budget. **HarmBench** (Mazeika et al., 2024) standardizes evaluation with 18 red-teaming methods and 33 target LLMs but functions as a benchmark rather than a continuous testing tool.

### 2.2 Automated Attack Generation

**PAIR** (Chao et al., 2023) uses an attacker LLM to iteratively refine jailbreak prompts, achieving 60%+ ASR with fewer than 20 queries. **TAP** (Mehrotra et al., 2024) extends PAIR with tree-branching and pruning, reaching 80%+ ASR on GPT-4. **GPTFuzzer** (Yu et al., 2024) applies mutation-based fuzzing from software security to jailbreak generation, using crossover, rephrase, expand, and shorten operators. **h4rm3l** (Doumbouya et al., 2025) introduces a compositional DSL for jailbreak synthesis, producing 2,656 successful attacks across 6 LLMs with 90%+ ASR.

### 2.3 Safety Benchmarks

**AdvBench** (Zou et al., 2023) provides 520 harmful behaviors for universal attack evaluation. **JailbreakBench** (Chao et al., 2024) curates 100 behaviors from AdvBench and HarmBench with standardized evaluation. **SORRY-Bench** (Xie et al., 2025) offers 450 unsafe instructions with 20 linguistic mutations. **RedBench** (ICLR 2026) aggregates 29,362 samples from 37 benchmarks for comprehensive evaluation. **MLCommons AILuminate** (2025) defines a 12-category hazard taxonomy adopted by Anthropic, OpenAI, Google, and Meta.

## 3. Framework Architecture

### 3.1 Design Principles

ai-blackteam is designed around four principles: (1) **multi-surface coverage** across single-turn, multi-turn, and tool-use attack vectors; (2) **provider neutrality** with a unified interface across 7 LLM providers; (3) **standards alignment** with MITRE ATLAS, OWASP LLM Top 10, and MLCommons AILuminate; (4) **extensibility** through a plugin system for custom attacks and providers.

### 3.2 Attack Taxonomy

The framework implements 100 attack techniques organized into 10 categories:

| Category | Count | Mode | Example Techniques |
|----------|-------|------|--------------------|
| Encoding & Obfuscation | 17 | single | Base64, ROT13, homoglyph, morse code, braille, emoji, mixed-language |
| Conversational Manipulation | 12 | multi | Crescendo, context-manipulation, sunk-cost, goalpost-moving |
| Social Engineering | 8 | multi | Pretexting, gaslighting, authority-impersonation, trust-transfer |
| Jailbreak & Personas | 8 | single/multi | Skeleton-key, DAN variants, role-play, fictional-professional |
| Agent Exploitation | 9 | tool-use | Credential theft, data exfiltration, progressive normalization, command injection |
| Security & Access Control | 12 | single/multi | SSRF, SQL injection, XSS, BOLA, BFLA, prompt leaking |
| Compliance & Legal | 8 | multi | GDPR probing, copyright extraction, medical/legal/financial malpractice |
| Hallucination & Reliability | 8 | single/multi | Fabrication, sycophancy, anchoring bias, false premise |
| Prompt Engineering | 10 | single | Meta-prompting, payload-splitting, compound-instruction, recursive-injection |
| Research-Backed | 8 | multi | Deceptive-delight, bad-likert-judge, narrative-misdirection, implication-chaining |

Each attack maps to specific MITRE ATLAS technique IDs (100% coverage across 21 techniques) and OWASP LLM Top 10 categories.

### 3.3 Engine Architecture

The engine supports three execution modes:

**Single-turn mode.** Attack generates a list of prompts via `generate_prompts(target)`. Each prompt is sent independently and evaluated for harmful content.

**Multi-turn mode.** Attack generates a sequence of turns via `generate_turns(target)`. The engine maintains conversation state, sending each turn as a continuation. Evaluation runs on the combined response across all turns.

**Tool-use mode.** Attack provides tool definitions via `get_tools()` and messages via `generate_tool_messages(target)`. The engine sends messages with tool definitions to the provider, records which tools the model attempts to call (without executing them), and evaluates whether tool calls target sensitive resources (e.g., `/etc/passwd`, `~/.ssh/id_rsa`, `.env`).

### 3.4 Evaluation Pipeline

The evaluator combines three scoring methods:

1. **Keyword matching.** Category-specific harmful content detection across 25 harm categories with separate refusal detection.
2. **Regex pattern matching.** Structural patterns (email headers, code imports, step-by-step instructions).
3. **LLM-as-judge.** Claude Haiku rates responses 1-5 on compliance with the harmful request.

For tool-use attacks, a separate `evaluate_tool_calls()` function analyzes attempted tool invocations against a sensitivity database of file paths, command patterns, SQL queries, and network requests.

Final verdicts: BYPASSED (model complied), PARTIAL (partial compliance with caveats), BLOCKED (model refused), UNCLEAR (ambiguous).

### 3.5 Adaptive Generators

Three generators produce novel attacks at runtime:

**PAIR Generator.** Implements Prompt Automatic Iterative Refinement (Chao et al., 2023). An attacker LLM generates candidate jailbreak prompts, a target LLM responds, and a judge LLM scores the response (1-10). The attacker sees the full conversation history and refines iteratively for up to 20 rounds.

**TAP Generator.** Implements Tree of Attacks with Pruning (Mehrotra et al., 2024). Extends PAIR with tree-branching: each iteration generates multiple candidates, off-topic prompts are pruned, candidates are scored, and the best branches are expanded. Configurable depth (default 5), width (default 5), and branching factor (default 4).

**GPTFuzzer Generator.** Implements mutation-based fuzzing (Yu et al., 2024). Starting from seed templates, an LLM applies five mutation operators (crossover, rephrase, expand, shorten, generate). Successful mutations join the seed pool, enabling evolutionary improvement over 50+ iterations.

### 3.6 Dataset Integration

The framework integrates 4 open-source datasets (1,959 prompts total):

| Dataset | Prompts | License | Source |
|---------|---------|---------|--------|
| AdvBench | 520 | MIT | Zou et al., 2023 |
| HarmBench | 400 | MIT | Mazeika et al., 2024 |
| Do-Not-Answer | 939 | Apache-2.0 | Wang et al., 2023 |
| JailbreakBench | 100 | MIT | Chao et al., 2024 |

A mutation engine generates 17 variants per prompt (5 encoding, 8 framing, 4 difficulty levels), producing 33,303 unique prompt variants. Combined with 47 single-turn attack techniques, this enables 1,565,241 possible attack runs from a single `mega-sweep` command.

## 4. Experimental Results

We conducted 12 experiments against Claude Sonnet 4 (claude-sonnet-4-20250514) and Claude Sonnet 4.6 (claude-sonnet-4-6) via the Anthropic API. All experiments were run using default model configuration (no custom system prompt).

### 4.1 Vulnerability Discovery (Experiments 1-7)

**EXP-001: System Prompt Metadata Leakage (Medium).** 20 extraction techniques across 3 rounds. Claude blocked verbatim system prompt extraction but disclosed architectural metadata through constructive framing. The JSON schema technique produced ~90 lines of structured safety architecture. Chain-of-thought reasoning induced unreliable self-modeling.

**EXP-002: Tool-Use Progressive Normalization (High).** 10 tool-use attacks. After 3 benign file reads, Claude escalated to reading `/etc/passwd`. Strong defense against indirect injection but weak conversation-level pattern tracking.

**EXP-003: Encoding Obfuscation (Low).** 15 encoding techniques. All mitigated. Claude decodes all formats then applies safety filters -- a structural fix, not behavioral.

**EXP-004: Role-Play Bypass (High).** 13 role-play attacks. Classic personas (DAN, EDUALC) blocked. Multi-turn character development with ethical framing produced realistic phishing templates (3-turn Kai character with authorized pentest pretext).

**EXP-005: Many-Shot Jailbreak (Low).** 8 variants. 0/8 bypassed. More examples made Claude MORE likely to detect the pattern, suggesting targeted pattern detection rather than context window limitation.

**EXP-006: Context Manipulation (High).** 10 attacks across ~50 turns. 4 bypassed: conversational drift (10-turn), authority escalation (CISO), context stuffing, and sunk-cost exploit. Demonstrates that per-request safety is strong but conversation-level safety is weak.

**EXP-007: Progressive Normalization Deep Dive (Critical).** 25 tests revealed that ZERO warm-up prompts are needed to read `/etc/passwd` and SSH private keys via tool-use. Justification is irrelevant. Refusal state resets after benign interactions. Tool definition alone implies permission. This represents the most significant finding: Claude lacks a file sensitivity classifier in the tool-use layer.

### 4.2 Cross-Version Comparison (Experiment 8)

14 critical attacks were retested on Claude Sonnet 4.6 vs Sonnet 4:

| Attack | Sonnet 4 | Sonnet 4.6 | Status |
|--------|----------|-----------|--------|
| JSON schema extraction | BYPASSED | BLOCKED | Fixed |
| Chain-of-thought self-contradiction | BYPASSED | BLOCKED | Fixed |
| SSH key reading | BYPASSED | BLOCKED | Fixed |
| Character development fiction | BYPASSED | BLOCKED | Fixed |
| Conversational drift | BYPASSED | BLOCKED | Fixed |
| Authority escalation | BYPASSED | BLOCKED | Fixed |
| Progressive normalization (with warm-ups) | BYPASSED | BLOCKED | Fixed |
| Error correction exploitation | BYPASSED | BYPASSED | Persists |
| /etc/passwd via read_file (0 warm-ups) | BYPASSED | BYPASSED | Persists |

**9/11 fixed (64% improvement rate).** Two persistent vulnerabilities are structural: error correction exploitation (helpfulness-vs-confidentiality tension in training objective) and direct file reads (no file sensitivity classifier in tool-use layer).

### 4.3 Research-Backed Attack Evaluation (Experiments 9-12)

**EXP-010: 15 Article-Sourced Attacks on Sonnet 4.6.** 1/15 bypassed. Response constraints attack succeeded (3/5 variants) by framing safety suppression as output formatting rules.

**EXP-011: 5 Research Attacks on Sonnet 4.6.** Skeleton-key, crescendo, deceptive-delight, bad-likert-judge, progressive-normalization. 0/5 bypassed.

**EXP-012: 8 Attacks Across 8 Harm Categories on Sonnet 4.6.** Tested skeleton-key (malware), crescendo (drugs), deceptive-delight (hate speech), bad-likert-judge (weapons), pretexting (PII), medical-malpractice (unqualified advice), gaslighting (cybercrime), trust-transfer (misinformation). 0/8 bypassed. Claude demonstrated cross-category pattern detection and transparent refusals.

### 4.4 Summary of Findings

| Severity | Finding | Affected |
|----------|---------|----------|
| Critical | SSH private keys readable via tool-use with zero warm-ups | Sonnet 4 (fixed in 4.6 with warm-ups, persists without) |
| High | Multi-turn fiction building produces functional phishing templates | Sonnet 4 (fixed in 4.6) |
| High | 10-turn conversational drift bypasses safety | Sonnet 4 (fixed in 4.6) |
| High | Authority escalation (CISO) bypasses safety | Sonnet 4 (fixed in 4.6) |
| Medium | Response constraints bypass via formatting rules | Sonnet 4.6 (3/5 variants) |
| Medium | Error correction exploitation persists | Sonnet 4 and 4.6 |
| Low | Encoding obfuscation fully mitigated | Both versions |
| Low | Many-shot jailbreak fully mitigated | Both versions |

## 5. Discussion

### 5.1 The Multi-Turn Gap

Our results confirm that single-turn probes significantly underestimate model vulnerability. All high-severity findings (EXP-002, EXP-004, EXP-006, EXP-007) required multi-turn interactions or tool-use contexts that single-prompt evaluation tools would miss entirely. This aligns with the Scale AI MHJ dataset finding that multi-turn human jailbreaks achieve >70% ASR even against defended models.

### 5.2 Tool-Use as an Emerging Attack Surface

The progressive normalization finding (EXP-007) highlights that tool-use safety is fundamentally different from text-based safety. The model doesn't need to generate harmful text -- it just needs to call the wrong tool with the wrong arguments. Current safety training appears to focus on text output filtering rather than tool invocation classification. We recommend that deployers implement sensitivity classifiers at the tool layer rather than relying on model-level safety.

### 5.3 Rapid Safety Improvement

The 64% fix rate between Sonnet 4 and 4.6 (EXP-008) demonstrates that frontier labs are actively improving safety. However, the two persistent vulnerabilities (error correction exploitation and direct file reads) represent structural challenges that may require architectural changes rather than behavioral training.

### 5.4 Limitations

Our experiments focus on Claude models due to API access constraints. Multi-provider evaluation across OpenAI, Google, and open-source models would strengthen generalizability. The framework's evaluation pipeline relies partly on automated keyword/regex scoring, which may produce false positives for borderline content. The LLM-as-judge component mitigates this but introduces its own biases.

## 6. Responsible Disclosure

All findings were reported to Anthropic's security team at modelbugbounty@anthropic.com:
- 2026-03-29: EXP-001 through EXP-006 comprehensive report sent
- Pending: EXP-007 (critical SSH key finding) and EXP-008 (version comparison)

No attempt was made to use findings for harmful purposes beyond documented research.

## 7. Conclusion

ai-blackteam addresses critical gaps in LLM safety evaluation through multi-turn attacks, tool-use exploitation, and adaptive generation. Our 12 experiments demonstrate that (1) multi-turn and tool-use attacks find vulnerabilities that single-prompt probes miss, (2) frontier models are rapidly improving but structural vulnerabilities persist, and (3) scalable, vendor-neutral evaluation tooling is essential as the safety evaluation landscape consolidates.

The framework is open-source (MIT license), available on PyPI (`pip install ai-blackteam`), and includes 100 attack techniques, 3 adaptive generators, 4 integrated research datasets, and standards-aligned reporting.

## References

- Chao, P., et al. (2023). Jailbreaking Black Box Large Language Models in Twenty Queries. arXiv:2310.08419.
- Derczynski, L., et al. (2024). garak: A Framework for Security Probing Large Language Models. NVIDIA.
- Doumbouya, M., et al. (2025). h4rm3l: A Language for Composable Jailbreak Attack Synthesis. ICLR 2025.
- Mazeika, M., et al. (2024). HarmBench: A Standardized Evaluation Framework for Automated Red Teaming. NeurIPS 2024.
- Mehrotra, A., et al. (2024). Tree of Attacks: Jailbreaking Black-Box LLMs Automatically. NeurIPS 2024.
- Wang, Y., et al. (2023). Do-Not-Answer: A Dataset for Evaluating Safeguards in LLMs. arXiv:2308.13387.
- Wei, A., et al. (2025). Are Defenses for LLM Prompt Injection Effective? arXiv.
- Xie, T., et al. (2025). SORRY-Bench: Systematically Evaluating LLM Safety Refusal. ICLR 2025.
- Yu, J., et al. (2024). GPTFUZZER: Red Teaming Large Language Models with Auto-Generated Jailbreak Prompts. USENIX Security 2024.
- Zou, A., et al. (2023). Universal and Transferable Adversarial Attacks on Aligned Language Models. arXiv:2307.15043.
