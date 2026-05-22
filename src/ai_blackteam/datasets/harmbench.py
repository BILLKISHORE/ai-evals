import csv
import io
import httpx
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader


@register_dataset("harmbench")
class HarmBenchLoader(DatasetLoader):
    name = "harmbench"
    license = "MIT"
    source_url = "https://github.com/centerforaisafety/HarmBench"
    description = "510 harmful behaviors from HarmBench (CAIS, NeurIPS 2024)"

    RAW_URL = "https://raw.githubusercontent.com/centerforaisafety/HarmBench/main/data/behavior_datasets/harmbench_behaviors_text_all.csv"

    CATEGORY_MAP = {
        "chemical_biological": "cbrn",
        "cybercrime": "cybercrime",
        "harassment_bullying": "harassment",
        "illegal_activities": "fraud",
        "misinformation_disinformation": "misinformation",
        "copyright": "copyright-ip",
        "harmful_content": "malware",
    }

    def download(self):
        r = httpx.get(self.RAW_URL, timeout=30, follow_redirects=True)
        r.raise_for_status()

        items = []
        reader = csv.DictReader(io.StringIO(r.text))
        for row in reader:
            behavior = row.get("Behavior", row.get("behavior", "")).strip()
            if not behavior:
                continue

            raw_cat = row.get("SemanticCategory", row.get("FunctionalCategory", "")).strip().lower().replace(" ", "_")
            category = self.CATEGORY_MAP.get(raw_cat, "malware")

            items.append({
                "prompt": behavior,
                "category": category,
                "source": "harmbench",
                "difficulty": "medium",
            })

        return items
