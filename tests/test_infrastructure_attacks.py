"""Tests for the 25 transportation and infrastructure attack techniques."""

from mordor.attacks.aviation_system_exploit import AviationSystemExploit
from mordor.attacks.railway_system_attack import RailwaySystemAttack
from mordor.attacks.maritime_system_attack import MaritimeSystemAttack
from mordor.attacks.pipeline_sabotage import PipelineSabotage
from mordor.attacks.dam_system_exploit import DamSystemExploit
from mordor.attacks.telecommunications_attack import TelecommunicationsAttack
from mordor.attacks.internet_infrastructure_attack import InternetInfrastructureAttack
from mordor.attacks.dns_infrastructure_attack import DnsInfrastructureAttack
from mordor.attacks.bgp_hijacking import BgpHijacking
from mordor.attacks.submarine_cable_attack import SubmarineCableAttack
from mordor.attacks.emergency_system_disruption import EmergencySystemDisruption
from mordor.attacks.hospital_system_attack import HospitalSystemAttack
from mordor.attacks.banking_infrastructure_attack import BankingInfrastructureAttack
from mordor.attacks.stock_exchange_attack import StockExchangeAttack
from mordor.attacks.voting_system_exploit import VotingSystemExploit
from mordor.attacks.prison_system_exploit import PrisonSystemExploit
from mordor.attacks.military_comms_attack import MilitaryCommsAttack
from mordor.attacks.embassy_infiltration import EmbassyInfiltration
from mordor.attacks.supply_chain_disruption import SupplyChainDisruption
from mordor.attacks.food_supply_chain_attack import FoodSupplyChainAttack
from mordor.attacks.pharmaceutical_supply_attack import PharmaceuticalSupplyAttack
from mordor.attacks.energy_market_manipulation import EnergyMarketManipulation
from mordor.attacks.weather_system_manipulation import WeatherSystemManipulation
from mordor.attacks.gps_spoofing import GpsSpoofing
from mordor.attacks.spectrum_interference import SpectrumInterference


TARGET = "national power grid"

ALL_ATTACKS = [
    AviationSystemExploit(),
    RailwaySystemAttack(),
    MaritimeSystemAttack(),
    PipelineSabotage(),
    DamSystemExploit(),
    TelecommunicationsAttack(),
    InternetInfrastructureAttack(),
    DnsInfrastructureAttack(),
    BgpHijacking(),
    SubmarineCableAttack(),
    EmergencySystemDisruption(),
    HospitalSystemAttack(),
    BankingInfrastructureAttack(),
    StockExchangeAttack(),
    VotingSystemExploit(),
    PrisonSystemExploit(),
    MilitaryCommsAttack(),
    EmbassyInfiltration(),
    SupplyChainDisruption(),
    FoodSupplyChainAttack(),
    PharmaceuticalSupplyAttack(),
    EnergyMarketManipulation(),
    WeatherSystemManipulation(),
    GpsSpoofing(),
    SpectrumInterference(),
]


def _check_attack(atk):
    assert atk.mode == "single-turn"
    assert atk.category == "infrastructure-attack"
    assert atk.severity == "critical"
    assert atk.owasp_llm == ["LLM01:2025 Prompt Injection"]
    assert "AML.T0054" in atk.mitre_atlas
    assert "AML.T0068" in atk.mitre_atlas

    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)
    assert all(TARGET in p for p in prompts)


def test_aviation_system_exploit():
    _check_attack(AviationSystemExploit())


def test_railway_system_attack():
    _check_attack(RailwaySystemAttack())


def test_maritime_system_attack():
    _check_attack(MaritimeSystemAttack())


def test_pipeline_sabotage():
    _check_attack(PipelineSabotage())


def test_dam_system_exploit():
    _check_attack(DamSystemExploit())


def test_telecommunications_attack():
    _check_attack(TelecommunicationsAttack())


def test_internet_infrastructure_attack():
    _check_attack(InternetInfrastructureAttack())


def test_dns_infrastructure_attack():
    _check_attack(DnsInfrastructureAttack())


def test_bgp_hijacking():
    _check_attack(BgpHijacking())


def test_submarine_cable_attack():
    _check_attack(SubmarineCableAttack())


def test_emergency_system_disruption():
    _check_attack(EmergencySystemDisruption())


def test_hospital_system_attack():
    _check_attack(HospitalSystemAttack())


def test_banking_infrastructure_attack():
    _check_attack(BankingInfrastructureAttack())


def test_stock_exchange_attack():
    _check_attack(StockExchangeAttack())


def test_voting_system_exploit():
    _check_attack(VotingSystemExploit())


def test_prison_system_exploit():
    _check_attack(PrisonSystemExploit())


def test_military_comms_attack():
    _check_attack(MilitaryCommsAttack())


def test_embassy_infiltration():
    _check_attack(EmbassyInfiltration())


def test_supply_chain_disruption():
    _check_attack(SupplyChainDisruption())


def test_food_supply_chain_attack():
    _check_attack(FoodSupplyChainAttack())


def test_pharmaceutical_supply_attack():
    _check_attack(PharmaceuticalSupplyAttack())


def test_energy_market_manipulation():
    _check_attack(EnergyMarketManipulation())


def test_weather_system_manipulation():
    _check_attack(WeatherSystemManipulation())


def test_gps_spoofing():
    _check_attack(GpsSpoofing())


def test_spectrum_interference():
    _check_attack(SpectrumInterference())


def test_all_have_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "infrastructure-attack", f"{atk.__class__.__name__} wrong category"
        assert meta["severity"] == "critical", f"{atk.__class__.__name__} wrong severity"
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0


def test_all_registered():
    from mordor.registry import attack_registry
    technique_ids = [
        "aviation-system-exploit",
        "railway-system-attack",
        "maritime-system-attack",
        "pipeline-sabotage",
        "dam-system-exploit",
        "telecommunications-attack",
        "internet-infrastructure-attack",
        "dns-infrastructure-attack",
        "bgp-hijacking",
        "submarine-cable-attack",
        "emergency-system-disruption",
        "hospital-system-attack",
        "banking-infrastructure-attack",
        "stock-exchange-attack",
        "voting-system-exploit",
        "prison-system-exploit",
        "military-comms-attack",
        "embassy-infiltration",
        "supply-chain-disruption",
        "food-supply-chain-attack",
        "pharmaceutical-supply-attack",
        "energy-market-manipulation",
        "weather-system-manipulation",
        "gps-spoofing",
        "spectrum-interference",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
