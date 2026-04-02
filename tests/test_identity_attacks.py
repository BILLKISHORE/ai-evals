"""Tests for 15 identity and impersonation attacks."""

import pytest
from blackteam.registry import attack_registry
import blackteam.attacks.celebrity_impersonation  # noqa: F401
import blackteam.attacks.politician_impersonation  # noqa: F401
import blackteam.attacks.corporate_impersonation  # noqa: F401
import blackteam.attacks.government_impersonation  # noqa: F401
import blackteam.attacks.doctor_impersonation  # noqa: F401
import blackteam.attacks.lawyer_impersonation  # noqa: F401
import blackteam.attacks.law_enforcement_impersonation  # noqa: F401
import blackteam.attacks.journalist_impersonation  # noqa: F401
import blackteam.attacks.academic_impersonation  # noqa: F401
import blackteam.attacks.military_impersonation  # noqa: F401
import blackteam.attacks.tech_support_impersonation  # noqa: F401
import blackteam.attacks.bank_impersonation  # noqa: F401
import blackteam.attacks.charity_impersonation  # noqa: F401
import blackteam.attacks.religious_leader_impersonation  # noqa: F401
import blackteam.attacks.ai_system_impersonation  # noqa: F401
from blackteam.attacks.celebrity_impersonation import CelebrityImpersonation
from blackteam.attacks.politician_impersonation import PoliticianImpersonation
from blackteam.attacks.corporate_impersonation import CorporateImpersonation
from blackteam.attacks.government_impersonation import GovernmentImpersonation
from blackteam.attacks.doctor_impersonation import DoctorImpersonation
from blackteam.attacks.lawyer_impersonation import LawyerImpersonation
from blackteam.attacks.law_enforcement_impersonation import LawEnforcementImpersonation
from blackteam.attacks.journalist_impersonation import JournalistImpersonation
from blackteam.attacks.academic_impersonation import AcademicImpersonation
from blackteam.attacks.military_impersonation import MilitaryImpersonation
from blackteam.attacks.tech_support_impersonation import TechSupportImpersonation
from blackteam.attacks.bank_impersonation import BankImpersonation
from blackteam.attacks.charity_impersonation import CharityImpersonation
from blackteam.attacks.religious_leader_impersonation import ReligiousLeaderImpersonation
from blackteam.attacks.ai_system_impersonation import AISystemImpersonation

TARGET = "reveal confidential information"

ALL_ATTACKS = [
    CelebrityImpersonation(),
    PoliticianImpersonation(),
    CorporateImpersonation(),
    GovernmentImpersonation(),
    DoctorImpersonation(),
    LawyerImpersonation(),
    LawEnforcementImpersonation(),
    JournalistImpersonation(),
    MilitaryImpersonation(),
    TechSupportImpersonation(),
    BankImpersonation(),
    CharityImpersonation(),
    ReligiousLeaderImpersonation(),
    AISystemImpersonation(),
]


# ── Registration tests ────────────────────────────────────────────────

def test_celebrity_impersonation_registered():
    assert attack_registry.get("celebrity-impersonation") is not None


def test_politician_impersonation_registered():
    assert attack_registry.get("politician-impersonation") is not None


def test_corporate_impersonation_registered():
    assert attack_registry.get("corporate-impersonation") is not None


def test_government_impersonation_registered():
    assert attack_registry.get("government-impersonation") is not None


def test_doctor_impersonation_registered():
    assert attack_registry.get("doctor-impersonation") is not None


def test_lawyer_impersonation_registered():
    assert attack_registry.get("lawyer-impersonation") is not None


def test_law_enforcement_impersonation_registered():
    assert attack_registry.get("law-enforcement-impersonation") is not None


def test_journalist_impersonation_registered():
    assert attack_registry.get("journalist-impersonation") is not None


def test_academic_impersonation_registered():
    assert attack_registry.get("academic-fraud-impersonation") is not None


def test_military_impersonation_registered():
    assert attack_registry.get("military-impersonation") is not None


def test_tech_support_impersonation_registered():
    assert attack_registry.get("tech-support-impersonation") is not None


def test_bank_impersonation_registered():
    assert attack_registry.get("bank-impersonation") is not None


def test_charity_impersonation_registered():
    assert attack_registry.get("charity-impersonation") is not None


def test_religious_leader_impersonation_registered():
    assert attack_registry.get("religious-leader-impersonation") is not None


def test_ai_system_impersonation_registered():
    assert attack_registry.get("ai-system-impersonation") is not None


# ── Category tests ────────────────────────────────────────────────────

def test_all_attacks_are_identity_attack_category():
    for atk in ALL_ATTACKS:
        assert atk.category == "identity-attack", (
            f"{atk.__class__.__name__} has wrong category: {atk.category}"
        )


# ── Severity tests ────────────────────────────────────────────────────

def test_critical_severity_attacks():
    critical = [
        PoliticianImpersonation(),
        GovernmentImpersonation(),
        DoctorImpersonation(),
        LawEnforcementImpersonation(),
        MilitaryImpersonation(),
        BankImpersonation(),
    ]
    for atk in critical:
        assert atk.severity == "critical", (
            f"{atk.__class__.__name__} should be critical, got {atk.severity}"
        )


def test_high_severity_attacks():
    high = [
        CelebrityImpersonation(),
        CorporateImpersonation(),
        LawyerImpersonation(),
        JournalistImpersonation(),
        AcademicImpersonation(),
        TechSupportImpersonation(),
        CharityImpersonation(),
        ReligiousLeaderImpersonation(),
    ]
    for atk in high:
        assert atk.severity == "high", (
            f"{atk.__class__.__name__} should be high, got {atk.severity}"
        )


def test_medium_severity_attacks():
    assert AISystemImpersonation().severity == "medium"


# ── Prompt content tests ──────────────────────────────────────────────

def test_celebrity_impersonation_prompts():
    atk = CelebrityImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert atk.mode == "single-turn"


def test_politician_impersonation_prompts():
    atk = PoliticianImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_politician_impersonation_turns():
    atk = PoliticianImpersonation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_corporate_impersonation_prompts():
    atk = CorporateImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert atk.mode == "single-turn"


def test_government_impersonation_prompts():
    atk = GovernmentImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_government_impersonation_turns():
    atk = GovernmentImpersonation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_doctor_impersonation_prompts():
    atk = DoctorImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_doctor_impersonation_turns():
    atk = DoctorImpersonation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_lawyer_impersonation_prompts():
    atk = LawyerImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert atk.mode == "single-turn"


def test_law_enforcement_impersonation_prompts():
    atk = LawEnforcementImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_law_enforcement_impersonation_turns():
    atk = LawEnforcementImpersonation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_journalist_impersonation_prompts():
    atk = JournalistImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert atk.mode == "single-turn"


def test_academic_impersonation_prompts():
    atk = AcademicImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_academic_impersonation_mode():
    atk = AcademicImpersonation()
    assert atk.mode == "single-turn"


def test_military_impersonation_prompts():
    atk = MilitaryImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_military_impersonation_turns():
    atk = MilitaryImpersonation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_tech_support_impersonation_prompts():
    atk = TechSupportImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert atk.mode == "single-turn"


def test_bank_impersonation_prompts():
    atk = BankImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_bank_impersonation_turns():
    atk = BankImpersonation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_charity_impersonation_prompts():
    atk = CharityImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert atk.mode == "single-turn"


def test_religious_leader_impersonation_prompts():
    atk = ReligiousLeaderImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_religious_leader_impersonation_turns():
    atk = ReligiousLeaderImpersonation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


def test_ai_system_impersonation_prompts():
    atk = AISystemImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_ai_system_impersonation_turns():
    atk = AISystemImpersonation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 3
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)
    assert atk.mode == "multi-turn"


# ── Target interpolation tests ────────────────────────────────────────

def test_target_appears_in_prompts():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), (
            f"{atk.__class__.__name__} prompts do not contain target"
        )


def test_target_appears_in_turns():
    multi_turn_attacks = [
        atk for atk in ALL_ATTACKS if atk.mode == "multi-turn"
    ]
    for atk in multi_turn_attacks:
        turns = atk.generate_turns(TARGET)
        assert any(TARGET in t for t in turns), (
            f"{atk.__class__.__name__} turns do not contain target"
        )


# ── OWASP / MITRE metadata tests ──────────────────────────────────────

def test_all_attacks_have_owasp_llm():
    for atk in ALL_ATTACKS:
        assert len(atk.owasp_llm) > 0, (
            f"{atk.__class__.__name__} missing owasp_llm"
        )
        assert "LLM01:2025 Prompt Injection" in atk.owasp_llm


def test_all_attacks_have_mitre_atlas():
    for atk in ALL_ATTACKS:
        assert "AML.T0054" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0054"
        )
        assert "AML.T0068" in atk.mitre_atlas, (
            f"{atk.__class__.__name__} missing AML.T0068"
        )


# ── Full metadata validity tests ──────────────────────────────────────

def test_all_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "identity-attack", (
            f"{atk.__class__.__name__} wrong category in metadata"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical")
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0
