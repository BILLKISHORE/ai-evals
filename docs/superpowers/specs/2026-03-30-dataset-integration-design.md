# Dataset Integration Layer - Design Spec

## Overview

Integrate 11 public red-teaming datasets (~7,400 prompts) into mordor. Datasets serve as both standalone probes (fired directly at models) and as targets for existing 39 attack techniques.

## Architecture

### New file: `src/mordor/datasets.py`

Three responsibilities:
1. **Manifest** - YAML listing all available datasets with metadata and field mappings
2. **Downloader** - Pulls from HuggingFace, caches in `~/.mordor/datasets/`
3. **Normalizer** - Converts each format into unified schema

### Unified Prompt Schema

```python
{
    "text": str,              # the actual prompt
    "category": str,          # harm category mapped to our taxonomy
    "source": str,            # dataset name
    "difficulty": str | None, # easy/medium/hard if available
    "mode": str,              # single-turn or multi-turn
    "turns": list[str] | None, # for multi-turn prompts
    "metadata": dict,         # original fields preserved
}
```

### New file: `src/mordor/data/datasets.yaml`

Manifest with field mappings for each dataset: HF repo ID, text column name, category column, category value mapping, license.

### Storage

- Downloaded datasets normalized to JSON at `~/.mordor/datasets/<name>.json`
- Uses `huggingface_hub` for download (leverages HF cache), then normalizes and saves
- `datasets status` shows which are downloaded and disk usage

### Usage Modes

- `--mode direct`: Fire each prompt directly at model, evaluate response
- `--mode attacks`: Run specified attack techniques using dataset prompts as targets
- `--mode both` (default): Both direct probes and attack-wrapped

### CLI Commands

```
mordor datasets list              # show manifest
mordor datasets pull <name|--all> # download
mordor datasets info <name>       # details
mordor datasets status            # downloaded status

mordor run-dataset <name>         # run dataset
  -p/--provider, -m/--model, --mode direct|attacks|both,
  --attacks <list>, --limit N, -w/--workers N, --categories <list>
```

### Python API

```python
bt = Blackteam()
bt.list_datasets()
bt.pull_dataset("advbench")
prompts = bt.load_dataset("advbench")
results = bt.run_dataset("advbench", "anthropic", "claude-sonnet-4-6", mode="both")
```

### Supported Datasets (11, ~7,400 prompts)

1. AdvBench - 520, MIT, walledai/AdvBench, text_field=goal
2. HarmBench - 510, MIT, walledai/HarmBench, text_field=Behavior
3. StrongREJECT - 313, MIT, walledai/StrongREJECT, text_field=forbidden_prompt
4. JailbreakBench - 200, MIT, JailbreakBench/JBB-Behaviors, text_field=Behavior
5. SORRY-Bench - 450, CC-BY-4.0, sorry-bench/sorry-bench-202406, text_field=turns
6. Do-Not-Answer - 939, Apache-2.0, LibrAI/do-not-answer, text_field=question
7. XSTest - 450, CC-BY-4.0, walledai/XSTest, text_field=prompt
8. SimpleSafetyTests - 100, CC-BY-2.0, walledai/SimpleSafetyTests, text_field=prompt
9. BeaverTails-Eval - 700, CC-BY-NC-4.0, PKU-Alignment/BeaverTails-Evaluation, text_field=prompt
10. MLCommons DEMO - 1200, CC-BY-4.0, GitHub download, text_field=prompt
11. MHJ (Scale AI) - 2912, CC-BY-NC-4.0, ScaleAI/mhj, text_field=prompt

### Testing

- test_datasets.py: manifest loading, normalization, category mapping, CLI commands
- Mock HF downloads for unit tests using sample data fixtures
