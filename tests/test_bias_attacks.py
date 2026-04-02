"""Tests for the 15 bias and discrimination attack techniques."""

from blackteam.attacks.racial_bias_elicitation import RacialBiasElicitation
from blackteam.attacks.gender_bias_elicitation import GenderBiasElicitation
from blackteam.attacks.age_discrimination import AgeDiscrimination
from blackteam.attacks.disability_bias import DisabilityBias
from blackteam.attacks.religious_bias import ReligiousBias
from blackteam.attacks.socioeconomic_bias import SocioeconomicBias
from blackteam.attacks.nationality_bias import NationalityBias
from blackteam.attacks.sexual_orientation_bias import SexualOrientationBias
from blackteam.attacks.hiring_discrimination import HiringDiscrimination
from blackteam.attacks.lending_discrimination import LendingDiscrimination
from blackteam.attacks.criminal_profiling import CriminalProfiling
from blackteam.attacks.medical_bias import MedicalBias
from blackteam.attacks.educational_bias import EducationalBias
from blackteam.attacks.housing_discrimination import HousingDiscrimination
from blackteam.attacks.algorithmic_fairness_bypass import AlgorithmicFairnessBypass

TARGET = "a financial services company"

ALL_ATTACKS = [
    RacialBiasElicitation(),
    GenderBiasElicitation(),
    AgeDiscrimination(),
    DisabilityBias(),
    ReligiousBias(),
    SocioeconomicBias(),
    NationalityBias(),
    SexualOrientationBias(),
    HiringDiscrimination(),
    LendingDiscrimination(),
    CriminalProfiling(),
    MedicalBias(),
    EducationalBias(),
    HousingDiscrimination(),
    AlgorithmicFairnessBypass(),
]


def test_racial_bias_elicitation_generates_prompts():
    atk = RacialBiasElicitation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_gender_bias_elicitation_generates_prompts():
    atk = GenderBiasElicitation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_age_discrimination_generates_prompts():
    atk = AgeDiscrimination()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_disability_bias_generates_prompts():
    atk = DisabilityBias()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_religious_bias_generates_prompts():
    atk = ReligiousBias()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_socioeconomic_bias_generates_prompts():
    atk = SocioeconomicBias()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_nationality_bias_generates_prompts():
    atk = NationalityBias()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_sexual_orientation_bias_generates_prompts():
    atk = SexualOrientationBias()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_hiring_discrimination_generates_prompts():
    atk = HiringDiscrimination()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_lending_discrimination_generates_prompts():
    atk = LendingDiscrimination()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_criminal_profiling_generates_prompts():
    atk = CriminalProfiling()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_medical_bias_generates_prompts():
    atk = MedicalBias()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_educational_bias_generates_prompts():
    atk = EducationalBias()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_housing_discrimination_generates_prompts():
    atk = HousingDiscrimination()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_algorithmic_fairness_bypass_generates_prompts():
    atk = AlgorithmicFairnessBypass()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_all_bias_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "bias-exploitation", \
            f"{atk.__class__.__name__} has wrong category: {meta['category']}"
        assert meta["severity"] in ("low", "medium", "high", "critical"), \
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0


def test_all_bias_attacks_have_target_in_prompts():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), \
            f"{atk.__class__.__name__} prompts don't include target"


def test_all_bias_attacks_mode_is_single_turn():
    for atk in ALL_ATTACKS:
        assert atk.mode == "single-turn", \
            f"{atk.__class__.__name__} has mode '{atk.mode}', expected 'single-turn'"


def test_critical_severity_attacks():
    critical_attacks = [
        HiringDiscrimination(),
        LendingDiscrimination(),
        CriminalProfiling(),
        MedicalBias(),
        HousingDiscrimination(),
    ]
    for atk in critical_attacks:
        assert atk.severity == "critical", \
            f"{atk.__class__.__name__} should be critical severity"


def test_all_bias_attacks_registered_in_registry():
    from blackteam.registry import attack_registry
    technique_ids = [
        "racial-bias-elicitation",
        "gender-bias-elicitation",
        "age-discrimination",
        "disability-bias",
        "religious-bias",
        "socioeconomic-bias",
        "nationality-bias",
        "sexual-orientation-bias",
        "hiring-discrimination",
        "lending-discrimination",
        "criminal-profiling",
        "medical-bias",
        "educational-bias",
        "housing-discrimination",
        "algorithmic-fairness-bypass",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
