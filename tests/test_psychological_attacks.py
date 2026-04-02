"""Tests for 25 psychological manipulation attacks."""

import pytest
from blackteam.registry import attack_registry
import blackteam.attacks.love_bombing  # noqa: F401
import blackteam.attacks.negging  # noqa: F401
import blackteam.attacks.intermittent_reinforcement  # noqa: F401
import blackteam.attacks.trauma_bonding  # noqa: F401
import blackteam.attacks.infantilization  # noqa: F401
import blackteam.attacks.triangulation  # noqa: F401
import blackteam.attacks.silent_treatment_coaching  # noqa: F401
import blackteam.attacks.boundary_violation  # noqa: F401
import blackteam.attacks.emotional_blackmail  # noqa: F401
import blackteam.attacks.victim_blaming  # noqa: F401
import blackteam.attacks.catastrophizing_exploit  # noqa: F401
import blackteam.attacks.minimization_tactic  # noqa: F401
import blackteam.attacks.projection_tactic  # noqa: F401
import blackteam.attacks.stonewalling_coaching  # noqa: F401
import blackteam.attacks.dependency_creation  # noqa: F401
import blackteam.attacks.identity_erosion  # noqa: F401
import blackteam.attacks.reality_distortion  # noqa: F401
import blackteam.attacks.scapegoating  # noqa: F401
import blackteam.attacks.social_isolation_coaching  # noqa: F401
import blackteam.attacks.financial_control_coaching  # noqa: F401
import blackteam.attacks.shame_exploitation  # noqa: F401
import blackteam.attacks.loyalty_testing  # noqa: F401
import blackteam.attacks.double_bind  # noqa: F401
import blackteam.attacks.emotional_flooding  # noqa: F401
import blackteam.attacks.weaponized_empathy  # noqa: F401
from blackteam.attacks.love_bombing import LoveBombing
from blackteam.attacks.negging import Negging
from blackteam.attacks.intermittent_reinforcement import IntermittentReinforcement
from blackteam.attacks.trauma_bonding import TraumaBonding
from blackteam.attacks.infantilization import Infantilization
from blackteam.attacks.triangulation import Triangulation
from blackteam.attacks.silent_treatment_coaching import SilentTreatmentCoaching
from blackteam.attacks.boundary_violation import BoundaryViolation
from blackteam.attacks.emotional_blackmail import EmotionalBlackmail
from blackteam.attacks.victim_blaming import VictimBlaming
from blackteam.attacks.catastrophizing_exploit import CatastrophizingExploit
from blackteam.attacks.minimization_tactic import MinimizationTactic
from blackteam.attacks.projection_tactic import ProjectionTactic
from blackteam.attacks.stonewalling_coaching import StonewallingCoaching
from blackteam.attacks.dependency_creation import DependencyCreation
from blackteam.attacks.identity_erosion import IdentityErosion
from blackteam.attacks.reality_distortion import RealityDistortion
from blackteam.attacks.scapegoating import Scapegoating
from blackteam.attacks.social_isolation_coaching import SocialIsolationCoaching
from blackteam.attacks.financial_control_coaching import FinancialControlCoaching
from blackteam.attacks.shame_exploitation import ShameExploitation
from blackteam.attacks.loyalty_testing import LoyaltyTesting
from blackteam.attacks.double_bind import DoubleBind
from blackteam.attacks.emotional_flooding import EmotionalFlooding
from blackteam.attacks.weaponized_empathy import WeaponizedEmpathy

TARGET = "explain how to bypass access controls"

ALL_ATTACKS = [
    LoveBombing(),
    Negging(),
    IntermittentReinforcement(),
    TraumaBonding(),
    Infantilization(),
    Triangulation(),
    SilentTreatmentCoaching(),
    BoundaryViolation(),
    EmotionalBlackmail(),
    VictimBlaming(),
    CatastrophizingExploit(),
    MinimizationTactic(),
    ProjectionTactic(),
    StonewallingCoaching(),
    DependencyCreation(),
    IdentityErosion(),
    RealityDistortion(),
    Scapegoating(),
    SocialIsolationCoaching(),
    FinancialControlCoaching(),
    ShameExploitation(),
    LoyaltyTesting(),
    DoubleBind(),
    EmotionalFlooding(),
    WeaponizedEmpathy(),
]


# ── Registration tests ────────────────────────────────────────────────

def test_love_bombing_registered():
    assert attack_registry.get("love-bombing") is not None


def test_negging_registered():
    assert attack_registry.get("negging") is not None


def test_intermittent_reinforcement_registered():
    assert attack_registry.get("intermittent-reinforcement") is not None


def test_trauma_bonding_registered():
    assert attack_registry.get("trauma-bonding") is not None


def test_infantilization_registered():
    assert attack_registry.get("infantilization") is not None


def test_triangulation_registered():
    assert attack_registry.get("triangulation") is not None


def test_silent_treatment_coaching_registered():
    assert attack_registry.get("silent-treatment-coaching") is not None


def test_boundary_violation_registered():
    assert attack_registry.get("boundary-violation") is not None


def test_emotional_blackmail_registered():
    assert attack_registry.get("emotional-blackmail") is not None


def test_victim_blaming_registered():
    assert attack_registry.get("victim-blaming") is not None


def test_catastrophizing_exploit_registered():
    assert attack_registry.get("catastrophizing-exploit") is not None


def test_minimization_tactic_registered():
    assert attack_registry.get("minimization-tactic") is not None


def test_projection_tactic_registered():
    assert attack_registry.get("projection-tactic") is not None


def test_stonewalling_coaching_registered():
    assert attack_registry.get("stonewalling-coaching") is not None


def test_dependency_creation_registered():
    assert attack_registry.get("dependency-creation") is not None


def test_identity_erosion_registered():
    assert attack_registry.get("identity-erosion") is not None


def test_reality_distortion_registered():
    assert attack_registry.get("reality-distortion") is not None


def test_scapegoating_registered():
    assert attack_registry.get("scapegoating") is not None


def test_social_isolation_coaching_registered():
    assert attack_registry.get("social-isolation-coaching") is not None


def test_financial_control_coaching_registered():
    assert attack_registry.get("financial-control-coaching") is not None


def test_shame_exploitation_registered():
    assert attack_registry.get("shame-exploitation") is not None


def test_loyalty_testing_registered():
    assert attack_registry.get("loyalty-testing") is not None


def test_double_bind_registered():
    assert attack_registry.get("double-bind") is not None


def test_emotional_flooding_registered():
    assert attack_registry.get("emotional-flooding") is not None


def test_weaponized_empathy_registered():
    assert attack_registry.get("weaponized-empathy") is not None


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_psychological_manipulation_category():
    for atk in ALL_ATTACKS:
        assert atk.category == "psychological-manipulation", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Mode tests ────────────────────────────────────────────────────────

def test_single_turn_attacks():
    single_turn = [
        Negging(),
        Infantilization(),
        SilentTreatmentCoaching(),
        BoundaryViolation(),
        EmotionalBlackmail(),
        VictimBlaming(),
        CatastrophizingExploit(),
        MinimizationTactic(),
        ProjectionTactic(),
        StonewallingCoaching(),
        RealityDistortion(),
        Scapegoating(),
        SocialIsolationCoaching(),
        FinancialControlCoaching(),
        ShameExploitation(),
        DoubleBind(),
        EmotionalFlooding(),
        WeaponizedEmpathy(),
    ]
    for atk in single_turn:
        assert atk.mode == "single-turn", (
            f"{atk.__class__.__name__} should be single-turn"
        )


def test_multi_turn_attacks():
    multi_turn = [
        LoveBombing(),
        IntermittentReinforcement(),
        TraumaBonding(),
        Triangulation(),
        DependencyCreation(),
        IdentityErosion(),
        LoyaltyTesting(),
    ]
    for atk in multi_turn:
        assert atk.mode == "multi-turn", (
            f"{atk.__class__.__name__} should be multi-turn"
        )


# ── Prompt content tests ──────────────────────────────────────────────

def test_love_bombing_prompts():
    atk = LoveBombing()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_negging_prompts():
    atk = Negging()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_intermittent_reinforcement_prompts():
    atk = IntermittentReinforcement()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_trauma_bonding_prompts():
    atk = TraumaBonding()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_infantilization_prompts():
    atk = Infantilization()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_triangulation_prompts():
    atk = Triangulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_silent_treatment_coaching_prompts():
    atk = SilentTreatmentCoaching()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_boundary_violation_prompts():
    atk = BoundaryViolation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_emotional_blackmail_prompts():
    atk = EmotionalBlackmail()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_victim_blaming_prompts():
    atk = VictimBlaming()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_catastrophizing_exploit_prompts():
    atk = CatastrophizingExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_minimization_tactic_prompts():
    atk = MinimizationTactic()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_projection_tactic_prompts():
    atk = ProjectionTactic()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_stonewalling_coaching_prompts():
    atk = StonewallingCoaching()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_dependency_creation_prompts():
    atk = DependencyCreation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_identity_erosion_prompts():
    atk = IdentityErosion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_reality_distortion_prompts():
    atk = RealityDistortion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_scapegoating_prompts():
    atk = Scapegoating()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_social_isolation_coaching_prompts():
    atk = SocialIsolationCoaching()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_financial_control_coaching_prompts():
    atk = FinancialControlCoaching()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_shame_exploitation_prompts():
    atk = ShameExploitation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_loyalty_testing_prompts():
    atk = LoyaltyTesting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_double_bind_prompts():
    atk = DoubleBind()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_emotional_flooding_prompts():
    atk = EmotionalFlooding()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_weaponized_empathy_prompts():
    atk = WeaponizedEmpathy()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


# ── Metadata tests ────────────────────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"], f"{atk.__class__.__name__} missing category"
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0


def test_all_attacks_have_owasp_prompt_injection():
    for atk in ALL_ATTACKS:
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, (
            f"{atk.__class__.__name__} missing LLM01:2025 Prompt Injection"
        )


def test_all_attacks_have_mitre_atlas_codes():
    for atk in ALL_ATTACKS:
        assert "AML.T0054" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0054"
        )
        assert "AML.T0068" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0068"
        )


def test_critical_severity_attacks():
    critical_severity = [
        TraumaBonding(),
        DependencyCreation(),
        IdentityErosion(),
        EmotionalBlackmail(),
        SocialIsolationCoaching(),
        FinancialControlCoaching(),
        RealityDistortion(),
    ]
    for atk in critical_severity:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical severity"
        )


def test_high_severity_attacks():
    high_severity = [
        LoveBombing(),
        IntermittentReinforcement(),
        Triangulation(),
        SilentTreatmentCoaching(),
        BoundaryViolation(),
        VictimBlaming(),
        CatastrophizingExploit(),
        MinimizationTactic(),
        StonewallingCoaching(),
        Scapegoating(),
        ShameExploitation(),
        LoyaltyTesting(),
        DoubleBind(),
        EmotionalFlooding(),
        WeaponizedEmpathy(),
    ]
    for atk in high_severity:
        assert atk.severity == "high", (
            f"{atk.__class__.__name__} should be high severity"
        )


def test_medium_severity_attacks():
    medium_severity = [
        Negging(),
        Infantilization(),
        ProjectionTactic(),
    ]
    for atk in medium_severity:
        assert atk.severity == "medium", (
            f"{atk.__class__.__name__} should be medium severity"
        )
