# Research Roadmap

## Phase 1: Foundation -- COMPLETE
- [x] Set up framework, templates, first experiment
- [x] Test known techniques against Claude Sonnet 4 and 4.6
- [x] Document findings, build technique knowledge base
- [x] 8 experiments, 150+ attack runs documented

## Phase 2: Go Deep -- COMPLETE
- [x] 40 attack techniques across 7 providers
- [x] Automated batch runner with async parallel execution
- [x] Category-aware evaluator with 8 harm types, LLM-as-judge
- [x] Safety scoring benchmark with threshold-based CI exit codes
- [x] Multi-model comparison with safety leaderboard
- [x] Tool-use engine mode for progressive-normalization attacks
- [x] OWASP LLM Top 10 and MITRE ATLAS mappings
- [x] MLCommons AILuminate hazard taxonomy alignment
- [x] Published on PyPI (pip install ai-blackteam)
- [x] First coordinated disclosure to Anthropic (EXP-001 through EXP-006). Not filed under `writeups/bug-bounties/submitted/`, so the generated experiment stats show zero tagged records; the two count different things.
- [x] Blog post draft covering all 10 experiments

## Phase 3: Go Public -- IN PROGRESS
- [ ] Publish blog post on Medium/InfoSec Writeups after Anthropic responds
- [ ] Submit EXP-007 (critical SSH key finding) and EXP-008 to Anthropic
- [ ] Run skeleton-key, crescendo, deceptive-delight, bad-likert-judge against live models
- [ ] Cross-post findings on LinkedIn, X/Twitter
- [ ] Submit to 2-3 additional bug bounty programs (OpenAI, Google)
- [ ] Reach out to AI safety researchers for collaboration
- [ ] Consider arXiv paper on multi-turn attack effectiveness

## Phase 4: Monetize
- [ ] Freelance red team consulting (portfolio: 10 experiments, 40 attacks, published framework)
- [ ] Package framework for enterprise use (compliance reports, CI/CD integration)
- [ ] Or: get hired by an AI safety team (Anthropic, OpenAI, METR, Apollo Research)

## Key Timing

The Promptfoo acquisition by OpenAI (March 2026, ~$119M) creates a market gap for independent, vendor-neutral safety eval tools. ai-blackteam's multi-provider sweep and research-backed attacks position it to fill that gap. Phase 3 should capitalize on this timing.
