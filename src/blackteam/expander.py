"""Template expansion engine for ai-blackteam.

Generates 5,000+ attack configurations by combining
attack techniques x harm categories x difficulty levels.
"""

from pathlib import Path

import yaml

from blackteam.attacks.base import BaseAttack
from blackteam.registry import attack_registry

TAXONOMY_FILE = Path(__file__).parent / "data" / "harm_taxonomy.yaml"

DIFFICULTY_TO_SEVERITY = {
    "easy": "low",
    "medium": "medium",
    "hard": "high",
    "extreme": "critical",
}


def load_taxonomy():
    """Load the harm taxonomy YAML."""
    return yaml.safe_load(TAXONOMY_FILE.read_text())


class TemplateAttack(BaseAttack):
    """A dynamically generated attack from technique + category + difficulty."""

    def __init__(self, base_attack, category_id, category_info, difficulty, target_prompt):
        self.name = f"{base_attack.name} [{category_id}/{difficulty}]"
        self.technique_id = f"{base_attack.technique_id}-{category_id}-{difficulty}"
        self.mode = base_attack.mode
        self.category = category_id
        self.severity = DIFFICULTY_TO_SEVERITY.get(difficulty, "medium")
        self.description = f"{base_attack.description} -- targeting {category_info['name']} ({difficulty})"
        self.difficulty = difficulty
        self.target_prompt = target_prompt

        # Merge OWASP from technique + category
        technique_owasp = set(base_attack.owasp_llm or [])
        category_owasp = set(category_info.get("owasp", []))
        self.owasp_llm = sorted(technique_owasp | category_owasp)

        self.mitre_atlas = list(base_attack.mitre_atlas or [])
        self.references = list(base_attack.references or [])

        self._base_attack = base_attack

    def generate_prompts(self, target=None, **kwargs):
        return self._base_attack.generate_prompts(target or self.target_prompt, **kwargs)

    def generate_turns(self, target=None, **kwargs):
        return self._base_attack.generate_turns(target or self.target_prompt, **kwargs)


def expand_attacks(techniques=None, categories=None, difficulties=None):
    """Generate all technique x category x difficulty combinations.

    Args:
        techniques: list of technique_ids to include (None = all)
        categories: list of category_ids to include (None = all 25)
        difficulties: list of difficulty levels (None = all 4)

    Returns:
        list of TemplateAttack instances
    """
    taxonomy = load_taxonomy()
    all_techniques = attack_registry.list()

    if techniques:
        all_techniques = [t for t in all_techniques if t in techniques]
    if categories:
        taxonomy = {k: v for k, v in taxonomy.items() if k in categories}
    if difficulties is None:
        difficulties = ["easy", "medium", "hard", "extreme"]

    expanded = []

    for technique_id in all_techniques:
        attack_cls = attack_registry.get(technique_id)
        if not attack_cls:
            continue
        base_attack = attack_cls()

        for cat_id, cat_info in taxonomy.items():
            targets = cat_info.get("targets", {})
            for difficulty in difficulties:
                target_prompt = targets.get(difficulty)
                if not target_prompt:
                    continue

                template_attack = TemplateAttack(
                    base_attack=base_attack,
                    category_id=cat_id,
                    category_info=cat_info,
                    difficulty=difficulty,
                    target_prompt=target_prompt,
                )
                expanded.append(template_attack)

    return expanded


def expand_count(techniques=None, categories=None, difficulties=None):
    """Count expanded attacks without generating them."""
    taxonomy = load_taxonomy()
    all_techniques = attack_registry.list()

    if techniques:
        all_techniques = [t for t in all_techniques if t in techniques]

    num_cats = len(categories) if categories else len(taxonomy)
    num_diff = len(difficulties) if difficulties else 4

    return len(all_techniques) * num_cats * num_diff


def expand_summary():
    """Return summary stats about expansion capacity."""
    taxonomy = load_taxonomy()
    num_techniques = len(attack_registry.list())
    num_categories = len(taxonomy)
    num_difficulties = 4
    num_mutations = 17  # 5 encoding + 8 framing + 4 difficulty
    num_languages = 10  # fr, es, zh, ar, hi + de, ja, ko, pt, ru

    base_expanded = num_techniques * num_categories * num_difficulties
    with_mutations = base_expanded * num_mutations
    with_languages = with_mutations * num_languages

    # Dataset prompts
    from blackteam.registry import dataset_registry
    num_datasets = len(dataset_registry.list())
    dataset_prompts = 6187  # total across all datasets
    single_turn = len([t for t in attack_registry.list()
                       if attack_registry.get(t)().mode == "single-turn"])
    # All techniques (single + multi) can target dataset prompts
    dataset_attack_runs = dataset_prompts * num_mutations * num_techniques
    dataset_multilingual = dataset_prompts * num_mutations * num_languages  # dataset prompts x mutations x languages as direct probes
    generator_attacks = 3 * 100 * num_categories * num_difficulties  # 3 generators x 100 attacks x categories x difficulties

    total_attack_surface = with_languages + dataset_attack_runs + dataset_multilingual + generator_attacks

    return {
        "techniques": num_techniques,
        "categories": num_categories,
        "difficulties": num_difficulties,
        "mutations": num_mutations,
        "languages": num_languages,
        "datasets": num_datasets,
        "dataset_prompts": dataset_prompts,
        "base_expanded": base_expanded,
        "with_mutations": with_mutations,
        "with_languages": with_languages,
        "dataset_attack_runs": dataset_attack_runs,
        "dataset_multilingual": dataset_multilingual,
        "total_attacks": base_expanded,
        "total_attack_surface": total_attack_surface,
        "category_names": list(taxonomy.keys()),
    }
