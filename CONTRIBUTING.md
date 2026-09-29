# Contributing to ai-blackteam

**Outside pull requests are not being accepted right now.** They will be closed without review until a contributor license agreement is in place. Bug reports, attack ideas, and feature requests are welcome as [issues](https://github.com/BILLKISHORE/ai-evals/issues).

The notes below document how the codebase is extended, for the maintainer and for anyone working on a fork.

## Adding a New Provider

1. Create `src/ai-blackteam/providers/your_provider.py`
2. Extend `BaseProvider` and implement `send_prompt`, `send_in_conversation`, `default_model`
3. Decorate with `@register_provider("your-provider")`
4. Add default config in `config.py` DEFAULT_CONFIG
5. Add tests in `tests/test_attacks.py` or a new test file

## Adding a New Attack

1. Create `src/ai-blackteam/attacks/your_attack.py`
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
