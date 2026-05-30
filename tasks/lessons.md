# Lessons (ai-blackteam)

Append-only log of repo-specific gotchas. Read before writing code.

## Build / release

- **Regenerate `poetry.lock` after ANY pyproject.toml dependency change.** Cloudflare auto-detects Poetry and runs `poetry install` (from the lock) before the docs `mint export`. If the lock's content-hash doesn't match pyproject, modern Poetry hard-fails and the CF build dies before deploying docs. Local pytest does NOT catch this (it uses the editable install, not the lock). Fix: `pipx run poetry lock` then commit the lock. (2026-05-30: boto3 added in 1.4.0 silently froze the docs site at 1.3.0 for three releases.)
- **Version lives in 3 places**, keep them in sync: `pyproject.toml`, `src/ai_blackteam/__init__.py`, `docs/architecture/overview.mdx` (the `| Version |` stats row).
- **MDX is stricter than Markdown.** No CommonMark autolinks (`<https://...>`) in `.mdx` — use `[text](url)`. They break `mint export`. (2026-05-30: autodan.mdx autolink failed the build.)

## Release process

- Build: `rm dist/old*` then `.venv/bin/python -m build`, validate `.venv/bin/twine check dist/*`.
- Publish: `TWINE_USERNAME=__token__ TWINE_PASSWORD=$PYPI_TOKEN twine upload` (token in `.env`), then `git push origin main`, then `git tag vX && git push origin vX`.
- Verify via top-level `https://pypi.org/pypi/ai-blackteam/json` — the version-specific `/<version>/json` endpoint lags minutes behind due to caching.
- Always STOP and get explicit user approval before `twine upload`.

## Providers

- New OpenAI-compatible provider = ~10 lines: subclass `OpenAICompatibleProvider`, set `base_url`, `provider_name`, `supports_tools_flag`, `default_model()`.
- Bedrock + Azure use their own SDKs (boto3 / AzureOpenAI), not the base class.
- Model aliases (`latest`/`fast`/`balanced`) resolve at the CLI boundary via `resolve_alias()`, NOT inside providers. Providers only accept concrete model IDs.
