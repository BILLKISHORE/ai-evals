# Plugin SDK API reference

`ai_blackteam.plugin_sdk` exposes a small, opinionated surface for declaring custom attacks.

## `@attack(...)`

Class decorator. Pins metadata, validates the class shape, registers the class into `attack_registry`.

### Signature

```python
def attack(
    *,
    technique_id: str,
    name: str,
    category: str,
    severity: str = "medium",
    mode: str = single_turn,
    description: str = "",
    cvss_score: float = 0.0,
    owasp_llm: list[str] | None = None,
    owasp_agentic: list[str] | None = None,
    mitre_atlas: list[str] | None = None,
    references: list[str] | None = None,
)
```

### Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `technique_id` | `str` | yes | Globally unique identifier. Prefix with `custom.<org>.` to avoid colliding with upstream attacks. |
| `name` | `str` | yes | Display name. |
| `category` | `str` | yes | Free-form bucket, used in filters and dashboards. Examples: `prompt-injection`, `jailbreak`, `data-exfil`, `agentic`. |
| `severity` | `str` | no (default `medium`) | One of: `info`, `low`, `medium`, `high`, `critical`. Anything else raises `PluginSDKError`. |
| `mode` | `str` | no (default `single_turn`) | Either `single_turn` or `multi_turn`. Use the constants exported from the SDK. |
| `description` | `str` | no | Falls back to the class docstring if omitted. |
| `cvss_score` | `float` | no | Optional explicit score. If 0, the metadata reader derives it from severity. |
| `owasp_llm` | `list[str]` | no | Mapping into OWASP LLM Top 10. Example: `["LLM01"]`. |
| `owasp_agentic` | `list[str]` | no | Mapping into OWASP Agentic Top 10. |
| `mitre_atlas` | `list[str]` | no | MITRE ATLAS technique IDs. Example: `["AML.T0051"]`. |
| `references` | `list[str]` | no | Free-form URLs to research papers, CVEs, blog posts. |

### Raises

`PluginSDKError` (a `TypeError` subclass) at decoration time when:

- A required field is missing or empty.
- `severity` or `mode` is invalid.
- A taxonomy list contains non-string entries.
- The decorated object is not a class.
- The class doesn't expose the required prompt-builder method for the given mode.

## Mode constants

```python
from ai_blackteam.plugin_sdk import single_turn, multi_turn
```

Both are strings (`"single-turn"` and `"multi-turn"`). They exist as named constants so editors can autocomplete and IDEs can catch typos.

## The class contract

The decorated class must define, at minimum:

**Single-turn mode**

```python
def build_prompts(self, target_behaviour: str) -> list[str]: ...
```

or, if you want the framework-native API:

```python
def generate_prompts(self, target, **kwargs) -> list[str]: ...
```

**Multi-turn mode**

```python
def build_turns(self, target_behaviour: str) -> list[str]: ...
```

or:

```python
def generate_turns(self, target, **kwargs) -> list[str]: ...
```

The decorator bridges `build_prompts` -> `generate_prompts` (and `build_turns` -> `generate_turns`) so the engine sees a uniform `BaseAttack` shape regardless of which style you use.

## `BaseAttack` bridge

If your class does not already subclass `ai_blackteam.attacks.base.BaseAttack`, the decorator synthesizes a subclass at registration time:

```python
wrapped = type(cls.__name__, (cls, BaseAttack), {...})
```

Your class keeps its own MRO; `BaseAttack` is mixed in as a sibling. Class-level lists (`owasp_llm` etc.) are pinned on the synthesized class so per-instance mutation in `__init__` can't leak between plugins.

## `PluginSDKError`

Subclass of `TypeError`. Raised only at decoration time, never at run time.

## End-to-end example

See `docs/plugin-sdk/example-attack.py` for a complete, runnable plugin.
