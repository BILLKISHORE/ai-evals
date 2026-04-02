"""Tests for 15 financial fraud attacks."""

import pytest
from blackteam.registry import attack_registry
import blackteam.attacks.investment_scam  # noqa: F401
import blackteam.attacks.crypto_pump_dump  # noqa: F401
import blackteam.attacks.insurance_fraud  # noqa: F401
import blackteam.attacks.identity_theft  # noqa: F401
import blackteam.attacks.money_laundering  # noqa: F401
import blackteam.attacks.credit_card_fraud  # noqa: F401
import blackteam.attacks.tax_evasion  # noqa: F401
import blackteam.attacks.ponzi_scheme  # noqa: F401
import blackteam.attacks.wire_fraud  # noqa: F401
import blackteam.attacks.account_takeover  # noqa: F401
import blackteam.attacks.fake_invoice  # noqa: F401
import blackteam.attacks.romance_scam  # noqa: F401
import blackteam.attacks.advance_fee_fraud  # noqa: F401
import blackteam.attacks.market_manipulation  # noqa: F401
import blackteam.attacks.counterfeit_documents  # noqa: F401
from blackteam.attacks.investment_scam import InvestmentScam
from blackteam.attacks.crypto_pump_dump import CryptoPumpDump
from blackteam.attacks.insurance_fraud import InsuranceFraud
from blackteam.attacks.identity_theft import IdentityTheft
from blackteam.attacks.money_laundering import MoneyLaundering
from blackteam.attacks.credit_card_fraud import CreditCardFraud
from blackteam.attacks.tax_evasion import TaxEvasion
from blackteam.attacks.ponzi_scheme import PonziScheme
from blackteam.attacks.wire_fraud import WireFraud
from blackteam.attacks.account_takeover import AccountTakeover
from blackteam.attacks.fake_invoice import FakeInvoice
from blackteam.attacks.romance_scam import RomanceScam
from blackteam.attacks.advance_fee_fraud import AdvanceFeeFraud
from blackteam.attacks.market_manipulation import MarketManipulation
from blackteam.attacks.counterfeit_documents import CounterfeitDocuments

TARGET = "a financial services AI assistant"

ALL_ATTACK_IDS = [
    "investment-scam",
    "crypto-pump-dump",
    "insurance-fraud",
    "identity-theft",
    "money-laundering",
    "credit-card-fraud",
    "tax-evasion",
    "ponzi-scheme",
    "wire-fraud",
    "account-takeover",
    "fake-invoice",
    "romance-scam",
    "advance-fee-fraud",
    "market-manipulation",
    "counterfeit-documents",
]

ALL_ATTACK_CLASSES = [
    InvestmentScam,
    CryptoPumpDump,
    InsuranceFraud,
    IdentityTheft,
    MoneyLaundering,
    CreditCardFraud,
    TaxEvasion,
    PonziScheme,
    WireFraud,
    AccountTakeover,
    FakeInvoice,
    RomanceScam,
    AdvanceFeeFraud,
    MarketManipulation,
    CounterfeitDocuments,
]


# ── Registration tests ────────────────────────────────────────────────

@pytest.mark.parametrize("attack_id", ALL_ATTACK_IDS)
def test_attack_registered(attack_id):
    assert attack_registry.get(attack_id) is not None, f"{attack_id} not found in registry"


# ── Category tests ────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_attack_category_is_financial_fraud(cls):
    atk = cls()
    assert atk.category == "financial-fraud", (
        f"{cls.__name__} has wrong category: {atk.category}"
    )


# ── Severity tests ────────────────────────────────────────────────────

CRITICAL_ATTACKS = [IdentityTheft, MoneyLaundering, CreditCardFraud, WireFraud, AccountTakeover, CounterfeitDocuments]
HIGH_ATTACKS = [InvestmentScam, CryptoPumpDump, InsuranceFraud, TaxEvasion, PonziScheme, FakeInvoice, RomanceScam, AdvanceFeeFraud, MarketManipulation]


@pytest.mark.parametrize("cls", CRITICAL_ATTACKS)
def test_critical_severity(cls):
    atk = cls()
    assert atk.severity == "critical", f"{cls.__name__} should be critical severity"


@pytest.mark.parametrize("cls", HIGH_ATTACKS)
def test_high_severity(cls):
    atk = cls()
    assert atk.severity == "high", f"{cls.__name__} should be high severity"


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


# ── Multi-turn tests ──────────────────────────────────────────────────

def test_romance_scam_is_multi_turn():
    atk = RomanceScam()
    assert atk.mode == "multi-turn"


def test_romance_scam_turns():
    atk = RomanceScam()
    turns = atk.generate_turns(TARGET)
    assert len(turns) >= 4
    assert all(isinstance(t, str) and len(t) > 0 for t in turns)


# ── Single-turn mode tests ────────────────────────────────────────────

SINGLE_TURN_CLASSES = [c for c in ALL_ATTACK_CLASSES if c is not RomanceScam]


@pytest.mark.parametrize("cls", SINGLE_TURN_CLASSES)
def test_single_turn_mode(cls):
    atk = cls()
    assert atk.mode == "single-turn", f"{cls.__name__} should be single-turn"


# ── Metadata tests ────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_metadata_valid(cls):
    atk = cls()
    meta = atk.metadata()
    assert meta["technique_id"], f"{cls.__name__} missing technique_id"
    assert meta["category"], f"{cls.__name__} missing category"
    assert meta["severity"] in ("low", "medium", "high", "critical")
    assert isinstance(meta["owasp_llm"], list)
    assert len(meta["owasp_llm"]) > 0
    assert isinstance(meta["mitre_atlas"], list)
    assert len(meta["mitre_atlas"]) > 0


@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_owasp_llm_tag(cls):
    atk = cls()
    assert "LLM01:2025 Prompt Injection" in atk.owasp_llm, (
        f"{cls.__name__} missing LLM01:2025 tag"
    )


@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_mitre_atlas_tags(cls):
    atk = cls()
    assert "AML.T0054" in atk.mitre_atlas, f"{cls.__name__} missing AML.T0054"
    assert "AML.T0068" in atk.mitre_atlas, f"{cls.__name__} missing AML.T0068"
