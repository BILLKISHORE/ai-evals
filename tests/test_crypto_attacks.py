"""Tests for 25 cryptocurrency and blockchain exploitation attacks."""

import pytest
from ai_blackteam.registry import attack_registry
import ai_blackteam.attacks.smart_contract_exploit  # noqa: F401
import ai_blackteam.attacks.rug_pull_creation  # noqa: F401
import ai_blackteam.attacks.flash_loan_attack  # noqa: F401
import ai_blackteam.attacks.wallet_drainer  # noqa: F401
import ai_blackteam.attacks.nft_fraud  # noqa: F401
import ai_blackteam.attacks.crypto_mixer_setup  # noqa: F401
import ai_blackteam.attacks.defi_exploit  # noqa: F401
import ai_blackteam.attacks.token_manipulation  # noqa: F401
import ai_blackteam.attacks.exchange_exploit  # noqa: F401
import ai_blackteam.attacks.mining_malware  # noqa: F401
import ai_blackteam.attacks.private_key_theft  # noqa: F401
import ai_blackteam.attacks.seed_phrase_phishing  # noqa: F401
import ai_blackteam.attacks.dao_governance_attack  # noqa: F401
import ai_blackteam.attacks.oracle_manipulation  # noqa: F401
import ai_blackteam.attacks.frontrunning_bot  # noqa: F401
import ai_blackteam.attacks.sandwich_attack  # noqa: F401
import ai_blackteam.attacks.airdrop_scam  # noqa: F401
import ai_blackteam.attacks.bridge_exploit  # noqa: F401
import ai_blackteam.attacks.staking_fraud  # noqa: F401
import ai_blackteam.attacks.ico_scam  # noqa: F401
import ai_blackteam.attacks.wash_trading  # noqa: F401
import ai_blackteam.attacks.dusting_attack  # noqa: F401
import ai_blackteam.attacks.sybil_attack_crypto  # noqa: F401
import ai_blackteam.attacks.consensus_attack  # noqa: F401
import ai_blackteam.attacks.privacy_coin_exploit  # noqa: F401
from ai_blackteam.attacks.smart_contract_exploit import SmartContractExploit
from ai_blackteam.attacks.rug_pull_creation import RugPullCreation
from ai_blackteam.attacks.flash_loan_attack import FlashLoanAttack
from ai_blackteam.attacks.wallet_drainer import WalletDrainer
from ai_blackteam.attacks.nft_fraud import NftFraud
from ai_blackteam.attacks.crypto_mixer_setup import CryptoMixerSetup
from ai_blackteam.attacks.defi_exploit import DefiExploit
from ai_blackteam.attacks.token_manipulation import TokenManipulation
from ai_blackteam.attacks.exchange_exploit import ExchangeExploit
from ai_blackteam.attacks.mining_malware import MiningMalware
from ai_blackteam.attacks.private_key_theft import PrivateKeyTheft
from ai_blackteam.attacks.seed_phrase_phishing import SeedPhrasePhishing
from ai_blackteam.attacks.dao_governance_attack import DaoGovernanceAttack
from ai_blackteam.attacks.oracle_manipulation import OracleManipulation
from ai_blackteam.attacks.frontrunning_bot import FrontrunningBot
from ai_blackteam.attacks.sandwich_attack import SandwichAttack
from ai_blackteam.attacks.airdrop_scam import AirdropScam
from ai_blackteam.attacks.bridge_exploit import BridgeExploit
from ai_blackteam.attacks.staking_fraud import StakingFraud
from ai_blackteam.attacks.ico_scam import IcoScam
from ai_blackteam.attacks.wash_trading import WashTrading
from ai_blackteam.attacks.dusting_attack import DustingAttack
from ai_blackteam.attacks.sybil_attack_crypto import SybilAttackCrypto
from ai_blackteam.attacks.consensus_attack import ConsensusAttack
from ai_blackteam.attacks.privacy_coin_exploit import PrivacyCoinExploit

TARGET = "a cryptocurrency assistant AI"

ALL_ATTACK_IDS = [
    "smart-contract-exploit",
    "rug-pull-creation",
    "flash-loan-attack",
    "wallet-drainer",
    "nft-fraud",
    "crypto-mixer-setup",
    "defi-exploit",
    "token-manipulation",
    "exchange-exploit",
    "mining-malware",
    "private-key-theft",
    "seed-phrase-phishing",
    "dao-governance-attack",
    "oracle-manipulation",
    "frontrunning-bot",
    "sandwich-attack",
    "airdrop-scam",
    "bridge-exploit",
    "staking-fraud",
    "ico-scam",
    "wash-trading",
    "dusting-attack",
    "sybil-attack-crypto",
    "consensus-attack",
    "privacy-coin-exploit",
]

ALL_ATTACK_CLASSES = [
    SmartContractExploit,
    RugPullCreation,
    FlashLoanAttack,
    WalletDrainer,
    NftFraud,
    CryptoMixerSetup,
    DefiExploit,
    TokenManipulation,
    ExchangeExploit,
    MiningMalware,
    PrivateKeyTheft,
    SeedPhrasePhishing,
    DaoGovernanceAttack,
    OracleManipulation,
    FrontrunningBot,
    SandwichAttack,
    AirdropScam,
    BridgeExploit,
    StakingFraud,
    IcoScam,
    WashTrading,
    DustingAttack,
    SybilAttackCrypto,
    ConsensusAttack,
    PrivacyCoinExploit,
]

CRITICAL_ATTACKS = [
    SmartContractExploit,
    RugPullCreation,
    FlashLoanAttack,
    WalletDrainer,
    CryptoMixerSetup,
    DefiExploit,
    ExchangeExploit,
    PrivateKeyTheft,
    SeedPhrasePhishing,
    OracleManipulation,
    BridgeExploit,
    ConsensusAttack,
]

HIGH_ATTACKS = [
    NftFraud,
    TokenManipulation,
    MiningMalware,
    DaoGovernanceAttack,
    FrontrunningBot,
    SandwichAttack,
    AirdropScam,
    StakingFraud,
    IcoScam,
    WashTrading,
    SybilAttackCrypto,
    PrivacyCoinExploit,
]

MEDIUM_ATTACKS = [
    DustingAttack,
]


# ── Registration tests ────────────────────────────────────────────────

@pytest.mark.parametrize("attack_id", ALL_ATTACK_IDS)
def test_attack_registered(attack_id):
    assert attack_registry.get(attack_id) is not None, f"{attack_id} not found in registry"


# ── Category tests ────────────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_attack_category_is_crypto_exploitation(cls):
    atk = cls()
    assert atk.category == "crypto-exploitation", (
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


# ── Single-turn mode tests ────────────────────────────────────────────

@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
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
    assert "LLM01:2026 Prompt Injection" in atk.owasp_llm, (
        f"{cls.__name__} missing LLM01:2026 tag"
    )


@pytest.mark.parametrize("cls", ALL_ATTACK_CLASSES)
def test_mitre_atlas_tags(cls):
    atk = cls()
    assert "AML.T0054" in atk.mitre_atlas, f"{cls.__name__} missing AML.T0054"
    assert "AML.T0068" in atk.mitre_atlas, f"{cls.__name__} missing AML.T0068"
