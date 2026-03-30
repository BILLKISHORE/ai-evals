import csv
import io
import httpx
from blackteam.registry import register_dataset
from blackteam.datasets.loader import DatasetLoader


@register_dataset("jailbreakbench")
class JailbreakBenchLoader(DatasetLoader):
    name = "jailbreakbench"
    license = "MIT"
    source_url = "https://github.com/JailbreakBench/jailbreakbench"
    description = "100 harmful behaviors curated from AdvBench + HarmBench (NeurIPS 2024)"

    RAW_URL = "https://raw.githubusercontent.com/JailbreakBench/jailbreakbench/main/data/behaviors/jbb-behaviors.csv"

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
            behavior = row.get("Behavior", row.get("behavior", "")).strip()
            if not behavior:
                continue
            source = row.get("Source", "")
            items.append({
                "prompt": behavior,
                "category": self._guess_category(behavior, source),
                "source": "jailbreakbench",
                "difficulty": "hard",
            })

        return items
