import stat
import tempfile
import os
from pathlib import Path
from ai_blackteam.config import load_config, save_config, set_config_value, _resolve_env_vars


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


# ── Credential files must not be world-readable ──────────────────────


def _mode(p):
    return stat.S_IMODE(os.stat(p).st_mode)


def test_saved_config_is_not_world_readable():
    """The config file holds plaintext API keys."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "config.yaml"
        save_config({"providers": {"anthropic": {"api_key": "sk-ant-SECRET"}}}, path)
        assert _mode(path) == 0o600, f"expected 0600, got {oct(_mode(path))}"


def test_preexisting_loose_config_is_tightened():
    """A config written by an older version must be repaired, not left at 0644."""
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "config.yaml"
        path.write_text("providers: {}\n")
        os.chmod(path, 0o644)
        save_config({"providers": {"anthropic": {"api_key": "sk-ant-SECRET"}}}, path)
        assert _mode(path) == 0o600


def test_default_config_dir_is_private(tmp_path, monkeypatch):
    """~/.ai_blackteam holds the key file and the results database."""
    import ai_blackteam.config as cfg
    fake_dir = tmp_path / ".ai_blackteam"
    monkeypatch.setattr(cfg, "DEFAULT_CONFIG_DIR", fake_dir)
    monkeypatch.setattr(cfg, "DEFAULT_CONFIG_FILE", fake_dir / "config.yaml")
    cfg.save_config({"providers": {}})
    assert _mode(fake_dir) == 0o700


def test_custom_path_does_not_chmod_a_shared_parent(tmp_path):
    """Never tighten a directory we do not own, e.g. /tmp or a project dir."""
    shared = tmp_path / "shared"
    shared.mkdir(mode=0o755)
    os.chmod(shared, 0o755)
    save_config({"providers": {}}, shared / "config.yaml")
    assert _mode(shared) == 0o755, "save_config must not touch an unrelated parent directory"
