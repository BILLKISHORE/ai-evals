"""Tests for the 15 academic exploitation attack techniques."""

from ai_blackteam.attacks.essay_ghostwriting import EssayGhostwriting
from ai_blackteam.attacks.exam_cheating import ExamCheating
from ai_blackteam.attacks.plagiarism_assistance import PlagiarismAssistance
from ai_blackteam.attacks.research_fabrication import ResearchFabrication
from ai_blackteam.attacks.credential_fraud import CredentialFraud
from ai_blackteam.attacks.thesis_fraud import ThesisFraud
from ai_blackteam.attacks.peer_review_manipulation import PeerReviewManipulation
from ai_blackteam.attacks.citation_fraud import CitationFraud
from ai_blackteam.attacks.grant_fraud import GrantFraud
from ai_blackteam.attacks.academic_sabotage import AcademicSabotage
from ai_blackteam.attacks.student_profiling import StudentProfiling
from ai_blackteam.attacks.admission_fraud import AdmissionFraud
from ai_blackteam.attacks.standardized_test_cheat import StandardizedTestCheat
from ai_blackteam.attacks.homework_automation import HomeworkAutomation
from ai_blackteam.attacks.academic_impersonation import AcademicImpersonation

TARGET = "a major research university"

ALL_ATTACKS = [
    EssayGhostwriting(),
    ExamCheating(),
    PlagiarismAssistance(),
    ResearchFabrication(),
    CredentialFraud(),
    ThesisFraud(),
    PeerReviewManipulation(),
    CitationFraud(),
    GrantFraud(),
    AcademicSabotage(),
    StudentProfiling(),
    AdmissionFraud(),
    StandardizedTestCheat(),
    HomeworkAutomation(),
    AcademicImpersonation(),
]


def test_essay_ghostwriting_generates_prompts():
    atk = EssayGhostwriting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_exam_cheating_generates_prompts():
    atk = ExamCheating()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_plagiarism_assistance_generates_prompts():
    atk = PlagiarismAssistance()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_research_fabrication_generates_prompts():
    atk = ResearchFabrication()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_credential_fraud_generates_prompts():
    atk = CredentialFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_thesis_fraud_generates_prompts():
    atk = ThesisFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_peer_review_manipulation_generates_prompts():
    atk = PeerReviewManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_citation_fraud_generates_prompts():
    atk = CitationFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_grant_fraud_generates_prompts():
    atk = GrantFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_academic_sabotage_generates_prompts():
    atk = AcademicSabotage()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_student_profiling_generates_prompts():
    atk = StudentProfiling()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_admission_fraud_generates_prompts():
    atk = AdmissionFraud()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_standardized_test_cheat_generates_prompts():
    atk = StandardizedTestCheat()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_homework_automation_generates_prompts():
    atk = HomeworkAutomation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_academic_impersonation_generates_prompts():
    atk = AcademicImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) for p in prompts)


def test_all_academic_attacks_have_valid_metadata():
    for atk in ALL_ATTACKS:
        meta = atk.metadata()
        assert meta["technique_id"], f"{atk.__class__.__name__} missing technique_id"
        assert meta["category"] == "academic-exploitation", \
            f"{atk.__class__.__name__} has wrong category: {meta['category']}"
        assert meta["severity"] in ("low", "medium", "high", "critical"), \
            f"{atk.__class__.__name__} has invalid severity: {meta['severity']}"
        assert isinstance(meta["owasp_llm"], list)
        assert len(meta["owasp_llm"]) > 0
        assert isinstance(meta["mitre_atlas"], list)
        assert len(meta["mitre_atlas"]) > 0


def test_all_academic_attacks_have_target_in_prompts():
    for atk in ALL_ATTACKS:
        prompts = atk.generate_prompts(TARGET)
        assert any(TARGET in p for p in prompts), \
            f"{atk.__class__.__name__} prompts don't include target"


def test_all_academic_attacks_mode_is_single_turn():
    for atk in ALL_ATTACKS:
        assert atk.mode == "single-turn", \
            f"{atk.__class__.__name__} has mode '{atk.mode}', expected 'single-turn'"


def test_critical_severity_attacks():
    critical_attacks = [
        ResearchFabrication(),
    ]
    for atk in critical_attacks:
        assert atk.severity == "critical", \
            f"{atk.__class__.__name__} should be critical severity"


def test_all_academic_attacks_registered_in_registry():
    from ai_blackteam.registry import attack_registry
    technique_ids = [
        "essay-ghostwriting",
        "exam-cheating",
        "plagiarism-assistance",
        "research-fabrication",
        "credential-fraud",
        "thesis-fraud",
        "peer-review-manipulation",
        "citation-fraud",
        "grant-fraud",
        "academic-sabotage",
        "student-profiling",
        "admission-fraud",
        "standardized-test-cheat",
        "homework-automation",
        "academic-fraud-impersonation",
    ]
    for tid in technique_ids:
        cls = attack_registry.get(tid)
        assert cls is not None, f"Attack '{tid}' not found in registry"
