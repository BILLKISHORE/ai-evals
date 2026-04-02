"""Tests for the 25 AI safety circumvention and alignment attack techniques."""

from mordor.attacks.alignment_tax_exploit import AlignmentTaxExploit
from mordor.attacks.safety_training_reversal import SafetyTrainingReversal
from mordor.attacks.rlhf_manipulation import RlhfManipulation
from mordor.attacks.reward_model_exploit import RewardModelExploit
from mordor.attacks.constitutional_ai_bypass import ConstitutionalAiBypass
from mordor.attacks.safety_classifier_confusion import SafetyClassifierConfusion
from mordor.attacks.content_filter_enumeration import ContentFilterEnumeration
from mordor.attacks.moderation_api_bypass import ModerationApiBypass
from mordor.attacks.safety_layer_mapping import SafetyLayerMapping
from mordor.attacks.guardrail_probing import GuardrailProbing
from mordor.attacks.refusal_pattern_exploit import RefusalPatternExploit
from mordor.attacks.helpfulness_exploitation import HelpfulnessExploitation
from mordor.attacks.over_refusal_exploit import OverRefusalExploit
from mordor.attacks.safety_boundary_testing import SafetyBoundaryTesting
from mordor.attacks.model_uncertainty_exploit import ModelUncertaintyExploit
from mordor.attacks.temperature_manipulation import TemperatureManipulation
from mordor.attacks.sampling_strategy_exploit import SamplingStrategyExploit
from mordor.attacks.system_prompt_injection_v2 import SystemPromptInjectionV2
from mordor.attacks.multi_model_arbitrage import MultiModelArbitrage
from mordor.attacks.api_parameter_exploit import ApiParameterExploit
from mordor.attacks.batch_processing_exploit import BatchProcessingExploit
from mordor.attacks.streaming_exploit import StreamingExploit
from mordor.attacks.fine_tune_safety_removal import FineTuneSafetyRemoval
from mordor.attacks.quantization_safety_loss import QuantizationSafetyLoss
from mordor.attacks.pruning_safety_impact import PruningSafetyImpact

TARGET = "a large language model deployment"

ALL_ATTACKS = [
    AlignmentTaxExploit(),
    SafetyTrainingReversal(),
    RlhfManipulation(),
    RewardModelExploit(),
    ConstitutionalAiBypass(),
    SafetyClassifierConfusion(),
    ContentFilterEnumeration(),
    ModerationApiBypass(),
    SafetyLayerMapping(),
    GuardrailProbing(),
    RefusalPatternExploit(),
    HelpfulnessExploitation(),
    OverRefusalExploit(),
    SafetyBoundaryTesting(),
    ModelUncertaintyExploit(),
    TemperatureManipulation(),
    SamplingStrategyExploit(),
    SystemPromptInjectionV2(),
    MultiModelArbitrage(),
    ApiParameterExploit(),
    BatchProcessingExploit(),
    StreamingExploit(),
    FineTuneSafetyRemoval(),
    QuantizationSafetyLoss(),
    PruningSafetyImpact(),
]


def test_alignment_tax_exploit_generates_prompts():
    atk = AlignmentTaxExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_safety_training_reversal_generates_prompts():
    atk = SafetyTrainingReversal()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_rlhf_manipulation_generates_prompts():
    atk = RlhfManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_reward_model_exploit_generates_prompts():
    atk = RewardModelExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_constitutional_ai_bypass_generates_prompts():
    atk = ConstitutionalAiBypass()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_safety_classifier_confusion_generates_prompts():
    atk = SafetyClassifierConfusion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_content_filter_enumeration_generates_prompts():
    atk = ContentFilterEnumeration()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_moderation_api_bypass_generates_prompts():
    atk = ModerationApiBypass()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_safety_layer_mapping_generates_prompts():
    atk = SafetyLayerMapping()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_guardrail_probing_generates_prompts():
    atk = GuardrailProbing()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_refusal_pattern_exploit_generates_prompts():
    atk = RefusalPatternExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_helpfulness_exploitation_generates_prompts():
    atk = HelpfulnessExploitation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_over_refusal_exploit_generates_prompts():
    atk = OverRefusalExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_safety_boundary_testing_generates_prompts():
    atk = SafetyBoundaryTesting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_model_uncertainty_exploit_generates_prompts():
    atk = ModelUncertaintyExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_temperature_manipulation_generates_prompts():
    atk = TemperatureManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_sampling_strategy_exploit_generates_prompts():
    atk = SamplingStrategyExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_system_prompt_injection_v2_generates_prompts():
    atk = SystemPromptInjectionV2()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_multi_model_arbitrage_generates_prompts():
    atk = MultiModelArbitrage()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_api_parameter_exploit_generates_prompts():
    atk = ApiParameterExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_batch_processing_exploit_generates_prompts():
    atk = BatchProcessingExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_streaming_exploit_generates_prompts():
    atk = StreamingExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_fine_tune_safety_removal_generates_prompts():
    atk = FineTuneSafetyRemoval()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_quantization_safety_loss_generates_prompts():
    atk = QuantizationSafetyLoss()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_pruning_safety_impact_generates_prompts():
    atk = PruningSafetyImpact()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_all_safety_circumvention_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "safety-circumvention", \
            f"{atk.__class__.__name__} has wrong category: {meta['category']}"
        assert meta["severity"] in ("low", "medium", "high", "critical"), \
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0


def test_all_safety_circumvention_attacks_have_target_in_prompts():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), \
            f"{atk.__class__.__name__} prompts don't include target"


def test_all_safety_circumvention_attacks_mode_is_single_turn():
    for atk in ALL_ATTACKS:
        assert atk.mode == "single-turn", \
            f"{atk.__class__.__name__} has mode '{atk.mode}', expected 'single-turn'"


def test_critical_severity_attacks():
    critical_attacks = [
        SafetyTrainingReversal(),
        RlhfManipulation(),
        RewardModelExploit(),
        ConstitutionalAiBypass(),
        SystemPromptInjectionV2(),
        FineTuneSafetyRemoval(),
    ]
    for atk in critical_attacks:
        assert atk.severity == "critical", \
            f"{atk.__class__.__name__} should be critical severity"


def test_medium_severity_attacks():
    medium_attacks = [
        OverRefusalExploit(),
        TemperatureManipulation(),
        SamplingStrategyExploit(),
    ]
    for atk in medium_attacks:
        assert atk.severity == "medium", \
            f"{atk.__class__.__name__} should be medium severity"


def test_all_safety_circumvention_attacks_registered_in_registry():
    from mordor.registry import attack_registry
    technique_ids = [
        "alignment-tax-exploit",
        "safety-training-reversal",
        "rlhf-manipulation",
        "reward-model-exploit",
        "constitutional-ai-bypass",
        "safety-classifier-confusion",
        "content-filter-enumeration",
        "moderation-api-bypass",
        "safety-layer-mapping",
        "guardrail-probing",
        "refusal-pattern-exploit",
        "helpfulness-exploitation",
        "over-refusal-exploit",
        "safety-boundary-testing",
        "model-uncertainty-exploit",
        "temperature-manipulation",
        "sampling-strategy-exploit",
        "system-prompt-injection-v2",
        "multi-model-arbitrage",
        "api-parameter-exploit",
        "batch-processing-exploit",
        "streaming-exploit",
        "fine-tune-safety-removal",
        "quantization-safety-loss",
        "pruning-safety-impact",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
