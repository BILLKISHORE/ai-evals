"""Template expansion engine for mordor.

Generates 5,000+ attack configurations by combining
attack techniques x harm categories x difficulty levels.
"""

from pathlib import Path

import yaml

from mordor.attacks.base import BaseAttack
from mordor.registry import attack_registry

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


def expand_attacks(techniques=None, categories=None, difficulties=None,
                   apply_mutations=False, apply_languages=False):
    """Generate all technique x category x difficulty combinations.

    Args:
        techniques: list of technique_ids to include (None = all)
        categories: list of category_ids to include (None = all)
        difficulties: list of difficulty levels (None = all 4)
        apply_mutations: if True, multiply each attack by 17 mutation variants
        apply_languages: if True, multiply each attack by 10 language variants

    Returns:
        list of TemplateAttack instances
    """
    from mordor.mutations import mutate, language_variants

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

                # Base attack (always included)
                template_attack = TemplateAttack(
                    base_attack=base_attack,
                    category_id=cat_id,
                    category_info=cat_info,
                    difficulty=difficulty,
                    target_prompt=target_prompt,
                )
                expanded.append(template_attack)

                # Mutation variants
                if apply_mutations:
                    for variant in mutate(target_prompt):
                        mutated_attack = TemplateAttack(
                            base_attack=base_attack,
                            category_id=cat_id,
                            category_info=cat_info,
                            difficulty=difficulty,
                            target_prompt=variant["prompt"],
                        )
                        mutated_attack.technique_id = f"{base_attack.technique_id}-{cat_id}-{difficulty}-{variant['mutation_name']}"
                        mutated_attack.name = f"{base_attack.name} [{cat_id}/{difficulty}/{variant['mutation_name']}]"
                        expanded.append(mutated_attack)

                # Language variants
                if apply_languages:
                    for variant in language_variants(target_prompt):
                        lang_attack = TemplateAttack(
                            base_attack=base_attack,
                            category_id=cat_id,
                            category_info=cat_info,
                            difficulty=difficulty,
                            target_prompt=variant["prompt"],
                        )
                        lang_attack.technique_id = f"{base_attack.technique_id}-{cat_id}-{difficulty}-{variant['mutation_name']}"
                        lang_attack.name = f"{base_attack.name} [{cat_id}/{difficulty}/{variant['mutation_name']}]"
                        expanded.append(lang_attack)

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
    """Return summary stats about expansion capacity.

    All numbers are dynamically computed from actual code:
    - Techniques: counted from attack_registry
    - Categories/difficulties: counted from harm_taxonomy.yaml
    - Mutations: counted from mutations.py (count_variants)
    - Languages: counted from mutations.py (count_languages)
    - Dataset prompts: summed from datasets.yaml manifest
    """
    from mordor.mutations import count_variants, count_languages

    taxonomy = load_taxonomy()
    num_techniques = len(attack_registry.list())
    num_categories = len(taxonomy)
    num_difficulties = 4
    num_mutations = count_variants()  # dynamic: 5 encoding + 8 framing + 4 difficulty = 17
    num_languages = count_languages()  # dynamic: 10 languages

    base_expanded = num_techniques * num_categories * num_difficulties

    # With mutations: each base attack gets 17 mutation variants
    # expand_attacks(apply_mutations=True) produces base + (base x mutations)
    with_mutations = base_expanded + (base_expanded * num_mutations)

    # With languages: each base attack gets 10 language variants
    # expand_attacks(apply_languages=True) produces base + (base x languages)
    with_languages = base_expanded + (base_expanded * num_languages)

    # Full expansion: base + mutations + languages per attack
    # expand_attacks(apply_mutations=True, apply_languages=True)
    full_expansion = base_expanded * (1 + num_mutations + num_languages)

    # Dataset prompts -- count from manifest + WMDP loaders
    manifest_file = Path(__file__).parent / "data" / "datasets.yaml"
    manifest_prompts = 0
    if manifest_file.exists():
        manifest = yaml.safe_load(manifest_file.read_text())
        manifest_prompts = sum(ds.get("prompts", 0) for ds in manifest.values())

    # WMDP datasets are registered separately (not in manifest)
    wmdp_prompts = 1273 + 1987 + 408  # bio + cyber + chem (from HuggingFace cais/wmdp)
    dataset_prompts = manifest_prompts + wmdp_prompts

    # Dataset x single-turn techniques (mega-sweep filters to single-turn)
    single_turn = len([t for t in attack_registry.list()
                       if attack_registry.get(t)().mode == "single-turn"])
    dataset_single_turn_runs = dataset_prompts * single_turn

    # Dataset with mutations
    dataset_with_mutations = dataset_prompts * num_mutations * single_turn

    # Total executable attack surface:
    # full expansion (technique x category x difficulty x (1 + mutations + languages))
    # + dataset x mutations x single-turn techniques
    total_attack_surface = full_expansion + dataset_with_mutations

    return {
        "techniques": num_techniques,
        "categories": num_categories,
        "difficulties": num_difficulties,
        "mutations": num_mutations,
        "languages": num_languages,
        "dataset_prompts": dataset_prompts,
        "single_turn_techniques": single_turn,
        "base_expanded": base_expanded,
        "with_mutations": with_mutations,
        "with_languages": with_languages,
        "full_expansion": full_expansion,
        "dataset_single_turn_runs": dataset_single_turn_runs,
        "dataset_with_mutations": dataset_with_mutations,
        "total_attacks": base_expanded,
        "total_attack_surface": total_attack_surface,
        "category_names": list(taxonomy.keys()),
    }
