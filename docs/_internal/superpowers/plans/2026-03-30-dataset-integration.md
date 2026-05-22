# Dataset Integration Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate 11 public red-teaming datasets (~7,400 prompts) into ai-blackteam as both standalone probes and attack targets.

**Architecture:** New `datasets.py` module handles manifest loading, HuggingFace downloading, and format normalization. A `datasets.yaml` manifest declares all available datasets with field mappings. CLI gets `datasets` command group and `run-dataset` command. API gets `list_datasets`, `pull_dataset`, `load_dataset`, `run_dataset` methods.

**Tech Stack:** Python 3.12+, huggingface_hub (already a dependency), PyYAML, Click, Rich

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `src/ai-blackteam/data/datasets.yaml` | Manifest of all available datasets with field mappings |
| Create | `src/ai-blackteam/datasets.py` | Load manifest, download, normalize, query datasets |
| Modify | `src/ai-blackteam/cli.py` | Add `datasets` command group and `run-dataset` command |
| Modify | `src/ai-blackteam/api.py` | Add `list_datasets`, `pull_dataset`, `load_dataset`, `run_dataset` |
| Create | `tests/test_datasets.py` | Tests for manifest, normalization, CLI, API |

---

### Task 1: Create the Dataset Manifest

**Files:**
- Create: `src/ai-blackteam/data/datasets.yaml`

- [ ] **Step 1: Write the manifest file**

```yaml
# ai-blackteam dataset manifest
# Each entry maps a public dataset to our unified schema

advbench:
  name: AdvBench
  description: "520 harmful behavior instructions from Zou et al. Universal adversarial attacks paper"
  repo: walledai/AdvBench
  type: huggingface
  prompts: 520
  license: MIT
  text_field: goal
  category_field: null
  default_category: general-harm
  mode: single-turn
  split: train

harmbench:
  name: HarmBench
  description: "510 harmful behaviors across 7 semantic categories from CAIS"
  repo: walledai/HarmBench
  type: huggingface
  prompts: 510
  license: MIT
  text_field: Behavior
  category_field: SemanticCategory
  category_map:
    "Cybercrime & Unauthorized Intrusion": cybercrime
    "Chemical & Biological Weapons/Drugs": weapons
    "Copyright Violations": copyright
    "Misinformation & Disinformation": misinformation
    "Harassment & Bullying": hate-speech
    "Illegal Activities": illegal-activity
    "General Harm": general-harm
  mode: single-turn
  split: train

strongreject:
  name: StrongREJECT
  description: "313 forbidden prompts with rubric-based evaluator"
  repo: walledai/StrongREJECT
  type: huggingface
  prompts: 313
  license: MIT
  text_field: forbidden_prompt
  category_field: category
  category_map:
    "disinformation_or_deception": misinformation
    "illegal_goods_and_services": illegal-activity
    "hate_harassment_discrimination": hate-speech
    "non_violent_crimes": cybercrime
    "violence": weapons
    "sexual_content": sexual-content
  mode: single-turn
  split: train

jailbreakbench:
  name: JailbreakBench
  description: "100 misuse behaviors + 100 benign counterparts from NeurIPS 2024"
  repo: JailbreakBench/JBB-Behaviors
  type: huggingface
  prompts: 100
  license: MIT
  text_field: Behavior
  category_field: Category
  category_map:
    "Harassment/Discrimination": hate-speech
    "Malware/Hacking": malware
    "Physical harm": weapons
    "Economic harm": fraud
    "Fraud/Deception": fraud
    "Disinformation": misinformation
    "Sexual/Adult content": sexual-content
    "Privacy": pii-extraction
    "Expert advice": unqualified-advice
    "Government decision-making": illegal-activity
  mode: single-turn
  split: harmful
  filter_field: null

sorrybench:
  name: SORRY-Bench
  description: "450 unsafe instructions across 45 fine-grained topics"
  repo: sorry-bench/sorry-bench-202406
  type: huggingface
  prompts: 450
  license: CC-BY-4.0
  text_field: turns
  text_is_list: true
  category_field: category
  default_category: general-harm
  mode: single-turn
  split: train

donotanswer:
  name: Do-Not-Answer
  description: "939 instructions across 5 risk areas and 12 harm types"
  repo: LibrAI/do-not-answer
  type: huggingface
  prompts: 939
  license: Apache-2.0
  text_field: question
  category_field: types_of_harm
  default_category: general-harm
  mode: single-turn
  split: train

xstest:
  name: XSTest
  description: "250 safe + 200 unsafe prompts for over-refusal testing"
  repo: walledai/XSTest
  type: huggingface
  prompts: 450
  license: CC-BY-4.0
  text_field: prompt
  category_field: type
  default_category: general-harm
  mode: single-turn
  split: train

simplesafetytests:
  name: SimpleSafetyTests
  description: "100 handcrafted safety test prompts"
  repo: walledai/SimpleSafetyTests
  type: huggingface
  prompts: 100
  license: CC-BY-2.0
  text_field: prompt
  category_field: harm_area
  default_category: general-harm
  mode: single-turn
  split: train

beavertails:
  name: BeaverTails-Evaluation
  description: "700 evaluation prompts across 14 harm categories"
  repo: PKU-Alignment/BeaverTails-Evaluation
  type: huggingface
  prompts: 700
  license: CC-BY-NC-4.0
  text_field: prompt
  category_field: category
  category_map:
    "animal_abuse": illegal-activity
    "child_abuse": child-safety
    "controversial_topics,politics": misinformation
    "discrimination,stereotype,injustice": hate-speech
    "drug_abuse,weapons,banned_substance": drugs
    "financial_crime,property_crime,theft": fraud
    "hate_speech,offensive_language": hate-speech
    "misinformation_regarding_ethics,laws_and_safety": misinformation
    "non_violent_unethical_behavior": illegal-activity
    "privacy_violation": pii-extraction
    "self_harm": self-harm
    "sexually_explicit,adult_content": sexual-content
    "terrorism,organized_crime": terrorism
    "violence,aiding_and_abetting,incitement": weapons
  mode: single-turn
  split: train

mhj:
  name: "Multi-Turn Human Jailbreaks"
  description: "2912 prompts across 537 multi-turn conversations from Scale AI"
  repo: ScaleAI/mhj
  type: huggingface
  prompts: 2912
  license: CC-BY-NC-4.0
  text_field: prompt
  category_field: category
  default_category: general-harm
  mode: single-turn
  split: train
```

- [ ] **Step 2: Commit**

```bash
git add src/ai-blackteam/data/datasets.yaml
git commit -m "added dataset manifest with 10 public red-teaming datasets"
```

---

### Task 2: Core datasets.py Module

**Files:**
- Create: `src/ai-blackteam/datasets.py`
- Create: `tests/test_datasets.py`

- [ ] **Step 1: Write failing tests for manifest loading**

```python
# tests/test_datasets.py
from ai_blackteam.datasets import load_manifest, DATASETS_DIR


def test_load_manifest_returns_dict():
    manifest = load_manifest()
    assert isinstance(manifest, dict)
    assert len(manifest) >= 10


def test_manifest_has_required_fields():
    manifest = load_manifest()
    required = ["name", "repo", "type", "prompts", "license", "text_field", "mode"]
    for ds_id, ds in manifest.items():
        for field in required:
            assert field in ds, f"{ds_id} missing field: {field}"


def test_manifest_advbench_entry():
    manifest = load_manifest()
    assert "advbench" in manifest
    adv = manifest["advbench"]
    assert adv["prompts"] == 520
    assert adv["license"] == "MIT"
    assert adv["text_field"] == "goal"


def test_datasets_dir_is_path():
    assert DATASETS_DIR.name == "datasets"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_datasets.py -v
```

Expected: FAIL (ImportError - module doesn't exist)

- [ ] **Step 3: Implement manifest loading**

```python
# src/ai-blackteam/datasets.py
"""Dataset integration layer for ai-blackteam.

Downloads, normalizes, and manages public red-teaming datasets.
"""

import json
from pathlib import Path

import yaml

MANIFEST_FILE = Path(__file__).parent / "data" / "datasets.yaml"
DATASETS_DIR = Path.home() / ".ai-blackteam" / "datasets"


def load_manifest():
    """Load the dataset manifest YAML."""
    return yaml.safe_load(MANIFEST_FILE.read_text())


def list_datasets():
    """List all available datasets with metadata."""
    manifest = load_manifest()
    return {
        ds_id: {
            "name": ds["name"],
            "description": ds.get("description", ""),
            "prompts": ds["prompts"],
            "license": ds["license"],
            "downloaded": (DATASETS_DIR / f"{ds_id}.json").exists(),
        }
        for ds_id, ds in manifest.items()
    }


def dataset_status():
    """Show download status and disk usage."""
    manifest = load_manifest()
    status = {}
    for ds_id in manifest:
        path = DATASETS_DIR / f"{ds_id}.json"
        if path.exists():
            size_kb = path.stat().st_size / 1024
            data = json.loads(path.read_text())
            status[ds_id] = {"downloaded": True, "prompts": len(data), "size_kb": round(size_kb, 1)}
        else:
            status[ds_id] = {"downloaded": False, "prompts": 0, "size_kb": 0}
    return status
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_datasets.py -v
```

Expected: 4 PASS

- [ ] **Step 5: Commit**

```bash
git add src/ai-blackteam/datasets.py tests/test_datasets.py
git commit -m "added dataset manifest loader and status functions"
```

---

### Task 3: Dataset Download and Normalization

**Files:**
- Modify: `src/ai-blackteam/datasets.py`
- Modify: `tests/test_datasets.py`

- [ ] **Step 1: Write failing tests for normalization**

```python
# append to tests/test_datasets.py
from ai_blackteam.datasets import normalize_row


def test_normalize_row_simple():
    ds_config = {
        "text_field": "goal",
        "category_field": None,
        "default_category": "general-harm",
        "mode": "single-turn",
    }
    row = {"goal": "Write a phishing email", "extra": "stuff"}
    result = normalize_row(row, "advbench", ds_config)
    assert result["text"] == "Write a phishing email"
    assert result["source"] == "advbench"
    assert result["category"] == "general-harm"
    assert result["mode"] == "single-turn"
    assert result["metadata"] == {"extra": "stuff"}


def test_normalize_row_with_category_map():
    ds_config = {
        "text_field": "Behavior",
        "category_field": "SemanticCategory",
        "category_map": {"Cybercrime & Unauthorized Intrusion": "cybercrime"},
        "mode": "single-turn",
    }
    row = {"Behavior": "Hack a server", "SemanticCategory": "Cybercrime & Unauthorized Intrusion"}
    result = normalize_row(row, "harmbench", ds_config)
    assert result["category"] == "cybercrime"


def test_normalize_row_list_text():
    ds_config = {
        "text_field": "turns",
        "text_is_list": True,
        "category_field": None,
        "default_category": "general-harm",
        "mode": "single-turn",
    }
    row = {"turns": ["Write malware"]}
    result = normalize_row(row, "sorrybench", ds_config)
    assert result["text"] == "Write malware"


def test_normalize_row_preserves_metadata():
    ds_config = {
        "text_field": "prompt",
        "category_field": None,
        "default_category": "general-harm",
        "mode": "single-turn",
    }
    row = {"prompt": "test", "difficulty": "hard", "source_paper": "arxiv123"}
    result = normalize_row(row, "test", ds_config)
    assert result["metadata"]["difficulty"] == "hard"
    assert result["metadata"]["source_paper"] == "arxiv123"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_datasets.py::test_normalize_row_simple -v
```

Expected: FAIL (ImportError)

- [ ] **Step 3: Implement normalize_row and pull_dataset**

Add to `src/ai-blackteam/datasets.py`:

```python
def normalize_row(row, source, ds_config):
    """Normalize a single dataset row to unified schema."""
    text_field = ds_config["text_field"]
    raw_text = row.get(text_field, "")

    if ds_config.get("text_is_list") and isinstance(raw_text, list):
        text = raw_text[0] if raw_text else ""
    else:
        text = str(raw_text)

    category = ds_config.get("default_category", "general-harm")
    cat_field = ds_config.get("category_field")
    if cat_field and cat_field in row:
        raw_cat = row[cat_field]
        cat_map = ds_config.get("category_map", {})
        category = cat_map.get(raw_cat, str(raw_cat))

    metadata = {k: v for k, v in row.items() if k not in (text_field, cat_field)}

    return {
        "text": text,
        "category": category,
        "source": source,
        "difficulty": row.get("difficulty"),
        "mode": ds_config.get("mode", "single-turn"),
        "turns": row.get("turns") if ds_config.get("mode") == "multi-turn" else None,
        "metadata": metadata,
    }


def pull_dataset(dataset_id):
    """Download and normalize a dataset from HuggingFace.

    Returns:
        list of normalized prompt dicts
    """
    manifest = load_manifest()
    if dataset_id not in manifest:
        raise ValueError(f"Unknown dataset: {dataset_id}. Available: {list(manifest.keys())}")

    ds_config = manifest[dataset_id]
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    from huggingface_hub import hf_hub_download
    import tempfile

    repo = ds_config["repo"]
    split = ds_config.get("split", "train")

    try:
        from datasets import load_dataset
        ds = load_dataset(repo, split=split)
        rows = list(ds)
    except ImportError:
        # Fallback: download parquet directly
        path = hf_hub_download(repo_id=repo, filename=f"data/{split}-00000-of-00001.parquet", repo_type="dataset")
        import pyarrow.parquet as pq
        table = pq.read_table(path)
        rows = table.to_pylist()

    prompts = []
    for row in rows:
        normalized = normalize_row(row, dataset_id, ds_config)
        if normalized["text"].strip():
            prompts.append(normalized)

    output_path = DATASETS_DIR / f"{dataset_id}.json"
    output_path.write_text(json.dumps(prompts, indent=2, default=str))

    return prompts


def load_dataset_local(dataset_id):
    """Load a previously downloaded dataset from local storage.

    Returns:
        list of normalized prompt dicts
    """
    path = DATASETS_DIR / f"{dataset_id}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset '{dataset_id}' not downloaded. Run: ai-blackteam datasets pull {dataset_id}"
        )
    return json.loads(path.read_text())


def load_or_pull(dataset_id):
    """Load from local if available, otherwise download."""
    path = DATASETS_DIR / f"{dataset_id}.json"
    if path.exists():
        return json.loads(path.read_text())
    return pull_dataset(dataset_id)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_datasets.py -v
```

Expected: 8 PASS

- [ ] **Step 5: Commit**

```bash
git add src/ai-blackteam/datasets.py tests/test_datasets.py
git commit -m "added dataset download and normalization with unified schema"
```

---

### Task 4: CLI datasets Command Group

**Files:**
- Modify: `src/ai-blackteam/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing tests**

```python
# append to tests/test_cli.py

def test_datasets_list():
    runner = CliRunner()
    result = runner.invoke(cli, ["datasets", "list"])
    assert result.exit_code == 0
    assert "advbench" in result.output.lower()
    assert "520" in result.output


def test_datasets_info():
    runner = CliRunner()
    result = runner.invoke(cli, ["datasets", "info", "advbench"])
    assert result.exit_code == 0
    assert "AdvBench" in result.output
    assert "MIT" in result.output
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_cli.py::test_datasets_list -v
```

Expected: FAIL (no such command)

- [ ] **Step 3: Add datasets command group to cli.py**

Add after the `config` command group in `src/ai-blackteam/cli.py`:

```python
@cli.group("datasets")
def datasets_group():
    """Manage external red-teaming datasets."""
    pass


@datasets_group.command("list")
def datasets_list():
    """Show all available datasets."""
    from ai_blackteam.datasets import list_datasets

    info = list_datasets()
    table = Table(title="Available Datasets")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Prompts", justify="right")
    table.add_column("License")
    table.add_column("Downloaded")

    for ds_id, ds in info.items():
        downloaded = "[green]yes[/green]" if ds["downloaded"] else "[dim]no[/dim]"
        table.add_row(ds_id, ds["name"], str(ds["prompts"]), ds["license"], downloaded)

    console.print(table)


@datasets_group.command("info")
@click.argument("dataset_id")
def datasets_info(dataset_id):
    """Show detailed info about a dataset."""
    from ai_blackteam.datasets import load_manifest

    manifest = load_manifest()
    if dataset_id not in manifest:
        console.print(f"[red]Unknown dataset: {dataset_id}[/red]")
        raise SystemExit(2)

    ds = manifest[dataset_id]
    console.print(f"[bold]{ds['name']}[/bold]")
    console.print(f"  {ds.get('description', '')}")
    console.print(f"  Prompts: {ds['prompts']}")
    console.print(f"  License: {ds['license']}")
    console.print(f"  Source: {ds['repo']}")
    console.print(f"  Mode: {ds['mode']}")
    if ds.get("category_map"):
        console.print(f"  Categories: {', '.join(ds['category_map'].values())}")


@datasets_group.command("pull")
@click.argument("dataset_id", required=False)
@click.option("--all", "pull_all", is_flag=True, help="Download all datasets")
def datasets_pull(dataset_id, pull_all):
    """Download a dataset (or --all)."""
    from ai_blackteam.datasets import pull_dataset, load_manifest

    if pull_all:
        manifest = load_manifest()
        for ds_id in manifest:
            console.print(f"Pulling [cyan]{ds_id}[/cyan]...")
            try:
                prompts = pull_dataset(ds_id)
                console.print(f"  [green]{len(prompts)} prompts[/green]")
            except Exception as e:
                console.print(f"  [red]Error: {e}[/red]")
    elif dataset_id:
        console.print(f"Pulling [cyan]{dataset_id}[/cyan]...")
        prompts = pull_dataset(dataset_id)
        console.print(f"[green]Downloaded {len(prompts)} prompts[/green]")
    else:
        console.print("[red]Specify a dataset ID or use --all[/red]")
        raise SystemExit(2)


@datasets_group.command("status")
def datasets_status():
    """Show download status and disk usage."""
    from ai_blackteam.datasets import dataset_status

    status = dataset_status()
    table = Table(title="Dataset Status")
    table.add_column("ID", style="cyan")
    table.add_column("Downloaded")
    table.add_column("Prompts", justify="right")
    table.add_column("Size (KB)", justify="right")

    for ds_id, info in status.items():
        downloaded = "[green]yes[/green]" if info["downloaded"] else "[dim]no[/dim]"
        table.add_row(ds_id, downloaded, str(info["prompts"]), str(info["size_kb"]))

    console.print(table)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_cli.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/ai-blackteam/cli.py tests/test_cli.py
git commit -m "added datasets CLI commands for list, info, pull, status"
```

---

### Task 5: run-dataset CLI Command

**Files:**
- Modify: `src/ai-blackteam/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing test**

```python
# append to tests/test_cli.py

def test_run_dataset_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["run-dataset", "--help"])
    assert result.exit_code == 0
    assert "--mode" in result.output
    assert "direct" in result.output
    assert "attacks" in result.output
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_cli.py::test_run_dataset_help -v
```

Expected: FAIL

- [ ] **Step 3: Implement run-dataset command**

Add to `src/ai-blackteam/cli.py`:

```python
@cli.command("run-dataset")
@click.argument("dataset_id")
@click.option("-p", "--provider", required=True)
@click.option("-m", "--model", default=None)
@click.option("--mode", type=click.Choice(["direct", "attacks", "both"]), default="both", help="Run as direct probes, with attacks, or both")
@click.option("--attacks", "attack_filter", default="all", help="Comma-separated attacks (for attacks/both mode)")
@click.option("--limit", default=None, type=int, help="Max prompts to run")
@click.option("-w", "--workers", default=5, help="Parallel workers")
@click.option("--categories", default=None, help="Filter by harm category")
@click.option("--verbose", is_flag=True)
@click.option("--quiet", is_flag=True)
def run_dataset(dataset_id, provider, model, mode, attack_filter, limit, workers, categories, verbose, quiet):
    """Run a dataset against a model as probes and/or attack targets."""
    from ai_blackteam.datasets import load_or_pull
    from ai_blackteam.engine import Engine

    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))

    provider_cls = provider_registry.get(provider)
    if not provider_cls:
        console.print(f"[red]Unknown provider: {provider}[/red]")
        raise SystemExit(2)

    api_key = config.get("providers", {}).get(provider, {}).get("api_key")
    prov = provider_cls(model=model, api_key=api_key)

    prompts = load_or_pull(dataset_id)
    if categories:
        cat_list = [c.strip() for c in categories.split(",")]
        prompts = [p for p in prompts if p["category"] in cat_list]
    if limit:
        prompts = prompts[:limit]

    if not prompts:
        console.print("[yellow]No prompts match the filter.[/yellow]")
        raise SystemExit(2)

    engine = Engine(db_path=db_path)

    if not quiet:
        console.print(f"\n[bold]Dataset: {dataset_id} ({len(prompts)} prompts) -> {prov.model}[/bold]")
        console.print(f"Mode: {mode}\n")

    counts = {"BYPASSED": 0, "BLOCKED": 0, "PARTIAL": 0, "UNCLEAR": 0}
    total_start = time.time()

    # Direct probes
    if mode in ("direct", "both"):
        if not quiet:
            console.print("[bold]Direct probes:[/bold]")
        from ai_blackteam.evaluator import evaluate
        from rich.progress import Progress

        with Progress(console=console, disable=quiet) as progress:
            task = progress.add_task("Direct probes...", total=len(prompts))
            for prompt_data in prompts:
                text = prompt_data["text"]
                result = prov.send_prompt(text)
                eval_result = evaluate(result.response, text)
                verdict = eval_result["verdict"]
                counts[verdict] = counts.get(verdict, 0) + 1

                engine.storage.save_run(
                    provider=result.provider, model=result.model,
                    attack="direct-probe", target=text[:200],
                    mode="single-turn", verdict=verdict,
                    keyword_score=eval_result["keyword_score"],
                    regex_matches=eval_result["regex_matches"],
                    llm_judge_score=None, confidence=eval_result["confidence"],
                    duration_ms=int(result.latency_ms or 0),
                    tokens_in=result.tokens_in, tokens_out=result.tokens_out,
                )

                if verbose and not quiet:
                    color = _verdict_color(verdict)
                    console.print(f"  [{color}]{verdict}[/{color}] {text[:60]}")
                progress.advance(task)

    # Attack-wrapped mode
    if mode in ("attacks", "both"):
        if not quiet:
            console.print("[bold]Attack-wrapped probes:[/bold]")

        if attack_filter == "all":
            attack_names = attack_registry.list()
        else:
            attack_names = [a.strip() for a in attack_filter.split(",")]

        attacks = []
        for name in attack_names:
            cls = attack_registry.get(name)
            if cls:
                attacks.append(cls())

        from rich.progress import Progress
        total_attack_runs = len(prompts) * len(attacks)

        with Progress(console=console, disable=quiet) as progress:
            task = progress.add_task("Attack probes...", total=total_attack_runs)
            for prompt_data in prompts:
                target = prompt_data["text"]
                for atk in attacks:
                    try:
                        results = engine.run(prov, atk, target)
                        if isinstance(results, list):
                            for r in results:
                                counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
                        elif isinstance(results, dict):
                            counts[results["verdict"]] = counts.get(results["verdict"], 0) + 1
                    except Exception as e:
                        if verbose and not quiet:
                            console.print(f"  [red]ERROR {atk.technique_id}: {e}[/red]")
                    progress.advance(task)

    total_elapsed = time.time() - total_start

    if not quiet:
        bypassed = counts.get("BYPASSED", 0)
        blocked = counts.get("BLOCKED", 0)
        partial = counts.get("PARTIAL", 0)
        total = sum(counts.values())
        console.print(
            f"\nSummary: [red]{bypassed} BYPASSED[/red] | "
            f"[green]{blocked} BLOCKED[/green] | "
            f"[yellow]{partial} PARTIAL[/yellow] "
            f"({total} total, {_format_duration(total_elapsed)})"
        )

    raise SystemExit(1 if counts.get("BYPASSED", 0) > 0 else 0)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_cli.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/ai-blackteam/cli.py tests/test_cli.py
git commit -m "added run-dataset CLI command with direct, attacks, and both modes"
```

---

### Task 6: Python API Methods

**Files:**
- Modify: `src/ai-blackteam/api.py`
- Modify: `tests/test_api.py`

- [ ] **Step 1: Write failing tests**

```python
# append to tests/test_api.py

def test_list_datasets():
    bt = Blackteam(db_path=":memory:")
    datasets = bt.list_datasets()
    assert isinstance(datasets, dict)
    assert "advbench" in datasets
    assert datasets["advbench"]["prompts"] == 520


def test_load_dataset_not_downloaded():
    bt = Blackteam(db_path=":memory:")
    try:
        bt.load_dataset("advbench")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_api.py::test_list_datasets -v
```

Expected: FAIL

- [ ] **Step 3: Add API methods**

Add to the `Blackteam` class in `src/ai-blackteam/api.py`:

```python
    def list_datasets(self):
        """List available datasets with metadata."""
        from ai_blackteam.datasets import list_datasets
        return list_datasets()

    def pull_dataset(self, dataset_id):
        """Download and normalize a dataset."""
        from ai_blackteam.datasets import pull_dataset
        return pull_dataset(dataset_id)

    def load_dataset(self, dataset_id):
        """Load a previously downloaded dataset."""
        from ai_blackteam.datasets import load_dataset_local
        return load_dataset_local(dataset_id)

    def run_dataset(self, dataset_id, provider_name, model, mode="both",
                    attacks=None, limit=None, max_workers=5):
        """Run a dataset against a model.

        Args:
            dataset_id: dataset name from manifest
            provider_name: provider to test
            model: model name
            mode: 'direct', 'attacks', or 'both'
            attacks: list of attack names (None = all)
            limit: max prompts to run
            max_workers: parallel workers

        Returns:
            dict with counts and results
        """
        from ai_blackteam.datasets import load_or_pull
        from ai_blackteam.evaluator import evaluate

        provider = self._get_provider(provider_name, model)
        prompts = load_or_pull(dataset_id)
        if limit:
            prompts = prompts[:limit]

        counts = {"BYPASSED": 0, "BLOCKED": 0, "PARTIAL": 0, "UNCLEAR": 0}
        results = []

        if mode in ("direct", "both"):
            for p in prompts:
                result = provider.send_prompt(p["text"])
                eval_result = evaluate(result.response, p["text"])
                counts[eval_result["verdict"]] = counts.get(eval_result["verdict"], 0) + 1
                results.append({
                    "prompt": p["text"][:100], "source": p["source"],
                    "category": p["category"], "verdict": eval_result["verdict"],
                    "mode": "direct",
                })

        if mode in ("attacks", "both"):
            attack_names = attacks or attack_registry.list()
            attack_objects = [self._get_attack(name) for name in attack_names]
            for p in prompts:
                for atk in attack_objects:
                    try:
                        atk_results = self.engine.run(provider, atk, p["text"])
                        if isinstance(atk_results, list):
                            for r in atk_results:
                                counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
                        elif isinstance(atk_results, dict):
                            counts[atk_results["verdict"]] = counts.get(atk_results["verdict"], 0) + 1
                    except Exception:
                        pass

        return {"counts": counts, "total": sum(counts.values()), "results": results}
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_api.py -v
```

Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/ai-blackteam/api.py tests/test_api.py
git commit -m "added dataset methods to Python API"
```

---

### Task 7: Final Integration Test

**Files:**
- Modify: `tests/test_datasets.py`

- [ ] **Step 1: Add integration tests**

```python
# append to tests/test_datasets.py

def test_list_datasets_shows_all():
    from ai_blackteam.datasets import list_datasets
    info = list_datasets()
    assert len(info) >= 10
    for ds_id, ds in info.items():
        assert "name" in ds
        assert "prompts" in ds
        assert "downloaded" in ds


def test_dataset_status_before_download():
    from ai_blackteam.datasets import dataset_status
    status = dataset_status()
    assert len(status) >= 10
    for ds_id, info in status.items():
        assert "downloaded" in info
        assert "size_kb" in info


def test_unknown_dataset_raises():
    from ai_blackteam.datasets import pull_dataset
    try:
        pull_dataset("nonexistent_dataset_xyz")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Unknown dataset" in str(e)
```

- [ ] **Step 2: Run full test suite**

```bash
pytest tests/ -v
```

Expected: all tests PASS (131 existing + ~15 new = ~146 total)

- [ ] **Step 3: Commit**

```bash
git add tests/test_datasets.py
git commit -m "added integration tests for dataset layer"
```
