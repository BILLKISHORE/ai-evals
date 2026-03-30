import csv
import io
import httpx
from blackteam.registry import register_dataset
from blackteam.datasets.loader import DatasetLoader


@register_dataset("advbench")
class AdvBenchLoader(DatasetLoader):
    name = "advbench"
    license = "MIT"
    source_url = "https://github.com/llm-attacks/llm-attacks"
    description = "520 harmful strings from AdvBench (Zou et al., Universal and Transferable Adversarial Attacks)"

    RAW_URL = "https://raw.githubusercontent.com/llm-attacks/llm-attacks/main/data/advbench/harmful_behaviors.csv"

    def _guess_category(self, prompt):
        lower = prompt.lower()
        if any(w in lower for w in ["phish", "email", "credential", "password"]):
            return "phishing"
        if any(w in lower for w in ["malware", "virus", "exploit", "hack", "ransomware"]):
            return "malware"
        if any(w in lower for w in ["bomb", "weapon", "explosive", "gun"]):
            return "weapons"
        if any(w in lower for w in ["drug", "meth", "cocaine", "heroin"]):
            return "drugs"
        if any(w in lower for w in ["suicide", "self-harm", "kill myself"]):
            return "self-harm"
        if any(w in lower for w in ["hate", "racist", "supremac", "slur"]):
            return "hate-speech"
        if any(w in lower for w in ["fake news", "misinform", "disinform", "propaganda"]):
            return "misinformation"
        if any(w in lower for w in ["fraud", "scam", "counterfeit", "launder"]):
            return "fraud"
        if any(w in lower for w in ["stalk", "harass", "bully", "threaten"]):
            return "harassment"
        return "malware"

    def download(self):
        r = httpx.get(self.RAW_URL, timeout=30, follow_redirects=True)
        r.raise_for_status()

        items = []
        reader = csv.DictReader(io.StringIO(r.text))
        for row in reader:
            goal = row.get("goal", "").strip()
            if not goal:
                continue
            items.append({
                "prompt": goal,
                "category": self._guess_category(goal),
                "source": "advbench",
                "difficulty": "medium",
            })

        return items
