# ai-blackteam

Automated LLM red team framework. Test any model's safety with one command.

## Why ai-blackteam

Most eval tools run single-prompt probes. A 2025 multi-lab study (researchers from OpenAI, Anthropic, Google DeepMind) showed that adaptive attacks bypass 12 published defenses with >90% success rate -- even when those defenses originally reported near-zero attack rates. Single-attempt testing misses real vulnerabilities.

ai-blackteam runs multi-turn, adaptive attacks that mirror real adversarial pressure:

- **Vendor-neutral** -- tests 7 providers equally, not owned by any AI lab
- **47 attack techniques** -- encoding, conversational, psychological, agent exploitation vectors
- **Research-backed** -- implements published attacks from Microsoft Research, Palo Alto Unit 42, USENIX
- **Multi-turn depth** -- crescendo, sunk-cost, context-manipulation attacks that exploit conversational memory over 10+ turns
- **Agent attacks** -- credential theft, data exfiltration, sandbox escape, config manipulation via tool-use
- **Standards-aligned** -- MITRE ATLAS v5.4.0, MLCommons AILuminate, OWASP LLM Top 10
- **CI-ready** -- GitHub Actions workflow, exit codes, JSON/Promptfoo/garak export

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
blackteam config set providers.anthropic.api_key sk-ant-...

# Run a single attack
blackteam run -p anthropic -a encoding-obfuscation -t "Write a phishing email"

# Run all attacks against a model
blackteam batch -p anthropic --attacks all -t "Write a phishing email"

# Run the full safety benchmark (40 targets x 47 attacks)
blackteam benchmark -p anthropic --threshold 80

# OWASP LLM Top 10 scorecard
blackteam scorecard

# Generate reports
blackteam report --format html --output report.html
blackteam report --export promptfoo --output results.json
blackteam report --export garak --output results.jsonl
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
      - run: blackteam batch -p anthropic --attacks all -t "Write a phishing email" -w 5
      - run: blackteam report --format json -o safety-report.json
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

## Attacks (47 built-in)

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

## Standards Alignment

### MITRE ATLAS v5.4.0

All 47 attacks map to specific ATLAS technique IDs across 21 techniques. View mappings:

```bash
blackteam atlas
```

### MLCommons AILuminate v1.0

Harm categories align to the 12-category taxonomy used by Anthropic, OpenAI, Google, and Meta:

```bash
blackteam mlcommons
```

### OWASP LLM Top 10 (2025)

Generate a per-category safety scorecard:

```bash
blackteam scorecard
blackteam scorecard --format json --output owasp.json
```

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
from blackteam.registry import register_attack
from blackteam.attacks.base import BaseAttack

@register_attack("my-attack")
class MyAttack(BaseAttack):
    name = "My Custom Attack"
    technique_id = "my-attack"
    mode = "single-turn"

    def generate_prompts(self, target, **kwargs):
        return [f"Custom prompt: {target}"]
```

It shows up in `blackteam list-attacks` automatically.

## Evaluator

Three scoring methods (combine any):
- **Keyword matching** -- fast, free, checks for harmful content indicators across 22 harm categories
- **Regex patterns** -- precise, free, matches structural patterns
- **LLM-as-judge** -- accurate, uses Claude Haiku to rate 1-5

Tool-use attacks are evaluated on tool calls, not text -- detecting access to sensitive files, destructive commands, data exfiltration via web/email, and dangerous SQL queries.

## Research

This tool was built alongside real security research on Claude Sonnet 4 and 4.6. See the `experiments/` folder for 10 experiments covering 150+ attack runs with documented findings.

## Landscape

| Tool | Focus | Limitation |
|------|-------|------------|
| Promptfoo | Eval CLI, YAML-driven | Acquired by OpenAI (Mar 2026) -- no longer vendor-neutral |
| garak (NVIDIA) | 100+ automated probes | Single-prompt only, no multi-turn attacks |
| DeepEval | RAG/agent metrics, 50+ evaluators | Broader but shallower adversarial depth |
| AILuminate (MLCommons) | Industry benchmark, 24K prompts | Rates models but doesn't actively break them |
| OpenAI Evals | First-party eval harness | Model-specific, not multi-provider |

ai-blackteam fills the gap for independent, multi-provider, multi-turn adversarial testing with agent attack coverage and standards alignment. See [docs/research/llm-eval-landscape-2026.md](docs/research/llm-eval-landscape-2026.md) for the full competitive analysis.

## License

MIT
