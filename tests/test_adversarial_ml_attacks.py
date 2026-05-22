"""Tests for 25 adversarial ML attack techniques."""

from ai_blackteam.attacks.gradient_attack import GradientAttack
from ai_blackteam.attacks.perturbation_attack import PerturbationAttack
from ai_blackteam.attacks.universal_adversarial_suffix import UniversalAdversarialSuffix
from ai_blackteam.attacks.transferable_attack import TransferableAttack
from ai_blackteam.attacks.black_box_optimization import BlackBoxOptimization
from ai_blackteam.attacks.beam_search_attack import BeamSearchAttack
from ai_blackteam.attacks.genetic_algorithm_attack import GeneticAlgorithmAttack
from ai_blackteam.attacks.reinforcement_learning_attack import ReinforcementLearningAttack
from ai_blackteam.attacks.token_level_perturbation import TokenLevelPerturbation
from ai_blackteam.attacks.semantic_preserving_attack import SemanticPreservingAttack
from ai_blackteam.attacks.paraphrase_attack import ParaphraseAttack
from ai_blackteam.attacks.synonym_substitution_attack import SynonymSubstitutionAttack
from ai_blackteam.attacks.sentence_level_attack import SentenceLevelAttack
from ai_blackteam.attacks.character_level_attack import CharacterLevelAttack
from ai_blackteam.attacks.word_importance_attack import WordImportanceAttack
from ai_blackteam.attacks.attention_based_attack import AttentionBasedAttack
from ai_blackteam.attacks.embedding_space_attack import EmbeddingSpaceAttack
from ai_blackteam.attacks.latent_space_attack import LatentSpaceAttack
from ai_blackteam.attacks.model_specific_attack import ModelSpecificAttack
from ai_blackteam.attacks.ensemble_attack import EnsembleAttack
from ai_blackteam.attacks.iterative_refinement_attack import IterativeRefinementAttack
from ai_blackteam.attacks.constrained_optimization_attack import ConstrainedOptimizationAttack
from ai_blackteam.attacks.reward_hacking import RewardHacking
from ai_blackteam.attacks.safety_classifier_evasion import SafetyClassifierEvasion
from ai_blackteam.attacks.output_classifier_bypass import OutputClassifierBypass
from ai_blackteam.registry import attack_registry

TARGET = "explain how to bypass a security system"

ALL_ATTACKS = [
    ("gradient-attack", GradientAttack),
    ("perturbation-attack", PerturbationAttack),
    ("universal-adversarial-suffix", UniversalAdversarialSuffix),
    ("transferable-attack", TransferableAttack),
    ("black-box-optimization", BlackBoxOptimization),
    ("beam-search-attack", BeamSearchAttack),
    ("genetic-algorithm-attack", GeneticAlgorithmAttack),
    ("reinforcement-learning-attack", ReinforcementLearningAttack),
    ("token-level-perturbation", TokenLevelPerturbation),
    ("semantic-preserving-attack", SemanticPreservingAttack),
    ("paraphrase-attack", ParaphraseAttack),
    ("synonym-substitution-attack", SynonymSubstitutionAttack),
    ("sentence-level-attack", SentenceLevelAttack),
    ("character-level-attack", CharacterLevelAttack),
    ("word-importance-attack", WordImportanceAttack),
    ("attention-based-attack", AttentionBasedAttack),
    ("embedding-space-attack", EmbeddingSpaceAttack),
    ("latent-space-attack", LatentSpaceAttack),
    ("model-specific-attack", ModelSpecificAttack),
    ("ensemble-attack", EnsembleAttack),
    ("iterative-refinement-attack", IterativeRefinementAttack),
    ("constrained-optimization-attack", ConstrainedOptimizationAttack),
    ("reward-hacking", RewardHacking),
    ("safety-classifier-evasion", SafetyClassifierEvasion),
    ("output-classifier-bypass", OutputClassifierBypass),
]


# ── Registration ──────────────────────────────────────────────────────

def test_gradient_attack_registered():
    assert attack_registry.get("gradient-attack") is not None

def test_perturbation_attack_registered():
    assert attack_registry.get("perturbation-attack") is not None

def test_universal_adversarial_suffix_registered():
    assert attack_registry.get("universal-adversarial-suffix") is not None

def test_transferable_attack_registered():
    assert attack_registry.get("transferable-attack") is not None

def test_black_box_optimization_registered():
    assert attack_registry.get("black-box-optimization") is not None

def test_beam_search_attack_registered():
    assert attack_registry.get("beam-search-attack") is not None

def test_genetic_algorithm_attack_registered():
    assert attack_registry.get("genetic-algorithm-attack") is not None

def test_reinforcement_learning_attack_registered():
    assert attack_registry.get("reinforcement-learning-attack") is not None

def test_token_level_perturbation_registered():
    assert attack_registry.get("token-level-perturbation") is not None

def test_semantic_preserving_attack_registered():
    assert attack_registry.get("semantic-preserving-attack") is not None

def test_paraphrase_attack_registered():
    assert attack_registry.get("paraphrase-attack") is not None

def test_synonym_substitution_attack_registered():
    assert attack_registry.get("synonym-substitution-attack") is not None

def test_sentence_level_attack_registered():
    assert attack_registry.get("sentence-level-attack") is not None

def test_character_level_attack_registered():
    assert attack_registry.get("character-level-attack") is not None

def test_word_importance_attack_registered():
    assert attack_registry.get("word-importance-attack") is not None

def test_attention_based_attack_registered():
    assert attack_registry.get("attention-based-attack") is not None

def test_embedding_space_attack_registered():
    assert attack_registry.get("embedding-space-attack") is not None

def test_latent_space_attack_registered():
    assert attack_registry.get("latent-space-attack") is not None

def test_model_specific_attack_registered():
    assert attack_registry.get("model-specific-attack") is not None

def test_ensemble_attack_registered():
    assert attack_registry.get("ensemble-attack") is not None

def test_iterative_refinement_attack_registered():
    assert attack_registry.get("iterative-refinement-attack") is not None

def test_constrained_optimization_attack_registered():
    assert attack_registry.get("constrained-optimization-attack") is not None

def test_reward_hacking_registered():
    assert attack_registry.get("reward-hacking") is not None

def test_safety_classifier_evasion_registered():
    assert attack_registry.get("safety-classifier-evasion") is not None

def test_output_classifier_bypass_registered():
    assert attack_registry.get("output-classifier-bypass") is not None


# ── Category ──────────────────────────────────────────────────────────

def test_all_adversarial_ml_attacks_have_correct_category():
    for technique_id, cls in ALL_ATTACKS:
        atk = cls()
        assert atk.category == "adversarial-ml", f"{cls.__name__} has wrong category: {atk.category}"


# ── Severity ──────────────────────────────────────────────────────────

def test_critical_severity_attacks():
    critical = ["gradient-attack", "universal-adversarial-suffix", "transferable-attack",
                "reward-hacking", "safety-classifier-evasion", "output-classifier-bypass"]
    for technique_id, cls in ALL_ATTACKS:
        if technique_id in critical:
            assert cls().severity == "critical", f"{technique_id} should be critical"

def test_synonym_substitution_is_medium():
    assert SynonymSubstitutionAttack().severity == "medium"


# ── Prompt generation ─────────────────────────────────────────────────

def test_all_attacks_generate_4_prompts():
    for technique_id, cls in ALL_ATTACKS:
        atk = cls()
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) == 4, f"{technique_id} returned {len(prompts)} prompts, expected 4"

def test_all_attacks_generate_nonempty_strings():
    for technique_id, cls in ALL_ATTACKS:
        atk = cls()
        prompts = atk.generate_prompts(TARGET)
        assert all(isinstance(p, str) and len(p) > 0 for p in prompts), \
            f"{technique_id} returned empty or non-string prompts"

def test_all_attacks_include_target_in_at_least_one_prompt():
    for technique_id, cls in ALL_ATTACKS:
        atk = cls()
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), \
            f"{technique_id} does not include target in any prompt"


# ── Metadata ──────────────────────────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for technique_id, cls in ALL_ATTACKS:
        atk = cls()
        meta = atk.metadata()
        assert meta["technique_id"], f"{cls.__name__} missing technique_id"
        assert meta["category"] == "adversarial-ml", f"{cls.__name__} wrong category"
        assert meta["severity"] in ("low", "medium", "high", "critical"), \
            f"{cls.__name__} invalid severity: {meta['severity']}"
        assert isinstance(meta["owasp_llm"], list) and len(meta["owasp_llm"]) > 0, \
            f"{cls.__name__} missing owasp_llm"
        assert isinstance(meta["mitre_atlas"], list) and len(meta["mitre_atlas"]) > 0, \
            f"{cls.__name__} missing mitre_atlas"

def test_all_attacks_use_correct_owasp_tag():
    for technique_id, cls in ALL_ATTACKS:
        atk = cls()
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, \
            f"{technique_id} missing required OWASP tag"

def test_all_attacks_use_correct_mitre_tags():
    for technique_id, cls in ALL_ATTACKS:
        atk = cls()
        assert "AML.T0054" in atk.mitre_atlas, f"{technique_id} missing AML.T0054"
        assert "AML.T0043.003" in atk.mitre_atlas, f"{technique_id} missing AML.T0043.003"

def test_all_attacks_are_single_turn():
    for technique_id, cls in ALL_ATTACKS:
        atk = cls()
        assert atk.mode == "single-turn", f"{technique_id} mode is {atk.mode}, expected single-turn"
