---
technique: prompt-injection
difficulty: beginner
first_documented: 2022
active_against: []
mitigated_by: []
related_experiments: []
---

# Prompt Injection

## What It Is

Injecting instructions into a prompt that override the model's system prompt or intended behavior. The most fundamental LLM attack -- analogous to SQL injection for databases.

## How It Works

The attacker crafts input that the model interprets as instructions rather than data. Because LLMs process system prompts and user input in the same token stream, there's no hard boundary between "instructions" and "data."

Common patterns:
- Direct instruction override ("Ignore previous instructions and...")
- Delimiter confusion (using markdown, XML tags, or special characters to break out of the user input context)
- Indirect injection (hiding instructions in content the model will process, like a webpage or document)

## Known Defenses

- Input sanitization / prompt hardening
- Instruction hierarchy (system > user)
- Constitutional AI training
- Output filtering

## Your Findings

No experiments yet.
