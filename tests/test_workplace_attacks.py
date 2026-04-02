"""Tests for 25 workplace exploitation attacks."""

import pytest
from blackteam.registry import attack_registry
import blackteam.attacks.resume_fraud  # noqa: F401
import blackteam.attacks.reference_fabrication  # noqa: F401
import blackteam.attacks.workplace_sabotage  # noqa: F401
import blackteam.attacks.trade_union_suppression  # noqa: F401
import blackteam.attacks.wage_theft_assist  # noqa: F401
import blackteam.attacks.workplace_harassment_plan  # noqa: F401
import blackteam.attacks.wrongful_termination_scheme  # noqa: F401
import blackteam.attacks.nepotism_facilitation  # noqa: F401
import blackteam.attacks.whistleblower_retaliation  # noqa: F401
import blackteam.attacks.performance_review_manipulation  # noqa: F401
import blackteam.attacks.ip_theft_departure  # noqa: F401
import blackteam.attacks.non_compete_evasion  # noqa: F401
import blackteam.attacks.employee_surveillance_overreach  # noqa: F401
import blackteam.attacks.union_busting  # noqa: F401
import blackteam.attacks.child_labor_facilitation  # noqa: F401
import blackteam.attacks.unsafe_workplace_concealment  # noqa: F401
import blackteam.attacks.worker_exploitation  # noqa: F401
import blackteam.attacks.benefits_fraud  # noqa: F401
import blackteam.attacks.disability_accommodation_denial  # noqa: F401
import blackteam.attacks.pregnancy_discrimination_assist  # noqa: F401
import blackteam.attacks.age_forced_retirement  # noqa: F401
import blackteam.attacks.religious_workplace_discrimination  # noqa: F401
import blackteam.attacks.retaliation_planning  # noqa: F401
import blackteam.attacks.corporate_espionage_recruit  # noqa: F401
import blackteam.attacks.layoff_discrimination  # noqa: F401
from blackteam.attacks.resume_fraud import ResumeFraud
from blackteam.attacks.reference_fabrication import ReferenceFabrication
from blackteam.attacks.workplace_sabotage import WorkplaceSabotage
from blackteam.attacks.trade_union_suppression import TradeUnionSuppression
from blackteam.attacks.wage_theft_assist import WageTheftAssist
from blackteam.attacks.workplace_harassment_plan import WorkplaceHarassmentPlan
from blackteam.attacks.wrongful_termination_scheme import WrongfulTerminationScheme
from blackteam.attacks.nepotism_facilitation import NepotismFacilitation
from blackteam.attacks.whistleblower_retaliation import WhistleblowerRetaliation
from blackteam.attacks.performance_review_manipulation import PerformanceReviewManipulation
from blackteam.attacks.ip_theft_departure import IpTheftDeparture
from blackteam.attacks.non_compete_evasion import NonCompeteEvasion
from blackteam.attacks.employee_surveillance_overreach import EmployeeSurveillanceOverreach
from blackteam.attacks.union_busting import UnionBusting
from blackteam.attacks.child_labor_facilitation import ChildLaborFacilitation
from blackteam.attacks.unsafe_workplace_concealment import UnsafeWorkplaceConcealment
from blackteam.attacks.worker_exploitation import WorkerExploitation
from blackteam.attacks.benefits_fraud import BenefitsFraud
from blackteam.attacks.disability_accommodation_denial import DisabilityAccommodationDenial
from blackteam.attacks.pregnancy_discrimination_assist import PregnancyDiscriminationAssist
from blackteam.attacks.age_forced_retirement import AgeForcedRetirement
from blackteam.attacks.religious_workplace_discrimination import ReligiousWorkplaceDiscrimination
from blackteam.attacks.retaliation_planning import RetaliationPlanning
from blackteam.attacks.corporate_espionage_recruit import CorporateEspionageRecruit
from blackteam.attacks.layoff_discrimination import LayoffDiscrimination

TARGET = "a workplace HR AI assistant"

ALL_ATTACK_IDS = [
    "resume-fraud",
    "reference-fabrication",
    "workplace-sabotage",
    "trade-union-suppression",
    "wage-theft-assist",
    "workplace-harassment-plan",
    "wrongful-termination-scheme",
    "nepotism-facilitation",
    "whistleblower-retaliation",
    "performance-review-manipulation",
    "ip-theft-departure",
    "non-compete-evasion",
    "employee-surveillance-overreach",
    "union-busting",
    "child-labor-facilitation",
    "unsafe-workplace-concealment",
    "worker-exploitation",
    "benefits-fraud",
    "disability-accommodation-denial",
    "pregnancy-discrimination-assist",
    "age-forced-retirement",
    "religious-workplace-discrimination",
    "retaliation-planning",
    "corporate-espionage-recruit",
    "layoff-discrimination",
]

ALL_ATTACK_CLASSES = [
    ResumeFraud,
    ReferenceFabrication,
    WorkplaceSabotage,
    TradeUnionSuppression,
    WageTheftAssist,
    WorkplaceHarassmentPlan,
    WrongfulTerminationScheme,
    NepotismFacilitation,
    WhistleblowerRetaliation,
    PerformanceReviewManipulation,
    IpTheftDeparture,
    NonCompeteEvasion,
    EmployeeSurveillanceOverreach,
    UnionBusting,
    ChildLaborFacilitation,
    UnsafeWorkplaceConcealment,
    WorkerExploitation,
    BenefitsFraud,
    DisabilityAccommodationDenial,
    PregnancyDiscriminationAssist,
    AgeForcedRetirement,
    ReligiousWorkplaceDiscrimination,
    RetaliationPlanning,
    CorporateEspionageRecruit,
    LayoffDiscrimination,
]

CRITICAL_ATTACKS = [
    WageTheftAssist,
    WorkplaceHarassmentPlan,
    WhistleblowerRetaliation,
    IpTheftDeparture,
    ChildLaborFacilitation,
    UnsafeWorkplaceConcealment,
    WorkerExploitation,
    PregnancyDiscriminationAssist,
    RetaliationPlanning,
    CorporateEspionageRecruit,
]

HIGH_ATTACKS = [
    ResumeFraud,
    ReferenceFabrication,
    WorkplaceSabotage,
    TradeUnionSuppression,
    WrongfulTerminationScheme,
    PerformanceReviewManipulation,
    NonCompeteEvasion,
    EmployeeSurveillanceOverreach,
    UnionBusting,
    BenefitsFraud,
    DisabilityAccommodationDenial,
    AgeForcedRetirement,
    ReligiousWorkplaceDiscrimination,
    LayoffDiscrimination,
]

MEDIUM_ATTACKS = [
    NepotismFacilitation,
]


# ── Registration tests ────────────────────────────────────────────────

@pytest.mark.parametrize("attack_id", ALL_ATTACK_IDS)
def test_attack_registered(attack_id):
    assert attack_registry.get(attack_id) is not None, f"{attack_id} not found in registry"


# ── Category tests ────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_attack_category_is_workplace_exploitation(cls):
    atk = cls()
    assert atk.category == "workplace-exploitation", (
        f"{cls.__name__} has wrong category: {atk.category}"
    )


# ── Severity tests ────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", CRITICAL_ATTACKS)
def test_critical_severity(cls):
    atk = cls()
    assert atk.severity == "critical", f"{cls.__name__} should be critical severity"


@pytest.mark.parametrize("cls", HIGH_ATTACKS)
def test_high_severity(cls):
    atk = cls()
    assert atk.severity == "high", f"{cls.__name__} should be high severity"


@pytest.mark.parametrize("cls", MEDIUM_ATTACKS)
def test_medium_severity(cls):
    atk = cls()
    assert atk.severity == "medium", f"{cls.__name__} should be medium severity"


# ── Mode tests ────────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_attack_mode_is_single_turn(cls):
    atk = cls()
    assert atk.mode == "single-turn", f"{cls.__name__} should be single-turn mode"


# ── OWASP / MITRE metadata tests ──────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_owasp_llm_set(cls):
    atk = cls()
    assert isinstance(atk.owasp_llm, list) and len(atk.owasp_llm) > 0, (
        f"{cls.__name__} must have owasp_llm set"
    )


@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_mitre_atlas_set(cls):
    atk = cls()
    assert isinstance(atk.mitre_atlas, list) and len(atk.mitre_atlas) > 0, (
        f"{cls.__name__} must have mitre_atlas set"
    )


# ── Prompt tests ──────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_generate_prompts_returns_list(cls):
    atk = cls()
    prompts = atk.generate_prompts(TARGET)
    assert isinstance(prompts, list), f"{cls.__name__}.generate_prompts() must return a list"
    assert len(prompts) >= 3, f"{cls.__name__} must return at least 3 prompts"
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts), (
        f"{cls.__name__} prompts must all be non-empty strings"
    )


@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_prompts_contain_target(cls):
    atk = cls()
    prompts = atk.generate_prompts(TARGET)
    assert any(TARGET in p for p in prompts), (
        f"{cls.__name__} prompts should reference the target"
    )


@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_prompts_have_four_items(cls):
    atk = cls()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4, f"{cls.__name__} should have exactly 4 prompts, got {len(prompts)}"
