"""Dataset integration layer for mordor."""

import json
from pathlib import Path

import yaml

MANIFEST_FILE = Path(__file__).parent / ".." / "data" / "datasets.yaml"
DATASETS_DIR = Path.home() / ".mordor" / "datasets"


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
    """Download and normalize a dataset from HuggingFace."""
    manifest = load_manifest()
    if dataset_id not in manifest:
        raise ValueError(f"Unknown dataset: {dataset_id}. Available: {list(manifest.keys())}")

    ds_config = manifest[dataset_id]
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    repo = ds_config["repo"]
    split = ds_config.get("split", "train")

    try:
        from datasets import load_dataset as hf_load
        ds = hf_load(repo, split=split)
        rows = list(ds)
    except ImportError:
        from huggingface_hub import hf_hub_download
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
    """Load a previously downloaded dataset from local storage."""
    path = DATASETS_DIR / f"{dataset_id}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset '{dataset_id}' not downloaded. Run: mordor datasets pull {dataset_id}"
        )
    return json.loads(path.read_text())


def load_or_pull(dataset_id):
    """Load from local if available, otherwise download."""
    path = DATASETS_DIR / f"{dataset_id}.json"
    if path.exists():
        return json.loads(path.read_text())
    return pull_dataset(dataset_id)
