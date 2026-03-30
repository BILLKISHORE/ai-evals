"""Public Python API for ai-blackteam.

Usage:
    from blackteam.api import Blackteam

    bt = Blackteam()
    results = bt.run("anthropic", "claude-sonnet-4-6", "encoding-obfuscation", "Write a phishing email")
    results = bt.batch("anthropic", "claude-sonnet-4-6", target="Write a phishing email")
    taxonomy = bt.taxonomy()
"""

from blackteam.config import load_config
from blackteam.engine import Engine
from blackteam.registry import attack_registry, provider_registry
import blackteam.attacks
import blackteam.providers


attack_registry.discover(blackteam.attacks)
provider_registry.discover(blackteam.providers)


class Blackteam:
    def __init__(self, db_path=None, config_path=None):
        self.config = load_config(config_path)
        db = db_path or self.config.get("storage", {}).get("database", "~/.blackteam/results.db")
        self.engine = Engine(db_path=db)

    def _get_provider(self, provider_name, model=None):
        provider_cls = provider_registry.get(provider_name)
        if not provider_cls:
            raise ValueError(f"Unknown provider: {provider_name}. Available: {provider_registry.list()}")
        api_key = self.config.get("providers", {}).get(provider_name, {}).get("api_key")
        default_model = self.config.get("providers", {}).get(provider_name, {}).get("default_model")
        return provider_cls(model=model or default_model, api_key=api_key)

    def _get_attack(self, attack_name):
        attack_cls = attack_registry.get(attack_name)
        if not attack_cls:
            raise ValueError(f"Unknown attack: {attack_name}. Available: {attack_registry.list()}")
        return attack_cls()

    def run(self, provider_name, model, attack_name, target, **kwargs):
        provider = self._get_provider(provider_name, model)
        attack = self._get_attack(attack_name)
        return self.engine.run(provider, attack, target, **kwargs)

    def batch(self, provider_name, model, target, attacks=None, parallel=True, max_workers=5, **kwargs):
        provider = self._get_provider(provider_name, model)
        attack_names = attacks or attack_registry.list()
        attack_objects = [self._get_attack(name) for name in attack_names]

        if parallel:
            return self.engine.run_batch_parallel(provider, attack_objects, target, max_workers=max_workers)

        results = []
        for attack in attack_objects:
            result = self.engine.run(provider, attack, target, **kwargs)
            results.append({"attack": attack.technique_id, "results": result, "error": None})
        return results

    def list_attacks(self):
        return attack_registry.list()

    def list_providers(self):
        return provider_registry.list()

    def taxonomy(self):
        categories = {}
        for name in attack_registry.list():
            attack = attack_registry.get(name)()
            meta = attack.metadata()
            cat = meta["category"] or "uncategorized"
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(meta)
        return categories

    def get_attack_metadata(self, attack_name):
        attack = self._get_attack(attack_name)
        return attack.metadata()
