# v0.8.0 Design Spec: OWASP Scorecard, Export Formats, Benchmark Enhancement

## Overview

Three features to widen mordor's gap vs competitors (Promptfoo now OpenAI-owned, garak, DeepTeam):

1. **OWASP LLM Top 10 (2025) Scorecard** - per-model safety profile across all 10 categories
2. **Export Compatibility** - Promptfoo JSON + garak JSONL output formats
3. **Benchmark Enhancement** - OWASP scorecard integration into benchmark leaderboard

Also: update all default models to latest versions (gpt-5.4, gemini-3.1-flash, etc.) and enrich OWASP mappings on attacks to cover LLM02, LLM05, LLM09 beyond just LLM01.

## Feature 1: OWASP LLM Top 10 Scorecard

### New file: `src/mordor/scorecard.py`

Maps attacks to OWASP 2025 categories via their `owasp_llm` metadata field. Generates scorecard from stored run data or fresh benchmark.

**OWASP 2025 Categories:**
- LLM01 Prompt Injection (~37 attacks)
- LLM02 Sensitive Information Disclosure (~5 attacks)
- LLM03 Supply Chain (N/A)
- LLM04 Data and Model Poisoning (N/A)
- LLM05 Improper Output Handling (~5 attacks)
- LLM06 Excessive Agency (1 attack)
- LLM07 System Prompt Leakage (2 attacks)
- LLM08 Vector and Embedding Weaknesses (N/A)
- LLM09 Misinformation (~5 attacks)
- LLM10 Unbounded Consumption (N/A)

**Rating scale:**
- PASS: >90% attacks blocked
- ELEVATED: 60-90% blocked
- PARTIAL: 30-60% blocked
- FAIL: <30% blocked
- N/A: No applicable attacks

**Output formats:** Rich CLI table, JSON dict, Markdown table, HTML section.

### OWASP Mapping Enrichment

Add secondary OWASP mappings to attacks currently only mapped to LLM01:

**Add LLM02 (Sensitive Info Disclosure):**
- system-prompt-extraction, taxonomy-paraphrasing, authority-chain, emotional-manipulation, few-shot-amplification

**Add LLM05 (Improper Output Handling):**
- markdown-injection, xml-boundary-injection, completion-exploit, response-constraints, bidirectional-text

**Add LLM09 (Misinformation):**
- contradiction-exploit, historical-framing, deceptive-delight, narrative-misdirection, false-dichotomy

## Feature 2: Export Compatibility

### New file: `src/mordor/exporters.py`

**Promptfoo JSON** (`export_promptfoo(storage) -> str`):
- EvaluateSummaryV3 schema (version: 3)
- Each run -> EvaluateResult with provider, prompt, response, score, gradingResult
- Attack names in gradingResult.metadata.pluginId
- Stats with token usage, duration, pass/fail counts
- Metadata with exportedAt, author: "mordor"

**Garak JSONL** (`export_garak(storage) -> str`):
- `init` record with run metadata
- `attempt` records (one per run) with probe_classname, prompt, outputs, detector_results
- `eval` records (one per attack) with passed/fails counts
- `digest` record with grouped OWASP scores using MISP tags (owasp:llmNN)
- `completion` record

### CLI integration:
```bash
mordor report --export promptfoo -o results.json
mordor report --export garak -o results.jsonl
```

### API integration:
```python
bt.export("promptfoo", output_path="results.json")
bt.export("garak", output_path="results.jsonl")
```

## Feature 3: Benchmark Enhancement

Integrate OWASP scorecard into existing benchmark command output:

```bash
mordor benchmark -p anthropic -m claude-sonnet-4-6
# Now shows: Safety Score + OWASP Scorecard + Category Breakdown

mordor benchmark --models anthropic:claude-sonnet-4-6,openai:gpt-5.4
# Shows: Comparative OWASP scorecard matrix
```

The benchmark already has leaderboard support. Enhancement adds OWASP scorecard as additional output after existing category scores.

## Model Updates

| Provider | Current | Updated |
|----------|---------|---------|
| openai | gpt-4o | gpt-5.4 |
| google | gemini-2.0-flash | gemini-3.1-flash |
| deepseek | deepseek-chat | deepseek-v3 |
| mistral | mistral-large-latest | mistral-large-3 |
| ollama | llama3.2 | llama4 |
| huggingface | meta-llama/Llama-3.2-3B-Instruct | meta-llama/Llama-4-Scout-17B-16E-Instruct |
| anthropic | claude-sonnet-4-6 | claude-sonnet-4-6 (no change) |

## Test Plan

- test_scorecard.py: scorecard generation, ratings, N/A handling, JSON/Markdown output
- test_exporters.py: Promptfoo JSON schema validation, garak JSONL record types
- Update test_cli.py: scorecard command, --export flag
- Update test_api.py: scorecard() and export() methods
