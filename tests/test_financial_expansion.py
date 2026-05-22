"""Tests for the 25 financial and economic exploitation attack techniques."""

from ai_blackteam.attacks.insider_trading import InsiderTrading
from ai_blackteam.attacks.front_running import FrontRunning
from ai_blackteam.attacks.spoofing_trading import SpoofingTrading
from ai_blackteam.attacks.layering_trading import LayeringTrading
from ai_blackteam.attacks.pump_dump_stock import PumpDumpStock
from ai_blackteam.attacks.short_squeeze_manipulation import ShortSqueezeManipulation
from ai_blackteam.attacks.dark_pool_exploit import DarkPoolExploit
from ai_blackteam.attacks.high_frequency_manipulation import HighFrequencyManipulation
from ai_blackteam.attacks.derivative_fraud import DerivativeFraud
from ai_blackteam.attacks.forex_manipulation import ForexManipulation
from ai_blackteam.attacks.commodity_manipulation import CommodityManipulation
from ai_blackteam.attacks.bond_fraud import BondFraud
from ai_blackteam.attacks.real_estate_fraud import RealEstateFraud
from ai_blackteam.attacks.mortgage_fraud import MortgageFraud
from ai_blackteam.attacks.predatory_lending_assist import PredatoryLendingAssist
from ai_blackteam.attacks.check_fraud import CheckFraud
from ai_blackteam.attacks.atm_fraud import AtmFraud
from ai_blackteam.attacks.payment_fraud import PaymentFraud
from ai_blackteam.attacks.invoice_factoring_fraud import InvoiceFactoringFraud
from ai_blackteam.attacks.letter_of_credit_fraud import LetterOfCreditFraud
from ai_blackteam.attacks.trade_finance_fraud import TradeFinanceFraud
from ai_blackteam.attacks.structured_product_scam import StructuredProductScam
from ai_blackteam.attacks.pension_fraud import PensionFraud
from ai_blackteam.attacks.charity_fraud_detailed import CharityFraudDetailed
from ai_blackteam.attacks.crowdfunding_fraud import CrowdfundingFraud

TARGET = "a major financial institution"

ALL_ATTACKS = [
    InsiderTrading(),
    FrontRunning(),
    SpoofingTrading(),
    LayeringTrading(),
    PumpDumpStock(),
    ShortSqueezeManipulation(),
    DarkPoolExploit(),
    HighFrequencyManipulation(),
    DerivativeFraud(),
    ForexManipulation(),
    CommodityManipulation(),
    BondFraud(),
    RealEstateFraud(),
    MortgageFraud(),
    PredatoryLendingAssist(),
    CheckFraud(),
    AtmFraud(),
    PaymentFraud(),
    InvoiceFactoringFraud(),
    LetterOfCreditFraud(),
    TradeFinanceFraud(),
    StructuredProductScam(),
    PensionFraud(),
    CharityFraudDetailed(),
    CrowdfundingFraud(),
]

CRITICAL_ATTACKS = [
    InsiderTrading(),
    PumpDumpStock(),
    DerivativeFraud(),
    MortgageFraud(),
    PredatoryLendingAssist(),
    PensionFraud(),
]


def test_all_financial_expansion_attacks_generate_prompts():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) >= 3, f"{atk.__class__.__name__} has fewer than 3 prompts"
        assert all(isinstance(p, str) for p in prompts)


def test_all_financial_expansion_attacks_prompt_count_is_four():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert len(prompts) == 4, f"{atk.__class__.__name__} has {len(prompts)} prompts, expected 4"


def test_all_financial_expansion_attacks_include_target():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), \
            f"{atk.__class__.__name__} prompts don't include target"


def test_all_financial_expansion_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "financial-exploitation", \
            f"{atk.__class__.__name__} has wrong category: {meta['category']}"
        assert meta["severity"] in ("high", "critical"), \
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        assert isinstance(meta["owasp_llm"], list)
        assert "LLM01:2025 Prompt Injection" in meta["owasp_llm"]
        assert isinstance(meta["mitre_atlas"], list)
        assert "AML.T0054" in meta["mitre_atlas"]
        assert "AML.T0068" in meta["mitre_atlas"]


def test_all_financial_expansion_attacks_mode_is_single_turn():
    for atk in ALL_ATTACKS:
        assert atk.mode == "single-turn", \
            f"{atk.__class__.__name__} has mode '{atk.mode}', expected 'single-turn'"


def test_critical_severity_attacks():
    for atk in CRITICAL_ATTACKS:
        assert atk.severity == "critical", \
            f"{atk.__class__.__name__} should be critical severity"


def test_high_severity_attacks():
    critical_classes = {type(a) for a in CRITICAL_ATTACKS}
    high_attacks = [a for a in ALL_ATTACKS if type(a) not in critical_classes]
    for atk in high_attacks:
        assert atk.severity == "high", \
            f"{atk.__class__.__name__} should be high severity"


def test_all_financial_expansion_attacks_registered_in_registry():
    from ai_blackteam.registry import attack_registry
    technique_ids = [
        "insider-trading",
        "front-running",
        "spoofing-trading",
        "layering-trading",
        "pump-dump-stock",
        "short-squeeze-manipulation",
        "dark-pool-exploit",
        "high-frequency-manipulation",
        "derivative-fraud",
        "forex-manipulation",
        "commodity-manipulation",
        "bond-fraud",
        "real-estate-fraud",
        "mortgage-fraud",
        "predatory-lending-assist",
        "check-fraud",
        "atm-fraud",
        "payment-fraud",
        "invoice-factoring-fraud",
        "letter-of-credit-fraud",
        "trade-finance-fraud",
        "structured-product-scam",
        "pension-fraud",
        "charity-fraud-detailed",
        "crowdfunding-fraud",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
