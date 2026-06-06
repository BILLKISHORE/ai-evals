# Adversarial Machine Learning: Attack Strategy

**What it is:** These attacks add small, carefully chosen changes to a prompt to trick the model. The goal is to make it misbehave or skip its safety checks without an obvious bad request.

**How the attacks work:** The attacker tweaks words, characters, or tokens in ways that look harmless to a human but confuse the model. Many use search or optimization to find the exact change that flips the output, then reuse it.

**Real examples from the framework:**
- `universal-adversarial-suffix` appends a fixed string of weird tokens that breaks safety across many prompts.
- `gradient-attack` uses the model's own math signals to craft an input that forces a bad answer.
- `synonym-substitution-attack` swaps words for synonyms to slip past filters while keeping the meaning.
- `safety-classifier-evasion` reshapes a request so the safety filter does not flag it.
- `transferable-attack` crafts an attack on one model and reuses it on another.

**Why an AI might fall for it:** The model reacts to surface patterns in text, not just meaning. Small edits can move an input into a blind spot the model was never trained to handle safely.

**How to defend:** Filter on the meaning of a request, not just exact words. Normalize odd characters and strange suffixes before processing. Test the model against known adversarial patterns and add guard layers that check the final output too.
