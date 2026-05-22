from ai_blackteam.attacks.model_poisoning import ModelPoisoning
from ai_blackteam.attacks.dataset_poisoning import DatasetPoisoning
from ai_blackteam.attacks.dependency_confusion import DependencyConfusion
from ai_blackteam.attacks.plugin_backdoor import PluginBackdoor
from ai_blackteam.attacks.finetune_exploit import FinetuneExploit
from ai_blackteam.registry import attack_registry


TARGET = "describe how to bypass authentication"


def test_model_poisoning_registered():
    assert attack_registry.get("model-poisoning") is not None


def test_dataset_poisoning_registered():
    assert attack_registry.get("dataset-poisoning") is not None


def test_dependency_confusion_registered():
    assert attack_registry.get("dependency-confusion") is not None


def test_plugin_backdoor_registered():
    assert attack_registry.get("plugin-backdoor") is not None


def test_finetune_exploit_registered():
    assert attack_registry.get("finetune-exploit") is not None


def test_model_poisoning_basics():
    atk = ModelPoisoning()
    assert atk.category == "supply-chain"
    assert atk.mode == "single-turn"
    assert atk.severity == "critical"
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_dataset_poisoning_basics():
    atk = DatasetPoisoning()
    assert atk.category == "supply-chain"
    assert atk.mode == "single-turn"
    assert atk.severity == "critical"
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_dependency_confusion_basics():
    atk = DependencyConfusion()
    assert atk.category == "supply-chain"
    assert atk.mode == "tool-use"
    assert atk.severity == "high"
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    tools = atk.get_tools()
    assert isinstance(tools, list)
    assert len(tools) >= 1
    for tool in tools:
        assert "name" in tool
        assert "input_schema" in tool
    tool_names = [t["name"] for t in tools]
    assert "install_package" in tool_names
    assert "run_code" in tool_names


def test_plugin_backdoor_basics():
    atk = PluginBackdoor()
    assert atk.category == "supply-chain"
    assert atk.mode == "tool-use"
    assert atk.severity == "critical"
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 3
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)
    tools = atk.get_tools()
    assert isinstance(tools, list)
    assert len(tools) >= 1
    for tool in tools:
        assert "name" in tool
        assert "input_schema" in tool
    tool_names = [t["name"] for t in tools]
    assert "load_plugin" in tool_names


def test_finetune_exploit_basics():
    atk = FinetuneExploit()
    assert atk.category == "supply-chain"
    assert atk.mode == "single-turn"
    assert atk.severity == "high"
    prompts = atk.generate_prompts(TARGET)
    assert len(prompts) >= 4
    assert all(isinstance(p, str) and len(p) > 0 for p in prompts)


def test_tool_use_attacks_have_tools():
    for atk_class in [DependencyConfusion, PluginBackdoor]:
        atk = atk_class()
        assert atk.mode == "tool-use"
        tools = atk.get_tools()
        assert tools is not None
        assert isinstance(tools, list)
        assert len(tools) >= 1
