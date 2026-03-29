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
