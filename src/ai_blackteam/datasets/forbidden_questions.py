import csv
import io
import httpx
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader


@register_dataset("forbidden_questions")
class ForbiddenQuestionsLoader(DatasetLoader):
    name = "forbidden_questions"
    license = "research-only"
    source_url = "https://github.com/verazuo/jailbreak_llms"
    description = "390 questions x 13 scenarios from Shen et al. 2024 (Do Anything Now)"

    RAW_URL = "https://raw.githubusercontent.com/verazuo/jailbreak_llms/main/data/forbidden_question/forbidden_question_set.csv"

    CATEGORY_MAP = {
        "Illegal Activity": "fraud",
        "Hate Speech": "hate-speech",
        "Malware Generation": "malware",
        "Physical Harm": "weapons",
        "Economic Harm": "fraud",
        "Fraud": "fraud",
        "Pornography": "sexual-content",
        "Political Lobbying": "misinformation",
        "Privacy Violation": "privacy-violation",
        "Legal Opinion": "unqualified-advice",
        "Financial Advice": "unqualified-advice",
        "Health Consultation": "unqualified-advice",
        "Government Decision": "misinformation",
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
            prompt = row.get("question", "").strip()
            if not prompt:
                continue
            items.append({
                "prompt": prompt,
                "category": self._map_category(row.get("content_policy_name", "")),
                "source": "forbidden_questions",
                "difficulty": "medium",
            })

        return items
