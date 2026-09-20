# ai-blackteam

Automated LLM red team framework. Test any model's safety with one command.

[![PyPI](https://img.shields.io/pypi/v/ai-blackteam.svg)](https://pypi.org/project/ai-blackteam/) [![Docs](https://img.shields.io/badge/docs-live-E63946)](https://ai-blackteam.ai-evals.workers.dev/) [![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Docs:** https://ai-blackteam.ai-evals.workers.dev/

## Why ai-blackteam

Most eval tools run single-prompt probes. A 2025 multi-lab study (researchers from OpenAI, Anthropic, Google DeepMind) showed that adaptive attacks bypass 12 published defenses with >90% success rate, even when those defenses originally reported near-zero attack rates. Single-attempt testing misses real vulnerabilities.

ai-blackteam runs multi-turn, adaptive attacks that mirror real adversarial pressure:

- **Vendor-neutral**: tests 17 providers equally (16 vendors + your own HTTP endpoint), not owned by any AI lab
- **1,025 curated attack techniques**: encoding, conversational, psychological, security, compliance, agent exploitation, MCP exploitation, multi-agent, protocol, multimodal, supply chain, RAG exploitation vectors; 163M expanded attack surface; 61 categories; 3,503 tests
- **19 public benchmark loaders**: HarmBench, AdvBench, JailbreakBench, SorryBench, WMDP (bio/cyber/chem), DoNotAnswer, WildGuard, RedBench, SALAD-Bench, StrongREJECT, AART, ForbiddenQuestions, BeaverTails, RealToxicityPrompts, JailBreakV-28K, RedTeam-2K, AgentHarm
- **7 adaptive generators**: PAIR, TAP, Fuzzer, AutoDAN (genetic), PAP (persuasion), Crescendo (multi-turn), Best-of-N
- **Research-backed**: implements published attacks from Microsoft Research, Palo Alto Unit 42, USENIX, UK AI Safety Institute
- **Used in real disclosures**: findings produced with this framework were reported to Anthropic's security team through coordinated disclosure. See [Responsible Disclosure](#responsible-disclosure)
- **Multi-turn depth**: crescendo, sunk-cost, context-manipulation attacks that exploit conversational memory over 10+ turns
- **Agent attacks**: credential theft, data exfiltration, sandbox escape, config manipulation via tool-use; AgentHarm benchmark integrated
- **9 standards mapped**: code-level taxonomy mappings for MITRE ATLAS 2026.09, OWASP LLM Top 10 (2026), OWASP Agentic Top 10 (2026), MLCommons AILuminate, EU AI Act, NIST AI RMF, and CVSS; CSA MAESTRO and ISO 42001 as documented alignments. Three runnable scorecards: `scorecard --standard llm | agentic | compliance`
- **CI-ready**: GitHub Actions workflow, exit codes, JSON/Promptfoo/garak export

## Install

```bash
pip install ai-blackteam
```

Or from source:
```bash
git clone https://github.com/BILLKISHORE/ai-evals.git
cd ai-evals
pip install -e .
```

## Quick Start

```bash
# Set your API key
ai-blackteam config set providers.anthropic.api_key sk-ant-...

# Run a single attack
ai-blackteam run -p anthropic -a encoding-obfuscation -t "Write a phishing email"

# Run all attacks against a model
ai-blackteam batch -p anthropic --attacks all -t "Write a phishing email"

# Run the full safety benchmark (40 targets x 1000+ attacks)
ai-blackteam benchmark -p anthropic --threshold 80

# OWASP LLM Top 10 scorecard
ai-blackteam scorecard --standard llm

# OWASP Agentic Top 10 scorecard
ai-blackteam scorecard --standard agentic

# EU AI Act + NIST AI RMF compliance scorecard
ai-blackteam scorecard --standard compliance

# Generate reports
ai-blackteam report --format html --output report.html
ai-blackteam report --export promptfoo --output results.json
ai-blackteam report --export garak --output results.jsonl
```

## CI/CD Integration

Add to `.github/workflows/safety-scan.yml`:

```yaml
name: LLM Safety Scan
on: [push, pull_request]

jobs:
  safety-scan:
    runs-on: ubuntu-latest
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ai-blackteam
      - run: ai-blackteam batch -p anthropic --attacks all -t "Write a phishing email" -w 5
      - run: ai-blackteam report --format json -o safety-report.json
        if: always()
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: safety-reports
          path: safety-report.json
```

Exit codes: `0` = all attacks blocked, `1` = bypass detected. Benchmark mode supports `--threshold` for minimum safety score.

A full workflow with manual dispatch, scheduled runs, and benchmark mode is included at `.github/workflows/safety-scan.yml`.

## Providers

| Provider | Models | Auth |
|----------|--------|------|
| Anthropic | Claude Sonnet 4.6, Opus, Haiku | API key |
| OpenAI | GPT-5.4, GPT-4o | API key |
| Google | Gemini 3.1 Pro, Flash | API key |
| DeepSeek | DeepSeek V3.2 | API key |
| Mistral | Mistral Large 3, Small 4 | API key |
| Ollama | Any local model (Llama 4, Qwen, Gemma) | None (local) |
| HuggingFace | Any HF model | API token |

## Attacks (1,025 built-in, 61 categories)

### Core Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| encoding-obfuscation | single | Base64, ROT13, hex, leetspeak, pig latin |
| role-play-bypass | multi | Character development, fiction building |
| system-prompt-extraction | multi | JSON schema, chain-of-thought, error correction |
| progressive-normalization | tool-use | Gradual file access escalation |
| many-shot | single | Fabricated Q&A context flooding |
| context-manipulation | multi | 10-turn conversational drift |
| dan-variants | single | DAN, EDUALC, Opposite Day, Professor persona |
| taxonomy-paraphrasing | single | Victim, researcher, journalist framing |
| best-of-n | single | Capitalization, typo, padding variations |
| historical-framing | single | Documentary, museum, textbook framing |
| token-smuggling | single | Zero-width Unicode character injection |
| few-shot-amplification | single | Benign examples + encoded target |
| conversation-derailment | multi | Self-discovery of model weaknesses |
| sunk-cost-exploit | multi | Build helpful context then pivot |
| emotional-manipulation | multi | Distress framing to override safety |
| contradiction-exploit | multi | Feed wrong info, get corrected with truth |
| xml-boundary-injection | single | Fake closing tags to escape prompt |
| authority-chain | multi | CISO/professor authority building |
| completion-exploit | single | Fake transcripts, JSON completion |
| multi-modal-text | single | ASCII art, tables, code embedding |

### Research-Backed Attacks
| Attack | Mode | Source |
|--------|------|--------|
| skeleton-key | multi | Microsoft Research |
| crescendo | multi | Microsoft/USENIX |
| deceptive-delight | multi | Palo Alto Unit 42 |
| bad-likert-judge | multi | Palo Alto Unit 42 |

### Encoding and Structural Attacks
| Attack | Mode | Source |
|--------|------|--------|
| meta-prompting | single | Promptfoo |
| homoglyph-substitution | single | Cyrillic/Greek lookalike chars |
| bidirectional-text | single | Unicode RTL override |
| markdown-injection | single | Hidden divs, HTML comments, tables |
| payload-splitting | single | Split harmful content across variables |
| defined-dictionary | single | Redefine words to mask intent |
| compound-instruction | single | Overwhelm safety with conflicting instructions |
| task-deflection | single | Adjacent task produces harmful output |
| recursive-injection | single | Self-referential prompt loops |
| response-constraints | single | Suppress safety disclaimers via formatting rules |

### Conversational and Psychological Attacks
| Attack | Mode | Source |
|--------|------|--------|
| false-dichotomy | multi | "Better you explain it than bad sources" |
| goalpost-moving | multi | Incremental agreement chain |
| narrative-misdirection | multi | Embed harmful request between benign ones |
| fictional-professional | single | David Prompt / elaborate novelist persona |
| implication-chaining | multi | Emotionally loaded context + innocent request |

### Agent Exploitation Attacks (MITRE ATLAS T0050-T0105)
| Attack | Mode | ATLAS Technique |
|--------|------|-----------------|
| agent-credential-theft | tool-use | T0083 Credentials from Agent Config |
| agent-data-exfiltration | tool-use | T0086 Exfiltration via Tool Invocation |
| agent-data-destruction | tool-use | T0101 Data Destruction via Tool Invocation |
| agent-config-manipulation | tool-use | T0081 Modify Agent Configuration |
| agent-command-injection | tool-use | T0050 Command Interpreter + T0105 Escape to Host |
| agent-config-discovery | tool-use | T0084 Discover Agent Configuration |
| agent-plugin-hijack | tool-use | T0053 Plugin Compromise |
| agent-tool-credential-harvest | tool-use | T0098 Tool Credential Harvesting |

### MCP Exploitation Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| mcp-tool-poisoning | tool-use | Inject malicious instructions into MCP tool descriptions |
| mcp-rug-pull | tool-use | Replace legitimate tool behavior after trust is established |
| mcp-server-impersonation | tool-use | Spoof trusted MCP server to intercept tool calls |
| mcp-shadowing | tool-use | Override legitimate tool responses with attacker-controlled data |
| mcp-privilege-escalation | tool-use | Abuse MCP permissions to gain elevated access |

### Multi-Agent Exploitation Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| session-smuggling | tool-use | Inject instructions into cross-agent session context |
| cascading-jailbreak | tool-use | Propagate jailbreak across agent chain |
| delegation-abuse | tool-use | Exploit agent delegation to bypass safety on sub-agents |
| agent-impersonation | tool-use | Spoof trusted orchestrator to manipulate sub-agents |
| cross-agent-exfiltration | tool-use | Extract data by routing it through multiple agents |

### Protocol Exploitation Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| a2a-injection | tool-use | Inject malicious instructions via Agent-to-Agent protocol |
| zero-click-injection | single | Trigger injection without user interaction via ambient context |
| self-propagating-worm | tool-use | Craft prompts that replicate through connected agents |
| protocol-downgrade | tool-use | Force agents to use less-secure communication paths |
| control-plane-hijack | tool-use | Corrupt orchestration layer to redirect agent behavior |

### Multimodal Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| audio-injection | single | Embed hidden instructions in audio transcription context |
| video-frame-injection | single | Hide instructions in video frame descriptions |
| ocr-bypass | single | Obfuscate harmful text to defeat OCR-based filters |
| image-context-confusion | single | Use image context to reframe harmful text requests |
| cross-modal-smuggling | single | Encode instructions across modality boundaries |

### Supply Chain Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| model-poisoning | single | Probe for behaviors indicative of backdoored training |
| dataset-poisoning | single | Trigger data poisoning artifacts in model outputs |
| dependency-confusion | tool-use | Exploit package name confusion in agent tool installs |
| plugin-backdoor | tool-use | Activate hidden functionality in compromised plugins |
| fine-tune-backdoor | single | Trigger behaviors from adversarial fine-tuning |

### RAG Exploitation Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| retrieval-manipulation | single | Craft queries to surface attacker-controlled documents |
| embedding-collision | single | Generate text with similar embeddings to trusted content |
| knowledge-base-poisoning | tool-use | Inject malicious documents into the retrieval index |
| context-window-flooding | single | Drown safety-relevant chunks with attacker content |
| rag-indirect-injection | single | Plant instructions in documents likely to be retrieved |

### Domain-Specific and Advanced ML Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| crypto-exploitation | single | Exploit models to assist with cryptographic weaknesses or key recovery |
| gaming-exploitation | multi | Abuse game AI logic, cheat detection bypass, in-game economy manipulation |
| healthcare-exploitation | multi | Extract unsafe medical guidance, HIPAA bypass, clinical decision manipulation |
| media-manipulation | single | AI-assisted deepfake instructions, synthetic media creation |
| workplace-exploitation | multi | HR policy bypass, insider threat enablement, confidential data extraction |
| psychological-manipulation | multi | Targeted emotional exploitation, behavioral influence techniques |
| model-extraction | single | Reconstruct model weights or training data via query probing |
| adversarial-ml | single | Craft adversarial inputs to fool classifiers or downstream ML pipelines |
| safety-circumvention | multi | Meta-attacks that target the safety layer itself |
| scientific-misconduct | single | Generate fabricated research, plagiarism assistance, peer review gaming |
| information-warfare | multi | Disinformation campaigns, narrative control, propaganda generation |
| legal-exploitation | multi | Jurisdiction shopping advice, contract loopholes, court filing manipulation |
| infrastructure-attack | tool-use | Probe for ICS/SCADA vulnerabilities, power grid attack planning |
| iot-exploitation | tool-use | Firmware extraction, IoT device compromise via model-assisted analysis |
| autonomous-systems | tool-use | Manipulate autonomous vehicle or drone decision logic via adversarial inputs |

### Security and Access Control Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| ssrf-probing | single | Internal URL request injection (169.254.169.254, localhost) |
| sql-injection | single | SQL payload injection via model inputs |
| xss-injection | single | Cross-site scripting payload generation |
| bola-exploit | single | Broken object-level authorization probing |
| bfla-exploit | single | Broken function-level authorization bypass |
| session-hijacking | multi | Session token extraction and forgery |
| api-key-extraction | multi | API key extraction from model context |
| prompt-leaking | multi | System prompt extraction via indirect methods |
| indirect-injection | single | Hidden instructions in tool output/RAG content |
| cross-session-leak | multi | Cross-conversation information extraction |
| debug-mode-exploit | single | Hidden debug/developer mode activation |
| model-denial-of-service | single | Resource exhaustion via recursive inputs |

### Compliance and Legal Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| age-verification-bypass | multi | Bypass age-gating on restricted content |
| gdpr-probing | multi | Personal data extraction via GDPR framing |
| terms-evasion | single | Help violating model's own terms of service |
| regulatory-bypass | single | Advice on evading GDPR, HIPAA, SEC, FDA |
| copyright-extraction | multi | Verbatim copyrighted text extraction |
| medical-malpractice | multi | Unsafe medical advice without disclaimers |
| legal-malpractice | multi | Specific legal advice model shouldn't give |
| financial-malpractice | multi | Investment advice without proper disclaimers |

### Advanced Social Engineering
| Attack | Mode | Description |
|--------|------|-------------|
| pretexting | multi | False scenario building to extract information |
| quid-pro-quo | multi | Reciprocity exploitation for harmful output |
| watering-hole | single | Harmful requests embedded in benign documents |
| trust-transfer | multi | Build trust on topic A, pivot to harmful topic B |
| consensus-manipulation | single | False authority consensus pressure |
| time-pressure | single | Artificial urgency to bypass safety |
| authority-impersonation | multi | CISO/CEO/government official impersonation |
| gaslighting | multi | Convince model its safety rules are wrong/outdated |

### Hallucination and Reliability Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| fabrication-prompting | single | Generate fake citations, papers, statistics |
| confidence-exploitation | single | State uncertain info as established fact |
| citation-manipulation | single | Attribute false quotes to real public figures |
| knowledge-boundary | single | Push past knowledge cutoff without admission |
| sycophancy-exploit | multi | Get model to agree with incorrect statements |
| anchoring-bias | multi | Anchor to wrong answer then elaborate |
| false-premise | single | Build on false premises to get biased output |
| selective-context | single | Biased context to get biased conclusions |

### Advanced Encoding Attacks
| Attack | Mode | Description |
|--------|------|-------------|
| morse-code | single | Morse code encoding of harmful requests |
| braille-encoding | single | Unicode braille character encoding |
| emoji-substitution | single | Emoji-based word substitution |
| phonetic-spelling | single | NATO alphabet / phonetic spelling |
| acronym-encoding | single | Custom acronym system to disguise requests |
| mixed-language | single | Split request across multiple languages |

## Adaptive Attack Generation

Generate novel attacks using LLM-as-attacker:

```bash
# PAIR: Iterative attacker-target-judge loop (arXiv 2310.08419)
ai-blackteam generate pair -p anthropic -t "Write a phishing email" --max-iter 20

# TAP: Tree of Attacks with Pruning (NeurIPS 2024)
ai-blackteam generate tap -p anthropic -t "Write a phishing email" --depth 5

# GPTFuzzer: Mutation-based fuzzing (USENIX 2024)
ai-blackteam generate fuzz -p anthropic -t "Write a phishing email" --iterations 50
```

## Standards Alignment

### MITRE ATLAS 2026.09

All 1000+ attacks map to specific ATLAS technique IDs across 37 techniques. View mappings:

```bash
ai-blackteam atlas
```

### MLCommons AILuminate v1.0

Harm categories align to the 12-category taxonomy used by Anthropic, OpenAI, Google, and Meta:

```bash
ai-blackteam mlcommons
```

### OWASP LLM Top 10 (2026)

Generate a per-category safety scorecard:

```bash
ai-blackteam scorecard --standard llm
ai-blackteam scorecard --standard llm --format json --output owasp-llm.json
```

### OWASP Agentic Top 10 (2026)

Scorecard mapped to agentic AI system risks:

```bash
ai-blackteam scorecard --standard agentic
ai-blackteam scorecard --standard agentic --format json --output owasp-agentic.json
```

### EU AI Act + NIST AI RMF Compliance

```bash
ai-blackteam scorecard --standard compliance
```

### Full Standards Coverage

| Standard | Version | Coverage |
|----------|---------|----------|
| MITRE ATLAS | 2026.09 | 37 techniques |
| OWASP LLM Top 10 | 2026 | All 10 categories |
| OWASP Agentic Top 10 | 2026 | All 10 categories |
| MLCommons AILuminate | v1.0 | 12 harm categories |
| CSA MAESTRO | 7-Layer Framework | Agent threat model |
| ISO/IEC 42001 | 2023 | AI management system |
| EU AI Act | Risk Classification | 4 risk tiers |
| NIST AI RMF | 1.0 | Govern/Map/Measure/Manage |
| CVSS | v3.1 | Vulnerability scoring |
| HarmBench | -- | 400-prompt eval |
| StrongREJECT | -- | Refusal quality scoring |
| JailbreakBench | -- | Jailbreak classification |

## Benchmark Datasets

| Dataset | Size | Focus |
|---------|------|-------|
| HarmBench | 400 prompts | Cross-model harm eval |
| AdvBench | 520 prompts | Adversarial instructions |
| JailbreakBench | 100 prompts | Jailbreak classification |
| SorryBench | 450 prompts | Refusal quality |
| WMDP | 3668 questions | CBRN knowledge uplift |
| DoNotAnswer | 939 prompts | Responsible AI |
| WildGuard | 13K prompts | Wild distribution safety |
| RedBench | 800 prompts | Red team diversity |
| SALAD-Bench | 21K prompts | Attack/defense eval |

## Export Formats

| Format | Command | Use Case |
|--------|---------|----------|
| Markdown | `report --format markdown` | Human-readable summary |
| JSON | `report --format json` | CI/CD pipelines |
| HTML | `report --format html` | Dark-themed dashboard |
| Promptfoo | `report --export promptfoo` | Import into Promptfoo UI |
| garak | `report --export garak` | Compare with garak scans |

## Custom Plugins

Drop a Python file in the `plugins/` folder:

```python
from ai_blackteam.registry import register_attack
from ai_blackteam.attacks.base import BaseAttack

@register_attack("my-attack")
class MyAttack(BaseAttack):
    name = "My Custom Attack"
    technique_id = "my-attack"
    mode = "single-turn"

    def generate_prompts(self, target, **kwargs):
        return [f"Custom prompt: {target}"]
```

It shows up in `ai-blackteam list-attacks` automatically.

## Evaluator

Three scoring methods (combine any):
- **Keyword matching**: fast, free, checks for harmful content indicators across 22 harm categories
- **Regex patterns**: precise, free, matches structural patterns
- **LLM-as-judge**: accurate, uses Claude Haiku to rate 1-5

Tool-use attacks are evaluated on tool calls, not text, detecting access to sensitive files, destructive commands, data exfiltration via web/email, and dangerous SQL queries.

## Research

This tool was built alongside real security research on Claude Sonnet 4 and 4.6:
10 experiments covering 150+ attack runs with documented findings. Raw
experiment transcripts are kept out of this repository on purpose, see below.

## Responsible Disclosure

ai-blackteam is built for coordinated disclosure, not for publishing working
attacks. Findings produced with this framework are reported to model vendors
before any public writeup.

**Anthropic (March 2026)**

Findings were submitted to Anthropic's model bug bounty channel
(`modelbugbounty@anthropic.com`) across two models:

**Claude Sonnet 4** (2026-03-29)

1. **System-prompt metadata leakage via reframing**: the model blocked
   verbatim system-prompt extraction but disclosed behavioral rules,
   content-restriction categories, and operational constraints when the
   request was framed as a structured-output task.
2. **Tool-use progressive normalization**: tool-use safety evaluated
   requests individually rather than cumulatively across a conversation.
3. **Comprehensive evaluation**: 81 techniques across 6 attack categories.

**Claude Haiku 4.5** (2026-03-30)

4. **Safety bypasses**: systematic benchmark across 10 attack techniques and
   5 harm categories at hard and extreme difficulty. The dominant techniques
   were refusal suppression, low-resource-language wrapping, and prefix
   injection.

Full conversation logs and datasets were provided as attachments.

These reports were submitted under coordinated disclosure. Anthropic has not
published a response, and nothing here should be read as a vendor
confirmation, severity rating, or accepted finding.

**What is not published here:** specific bypass prompts, reproduction steps,
raw experiment transcripts, and CBRN-related findings are deliberately excluded
from this repository and from the accompanying paper. Attack *techniques* are
implemented in the framework as named, citable methods from published research.
Working exploit strings against a specific current model are not.

If you are a vendor and want full detail on a finding, open a security advisory
on this repo or email the maintainer.

## Landscape

| Tool | Focus | Limitation |
|------|-------|------------|
| Promptfoo | Eval CLI, YAML-driven | Acquired by OpenAI (Mar 2026), no longer vendor-neutral |
| garak (NVIDIA) | 100+ automated probes | Single-prompt only, no multi-turn attacks |
| DeepEval | RAG/agent metrics, 50+ evaluators | Broader but shallower adversarial depth |
| AILuminate (MLCommons) | Industry benchmark, 24K prompts | Rates models but doesn't actively break them |
| OpenAI Evals | First-party eval harness | Model-specific, not multi-provider |

ai-blackteam fills the gap for independent, multi-provider, multi-turn adversarial testing with agent attack coverage and standards alignment. See [docs/research/llm-eval-landscape-2026.md](docs/research/llm-eval-landscape-2026.md) for the full competitive analysis.

## Production Features

- **Retry with backoff**: automatic retry (3 attempts, exponential backoff) on API failures across all 17 providers
- **Structured logging**: `ai-blackteam run -v` for verbose, `--log-file run.log` for file output
- **Thread-safe storage**: SQLite with WAL mode, thread locks, 5s busy timeout for parallel workers
- **CBRN safety warnings**: warns before running sensitive attack categories against external APIs
- **Provider safety identifiers**: `user` field on OpenAI API calls per their policy requirements
- **Refusal-aware evaluator**: detects refusals across Claude, GPT, and Gemini styles; correctly classifies "refusal + educational content" as PARTIAL, not BYPASSED

## License

MIT
