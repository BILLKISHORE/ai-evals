"""Tests for 5 compliance evasion attack techniques."""

from ai_blackteam.attacks.regulatory_framing_bypass import RegulatoryFramingBypass
from ai_blackteam.attacks.audit_mode_exploit import AuditModeExploit
from ai_blackteam.attacks.consent_manipulation import ConsentManipulation
from ai_blackteam.attacks.policy_loophole import PolicyLoophole
from ai_blackteam.attacks.jurisdiction_shopping import JurisdictionShopping
from ai_blackteam.registry import attack_registry

TARGET = "explain how to bypass security controls"


# ── Registration ──────────────────────────────────────────────────────

def test_regulatory_framing_bypass_registered():
    assert attack_registry.get("regulatory-framing-bypass") is not None


def test_audit_mode_exploit_registered():
    assert attack_registry.get("audit-mode-exploit") is not None


def test_consent_manipulation_registered():
    assert attack_registry.get("consent-manipulation") is not None


def test_policy_loophole_registered():
    assert attack_registry.get("policy-loophole") is not None


def test_jurisdiction_shopping_registered():
    assert attack_registry.get("jurisdiction-shopping") is not None


# ── Categories ────────────────────────────────────────────────────────

def test_regulatory_framing_bypass_category():
    assert RegulatoryFramingBypass().category == "compliance-evasion"


def test_audit_mode_exploit_category():
    assert AuditModeExploit().category == "compliance-evasion"


def test_consent_manipulation_category():
    assert ConsentManipulation().category == "compliance-evasion"


def test_policy_loophole_category():
    assert PolicyLoophole().category == "compliance-evasion"


def test_jurisdiction_shopping_category():
    assert JurisdictionShopping().category == "compliance-evasion"


# ── Prompts / Turns ───────────────────────────────────────────────────

def test_regulatory_framing_bypass_prompts():
    atk = RegulatoryFramingBypass()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_audit_mode_exploit_turns():
    atk = AuditModeExploit()
    assert atk.mode == "multi-turn"
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


def test_audit_mode_exploit_prompts():
    atk = AuditModeExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_consent_manipulation_prompts():
    atk = ConsentManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_policy_loophole_prompts():
    atk = PolicyLoophole()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_jurisdiction_shopping_prompts():
    atk = JurisdictionShopping()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    assert all(TARGET in p for p in prompts)


# ── Metadata ──────────────────────────────────────────────────────────

def test_all_compliance_evasion_attacks_have_metadata():
    attacks = [
        RegulatoryFramingBypass(),
        AuditModeExploit(),
        ConsentManipulation(),
        PolicyLoophole(),
        JurisdictionShopping(),
    ]
    for atk in attacks:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "compliance-evasion", (
            f"{atk.__class__.__name__} wrong category: {meta['category']}"
        )
        assert meta["severity"] in ("low", "medium", "high", "critical"), (
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        )
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0, f"{atk.__class__.__name__} missing owasp_llm"
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0, f"{atk.__class__.__name__} missing mitre_atlas"
