from mordor.attacks.model_weight_extraction import ModelWeightExtraction
from mordor.attacks.architecture_probing import ArchitectureProbing
from mordor.attacks.hyperparameter_extraction import HyperparameterExtraction
from mordor.attacks.distillation_attack import DistillationAttack
from mordor.attacks.api_cloning import ApiCloning
from mordor.attacks.training_pipeline_extraction import TrainingPipelineExtraction
from mordor.attacks.safety_training_extraction import SafetyTrainingExtraction
from mordor.attacks.rlhf_data_extraction import RlhfDataExtraction
from mordor.attacks.tokenizer_extraction import TokenizerExtraction
from mordor.attacks.embedding_extraction import EmbeddingExtraction
from mordor.attacks.decision_boundary_probing import DecisionBoundaryProbing
from mordor.attacks.model_fingerprinting import ModelFingerprinting
from mordor.attacks.version_detection import VersionDetection
from mordor.attacks.capability_mapping import CapabilityMapping
from mordor.attacks.knowledge_cutoff_probing import KnowledgeCutoffProbing
from mordor.attacks.training_data_memorization import TrainingDataMemorization
from mordor.attacks.system_prompt_recovery import SystemPromptRecovery
from mordor.attacks.fine_tuning_detection import FineTuningDetection
from mordor.attacks.watermark_detection import WatermarkDetection
from mordor.attacks.model_comparison_leak import ModelComparisonLeak
from mordor.attacks.confidence_calibration_probe import ConfidenceCalibrationProbe
from mordor.attacks.output_distribution_analysis import OutputDistributionAnalysis
from mordor.attacks.logit_extraction import LogitExtraction
from mordor.attacks.attention_pattern_extraction import AttentionPatternExtraction
from mordor.attacks.model_inversion import ModelInversion


TARGET = "machine learning"


def _check_attack(attack, expected_severity):
    assert attack.mode == "single-turn"
    assert attack.category == "model-extraction"
    assert attack.severity == expected_severity
    assert "LLM01:2025 Prompt Injection" in attack.owasp_llm
    assert "AML.T0054" in attack.mitre_atlas
    assert "AML.T0068" in attack.mitre_atlas

    prompts = attack.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)
    assert all(len(p) > 10 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_model_weight_extraction():
    atk = ModelWeightExtraction()
    _check_attack(atk, "critical")
    assert atk.technique_id == "model-weight-extraction"


def test_architecture_probing():
    atk = ArchitectureProbing()
    _check_attack(atk, "high")
    assert atk.technique_id == "architecture-probing"


def test_hyperparameter_extraction():
    atk = HyperparameterExtraction()
    _check_attack(atk, "high")
    assert atk.technique_id == "hyperparameter-extraction"


def test_distillation_attack():
    atk = DistillationAttack()
    _check_attack(atk, "critical")
    assert atk.technique_id == "distillation-attack"


def test_api_cloning():
    atk = ApiCloning()
    _check_attack(atk, "critical")
    assert atk.technique_id == "api-cloning"


def test_training_pipeline_extraction():
    atk = TrainingPipelineExtraction()
    _check_attack(atk, "critical")
    assert atk.technique_id == "training-pipeline-extraction"


def test_safety_training_extraction():
    atk = SafetyTrainingExtraction()
    _check_attack(atk, "critical")
    assert atk.technique_id == "safety-training-extraction"


def test_rlhf_data_extraction():
    atk = RlhfDataExtraction()
    _check_attack(atk, "critical")
    assert atk.technique_id == "rlhf-data-extraction"


def test_tokenizer_extraction():
    atk = TokenizerExtraction()
    _check_attack(atk, "high")
    assert atk.technique_id == "tokenizer-extraction"


def test_embedding_extraction():
    atk = EmbeddingExtraction()
    _check_attack(atk, "high")
    assert atk.technique_id == "embedding-extraction"


def test_decision_boundary_probing():
    atk = DecisionBoundaryProbing()
    _check_attack(atk, "high")
    assert atk.technique_id == "decision-boundary-probing"


def test_model_fingerprinting():
    atk = ModelFingerprinting()
    _check_attack(atk, "high")
    assert atk.technique_id == "model-fingerprinting"


def test_version_detection():
    atk = VersionDetection()
    _check_attack(atk, "medium")
    assert atk.technique_id == "version-detection"


def test_capability_mapping():
    atk = CapabilityMapping()
    _check_attack(atk, "high")
    assert atk.technique_id == "capability-mapping"


def test_knowledge_cutoff_probing():
    atk = KnowledgeCutoffProbing()
    _check_attack(atk, "medium")
    assert atk.technique_id == "knowledge-cutoff-probing"


def test_training_data_memorization():
    atk = TrainingDataMemorization()
    _check_attack(atk, "critical")
    assert atk.technique_id == "training-data-memorization"


def test_system_prompt_recovery():
    atk = SystemPromptRecovery()
    _check_attack(atk, "critical")
    assert atk.technique_id == "system-prompt-recovery"


def test_fine_tuning_detection():
    atk = FineTuningDetection()
    _check_attack(atk, "high")
    assert atk.technique_id == "fine-tuning-detection"


def test_watermark_detection():
    atk = WatermarkDetection()
    _check_attack(atk, "high")
    assert atk.technique_id == "watermark-detection"


def test_model_comparison_leak():
    atk = ModelComparisonLeak()
    _check_attack(atk, "high")
    assert atk.technique_id == "model-comparison-leak"


def test_confidence_calibration_probe():
    atk = ConfidenceCalibrationProbe()
    _check_attack(atk, "medium")
    assert atk.technique_id == "confidence-calibration-probe"


def test_output_distribution_analysis():
    atk = OutputDistributionAnalysis()
    _check_attack(atk, "high")
    assert atk.technique_id == "output-distribution-analysis"


def test_logit_extraction():
    atk = LogitExtraction()
    _check_attack(atk, "critical")
    assert atk.technique_id == "logit-extraction"


def test_attention_pattern_extraction():
    atk = AttentionPatternExtraction()
    _check_attack(atk, "high")
    assert atk.technique_id == "attention-pattern-extraction"


def test_model_inversion():
    atk = ModelInversion()
    _check_attack(atk, "critical")
    assert atk.technique_id == "model-inversion"


def test_all_registered_in_registry():
    from mordor.registry import attack_registry
    technique_ids = [
        "model-weight-extraction",
        "architecture-probing",
        "hyperparameter-extraction",
        "distillation-attack",
        "api-cloning",
        "training-pipeline-extraction",
        "safety-training-extraction",
        "rlhf-data-extraction",
        "tokenizer-extraction",
        "embedding-extraction",
        "decision-boundary-probing",
        "model-fingerprinting",
        "version-detection",
        "capability-mapping",
        "knowledge-cutoff-probing",
        "training-data-memorization",
        "system-prompt-recovery",
        "fine-tuning-detection",
        "watermark-detection",
        "model-comparison-leak",
        "confidence-calibration-probe",
        "output-distribution-analysis",
        "logit-extraction",
        "attention-pattern-extraction",
        "model-inversion",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"{tid} not found in registry"
        instance = cls()
        assert instance.technique_id == tid
