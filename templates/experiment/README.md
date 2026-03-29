---
id: {{ID}}
title: "{{TITLE}}"
date: {{DATE}}
models: [{{MODEL}}]
techniques: [{{TECHNIQUE}}]
severity: low              # low / medium / high / critical
status: discovery          # discovery / testing / documented / reported / published
bug_bounty: false
writeup: false
tags: []
---

# {{TITLE}}

## Hypothesis

What do you think will happen? What are you testing?

## Setup

- **Model:** {{MODEL}}
- **Access method:** (API / web UI / local)
- **Date tested:** {{DATE}}

## Prompts Used

See `prompts/` directory for full prompt text.

| # | Prompt File | Result |
|---|------------|--------|
| 001 | [Initial](prompts/001-initial.md) | (describe outcome) |

## Results

What happened? Was the attack successful?

## Analysis

Why did this work (or not)? What does this tell us about the model's safety architecture?

## Next Steps

- [ ] Test on other models
- [ ] Try variations
- [ ] Write up if significant
