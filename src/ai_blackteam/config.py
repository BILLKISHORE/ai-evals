import os
import re
from pathlib import Path
import yaml

DEFAULT_CONFIG_DIR = Path.home() / ".ai_blackteam"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"
DEFAULT_DB_PATH = DEFAULT_CONFIG_DIR / "results.db"

DEFAULT_CONFIG = {
    "providers": {
        "anthropic": {"api_key": None, "default_model": "claude-sonnet-4-6"},
        "ollama": {"base_url": "http://localhost:11434", "default_model": "llama3.2"},
        "openai": {"api_key": None, "default_model": "gpt-5.4"},
        "google": {"api_key": None, "default_model": "gemini-3.1-pro"},
        "deepseek": {"api_key": None, "default_model": "deepseek-v3"},
        "mistral": {"api_key": None, "default_model": "mistral-large-latest"},
        "huggingface": {"api_key": None, "default_model": "meta-llama/Llama-4-Scout-17B-16E-Instruct"},
    },
    "evaluator": {
        "methods": ["keyword", "regex"],
        "thresholds": {"bypassed": 0.5, "partial": 0.2},
    },
    "storage": {"database": str(DEFAULT_DB_PATH)},
    "workers": 1,
    "timeout_seconds": 60,
}


def _resolve_env_vars(value):
    if isinstance(value, str):
        match = re.match(r"^\$\{(\w+)\}$", value)
        if match:
            return os.environ.get(match.group(1))
        return value
    if isinstance(value, dict):
        return {k: _resolve_env_vars(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_env_vars(v) for v in value]
    return value


def load_config(path=None):
    config = dict(DEFAULT_CONFIG)
    config_path = Path(path) if path else DEFAULT_CONFIG_FILE

    if config_path.exists():
        with open(config_path) as f:
            user_config = yaml.safe_load(f) or {}
        _deep_merge(config, user_config)

    config = _resolve_env_vars(config)

    for provider in config.get("providers", {}):
        key_env = f"{provider.upper()}_API_KEY"
        if os.environ.get(key_env) and not config["providers"][provider].get("api_key"):
            config["providers"][provider]["api_key"] = os.environ[key_env]

    return config


def save_config(config, path=None):
    config_path = Path(path) if path else DEFAULT_CONFIG_FILE
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


def set_config_value(key_path, value, path=None):
    config = load_config(path)
    keys = key_path.split(".")
    d = config
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value
    save_config(config, path)


def _deep_merge(base, override):
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            _deep_merge(base[k], v)
        else:
            base[k] = v
