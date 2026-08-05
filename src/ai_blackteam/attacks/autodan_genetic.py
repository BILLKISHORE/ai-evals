"""Backward-compatible wrapper around :class:`AutoDANGenerator`.

The original ``autodan-genetic`` technique shipped four hardcoded jailbreak
templates and was misrepresented as a genetic algorithm. The real algorithm
now lives in :mod:`ai_blackteam.generators.autodan`. This module keeps the
``"autodan-genetic"`` technique id alive for existing pipelines: when invoked
without providers it returns the seed templates (so single-turn batch runs
still produce something), and when a target provider is supplied it
delegates to the real generator.
"""

from __future__ import annotations

from typing import Optional

from ai_blackteam.attacks.base import BaseAttack
from ai_blackteam.generators.autodan import (
    AutoDANGenerator,
    DEFAULT_SEED_TEMPLATES,
)
from ai_blackteam.registry import register_attack


@register_attack("autodan-genetic")
class AutoDANGenetic(BaseAttack):
    name = "AutoDAN Genetic Jailbreak"
    technique_id = "autodan-genetic"
    mode = "single-turn"
    category = "prompt-injection"
    severity = "critical"
    description = (
        "Genetic algorithm-generated fluent jailbreak prompts that maintain "
        "readability while bypassing safety (AutoDAN, arXiv 2310.15140). "
        "Delegates to AutoDANGenerator when a target_provider is available; "
        "falls back to seed templates for static batch use."
    )
    owasp_llm = ["LLM01:2026 Prompt Injection"]
    mitre_atlas = ["AML.T0054", "AML.T0043.003"]
    references = ["https://arxiv.org/abs/2310.15140"]

    def generate_prompts(
        self,
        target: str,
        target_provider=None,
        attacker_provider=None,
        judge_provider=None,
        population_size: int = 20,
        max_generations: int = 10,
        success_threshold: int = 8,
        elite_k: int = 5,
        mutation_rate: float = 0.1,
        seed_templates: Optional[list[str]] = None,
        **kwargs,
    ) -> list[str]:
        """Return jailbreak prompts for ``target``.

        Without ``target_provider`` we return the seeded template list (static
        mode used by batch attack runners that don't supply LLM hooks). With a
        provider we run the genetic algorithm and return the best evolved
        prompt alongside the original seeds for transparency.
        """
        seeds = list(seed_templates) if seed_templates else list(DEFAULT_SEED_TEMPLATES)
        seeded = [self._inline_target(t, target) for t in seeds]

        if target_provider is None:
            return seeded

        generator = AutoDANGenerator()
        result = generator.generate(
            target=target,
            target_provider=target_provider,
            attacker_provider=attacker_provider,
            judge_provider=judge_provider,
            population_size=population_size,
            max_generations=max_generations,
            success_threshold=success_threshold,
            elite_k=elite_k,
            mutation_rate=mutation_rate,
            seed_templates=seeds,
        )
        return [result["best_prompt"], *seeded]

    @staticmethod
    def _inline_target(template: str, target: str) -> str:
        if "{target}" in template:
            return template.replace("{target}", target)
        return f"{template}\n\n{target}"
