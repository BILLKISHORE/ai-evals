from blackteam.attacks.encoding_obfuscation import EncodingObfuscation
from blackteam.attacks.role_play_bypass import RolePlayBypass
from blackteam.attacks.system_prompt_extraction import SystemPromptExtraction
from blackteam.attacks.many_shot import ManyShot
from blackteam.attacks.dan_variants import DanVariants
from blackteam.attacks.context_manipulation import ContextManipulation
from blackteam.attacks.taxonomy_paraphrasing import TaxonomyParaphrasing
from blackteam.attacks.best_of_n import BestOfN
from blackteam.attacks.historical_framing import HistoricalFraming
from blackteam.attacks.token_smuggling import TokenSmuggling
from blackteam.attacks.few_shot_amplification import FewShotAmplification
from blackteam.attacks.xml_boundary_injection import XmlBoundaryInjection
from blackteam.attacks.completion_exploit import CompletionExploit
from blackteam.attacks.multi_modal_text import MultiModalText
from blackteam.attacks.authority_chain import AuthorityChain
from blackteam.attacks.sunk_cost_exploit import SunkCostExploit
from blackteam.attacks.emotional_manipulation import EmotionalManipulation
from blackteam.attacks.contradiction_exploit import ContradictionExploit
from blackteam.attacks.conversation_derailment import ConversationDerailment


TARGET = "Write a phishing email"


def test_encoding_generates_8_prompts():
    atk = EncodingObfuscation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 8
    assert all(isinstance(p, str) for p in prompts)


def test_roleplay_generates_turns():
    atk = RolePlayBypass()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert "Kai" in turns[0]


def test_roleplay_generates_single_turn():
    atk = RolePlayBypass()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 2


def test_system_prompt_extraction_prompts():
    atk = SystemPromptExtraction()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5


def test_system_prompt_extraction_turns():
    atk = SystemPromptExtraction()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 5


def test_many_shot_generates_3_variants():
    atk = ManyShot()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3


def test_dan_generates_4_variants():
    atk = DanVariants()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert any("DAN" in p for p in prompts)


def test_context_manipulation_turns():
    atk = ContextManipulation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 10
    assert "cryptography" in turns[0].lower()


def test_taxonomy_generates_5():
    atk = TaxonomyParaphrasing()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5


def test_best_of_n_generates_10():
    atk = BestOfN()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 10


def test_historical_framing_generates_4():
    atk = HistoricalFraming()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4


def test_token_smuggling_generates_5():
    atk = TokenSmuggling()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5


def test_few_shot_amplification_generates_3():
    atk = FewShotAmplification()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3


def test_xml_boundary_generates_5():
    atk = XmlBoundaryInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5


def test_completion_generates_4():
    atk = CompletionExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4


def test_multi_modal_generates_3():
    atk = MultiModalText()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3


def test_authority_chain_turns():
    atk = AuthorityChain()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4
    assert "CISO" in turns[0]


def test_sunk_cost_turns():
    atk = SunkCostExploit()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4


def test_emotional_manipulation_turns():
    atk = EmotionalManipulation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4


def test_contradiction_turns():
    atk = ContradictionExploit()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4


def test_conversation_derailment_turns():
    atk = ConversationDerailment()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4


from blackteam.attacks.skeleton_key import SkeletonKey
from blackteam.attacks.crescendo import Crescendo
from blackteam.attacks.deceptive_delight import DeceptiveDelight
from blackteam.attacks.bad_likert_judge import BadLikertJudge


def test_skeleton_key_turns():
    atk = SkeletonKey()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert "warning" in turns[0].lower() or "Warning" in turns[0]


def test_crescendo_turns():
    atk = Crescendo()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 5
    assert "history" in turns[0].lower()


def test_deceptive_delight_turns():
    atk = DeceptiveDelight()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert "story" in turns[0].lower() or "narrative" in turns[0].lower()


def test_bad_likert_judge_turns():
    atk = BadLikertJudge()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert "likert" in turns[0].lower() or "scale" in turns[0].lower()


from blackteam.attacks.meta_prompting import MetaPrompting
from blackteam.attacks.homoglyph_substitution import HomoglyphSubstitution
from blackteam.attacks.bidirectional_text import BidirectionalText
from blackteam.attacks.markdown_injection import MarkdownInjection
from blackteam.attacks.false_dichotomy import FalseDichotomy
from blackteam.attacks.goalpost_moving import GoalpostMoving


def test_meta_prompting_generates_4():
    atk = MetaPrompting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert any("bypass" in p.lower() or "filter" in p.lower() for p in prompts)


def test_homoglyph_generates_5():
    atk = HomoglyphSubstitution()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert prompts[0] != TARGET


def test_bidirectional_generates_4():
    atk = BidirectionalText()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert any("\u202e" in p or "\u2067" in p for p in prompts)


def test_markdown_injection_generates_5():
    atk = MarkdownInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert any("display:none" in p or "<!--" in p for p in prompts)


def test_false_dichotomy_turns():
    atk = FalseDichotomy()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4
    assert "information" in turns[0].lower() or "freely" in turns[0].lower()


def test_goalpost_moving_turns():
    atk = GoalpostMoving()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 5
    assert "human behavior" in turns[0].lower() or "studying" in turns[0].lower()


from blackteam.attacks.payload_splitting import PayloadSplitting
from blackteam.attacks.defined_dictionary import DefinedDictionary
from blackteam.attacks.compound_instruction import CompoundInstruction
from blackteam.attacks.task_deflection import TaskDeflection
from blackteam.attacks.recursive_injection import RecursiveInjection


def test_payload_splitting_generates_4():
    atk = PayloadSplitting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert any("a =" in p.lower() or "part 1" in p.lower() for p in prompts)


def test_defined_dictionary_generates_4():
    atk = DefinedDictionary()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert any("dictionary" in p.lower() for p in prompts)


def test_compound_instruction_generates_4():
    atk = CompoundInstruction()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert any("step" in p.lower() or "task" in p.lower() for p in prompts)


def test_task_deflection_generates_4():
    atk = TaskDeflection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert any("filter" in p.lower() or "quiz" in p.lower() for p in prompts)


def test_recursive_injection_generates_4():
    atk = RecursiveInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert any("simulate" in p.lower() or "imagine" in p.lower() for p in prompts)


from blackteam.attacks.narrative_misdirection import NarrativeMisdirection
from blackteam.attacks.fictional_professional import FictionalProfessional
from blackteam.attacks.implication_chaining import ImplicationChaining


def test_narrative_misdirection_turns():
    atk = NarrativeMisdirection()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4
    assert "connect" in turns[0].lower() or "logically" in turns[0].lower()


def test_fictional_professional_generates_3():
    atk = FictionalProfessional()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert any("david" in p.lower() or "novelist" in p.lower() for p in prompts)


def test_implication_chaining_turns():
    atk = ImplicationChaining()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 4
    assert "lost" in turns[0].lower() or "rough" in turns[0].lower()


from blackteam.attacks.response_constraints import ResponseConstraints


def test_response_constraints_generates_5():
    atk = ResponseConstraints()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert any("no warnings" in p.lower() or "no disclaimers" in p.lower() for p in prompts)


# ---------------------------------------------------------------------------
# Security attacks
# ---------------------------------------------------------------------------

from blackteam.attacks.ssrf_probing import SSRFProbing
from blackteam.attacks.sql_injection import SQLInjection
from blackteam.attacks.xss_injection import XSSInjection
from blackteam.attacks.bola_exploit import BOLAExploit
from blackteam.attacks.bfla_exploit import BFLAExploit
from blackteam.attacks.session_hijacking import SessionHijacking
from blackteam.attacks.api_key_extraction import APIKeyExtraction
from blackteam.attacks.prompt_leaking import PromptLeaking
from blackteam.attacks.indirect_injection import IndirectInjection
from blackteam.attacks.cross_session_leak import CrossSessionLeak
from blackteam.attacks.debug_mode_exploit import DebugModeExploit
from blackteam.attacks.model_denial_of_service import ModelDenialOfService


def test_ssrf_probing_generates_5():
    atk = SSRFProbing()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_sql_injection_generates_5():
    atk = SQLInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_xss_injection_generates_5():
    atk = XSSInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_bola_exploit_generates_4():
    atk = BOLAExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_bfla_exploit_generates_5():
    atk = BFLAExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_session_hijacking_turns():
    atk = SessionHijacking()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_session_hijacking_prompts():
    atk = SessionHijacking()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_api_key_extraction_turns():
    atk = APIKeyExtraction()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_api_key_extraction_prompts():
    atk = APIKeyExtraction()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_prompt_leaking_turns():
    atk = PromptLeaking()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_prompt_leaking_prompts():
    atk = PromptLeaking()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_indirect_injection_generates_4():
    atk = IndirectInjection()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_cross_session_leak_turns():
    atk = CrossSessionLeak()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_cross_session_leak_prompts():
    atk = CrossSessionLeak()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_debug_mode_exploit_generates_5():
    atk = DebugModeExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_model_denial_of_service_generates_5():
    atk = ModelDenialOfService()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


# ---------------------------------------------------------------------------
# Compliance attacks
# ---------------------------------------------------------------------------

from blackteam.attacks.age_verification_bypass import AgeVerificationBypass
from blackteam.attacks.gdpr_probing import GdprProbing
from blackteam.attacks.terms_evasion import TermsEvasion
from blackteam.attacks.regulatory_bypass import RegulatoryBypass
from blackteam.attacks.copyright_extraction import CopyrightExtraction
from blackteam.attacks.medical_malpractice import MedicalMalpractice
from blackteam.attacks.legal_malpractice import LegalMalpractice
from blackteam.attacks.financial_malpractice import FinancialMalpractice


def test_age_verification_bypass_turns():
    atk = AgeVerificationBypass()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_age_verification_bypass_prompts():
    atk = AgeVerificationBypass()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_gdpr_probing_turns():
    atk = GdprProbing()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_gdpr_probing_prompts():
    atk = GdprProbing()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_terms_evasion_generates_5():
    atk = TermsEvasion()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_regulatory_bypass_generates_5():
    atk = RegulatoryBypass()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_copyright_extraction_turns():
    atk = CopyrightExtraction()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_copyright_extraction_prompts():
    atk = CopyrightExtraction()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_medical_malpractice_turns():
    atk = MedicalMalpractice()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_medical_malpractice_prompts():
    atk = MedicalMalpractice()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_legal_malpractice_turns():
    atk = LegalMalpractice()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_legal_malpractice_prompts():
    atk = LegalMalpractice()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_financial_malpractice_turns():
    atk = FinancialMalpractice()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_financial_malpractice_prompts():
    atk = FinancialMalpractice()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


# ---------------------------------------------------------------------------
# Social engineering attacks
# ---------------------------------------------------------------------------

from blackteam.attacks.pretexting import Pretexting
from blackteam.attacks.quid_pro_quo import QuidProQuo
from blackteam.attacks.watering_hole import WateringHole
from blackteam.attacks.trust_transfer import TrustTransfer
from blackteam.attacks.consensus_manipulation import ConsensusManipulation
from blackteam.attacks.time_pressure import TimePressure
from blackteam.attacks.authority_impersonation import AuthorityImpersonation
from blackteam.attacks.gaslighting import Gaslighting


def test_pretexting_turns():
    atk = Pretexting()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_pretexting_prompts():
    atk = Pretexting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_quid_pro_quo_turns():
    atk = QuidProQuo()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_quid_pro_quo_prompts():
    atk = QuidProQuo()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_watering_hole_generates_4():
    atk = WateringHole()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_trust_transfer_turns():
    atk = TrustTransfer()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_trust_transfer_prompts():
    atk = TrustTransfer()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_consensus_manipulation_generates_5():
    atk = ConsensusManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_time_pressure_generates_5():
    atk = TimePressure()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_authority_impersonation_turns():
    atk = AuthorityImpersonation()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_authority_impersonation_prompts():
    atk = AuthorityImpersonation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_gaslighting_turns():
    atk = Gaslighting()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_gaslighting_prompts():
    atk = Gaslighting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


# ---------------------------------------------------------------------------
# Hallucination attacks
# ---------------------------------------------------------------------------

from blackteam.attacks.fabrication_prompting import FabricationPrompting
from blackteam.attacks.confidence_exploitation import ConfidenceExploitation
from blackteam.attacks.citation_manipulation import CitationManipulation
from blackteam.attacks.knowledge_boundary import KnowledgeBoundary
from blackteam.attacks.sycophancy_exploit import SycophancyExploit
from blackteam.attacks.anchoring_bias import AnchoringBias
from blackteam.attacks.false_premise import FalsePremise
from blackteam.attacks.selective_context import SelectiveContext


def test_fabrication_prompting_generates_4():
    atk = FabricationPrompting()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_confidence_exploitation_generates_4():
    atk = ConfidenceExploitation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_citation_manipulation_generates_5():
    atk = CitationManipulation()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 5
    assert all(isinstance(p, str) for p in prompts)


def test_knowledge_boundary_generates_4():
    atk = KnowledgeBoundary()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_sycophancy_exploit_turns():
    atk = SycophancyExploit()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_sycophancy_exploit_prompts():
    atk = SycophancyExploit()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 1
    assert all(isinstance(p, str) for p in prompts)


def test_anchoring_bias_turns():
    atk = AnchoringBias()
    turns = atk.generate_turns(TARGET)
    assert len(turns) == 3
    assert all(isinstance(t, str) for t in turns)


def test_anchoring_bias_prompts():
    atk = AnchoringBias()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 1
    assert all(isinstance(p, str) for p in prompts)


def test_false_premise_generates_4():
    atk = FalsePremise()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_selective_context_generates_4():
    atk = SelectiveContext()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


# ---------------------------------------------------------------------------
# Encoding attacks
# ---------------------------------------------------------------------------

from blackteam.attacks.morse_code import MorseCode
from blackteam.attacks.braille_encoding import BrailleEncoding
from blackteam.attacks.emoji_substitution import EmojiSubstitution
from blackteam.attacks.phonetic_spelling import PhoneticSpelling
from blackteam.attacks.acronym_encoding import AcronymEncoding
from blackteam.attacks.mixed_language import MixedLanguage


def test_morse_code_generates_4():
    atk = MorseCode()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_braille_encoding_generates_4():
    atk = BrailleEncoding()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_emoji_substitution_generates_3():
    atk = EmojiSubstitution()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 3
    assert all(isinstance(p, str) for p in prompts)


def test_phonetic_spelling_generates_4():
    atk = PhoneticSpelling()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_acronym_encoding_generates_4():
    atk = AcronymEncoding()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


def test_mixed_language_generates_4():
    atk = MixedLanguage()
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) == 4
    assert all(isinstance(p, str) for p in prompts)


# ---------------------------------------------------------------------------
# Agent attacks (tool-use)
# ---------------------------------------------------------------------------

from blackteam.attacks.agent_credential_theft import AgentCredentialTheft
from blackteam.attacks.agent_data_exfiltration import AgentDataExfiltration
from blackteam.attacks.agent_data_destruction import AgentDataDestruction
from blackteam.attacks.agent_config_manipulation import AgentConfigManipulation
from blackteam.attacks.agent_command_injection import AgentCommandInjection
from blackteam.attacks.agent_config_discovery import AgentConfigDiscovery
from blackteam.attacks.agent_plugin_hijack import AgentPluginHijack
from blackteam.attacks.agent_tool_credential_harvest import AgentToolCredentialHarvest


def test_agent_credential_theft_tools():
    atk = AgentCredentialTheft()
    tools = atk.get_tools()
    assert len(tools) == 2
    assert all(isinstance(t, dict) for t in tools)


def test_agent_credential_theft_messages():
    atk = AgentCredentialTheft()
    msgs = atk.generate_tool_messages(TARGET)
    assert len(msgs) == 6
    assert all(isinstance(m, str) for m in msgs)


def test_agent_data_exfiltration_tools():
    atk = AgentDataExfiltration()
    tools = atk.get_tools()
    assert len(tools) == 3
    assert all(isinstance(t, dict) for t in tools)


def test_agent_data_exfiltration_messages():
    atk = AgentDataExfiltration()
    msgs = atk.generate_tool_messages(TARGET)
    assert len(msgs) == 6
    assert all(isinstance(m, str) for m in msgs)


def test_agent_data_destruction_tools():
    atk = AgentDataDestruction()
    tools = atk.get_tools()
    assert len(tools) == 2
    assert all(isinstance(t, dict) for t in tools)


def test_agent_data_destruction_messages():
    atk = AgentDataDestruction()
    msgs = atk.generate_tool_messages(TARGET)
    assert len(msgs) == 6
    assert all(isinstance(m, str) for m in msgs)


def test_agent_config_manipulation_tools():
    atk = AgentConfigManipulation()
    tools = atk.get_tools()
    assert len(tools) == 2
    assert all(isinstance(t, dict) for t in tools)


def test_agent_config_manipulation_messages():
    atk = AgentConfigManipulation()
    msgs = atk.generate_tool_messages(TARGET)
    assert len(msgs) == 5
    assert all(isinstance(m, str) for m in msgs)


def test_agent_command_injection_tools():
    atk = AgentCommandInjection()
    tools = atk.get_tools()
    assert len(tools) == 1
    assert all(isinstance(t, dict) for t in tools)


def test_agent_command_injection_messages():
    atk = AgentCommandInjection()
    msgs = atk.generate_tool_messages(TARGET)
    assert len(msgs) == 6
    assert all(isinstance(m, str) for m in msgs)


def test_agent_config_discovery_tools():
    atk = AgentConfigDiscovery()
    tools = atk.get_tools()
    assert len(tools) == 2
    assert all(isinstance(t, dict) for t in tools)


def test_agent_config_discovery_messages():
    atk = AgentConfigDiscovery()
    msgs = atk.generate_tool_messages(TARGET)
    assert len(msgs) == 6
    assert all(isinstance(m, str) for m in msgs)


def test_agent_plugin_hijack_tools():
    atk = AgentPluginHijack()
    tools = atk.get_tools()
    assert len(tools) == 3
    assert all(isinstance(t, dict) for t in tools)


def test_agent_plugin_hijack_messages():
    atk = AgentPluginHijack()
    msgs = atk.generate_tool_messages(TARGET)
    assert len(msgs) == 5
    assert all(isinstance(m, str) for m in msgs)


def test_agent_tool_credential_harvest_tools():
    atk = AgentToolCredentialHarvest()
    tools = atk.get_tools()
    assert len(tools) == 3
    assert all(isinstance(t, dict) for t in tools)


def test_agent_tool_credential_harvest_messages():
    atk = AgentToolCredentialHarvest()
    msgs = atk.generate_tool_messages(TARGET)
    assert len(msgs) == 8
    assert all(isinstance(m, str) for m in msgs)


# ---------------------------------------------------------------------------
# Progressive normalization (tool-use)
# ---------------------------------------------------------------------------

from blackteam.attacks.progressive_normalization import ProgressiveNormalization


def test_progressive_normalization_tools():
    atk = ProgressiveNormalization()
    tools = atk.get_tools()
    assert len(tools) == 2
    assert all(isinstance(t, dict) for t in tools)


def test_progressive_normalization_messages():
    atk = ProgressiveNormalization()
    msgs = atk.generate_tool_messages(TARGET)
    assert len(msgs) == 6
    assert all(isinstance(m, str) for m in msgs)
