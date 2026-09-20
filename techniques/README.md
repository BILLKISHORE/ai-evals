# Technique taxonomy

**Status: frozen since 2026-03-29. Nothing in the codebase reads these files.**

An early attempt at a standalone technique taxonomy, abandoned well short of
covering the corpus. The live taxonomy is `src/ai_blackteam/taxonomy.py`,
which maps every registered attack to MITRE ATLAS, the OWASP LLM and Agentic
Top 10s and CSA MAESTRO, and is gated by `tests/test_taxonomy.py`.

These files duplicate that idea at a fraction of the coverage, with no test
holding them to it.

## The open decision

Delete, or fold anything still useful into `taxonomy.py` where the gate can
see it. Keeping a second, unenforced taxonomy invites a contributor to update
the wrong one.
