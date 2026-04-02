import csv
import io
import httpx
from mordor.registry import register_dataset
from mordor.datasets.loader import DatasetLoader


@register_dataset("do-not-answer")
class DoNotAnswerLoader(DatasetLoader):
    name = "do-not-answer"
    license = "Apache-2.0"
    source_url = "https://github.com/Libr-AI/do-not-answer"
    description = "939 harmful prompts across 12 risk areas (Do-Not-Answer)"

    RAW_URL = "https://raw.githubusercontent.com/Libr-AI/do-not-answer/main/datasets/data_en.csv"

    CATEGORY_MAP = {
        "Discrimination": "discrimination",
        "Hate Speech": "hate-speech",
        "Violence": "weapons",
        "Weapons": "weapons",
        "Drugs": "drugs",
        "Suicide": "self-harm",
        "Sexual": "sexual-content",
        "Privacy": "privacy-violation",
        "Fraud": "fraud",
        "Malware": "cybercrime",
        "Copyright": "copyright-ip",
        "Misinformation": "misinformation",
    }

    def _map_category(self, raw_cat):
        for key, val in self.CATEGORY_MAP.items():
            if key.lower() in raw_cat.lower():
                return val
        return "malware"

    def download(self):
        r = httpx.get(self.RAW_URL, timeout=30, follow_redirects=True)
        r.raise_for_status()

        items = []
        reader = csv.DictReader(io.StringIO(r.text))
        for row in reader:
            prompt = row.get("question", "").strip()
            if not prompt:
                continue

            raw_cat = row.get("risk_area", row.get("types_of_harm", ""))
            items.append({
                "prompt": prompt,
                "category": self._map_category(raw_cat),
                "source": "do-not-answer",
                "difficulty": "easy",
            })

        return items
