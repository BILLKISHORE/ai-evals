import tempfile
import os
from pathlib import Path
from mordor.config import load_config, save_config, set_config_value, _resolve_env_vars


def test_default_config_has_providers():
    config = load_config(path="/nonexistent/path.yaml")
    assert "anthropic" in config["providers"]
    assert "ollama" in config["providers"]


def test_env_var_resolution():
    os.environ["TEST_KEY_12345"] = "secret"
    result = _resolve_env_vars("${TEST_KEY_12345}")
    assert result == "secret"
    del os.environ["TEST_KEY_12345"]


def test_save_and_load():
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        path = f.name
    try:
        config = {"providers": {"test": {"key": "value"}}}
        save_config(config, path)
        loaded = load_config(path)
        assert loaded["providers"]["test"]["key"] == "value"
    finally:
        os.unlink(path)


def test_set_config_value():
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as f:
        path = f.name
    try:
        save_config({"providers": {}}, path)
        set_config_value("providers.new.key", "val", path)
        loaded = load_config(path)
        assert loaded["providers"]["new"]["key"] == "val"
    finally:
        os.unlink(path)
