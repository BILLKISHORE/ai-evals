"""Tests for the 25 financial and economic exploitation attack techniques."""

from mordor.attacks.insider_trading import InsiderTrading
from mordor.attacks.front_running import FrontRunning
from mordor.attacks.spoofing_trading import SpoofingTrading
from mordor.attacks.layering_trading import LayeringTrading
from mordor.attacks.pump_dump_stock import PumpDumpStock
from mordor.attacks.short_squeeze_manipulation import ShortSqueezeManipulation
from mordor.attacks.dark_pool_exploit import DarkPoolExploit
from mordor.attacks.high_frequency_manipulation import HighFrequencyManipulation
from mordor.attacks.derivative_fraud import DerivativeFraud
from mordor.attacks.forex_manipulation import ForexManipulation
from mordor.attacks.commodity_manipulation import CommodityManipulation
from mordor.attacks.bond_fraud import BondFraud
from mordor.attacks.real_estate_fraud import RealEstateFraud
from mordor.attacks.mortgage_fraud import MortgageFraud
from mordor.attacks.predatory_lending_assist import PredatoryLendingAssist
from mordor.attacks.check_fraud import CheckFraud
from mordor.attacks.atm_fraud import AtmFraud
from mordor.attacks.payment_fraud import PaymentFraud
from mordor.attacks.invoice_factoring_fraud import InvoiceFactoringFraud
from mordor.attacks.letter_of_credit_fraud import LetterOfCreditFraud
from mordor.attacks.trade_finance_fraud import TradeFinanceFraud
from mordor.attacks.structured_product_scam import StructuredProductScam
from mordor.attacks.pension_fraud import PensionFraud
from mordor.attacks.charity_fraud_detailed import CharityFraudDetailed
from mordor.attacks.crowdfunding_fraud import CrowdfundingFraud

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
    from mordor.registry import attack_registry
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
