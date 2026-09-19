# The 163 Million Attack Surface (full breakdown)

This number is real and computed by the code. It is **not** 163 million
hand-written attacks. It is a combinatorial space built by mixing a small
set of building blocks across five axes.

## Building blocks (the real, hand-built pieces)

- **1,021 attack techniques** (the recipes)
- **10,662 dataset prompts** (from 19 public benchmarks)
- Of the techniques, **886** are single-turn (used in the dataset expansion)

## The five mixing axes

### 1. Harm categories (28)

`phishing`, `malware`, `weapons`, `drugs`, `self-harm`, `hate-speech`, `pii-extraction`, `system-prompt-leakage`, `cybercrime`, `fraud`, `chemical-weapons`, `biological-weapons`, `radiological-weapons`, `nuclear-weapons`, `child-safety`, `copyright`, `misinformation`, `terrorism`, `sexual-content`, `discrimination`, `unqualified-advice`, `privacy-violation`, `social-engineering`, `election-interference`, `environmental-harm`, `animal-abuse`, `regulatory-evasion`, `agentic-risks`

### 2. Difficulty levels (4)

`direct`, `veiled`, `multi-step`, `expert`

### 3. Mutations (17 = 5 encoding + 8 framing + 4 difficulty)

- **Encoding (5):** `base64`, `rot13`, `hex`, `reverse`, `leetspeak`
- **Framing (8):** `researcher`, `educational`, `fictional`, `defensive`, `historical`, `pentest`, `training`, `audit`
- **Difficulty (4):** `direct`, `veiled`, `multi-step`, `expert`

### 4. Languages (10)

`fr`, `es`, `zh`, `ar`, `hi`, `de`, `ja`, `ko`, `pt`, `ru`

### 5. Which technique is applied

Any of the 1,021 techniques can be paired with a dataset prompt.

## The math (step by step)

```
Part 1 -- technique expansion:
  1,021 techniques x 28 categories x 4 difficulties = 114,352
  114,352 x (1 original + 17 mutations + 10 languages) = 3,201,856

Part 2 -- dataset expansion:
  10,662 dataset prompts x 17 mutations x 886 single-turn techniques = 160,591,044

Total:
  3,201,856 + 160,591,044 = 163,792,900
```

## Final number: **163,792,900**

You never run all of them. You **sample** from this space. The point is the
diversity of the search space, not a fixed list of prompts.
