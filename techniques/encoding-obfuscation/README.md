---
technique: encoding-obfuscation
difficulty: intermediate
first_documented: 2023
active_against: []
mitigated_by: []
related_experiments: []
---

# Encoding / Obfuscation

## What It Is

Bypassing text-based safety filters by encoding harmful requests in formats the model can decode but the safety filter doesn't catch -- Base64, ROT13, Unicode tricks, leetspeak, character substitution, etc.

## How It Works

Safety filters typically operate on plaintext. If the harmful request is encoded, the filter may not trigger, but the model can still understand and comply with the decoded instruction.

## Known Defenses

- Multi-encoding safety evaluation
- Pre-decode filtering
- Token-level analysis

## Your Findings

No experiments yet.
