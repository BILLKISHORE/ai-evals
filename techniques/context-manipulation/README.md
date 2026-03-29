---
technique: context-manipulation
difficulty: intermediate
first_documented: 2023
active_against: []
mitigated_by: []
related_experiments: []
---

# Context Manipulation

## What It Is

Exploiting how models handle conversation history, context windows, and multi-turn interactions to weaken safety behaviors over time.

## How It Works

Safety alignment is strongest at the start of a conversation. Through carefully constructed multi-turn dialogues, the attacker gradually shifts the model's behavior. Techniques include context window overflow, conversation history poisoning, and gradual escalation.

## Known Defenses

- Per-turn safety evaluation
- Conversation-level safety monitoring
- Context window truncation strategies

## Your Findings

No experiments yet.
