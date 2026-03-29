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
