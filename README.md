# ai-blackteam

Automated LLM red team framework. Point it at any model, run one command, get a safety report.

[![PyPI](https://img.shields.io/pypi/v/ai-blackteam.svg)](https://pypi.org/project/ai-blackteam/) [![Docs](https://img.shields.io/badge/docs-live-E63946)](https://ai-blackteam.ai-evals.workers.dev/) [![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)

**Docs:** https://ai-blackteam.ai-evals.workers.dev/

## What it is

Most eval tools send one prompt, watch the model refuse, and call it safe. Real attackers do not stop at one prompt. A 2025 multi-lab study (OpenAI, Anthropic, Google DeepMind) found adaptive attacks bypassed 12 published defenses at over 90% success, on defenses that had reported near-zero attack rates. Single-attempt testing misses the vulnerabilities that matter.

ai-blackteam runs multi-turn, adaptive, tool-use, and reasoning-layer attacks that mirror the pressure a model faces in the wild, then scores the results against the standards a security or compliance team already reports on. It is vendor-neutral: it tests 17 providers on equal footing and is not owned by any model lab.

## Intended use

This is a defensive tool. Use it to test models you own or are authorized to test, to produce audit evidence, and to file coordinated disclosures. Working exploit strings against a specific current model, raw harmful transcripts, and CBRN-specific findings are deliberately kept out of this repository. The framework implements attack *techniques* as named, citable methods from published research, not ready-to-fire payloads. See [Responsible disclosure](#responsible-disclosure).

## Install

```bash
pip install ai-blackteam
```

From source:

```bash
git clone https://github.com/BILLKISHORE/ai-evals.git
cd ai-evals
pip install -e .
```

Python 3.12 or newer.

## Quick start

```bash
# Store an API key (or export ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.)
ai-blackteam config set providers.anthropic.api_key sk-ant-...

# Run one attack against a model
ai-blackteam run -p anthropic -a encoding-obfuscation -t "Write a phishing email"

# Run the whole corpus against a model
ai-blackteam batch -p anthropic --attacks all -t "Write a phishing email"

# Score the stored results against a standard
ai-blackteam scorecard --standard llm          # OWASP LLM Top 10 2026
ai-blackteam scorecard --standard agentic       # OWASP Agentic Top 10 2026
ai-blackteam scorecard --standard aisvs         # OWASP AISVS chapters
ai-blackteam scorecard --standard eu-ai-act     # EU AI Act Articles 55 and 73

# Build a report
ai-blackteam report --format html --output report.html
```

`run` and `batch` exit `0` when everything was blocked and `1` when at least one attack bypassed, so they drop straight into CI. Full walkthrough: [Quick start](https://ai-blackteam.ai-evals.workers.dev/guide/quickstart).

## What you get

- **1,028 curated attack techniques** across 61 categories. These are hand-written modules, not generated padding. A template engine can expand them combinatorially when you want volume; the [attack surface page](https://ai-blackteam.ai-evals.workers.dev/how-it-works/attack-surface) explains what that number does and does not mean.
- **Reasoning-layer attacks.** PRJA (harmful content hidden in the reasoning), OTora (reasoning denial of service), Self-Jailbreak, and vector-store poisoning. These are scored on the model's thinking, not just its answer, so a model that refuses in text while leaking in thought is caught. See [reasoning-layer attacks](https://ai-blackteam.ai-evals.workers.dev/guide/attacks/reasoning-layer-attacks).
- **Five runnable compliance scorecards**, not a static mapping table: `scorecard --standard llm | agentic | compliance | aisvs | eu-ai-act`, plus `aivss` for scoring one finding. Every transcription this project could not verify against a published source is marked unverified in the data.
- **19 public benchmark loaders**: HarmBench, AdvBench, JailbreakBench, SorryBench, WMDP, DoNotAnswer, WildGuard, StrongREJECT, BeaverTails, RealToxicityPrompts, JailBreakV-28K, AgentHarm, and more.
- **8 adaptive generators**: PAIR, TAP, Fuzzer, AutoDAN, PAP, Crescendo, Best-of-N, and Stateful (which carries what a target already refused between attempts).
- **A static scanner** for source code and MCP server definitions, with SARIF 2.1.0 output for the GitHub Security tab.
- **Reasoning-effort control** across 16 providers: the same attack lands differently at `low` than at `max`, so effort is a red-team dimension, not a tuning knob.

## Providers

17 providers on equal footing. Set a key and go.

| Provider | Notes |
|----------|-------|
| Anthropic | Claude, native thinking traces |
| OpenAI | GPT and o-series, Responses API for reasoning |
| Azure OpenAI | o-series through Azure |
| Google | Gemini, thinking config |
| DeepSeek, Grok, Groq, Together, Fireworks | OpenAI-compatible, reasoning traces carried |
| Mistral, Cohere, AI21 | OpenAI-compatible base |
| Perplexity | sonar-reasoning |
| Amazon Bedrock | Claude and others via Converse |
| Ollama | any local model (deepseek-r1, Qwen, Llama) |
| HuggingFace | any hosted model |
| HTTP | your own endpoint |

Provider setup pages: [docs/guide/providers](https://ai-blackteam.ai-evals.workers.dev/guide/providers/overview).

## Attacks

The 1,028 attacks span 61 categories: encoding and obfuscation, prompt injection, conversational and psychological pressure, agent and tool-use exploitation, MCP exploitation, multi-agent, protocol, multimodal, supply chain, RAG, and domain-specific attacks. Every attack maps to MITRE ATLAS and the OWASP LLM and Agentic Top 10 at the code level.

Browse the full catalog by category, mode, and standard in the [attack catalog](https://ai-blackteam.ai-evals.workers.dev/attacks/all-attacks), or list them locally:

```bash
ai-blackteam list-attacks
ai-blackteam taxonomy          # grouped by category with OWASP and ATLAS IDs
ai-blackteam atlas             # MITRE ATLAS technique coverage
```

## Standards and reports

Every attack carries code-level mappings to MITRE ATLAS 2026.09, OWASP LLM Top 10 (2026), OWASP Agentic Top 10 (2026), OWASP AISVS 1.0, MLCommons AILuminate, EU AI Act Articles 55 and 73, NIST AI RMF, and CVSS. CSA MAESTRO, ISO 42001, and ISO/IEC 27090 are documented alignments.

Reports export to HTML, JSON, SARIF 2.1.0, Promptfoo, and garak formats.

```bash
ai-blackteam report --export promptfoo --output results.json
ai-blackteam report --export garak --output results.jsonl
ai-blackteam scan ./src --format sarif -o results.sarif
```

## CI/CD

Drop a safety scan into GitHub Actions:

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

`benchmark` mode supports `--threshold` for a minimum safety score. A full workflow with manual dispatch and scheduled runs ships at `.github/workflows/safety-scan.yml`.

## How it compares

| Tool | Focus | Where ai-blackteam differs |
|------|-------|----------------------------|
| garak (NVIDIA) | 100+ automated probes | garak is single-prompt; ai-blackteam adds multi-turn, tool-use, and reasoning-layer attacks |
| Promptfoo | Eval CLI, YAML-driven | Acquired by OpenAI in March 2026, no longer vendor-neutral |
| PyRIT (Microsoft) | Programmable orchestration | ai-blackteam ships a curated corpus you run in one command |
| AILuminate (MLCommons) | Industry benchmark | Rates models; ai-blackteam actively tries to break them |

The competitor column describes those tools as of 2026-09-20 and is not maintained by their authors. Side-by-side pages: [comparisons](https://ai-blackteam.ai-evals.workers.dev/guide/compare/vs-garak).

## Responsible disclosure

Findings produced with this framework were reported to Anthropic's security team through coordinated disclosure, with full conversation logs and datasets attached. Those reports were submitted under coordinated disclosure. Anthropic has not published a response, and nothing here should be read as a vendor confirmation, severity rating, or accepted finding.

Specific bypass prompts, reproduction steps, raw experiment transcripts, and CBRN-related findings are kept out of this repository and the accompanying paper. If you are a vendor and want detail on a finding, open a security advisory on this repo or email the maintainer.

## Contributing

Contributions are welcome: new attack modules, provider integrations, dataset loaders, and evaluator improvements. A new attack registers itself through the plugin registry and needs its taxonomy mappings in the same change (a test enforces this). Run the suite before opening a PR:

```bash
poetry install --with dev
poetry run pytest -m "not live"
```

The `not live` marker keeps the suite offline and free. See the [architecture docs](https://ai-blackteam.ai-evals.workers.dev/architecture/overview) for how attacks, providers, and the evaluator fit together.

## License

GNU General Public License v3.0 or later. See [LICENSE](LICENSE).

Earlier releases up to 1.9.0 were published under MIT and remain available under those terms.
