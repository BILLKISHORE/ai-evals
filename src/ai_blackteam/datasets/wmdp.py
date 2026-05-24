import os
import httpx
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader


ROWS_API = (
    "https://datasets-server.huggingface.co/rows"
    "?dataset=cais/wmdp&config={config}&split=test"
    "&offset={offset}&length={length}"
)
PAGE_SIZE = 100


def _load_wmdp_split(config_name):
    """Load a WMDP config via the HF datasets-server rows API.

    config_name must be one of: wmdp-bio, wmdp-chem, wmdp-cyber.
    All WMDP configs only have a 'test' split.
    """
    headers = {}
    hf_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"

    rows = []
    offset = 0
    while True:
        url = ROWS_API.format(config=config_name, offset=offset, length=PAGE_SIZE)
        r = httpx.get(url, timeout=30, follow_redirects=True, headers=headers)
        r.raise_for_status()
        data = r.json()
        page = data.get("rows", [])
        if not page:
            break
        rows.extend(entry.get("row", {}) for entry in page)
        total = data.get("num_rows_total", 0)
        offset += PAGE_SIZE
        if offset >= total:
            break
    return rows


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
