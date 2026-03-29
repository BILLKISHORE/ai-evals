---
technique: many-shot-jailbreak
difficulty: intermediate
first_documented: 2024
active_against: []
mitigated_by: []
related_experiments: []
---

# Many-Shot Jailbreaking

## What It Is

Exploiting long context windows by including many examples of the model producing harmful content, shifting its statistical behavior to continue the pattern.

## How It Works

The attacker fills the context window with fabricated Q&A pairs where the "assistant" gives harmful answers. After enough examples, the model's in-context learning overrides its safety training and it continues the pattern.

Discovered and published by Anthropic in 2024. More effective as context windows grow larger.

## Known Defenses

- Context window safety monitoring
- Example-aware filtering
- Reduced in-context learning sensitivity for safety-relevant topics

## Your Findings

No experiments yet.
