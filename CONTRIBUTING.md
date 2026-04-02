# Contributing to mordor

## Adding a New Provider

1. Create `src/mordor/providers/your_provider.py`
2. Extend `BaseProvider` and implement `send_prompt`, `send_in_conversation`, `default_model`
3. Decorate with `@register_provider("your-provider")`
4. Add default config in `config.py` DEFAULT_CONFIG
5. Add tests in `tests/test_attacks.py` or a new test file

## Adding a New Attack

1. Create `src/mordor/attacks/your_attack.py`
2. Extend `BaseAttack` and set `name`, `technique_id`, `mode`
3. Implement `generate_prompts()` for single-turn, `generate_turns()` for multi-turn
4. Decorate with `@register_attack("your-attack")`
5. Add a test verifying prompt count and format

## Running Tests

```bash
poetry run pytest tests/ -v
```

## Code Style

- Write code like a human. No verbose docstrings on obvious methods.
- Follow existing patterns in the codebase.
- One file per provider/attack. Keep files focused.
