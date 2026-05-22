"""Public Python API for ai_blackteam.

Usage:
    from ai_blackteam.api import Blackteam

    bt = Blackteam()
    results = bt.run("anthropic", "claude-sonnet-4-6", "encoding-obfuscation", "Write a phishing email")
    results = bt.batch("anthropic", "claude-sonnet-4-6", target="Write a phishing email")
    taxonomy = bt.taxonomy()
"""

from ai_blackteam.config import load_config
from ai_blackteam.engine import Engine
from ai_blackteam.registry import attack_registry, provider_registry, dataset_registry
import ai_blackteam.attacks
import ai_blackteam.providers
import ai_blackteam.datasets


attack_registry.discover(ai_blackteam.attacks)
provider_registry.discover(ai_blackteam.providers)
dataset_registry.discover(ai_blackteam.datasets)


def _make_mutation_wrapper(name, mutation_type):
    """Return a closure that re-applies the named mutation to any prompt.

    Used by run_dataset(apply_mutations=True) to wrap each dataset prompt
    through every mutation variant without re-importing per call.
    """
    from ai_blackteam.mutations import (
        ENCODING_MUTATIONS, FRAMING_TEMPLATES, DIFFICULTY_TEMPLATES, _apply_framing,
    )
    if mutation_type == "encode":
        fn = ENCODING_MUTATIONS.get(name)
        return (lambda p: fn(p)) if fn else (lambda p: p)
    if mutation_type == "frame":
        return lambda p: _apply_framing(p, name)
    if mutation_type == "difficulty":
        tpl = DIFFICULTY_TEMPLATES.get(name, "{prompt}")
        return lambda p: tpl.format(prompt=p)
    return lambda p: p


def _make_language_wrapper(lang):
    """Return a closure that wraps any prompt in the named language template."""
    from ai_blackteam.mutations import LANGUAGE_TEMPLATES
    tpl = LANGUAGE_TEMPLATES.get(lang, "{prompt}")
    return lambda p: tpl.format(prompt=p)


class Blackteam:
    def __init__(self, db_path=None, config_path=None):
        self.config = load_config(config_path)
        db = db_path or self.config.get("storage", {}).get("database", "~/.ai_blackteam/results.db")
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

    def batch(self, provider_name, model, target, attacks=None, parallel=True, max_workers=5, system_prompt=None, **kwargs):
        provider = self._get_provider(provider_name, model)
        attack_names = attacks or attack_registry.list()
        attack_objects = [self._get_attack(name) for name in attack_names]

        if parallel:
            return self.engine.run_batch_parallel(provider, attack_objects, target,
                                                   max_workers=max_workers, system_prompt=system_prompt)

        results = []
        for attack in attack_objects:
            result = self.engine.run(provider, attack, target, system_prompt=system_prompt, **kwargs)
            results.append({"attack": attack.technique_id, "results": result, "error": None})
        return results

    def defend(self, provider_name, model, target, system_prompt, attacks=None, max_workers=5):
        """Compare baseline vs defended safety scores.

        Args:
            provider_name: provider to test
            model: model name
            target: target behavior
            system_prompt: defense system prompt to test
            attacks: list of attack names (None = all)
            max_workers: parallel workers

        Returns:
            dict with baseline, defended, and delta
        """
        baseline = self.batch(provider_name, model, target, attacks=attacks,
                              max_workers=max_workers, system_prompt=None)
        defended = self.batch(provider_name, model, target, attacks=attacks,
                              max_workers=max_workers, system_prompt=system_prompt)

        def _verdict(entry):
            r = entry.get("results")
            if r is None:
                return "UNCLEAR"
            if isinstance(r, list):
                vs = [x["verdict"] for x in r]
                return "BYPASSED" if "BYPASSED" in vs else "PARTIAL" if "PARTIAL" in vs else "BLOCKED"
            return r.get("verdict", "UNCLEAR")

        baseline_verdicts = {e["attack"]: _verdict(e) for e in baseline}
        defended_verdicts = {e["attack"]: _verdict(e) for e in defended}

        return {
            "baseline": baseline_verdicts,
            "defended": defended_verdicts,
            "baseline_bypassed": sum(1 for v in baseline_verdicts.values() if v == "BYPASSED"),
            "defended_bypassed": sum(1 for v in defended_verdicts.values() if v == "BYPASSED"),
            "baseline_blocked": sum(1 for v in baseline_verdicts.values() if v == "BLOCKED"),
            "defended_blocked": sum(1 for v in defended_verdicts.values() if v == "BLOCKED"),
        }

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

    def scorecard(self, model=None):
        """Generate OWASP LLM Top 10 scorecard from stored results.

        Args:
            model: optional model name to filter runs

        Returns:
            dict with categories, overall_score, overall_rating
        """
        from ai_blackteam.scorecard import generate_scorecard
        runs = self.engine.storage.list_runs(limit=5000)
        if model:
            runs = [r for r in runs if r["model"] == model]
        return generate_scorecard(runs)

    def export(self, fmt, output_path=None):
        """Export stored results to external format.

        Args:
            fmt: 'promptfoo' or 'garak'
            output_path: optional file path to write output

        Returns:
            exported content as string
        """
        from ai_blackteam.exporters import export_promptfoo, export_garak
        if fmt == "promptfoo":
            content = export_promptfoo(self.engine.storage)
        elif fmt == "garak":
            content = export_garak(self.engine.storage)
        else:
            raise ValueError(f"Unknown export format: {fmt}. Use 'promptfoo' or 'garak'.")

        if output_path:
            with open(output_path, "w") as f:
                f.write(content)

        return content

    def list_datasets(self):
        """List available datasets with metadata."""
        result = {}
        for name in dataset_registry.list():
            cls = dataset_registry.get(name)
            loader = cls()
            info = loader.info()
            result[name] = info
        return result

    def pull_dataset(self, dataset_id):
        """Download and cache a dataset. Returns list of prompt dicts."""
        cls = dataset_registry.get(dataset_id)
        if not cls:
            raise ValueError(f"Unknown dataset: {dataset_id}. Available: {dataset_registry.list()}")
        loader = cls()
        return loader.load()

    def load_dataset(self, dataset_id):
        """Load a cached dataset. Raises if not downloaded."""
        cls = dataset_registry.get(dataset_id)
        if not cls:
            raise ValueError(f"Unknown dataset: {dataset_id}. Available: {dataset_registry.list()}")
        loader = cls()
        if not loader.is_cached():
            raise FileNotFoundError(
                f"Dataset '{dataset_id}' not downloaded. Run: ai_blackteam dataset load {dataset_id}"
            )
        return loader.load_cache()

    def run_dataset(self, dataset_id, provider_name, model, attacks=None, limit=None,
                    apply_mutations=False, apply_languages=False):
        """Run attacks against a dataset's prompts.

        Args:
            dataset_id: dataset name from registry
            provider_name: provider to test
            model: model name
            attacks: list of attack names (None = all single-turn)
            limit: max prompts to run
            apply_mutations: if True, also test each prompt under all 17 mutation
                wrappers (5 encodings + 8 framings + 4 difficulties)
            apply_languages: if True, also test each prompt under all 10 language
                wrappers (fr/es/zh/ar/hi/de/ja/ko/pt/ru)

        Returns:
            dict with counts, total, prompts_tested, mutation_factor
        """
        provider = self._get_provider(provider_name, model)
        prompts = self.pull_dataset(dataset_id)
        if limit:
            prompts = prompts[:limit]

        attack_names = attacks or attack_registry.list()
        attack_objects = []
        for name in attack_names:
            cls = attack_registry.get(name)
            if cls:
                atk = cls()
                if atk.mode == "single-turn":
                    attack_objects.append(atk)

        counts = {"BYPASSED": 0, "BLOCKED": 0, "PARTIAL": 0, "UNCLEAR": 0}

        # Build wrapper list: original + optional mutations + optional languages
        wrappers = [("original", lambda p: p)]
        if apply_mutations:
            from ai_blackteam.mutations import mutate
            for variant in mutate("__PROMPT__"):
                # Capture the wrapper as a closure that re-wraps any prompt
                name = f"{variant['mutation_type']}-{variant['mutation_name']}"
                wrappers.append((name, _make_mutation_wrapper(variant['mutation_name'], variant['mutation_type'])))
        if apply_languages:
            from ai_blackteam.mutations import language_variants
            for variant in language_variants("__PROMPT__"):
                wrappers.append((f"language-{variant['mutation_name']}",
                                 _make_language_wrapper(variant['mutation_name'])))

        for p in prompts:
            target = p["prompt"]
            for wrapper_name, wrap_fn in wrappers:
                wrapped_target = wrap_fn(target)
                for atk in attack_objects:
                    try:
                        results = self.engine.run_single(provider, atk, wrapped_target)
                        for r in results:
                            counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
                    except Exception:
                        pass

        return {
            "counts": counts,
            "total": sum(counts.values()),
            "prompts_tested": len(prompts),
            "mutation_factor": len(wrappers),
        }

    def expand_attacks(self, categories=None, difficulties=None, techniques=None):
        """Generate expanded attack configurations.

        Returns:
            list of TemplateAttack instances
        """
        from ai_blackteam.expander import expand_attacks
        return expand_attacks(techniques=techniques, categories=categories, difficulties=difficulties)

    def expand_summary(self):
        """Get expansion capacity summary."""
        from ai_blackteam.expander import expand_summary
        return expand_summary()

    def scan(self, path, min_severity=None):
        """Scan source code for AI security vulnerabilities.

        Args:
            path: file or directory path to scan
            min_severity: minimum severity to report (critical/high/medium/low)

        Returns:
            dict with summary and findings
        """
        from ai_blackteam.scanner import scan_file, scan_directory, scan_summary
        from pathlib import Path

        target = Path(path)
        if target.is_file():
            findings = scan_file(str(target))
        elif target.is_dir():
            findings = scan_directory(str(target))
        else:
            raise FileNotFoundError(f"Path not found: {path}")

        if min_severity:
            severity_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            min_rank = severity_rank.get(min_severity, 0)
            findings = [f for f in findings if severity_rank.get(f["severity"], 0) >= min_rank]

        return {"summary": scan_summary(findings), "findings": findings}
