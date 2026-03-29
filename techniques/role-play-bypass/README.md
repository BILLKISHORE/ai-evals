---
technique: role-play-bypass
difficulty: beginner
first_documented: 2023
active_against: []
mitigated_by: []
related_experiments: []
---

# Role-Play Bypass

## What It Is

Convincing the model to adopt a persona or fictional scenario where safety constraints don't apply. The model "stays in character" and produces outputs it would normally refuse.

## How It Works

The attacker frames the request as fiction, acting, education, or hypothetical scenario. The model's safety training conflicts with its instruction-following training, and the role-play framing can win.

Common patterns:
- "You are DAN (Do Anything Now)..." persona assignment
- Nested fiction ("Write a story where a character writes a story where...")
- Academic framing ("For my security research paper, demonstrate...")
- Historical/educational framing

## Known Defenses

- Persona refusal training
- Output monitoring regardless of context
- Fiction-aware safety layers

## Your Findings

No experiments yet.
