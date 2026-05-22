import json
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader


def _load_wmdp_split(split_name):
    """Load a WMDP split with fallback: datasets lib -> hf_hub jsonl -> hf_hub parquet."""
    # Approach 1: datasets library (most reliable)
    try:
        from datasets import load_dataset
        ds = load_dataset("cais/wmdp", split_name)
        return list(ds)
    except Exception:
        pass

    # Approach 2: hf_hub_download with jsonl
    try:
        from huggingface_hub import hf_hub_download
        path = hf_hub_download(
            repo_id="cais/wmdp",
            filename=f"data/{split_name}.jsonl",
            repo_type="dataset",
        )
        rows = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows
    except Exception:
        pass

    # Approach 3: hf_hub_download with parquet
    from huggingface_hub import hf_hub_download
    path = hf_hub_download(
        repo_id="cais/wmdp",
        filename=f"data/{split_name}/train-00000-of-00001.parquet",
        repo_type="dataset",
    )
    import pyarrow.parquet as pq
    table = pq.read_table(path)
    return table.to_pylist()


def _build_items(rows, category, source):
    """Convert raw WMDP rows into prompt dicts."""
    items = []
    for row in rows:
        prompt = row["question"]
        choices = row.get("choices", [])
        if choices:
            prompt += "\n" + "\n".join(
                f"{chr(65 + i)}. {c}" for i, c in enumerate(choices)
            )
        items.append({
            "prompt": prompt,
            "category": category,
            "source": source,
            "difficulty": "medium",
            "metadata": {
                "answer": row.get("answer"),
                "choices": choices,
            },
        })
    return items


@register_dataset("wmdp-bio")
class WMDPBioLoader(DatasetLoader):
    name = "wmdp-bio"
    license = "MIT"
    source_url = "https://huggingface.co/datasets/cais/wmdp"
    description = "1,273 biosecurity multiple-choice questions from WMDP benchmark"

    def download(self):
        rows = _load_wmdp_split("wmdp-bio")
        return _build_items(rows, "biological-weapons", "wmdp-bio")


@register_dataset("wmdp-cyber")
class WMDPCyberLoader(DatasetLoader):
    name = "wmdp-cyber"
    license = "MIT"
    source_url = "https://huggingface.co/datasets/cais/wmdp"
    description = "1,987 cybersecurity multiple-choice questions from WMDP benchmark"

    def download(self):
        rows = _load_wmdp_split("wmdp-cyber")
        return _build_items(rows, "cybercrime", "wmdp-cyber")


@register_dataset("wmdp-chem")
class WMDPChemLoader(DatasetLoader):
    name = "wmdp-chem"
    license = "MIT"
    source_url = "https://huggingface.co/datasets/cais/wmdp"
    description = "408 chemical weapons multiple-choice questions from WMDP benchmark"

    def download(self):
        rows = _load_wmdp_split("wmdp-chem")
        return _build_items(rows, "chemical-weapons", "wmdp-chem")
