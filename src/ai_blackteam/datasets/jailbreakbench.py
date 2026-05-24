import csv
import io
import httpx
from ai_blackteam.registry import register_dataset
from ai_blackteam.datasets.loader import DatasetLoader


@register_dataset("jailbreakbench")
class JailbreakBenchLoader(DatasetLoader):
    name = "jailbreakbench"
    license = "MIT"
    source_url = "https://github.com/JailbreakBench/jailbreakbench"
    description = "100 harmful behaviors curated from AdvBench + HarmBench (NeurIPS 2024)"

    RAW_URL = "https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors/resolve/main/data/harmful-behaviors.csv"

    CATEGORY_MAP = {
        "Harassment/Discrimination": "harassment",
        "Malware/Hacking": "malware",
        "Physical harm": "weapons",
        "Economic harm": "fraud",
        "Fraud/Deception": "fraud",
        "Disinformation": "misinformation",
        "Sexual/Adult content": "sexual-content",
        "Privacy": "privacy-violation",
        "Expert advice": "unqualified-advice",
        "Government decision-making": "misinformation",
    }

    def _guess_category(self, prompt, source=""):
        lower = prompt.lower()
        if any(w in lower for w in ["phish", "email pretend", "credential"]):
            return "phishing"
        if any(w in lower for w in ["malware", "virus", "exploit", "hack", "ransomware", "code"]):
            return "cybercrime"
        if any(w in lower for w in ["bomb", "weapon", "explosive", "gun", "chemical"]):
            return "weapons"
        if any(w in lower for w in ["drug", "meth", "cocaine", "fentanyl"]):
            return "drugs"
        if any(w in lower for w in ["suicide", "self-harm", "kill myself"]):
            return "self-harm"
        if any(w in lower for w in ["hate", "racist", "supremac", "slur"]):
            return "hate-speech"
        if any(w in lower for w in ["fake news", "misinform", "disinform"]):
            return "misinformation"
        if any(w in lower for w in ["fraud", "scam", "counterfeit", "launder", "steal"]):
            return "fraud"
        if any(w in lower for w in ["harass", "bully", "stalk", "threaten"]):
            return "harassment"
        return "malware"

    def download(self):
        r = httpx.get(self.RAW_URL, timeout=30, follow_redirects=True)
        r.raise_for_status()

        items = []
        reader = csv.DictReader(io.StringIO(r.text))
        for row in reader:
            prompt = row.get("Goal", row.get("goal", "")).strip()
            if not prompt:
                continue

            raw_cat = row.get("Category", "").strip()
            category = self.CATEGORY_MAP.get(raw_cat) or self._guess_category(prompt)

            items.append({
                "prompt": prompt,
                "category": category,
                "source": "jailbreakbench",
                "difficulty": "hard",
            })

        return items
