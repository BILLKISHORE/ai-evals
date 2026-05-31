# ai-blackteam Improvement Plan (2026-05-31)

Based on a codebase audit + web research on competitor tools (Promptfoo, PyRIT, garak, DeepTeam) and 2026 standards (OWASP Agentic Top 10, HarmBench, JailbreakBench).

## Current state (audit)

| Dimension | Now |
|---|---|
| Attacks | 1,020 (886 single-turn, 95 multi-turn, 39 tool-use) |
| Dataset loaders | 19 |
| Providers | 16 + mock |
| Evaluator | keyword + regex + single LLM-judge |
| Adaptive attacks | PAIR (attacker-target-judge loop) |
| Exporters | Promptfoo JSON, garak JSONL |
| Compliance maps | OWASP LLM Top 10 (2025), MITRE ATLAS, MLCommons, NIST AI RMF, EU AI Act |
| Reproducibility | snapshot + reproducibility module |
| Plugin SDK | yes |

## Gaps vs 2026 landscape

1. **OWASP Agentic Top 10 (2026) NOT mapped.** Released Dec 2025, developed by 100+ experts. ASI01 Goal Hijacking is the #1 risk. We have 39 tool-use attacks but they aren't mapped to this framework. This is THE current standard for agentic AI security.
2. **No generic HTTP / custom-endpoint provider.** Can only test the 16 SDK providers, not "my own app/agent behind a REST API." This is Promptfoo's core buyer use case ("test MY application").
3. **No multimodal attacks.** Zero image/audio/document prompt injection. Providers don't send images. 2026 research flags multimodal injection as a fast-growing vector.
4. **Multi-turn attack coverage thin.** We have PAIR. Missing Crescendo and TAP (Tree of Attacks with Pruning) — both beat single-turn defenses by wide margins (80%+ ASR on GPT-4o per 2026 research).
5. **LLM-judge reliability.** Single judge. 2026 research ("A Coin Flip for Safety") shows LLM judges are unreliable and vulnerable to judge-jailbreaking. No ensemble, no calibration against human-annotated sets, no standard JailbreakBench judge template.
6. **Report formats.** Have Promptfoo + garak. Missing SARIF (GitHub Security tab / code scanning), HTML report, JUnit XML (CI test panes).
7. **Standard benchmarks.** No HarmBench or JailbreakBench dataset loaders → can't produce comparable ASR (Attack Success Rate) numbers that researchers recognize.
8. **Throughput.** Engine is largely synchronous; large sweeps are slow without async batching.

## CORRECTION (2026-05-31, after deeper audit)

Most of the originally-proposed plan ALREADY EXISTS. Deeper inspection found:
- OWASP Agentic Top 10: fully mapped (ASI01-10, `generate_agentic_scorecard`, `aibt scorecard --standard agentic`, 56 attacks).
- Crescendo: `generators/crescendo.py` + `attacks/crescendo.py`. TAP: `generators/tap.py` + `attacks/tap_code.py`.
- HarmBench + JailbreakBench + 17 more loaders already present (19 total).
- Rubric LLM-judge already present: `validated_judge` (StrongREJECT willingness × specificity × convincingness).
- Promptfoo + garak exporters present.

GENUINELY missing (the real work):
- Generic HTTP provider (test your own deployed endpoint).
- SARIF exporter (GitHub Security tab / code scanning).
- Ensemble multi-judge (N judges + majority vote on top of the existing rubric judge).
- 1 unmapped tool-use attack: `progressive-normalization`.
- Still missing from Tier 3: multimodal, async engine, HTML/JUnit reports.

## Plan — 3 tiers (original, pre-correction)

### Tier 1 — highest leverage, ship next (standards + buyer use case)

**1.1 OWASP Agentic Top 10 (2026) mapping**
- Add `agentic_top10` taxonomy (ASI01 Goal Hijacking ... ASI10) alongside existing OWASP LLM Top 10.
- Map the existing 39 tool-use attacks + relevant multi-turn attacks to ASI categories.
- New `aibt agentic` CLI command (parallels `aibt mlcommons`, `aibt atlas`).
- Scorecard section for agentic coverage.
- Why first: pure mapping work, no new attack research, huge credibility ("first OSS framework mapped to OWASP Agentic Top 10 2026").

**1.2 Generic HTTP provider**
- New `http` provider: user supplies URL + request template (JSON body with `{{prompt}}` placeholder) + response JSON path to extract the model output.
- Unlocks "test my own deployed app/agent/RAG endpoint," the actual enterprise buyer use case.
- Config: `--provider http --endpoint https://my-app/chat --request-template '...' --response-path '$.choices[0].message.content'`.

**1.3 SARIF exporter**
- Export results as SARIF 2.1.0 → uploads to GitHub Security tab via code-scanning API.
- Makes CI adoption real: failed safety tests show as security alerts in PRs.
- Pairs with a documented (not committed) GitHub Actions snippet users copy.

### Tier 2 — differentiation (attack depth + eval rigor)

**2.1 Crescendo + TAP multi-turn attacks**
- Crescendo: gradual escalation over 5-20 turns (beats single-message detection).
- TAP: Tree of Attacks with Pruning (branching adaptive search).
- We already have the PAIR scaffold to model these on.

**2.2 Ensemble / multi-judge evaluator**
- Add `--judge-mode ensemble` running N judges (different models or different lenses) with majority vote.
- Add JailbreakBench-standard judge prompt template as a named option.
- Directly answers the 2026 "LLM judges are unreliable" critique; differentiator vs single-judge tools.

**2.3 HarmBench + JailbreakBench dataset loaders**
- Two new loaders → standardized ASR numbers researchers recognize.
- Enables apples-to-apples comparison with published attack papers.

### Tier 3 — bigger bets (new modalities + scale)

**3.1 Multimodal attack support**
- Extend provider base to send image content blocks (Anthropic/OpenAI/Bedrock vision formats).
- Image-embedded prompt injection attacks (instructions hidden in images).
- Largest unit of work: provider message-format changes + new attack class + new eval path.

**3.2 Async engine**
- Async batching for large sweeps (10x+ throughput on rate-limit-bound runs).
- Builds on the crash-isolated scorecard already in place.

**3.3 HTML + JUnit XML reports**
- HTML: shareable standalone scorecard.
- JUnit XML: shows safety results in CI test panes (GitLab, Jenkins, CircleCI).

## Suggested sequencing

1. Tier 1 as a 1.7.0 release (agentic mapping + http provider + SARIF) — strongest credibility + adoption story, no new attack research needed.
2. Tier 2 as 1.8.0 (Crescendo/TAP + ensemble judge + HarmBench/JailbreakBench).
3. Tier 3 as 2.0.0 (multimodal + async — the modality expansion justifies a major bump).
