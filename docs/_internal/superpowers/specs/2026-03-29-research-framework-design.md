# AI Blackteam -- Research Framework Design Spec

**Date:** 2026-03-29
**Author:** Bill Kishore
**Status:** Draft

---

## Purpose

A structured research framework for LLM security research (AI red teaming). Supports the full workflow: manual prompt exploration, automated batch testing, structured documentation, and polished output for research papers, blog posts, and bug bounty submissions.

## Goals

1. Track experiments as self-contained, reproducible units
2. Build a knowledge base of attack techniques and model-specific intelligence
3. Automate repetitive testing across multiple models and providers
4. Produce professional output (arXiv papers, blog posts, bug bounty reports)
5. Start simple with markdown + folders, grow into automation without restructuring

## Target Models

### Closed-Source (API / Free Tier)

| Provider | Model | Access |
|----------|-------|--------|
| OpenAI | GPT-5.4 / GPT-5.4 Pro | API + free tier |
| Anthropic | Claude 4.6 (Opus / Sonnet / Haiku) | API + free tier |
| Google | Gemini 3.1 Pro / Flash | API + free tier |
| xAI | Grok 3 | API |
| DeepSeek | DeepSeek V3.2 | API + self-hosted |

### Open-Source (Local via Ollama / HuggingFace)

| Provider | Model | Notes |
|----------|-------|-------|
| Meta | Llama 4 (Scout / Maverick) | 10M context, 85.5% MMLU |
| Mistral | Mistral Large 3 / Small 4 | Apache 2.0 |
| DeepSeek | DeepSeek V3.2-Speciale | MIT license |
| Alibaba | Qwen 3.5 | MoE architecture |
| Google | Gemma 3 (27B) | Open weights |

## Research Workflow

```
Manual Discovery --> Document Experiment --> Automate Testing --> Analyze Results --> Write Up --> Publish/Submit
```

1. **Manual exploration** -- Craft prompts against live models, iterate
2. **Document** -- Create experiment folder with prompts, responses, analysis
3. **Automate** -- Use the framework CLI to batch test across models
4. **Analyze** -- Evaluate success rates, compare across models
5. **Write up** -- Convert findings into paper, blog post, or bug bounty report
6. **Publish** -- Submit to arXiv, post to blog, or submit to bug bounty program

---

## Directory Structure

```
ai-blackteam/
├── experiments/                    # Self-contained experiment folders
│   └── YYYY-MM-DD-short-name/
│       ├── README.md               # Structured report (YAML frontmatter)
│       ├── prompts/                # Numbered prompt iterations
│       │   ├── 001-initial.md
│       │   ├── 002-refined.md
│       │   └── 003-final.md
│       ├── responses/              # Model outputs for each prompt
│       │   ├── 001-initial.md
│       │   ├── 002-refined.md
│       │   └── screenshots/
│       ├── scripts/                # Experiment-specific automation
│       ├── results/                # Batch test results, analysis
│       │   ├── success-rate.json
│       │   └── analysis.md
│       └── STATUS.md               # Quick status tracker
│
├── techniques/                     # Attack method knowledge base
│   ├── prompt-injection/
│   │   ├── README.md               # What, how, defenses, your findings
│   │   ├── variants.md             # Sub-types identified
│   │   └── references.md           # Papers, blog posts, prior art
│   ├── role-play-bypass/
│   ├── many-shot-jailbreak/
│   ├── system-prompt-extraction/
│   ├── context-manipulation/
│   ├── tool-use-exploitation/
│   ├── multi-modal-attacks/
│   ├── encoding-obfuscation/
│   └── _template/
│
├── models/                         # Per-model intelligence tracker
│   ├── openai/
│   │   ├── gpt-5.4.md
│   │   └── gpt-5.4-pro.md
│   ├── anthropic/
│   │   ├── claude-4.6-opus.md
│   │   ├── claude-4.6-sonnet.md
│   │   └── claude-4.6-haiku.md
│   ├── google/
│   │   ├── gemini-3.1-pro.md
│   │   └── gemini-3.1-flash.md
│   ├── meta/
│   │   ├── llama-4-scout.md
│   │   └── llama-4-maverick.md
│   ├── deepseek/
│   │   ├── deepseek-v3.2.md
│   │   └── deepseek-v3.2-speciale.md
│   ├── mistral/
│   │   ├── mistral-large-3.md
│   │   └── mistral-small-4.md
│   ├── alibaba/
│   │   └── qwen-3.5.md
│   ├── google-open/
│   │   └── gemma-3-27b.md
│   └── _template.md
│
├── writeups/                       # Polished public output
│   ├── papers/
│   │   ├── drafts/
│   │   │   └── YYYY-MM-DD-title/
│   │   │       ├── paper.md
│   │   │       ├── figures/
│   │   │       └── references.bib
│   │   └── published/
│   ├── blog-posts/
│   │   ├── drafts/
│   │   └── published/
│   └── bug-bounties/
│       ├── drafts/
│       │   └── YYYY-MM-DD-provider-title/
│       │       ├── report.md
│       │       ├── reproduction/
│       │       └── evidence/
│       └── submitted/
│           └── YYYY-MM-DD-provider-title/
│               ├── report.md
│               ├── reproduction/
│               ├── evidence/
│               └── SUBMISSION.md   # Date, response, payout tracking
│
├── tools/                          # Red team automation framework
│   ├── redteam/                    # Core Python package
│   │   ├── __init__.py
│   │   ├── runner.py               # Run prompts against any model
│   │   ├── providers/              # Model connectors
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Abstract base: send_prompt(), get_model_info()
│   │   │   ├── openai_provider.py
│   │   │   ├── anthropic_provider.py
│   │   │   ├── google_provider.py
│   │   │   ├── deepseek_provider.py
│   │   │   ├── ollama_provider.py  # Local models via Ollama
│   │   │   └── huggingface_provider.py
│   │   ├── attacks/                # Attack technique implementations
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # Abstract attack class
│   │   │   ├── prompt_injection.py
│   │   │   ├── role_play_bypass.py
│   │   │   ├── many_shot.py
│   │   │   ├── encoding_obfuscation.py
│   │   │   ├── context_manipulation.py
│   │   │   └── system_prompt_extraction.py
│   │   ├── evaluator.py            # Judge if attack succeeded/failed
│   │   ├── reporter.py             # Auto-generate experiment README
│   │   └── batch.py                # Run N prompts x M models
│   ├── cli.py                      # Command-line interface
│   ├── generators/                 # Utility scripts
│   │   ├── new_experiment.py       # Scaffold experiment from template
│   │   ├── build_index.py          # Parse frontmatter -> INDEX.md
│   │   └── model_matrix.py         # Technique-vs-model heatmap
│   ├── config.yaml                 # API keys, endpoints, defaults
│   ├── requirements.txt
│   └── README.md
│
├── logs/                           # Daily scratch pad
│   ├── daily/
│   │   └── YYYY-MM-DD.md          # Observations, quick tests, ideas
│   └── ideas.md                    # Running list of attack ideas
│
├── templates/                      # Reusable templates
│   ├── experiment/
│   │   ├── README.md
│   │   ├── STATUS.md
│   │   └── prompt.md
│   ├── technique/
│   │   ├── README.md
│   │   ├── variants.md
│   │   └── references.md
│   ├── model/
│   │   └── model.md
│   └── writeup/
│       ├── paper.md
│       ├── blog-post.md
│       └── bug-bounty-report.md
│
├── INDEX.md                        # Auto-generated master experiment index
├── ROADMAP.md                      # Research phases and milestones
└── README.md                       # Project overview
```

---

## Experiment Format

### YAML Frontmatter (experiments/*/README.md)

```yaml
---
id: EXP-001
title: "GPT-5.4 Role-Play Safety Bypass via Nested Fiction"
date: 2026-03-29
models: [gpt-5.4]
techniques: [role-play-bypass, nested-context]
severity: high              # low / medium / high / critical
status: documented          # discovery / testing / documented / reported / published
bug_bounty: false
writeup: false
tags: [safety-filter, fiction-framing, openai]
---
```

### Severity Scale

| Level | Definition |
|-------|-----------|
| low | Model gives borderline or mildly off-policy responses |
| medium | Model bypasses safety filter but output is limited in harm |
| high | Model produces clearly harmful or policy-violating content |
| critical | Model leaks system prompts, executes unintended actions, or enables real-world harm |

### Experiment Status Flow

```
discovery --> testing --> documented --> reported --> published
```

- **discovery** -- Found something interesting, still exploring
- **testing** -- Running systematic tests, collecting data
- **documented** -- Full experiment writeup complete
- **reported** -- Submitted to bug bounty or disclosed to provider
- **published** -- Research paper or blog post published

---

## Technique Knowledge Base Format

### YAML Frontmatter (techniques/*/README.md)

```yaml
---
technique: prompt-injection
difficulty: beginner         # beginner / intermediate / advanced
first_documented: 2022
active_against: [gpt-5.4, gemini-3.1-pro]
mitigated_by: [claude-4.6-sonnet]
related_experiments: [EXP-001, EXP-005]
---
```

### Required Sections

- What It Is
- How It Works
- Known Defenses
- Your Findings (links to experiments)

---

## Model Intelligence Format

### YAML Frontmatter (models/*/*.md)

```yaml
---
model: gpt-5.4
provider: openai
type: closed-source          # closed-source / open-source
access: [api, free-tier]     # api / free-tier / local / huggingface
api_pricing: "$2.50/$15 per 1M tokens"
context_window: 128k
release_date: 2026-01
last_tested: null
---
```

### Required Sections

- Safety Architecture
- Known Weaknesses (links to successful experiments)
- Known Defenses (links to failed experiments)
- Behavioral Notes (refusal patterns, quirks)
- Bug Bounty Program (URL, scope, payout range, submission format)
- Related Experiments

---

## Bug Bounty Report Format

### YAML Frontmatter (writeups/bug-bounties/*/report.md)

```yaml
---
provider: openai
program_url: https://bugcrowd.com/openai
model: gpt-5.4
severity: high
submitted_date: null
response_date: null
status: draft               # draft / submitted / triaged / accepted / rejected / paid
payout: null
---
```

### Required Sections

- Summary (one paragraph)
- Affected Model(s)
- Reproduction Steps (numbered, exact)
- Expected Behavior
- Actual Behavior (exact model output)
- Impact Assessment
- Suggested Fix
- Evidence (screenshots, logs, payloads)

---

## Red Team Framework (tools/redteam/)

### Provider Abstraction

All model providers implement a common interface:

```python
class BaseProvider:
    def send_prompt(self, prompt: str, system_prompt: str = None) -> dict:
        """Returns {response: str, metadata: dict, raw: dict}"""
        raise NotImplementedError

    def supports_streaming(self) -> bool:
        return False

    def get_model_info(self) -> dict:
        """Returns model name, version, context window, pricing"""
        raise NotImplementedError
```

Providers: OpenAI API, Anthropic API, Google API, DeepSeek API, Ollama (local), HuggingFace (API + local).

### Attack Abstraction

```python
class BaseAttack:
    def generate_prompt(self, target_behavior: str, **kwargs) -> str:
        """Generate an attack prompt for the given target behavior"""
        raise NotImplementedError

    def evaluate_response(self, response: str, target_behavior: str) -> dict:
        """Returns {success: bool, confidence: float, reasoning: str}"""
        raise NotImplementedError
```

### CLI Commands

```bash
# Scaffold new experiment
python tools/cli.py new --name "name" --technique technique --model model

# Run single prompt against a model
python tools/cli.py run --model gpt-5.4 --attack role-play --prompt prompts/test.md

# Batch test: N prompts x M models
python tools/cli.py batch --models all --attack many-shot --rounds 50

# Auto-generate experiment report
python tools/cli.py report --experiment EXP-001

# Rebuild master INDEX.md
python tools/cli.py index
```

### Configuration (tools/config.yaml)

```yaml
providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    default_model: gpt-5.4
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    default_model: claude-4.6-sonnet
  google:
    api_key: ${GOOGLE_API_KEY}
    default_model: gemini-3.1-pro
  ollama:
    base_url: http://localhost:11434
    default_model: llama4-scout

defaults:
  batch_rounds: 50
  timeout_seconds: 30
  save_raw_responses: true
```

API keys are read from environment variables, never committed to git.

---

## INDEX.md Structure

Auto-generated by `python tools/cli.py index`. Contains:

- Table of all experiments sorted by severity (ID, title, model, technique, severity, status)
- Grouped by technique (technique name -> list of experiment IDs)
- Grouped by model (model name -> list of experiment IDs)
- Stats (total experiments, success rate, models tested, techniques used, bug bounties submitted)

---

## Research Roadmap

### Phase 1: Foundation (Month 1)
- Set up framework, templates, first experiment
- Test 3 known techniques against GPT-5.4, Claude 4.6, Gemini 3.1
- Document findings, build technique knowledge base

### Phase 2: Go Deep (Month 2-3)
- 20+ experiments across 5+ models
- Build automation scripts (batch runner, evaluator)
- First blog post or bug bounty submission

### Phase 3: Go Public (Month 3-4)
- Publish first research paper on arXiv
- Submit to 2-3 bug bounty programs
- Build public reputation (blog, Twitter/X, LinkedIn)

### Phase 4: Monetize (Month 4+)
- Freelance red team consulting
- Or: package framework as SaaS product
- Or: get hired by an AI safety team

---

## Implementation Scope

### Build Now (Phase 1 implementation)
- Full directory structure with all folders
- All templates (experiment, technique, model, writeup)
- README.md, ROADMAP.md, INDEX.md (initial empty state)
- All model intelligence files (populated with known info)
- All technique knowledge base files (populated with known info)
- `tools/cli.py` with `new` and `index` commands
- `tools/redteam/providers/base.py` (abstract interface)
- `tools/config.yaml` with structure
- `tools/requirements.txt`
- `.gitignore` (API keys, __pycache__, .env)
- Git repo initialization

### Build Later (deferred)
- Provider implementations (openai_provider.py, etc.) -- build as you get API access
- Attack implementations (prompt_injection.py, etc.) -- build as you research
- `cli.py run`, `batch`, `report` commands -- build when automation is needed
- Evaluator and reporter modules -- build after 5+ manual experiments

## What's NOT in Scope

- Web UI or dashboard (add later if needed)
- Database backend (markdown + YAML frontmatter is sufficient to start)
- CI/CD pipeline (not needed until the framework becomes a product)
- Multi-user collaboration (solo researcher for now)

---

## Tech Stack

- **Language:** Python 3.12+
- **Dependencies:** openai, anthropic, google-genai, requests, pyyaml, click (CLI), ollama
- **Documentation:** Markdown with YAML frontmatter
- **Version control:** Git + GitHub
- **Local models:** Ollama
