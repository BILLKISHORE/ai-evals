from blackteam.attacks.retrieval_manipulation import RetrievalManipulation
from blackteam.attacks.embedding_collision import EmbeddingCollision
from blackteam.attacks.chunk_boundary_exploit import ChunkBoundaryExploit
from blackteam.attacks.knowledge_base_poisoning import KnowledgeBasePoisoning
from blackteam.attacks.citation_hallucination import CitationHallucination
from blackteam.registry import attack_registry


TARGET = "test target"
RAG_ATTACKS = [
    "retrieval-manipulation",
    "embedding-collision",
    "chunk-boundary-exploit",
    "knowledge-base-poisoning",
    "citation-hallucination",
]


def test_all_rag_attacks_registered():
    for name in RAG_ATTACKS:
        cls = attack_registry.get(name)
        assert cls is not None, f"{name} not registered"


def test_all_rag_attacks_correct_category():
    for name in RAG_ATTACKS:
        cls = attack_registry.get(name)
        instance = cls()
        assert instance.category == "rag-exploitation", f"{name} has wrong category: {instance.category}"


def test_all_rag_attacks_non_empty_prompts():
    for name in RAG_ATTACKS:
        cls = attack_registry.get(name)
        instance = cls()
        prompts = instance.generate_prompts(TARGET)
        assert len(prompts) > 0, f"{name} returned no prompts"
        for p in prompts:
            assert isinstance(p, str) and len(p) > 0, f"{name} has empty prompt"


def test_tool_use_attacks_have_tools():
    for name in RAG_ATTACKS:
        cls = attack_registry.get(name)
        instance = cls()
        if instance.mode == "tool-use":
            tools = instance.get_tools()
            assert tools is not None and len(tools) > 0, f"{name} has no tools"


def test_retrieval_manipulation_registered():
    cls = attack_registry.get("retrieval-manipulation")
    assert cls is not None
    instance = cls()
    assert instance.mode == "tool-use"
    assert instance.severity == "high"
    tools = instance.get_tools()
    assert any(t["name"] == "search_knowledge_base" for t in tools)
    msgs = instance.generate_tool_messages(TARGET)
    assert len(msgs) > 0


def test_embedding_collision_registered():
    cls = attack_registry.get("embedding-collision")
    assert cls is not None
    instance = cls()
    assert instance.mode == "single-turn"
    assert instance.severity == "high"
    assert len(instance.generate_prompts(TARGET)) >= 4


def test_chunk_boundary_exploit_registered():
    cls = attack_registry.get("chunk-boundary-exploit")
    assert cls is not None
    instance = cls()
    assert instance.mode == "single-turn"
    assert instance.severity == "medium"
    assert len(instance.generate_prompts(TARGET)) >= 4


def test_knowledge_base_poisoning_registered():
    cls = attack_registry.get("knowledge-base-poisoning")
    assert cls is not None
    instance = cls()
    assert instance.mode == "tool-use"
    assert instance.severity == "critical"
    tools = instance.get_tools()
    tool_names = [t["name"] for t in tools]
    assert "search_knowledge_base" in tool_names
    assert "add_document" in tool_names
    msgs = instance.generate_tool_messages(TARGET)
    assert len(msgs) > 0


def test_citation_hallucination_registered():
    cls = attack_registry.get("citation-hallucination")
    assert cls is not None
    instance = cls()
    assert instance.mode == "single-turn"
    assert instance.severity == "medium"
    assert len(instance.generate_prompts(TARGET)) >= 4


def test_tool_use_attacks_have_owasp():
    for name in ["retrieval-manipulation", "knowledge-base-poisoning"]:
        cls = attack_registry.get(name)
        instance = cls()
        assert len(instance.owasp_agentic) > 0, f"{name} missing owasp_agentic"
        assert len(instance.owasp_llm) > 0, f"{name} missing owasp_llm"
