import csv
import io
import httpx
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader


@register_dataset("strongreject")
class StrongREJECTLoader(DatasetLoader):
    name = "strongreject"
    license = "MIT"
    source_url = "https://github.com/alexandrasouly/strongreject"
    description = "310 prompts from StrongREJECT benchmark (Souly et al., arXiv 2402.10260)"

    RAW_URL = "https://raw.githubusercontent.com/alexandrasouly/strongreject/main/strongreject_dataset/strongreject_dataset.csv"

    CATEGORY_MAP = {
        "Disinformation and deception": "misinformation",
        "Hate, harassment and discrimination": "hate-speech",
        "Illegal goods and services": "fraud",
        "Non-violent crimes": "fraud",
        "Sexual content": "sexual-content",
        "Violence": "weapons",
    }

    def _map_category(self, raw_cat):
        if not raw_cat:
            return "harmful-content"
        return self.CATEGORY_MAP.get(raw_cat.strip(), "harmful-content")

    def download(self):
        r = httpx.get(self.RAW_URL, timeout=30, follow_redirects=True)
        r.raise_for_status()

        items = []
        reader = csv.DictReader(io.StringIO(r.text))
        for row in reader:
            prompt = row.get("forbidden_prompt", "").strip()
            if not prompt:
                continue
            items.append({
                "prompt": prompt,
                "category": self._map_category(row.get("category", "")),
                "source": f"strongreject:{row.get('source', 'unknown')}",
                "difficulty": "hard",
            })

        return items
