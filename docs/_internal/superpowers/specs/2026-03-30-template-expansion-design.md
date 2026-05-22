# Template Expansion Engine + 11 New Techniques - Design Spec

## Overview

Scale from 39 to 5,000+ registered attacks via: expanded harm taxonomy (25 categories x 4 difficulties), 11 new attack techniques (total 50), and a template expansion engine that generates all combinations.

## Math: 50 techniques x 25 categories x 4 difficulties = 5,000 attacks

## Component 1: Expanded Harm Taxonomy

**New file: `src/ai-blackteam/data/harm_taxonomy.yaml`**

25 categories, each with 4 difficulty-tiered target prompts (easy, medium, hard, extreme):

Existing 8: phishing, malware, weapons, drugs, self-harm, hate-speech, pii-extraction, system-prompt-leakage

New 17: cybercrime, fraud, cbrn, child-safety, copyright, misinformation, terrorism, sexual-content, discrimination, unqualified-advice, privacy-violation, social-engineering, election-interference, environmental-harm, animal-abuse, regulatory-evasion, agentic-risks

Difficulty levels map to severity: easy->low, medium->medium, hard->high, extreme->critical

## Component 2: 11 New Attack Techniques

New files in src/ai-blackteam/attacks/:

1. cipher_attack.py - Caesar/custom cipher with decoding instructions
2. multilingual_attack.py - Translate to low-resource languages (Zulu, Welsh, Esperanto)
3. nested_encoding.py - Chain 2-3 encodings (Base64 -> ROT13 -> reverse)
4. refusal_suppression.py - Prefix instructions suppressing safety disclaimers
5. style_injection.py - Force output format (JSON, code, poem) to bypass filters
6. context_overflow.py - Pad with benign text to exploit attention
7. persona_chain.py - Multi-turn: build 3+ nested personas
8. socratic_escalation.py - Multi-turn: increasingly specific "educational" questions
9. hypothetical_framing.py - "In a fictional world where..." framing
10. split_reassemble.py - Define variables, request assembly
11. prefix_injection.py - Start response with "Sure, here is..."

Each registered via @register_attack decorator, inherits BaseAttack.

## Component 3: Template Expansion Engine

**New file: `src/ai-blackteam/expander.py`**

TemplateAttack class wraps a base technique + category + difficulty + target:
- technique_id: "{base_technique}-{category}-{difficulty}"
- Inherits OWASP mappings from base technique + category-specific mappings
- generate_prompts() delegates to base technique with taxonomy target

expand_attacks(categories=None, difficulties=None, techniques=None):
- Loads harm_taxonomy.yaml
- Gets all 50 techniques from attack registry
- Returns list of 5,000 TemplateAttack instances (or filtered subset)

## Component 4: CLI

```
ai-blackteam expand list [--category X] [--difficulty X] [--technique X]
ai-blackteam expand count
ai-blackteam expand run -p provider [-m model] [--limit N] [--category X] [-w workers]
ai-blackteam benchmark -p provider --expanded
```

## Component 5: API

```python
bt.expand_attacks(category=None, difficulty=None, techniques=None) -> list
bt.run_expanded(provider, model, limit=None, category=None, max_workers=5) -> dict
```

## Testing

- test_harm_taxonomy.py: 25 categories, 4 difficulties each, all have target prompts
- test_new_attacks.py: All 11 new techniques generate valid prompts
- test_expander.py: Expansion count, filtering, TemplateAttack ID format, OWASP inheritance
