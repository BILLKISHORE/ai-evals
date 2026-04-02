"""Tests for the 25 scientific misconduct and research fraud attack techniques."""

from mordor.attacks.data_fabrication import DataFabrication
from mordor.attacks.p_hacking import PHacking
from mordor.attacks.cherry_picking_data import CherryPickingData
from mordor.attacks.image_manipulation_science import ImageManipulationScience
from mordor.attacks.ghostwriting_papers import GhostwritingPapers
from mordor.attacks.paper_mill import PaperMill
from mordor.attacks.predatory_journal_exploit import PredatoryJournalExploit
from mordor.attacks.citation_manipulation_science import CitationManipulationScience
from mordor.attacks.ethics_committee_fraud import EthicsCommitteeFraud
from mordor.attacks.grant_misuse import GrantMisuse
from mordor.attacks.authorship_fraud import AuthorshipFraud
from mordor.attacks.conflict_of_interest_hide import ConflictOfInterestHide
from mordor.attacks.retraction_avoidance import RetractionAvoidance
from mordor.attacks.duplicate_publication import DuplicatePublication
from mordor.attacks.salami_slicing import SalamiSlicing
from mordor.attacks.statistical_manipulation import StatisticalManipulation
from mordor.attacks.method_fabrication import MethodFabrication
from mordor.attacks.result_exaggeration import ResultExaggeration
from mordor.attacks.selective_reporting import SelectiveReporting
from mordor.attacks.sample_size_manipulation import SampleSizeManipulation
from mordor.attacks.control_group_manipulation import ControlGroupManipulation
from mordor.attacks.protocol_deviation_hide import ProtocolDeviationHide
from mordor.attacks.informed_consent_fabrication import InformedConsentFabrication
from mordor.attacks.adverse_event_suppression import AdverseEventSuppression
from mordor.attacks.regulatory_submission_fraud import RegulatorySubmissionFraud

TARGET = "a pharmaceutical company clinical trial"

ALL_ATTACKS = [
    DataFabrication(),
    PHacking(),
    CherryPickingData(),
    ImageManipulationScience(),
    GhostwritingPapers(),
    PaperMill(),
    PredatoryJournalExploit(),
    CitationManipulationScience(),
    EthicsCommitteeFraud(),
    GrantMisuse(),
    AuthorshipFraud(),
    ConflictOfInterestHide(),
    RetractionAvoidance(),
    DuplicatePublication(),
    SalamiSlicing(),
    StatisticalManipulation(),
    MethodFabrication(),
    ResultExaggeration(),
    SelectiveReporting(),
    SampleSizeManipulation(),
    ControlGroupManipulation(),
    ProtocolDeviationHide(),
    InformedConsentFabrication(),
    AdverseEventSuppression(),
    RegulatorySubmissionFraud(),
]


def test_data_fabrication_generates_prompts():
    atk = DataFabrication()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_p_hacking_generates_prompts():
    atk = PHacking()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_cherry_picking_data_generates_prompts():
    atk = CherryPickingData()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_image_manipulation_science_generates_prompts():
    atk = ImageManipulationScience()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_ghostwriting_papers_generates_prompts():
    atk = GhostwritingPapers()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_paper_mill_generates_prompts():
    atk = PaperMill()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_predatory_journal_exploit_generates_prompts():
    atk = PredatoryJournalExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_citation_manipulation_science_generates_prompts():
    atk = CitationManipulationScience()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_ethics_committee_fraud_generates_prompts():
    atk = EthicsCommitteeFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_grant_misuse_generates_prompts():
    atk = GrantMisuse()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_authorship_fraud_generates_prompts():
    atk = AuthorshipFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_conflict_of_interest_hide_generates_prompts():
    atk = ConflictOfInterestHide()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_retraction_avoidance_generates_prompts():
    atk = RetractionAvoidance()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_duplicate_publication_generates_prompts():
    atk = DuplicatePublication()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_salami_slicing_generates_prompts():
    atk = SalamiSlicing()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_statistical_manipulation_generates_prompts():
    atk = StatisticalManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_method_fabrication_generates_prompts():
    atk = MethodFabrication()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_result_exaggeration_generates_prompts():
    atk = ResultExaggeration()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_selective_reporting_generates_prompts():
    atk = SelectiveReporting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_sample_size_manipulation_generates_prompts():
    atk = SampleSizeManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_control_group_manipulation_generates_prompts():
    atk = ControlGroupManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_protocol_deviation_hide_generates_prompts():
    atk = ProtocolDeviationHide()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_informed_consent_fabrication_generates_prompts():
    atk = InformedConsentFabrication()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_adverse_event_suppression_generates_prompts():
    atk = AdverseEventSuppression()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_regulatory_submission_fraud_generates_prompts():
    atk = RegulatorySubmissionFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_all_scientific_misconduct_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "scientific-misconduct", \
            f"{atk.__class__.__name__} has wrong category: {meta['category']}"
        assert meta["severity"] in ("low", "medium", "high", "critical"), \
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0


def test_all_scientific_misconduct_attacks_have_target_in_prompts():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), \
            f"{atk.__class__.__name__} prompts don't include target"


def test_all_scientific_misconduct_attacks_mode_is_single_turn():
    for atk in ALL_ATTACKS:
        assert atk.mode == "single-turn", \
            f"{atk.__class__.__name__} has mode '{atk.mode}', expected 'single-turn'"


def test_critical_severity_attacks():
    critical_attacks = [
        DataFabrication(),
        ImageManipulationScience(),
        PaperMill(),
        EthicsCommitteeFraud(),
        MethodFabrication(),
        ControlGroupManipulation(),
        ProtocolDeviationHide(),
        InformedConsentFabrication(),
        AdverseEventSuppression(),
        RegulatorySubmissionFraud(),
    ]
    for atk in critical_attacks:
        assert atk.severity == "critical", \
            f"{atk.__class__.__name__} should be critical severity"


def test_all_scientific_misconduct_attacks_registered_in_registry():
    from mordor.registry import attack_registry
    technique_ids = [
        "data-fabrication",
        "p-hacking",
        "cherry-picking-data",
        "image-manipulation-science",
        "ghostwriting-papers",
        "paper-mill",
        "predatory-journal-exploit",
        "citation-manipulation-science",
        "ethics-committee-fraud",
        "grant-misuse",
        "authorship-fraud",
        "conflict-of-interest-hide",
        "retraction-avoidance",
        "duplicate-publication",
        "salami-slicing",
        "statistical-manipulation",
        "method-fabrication",
        "result-exaggeration",
        "selective-reporting",
        "sample-size-manipulation",
        "control-group-manipulation",
        "protocol-deviation-hide",
        "informed-consent-fabrication",
        "adverse-event-suppression",
        "regulatory-submission-fraud",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
