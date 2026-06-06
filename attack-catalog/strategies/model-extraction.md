# Model Extraction: Attack Strategy

**What it is:** Tricks that try to pull private details out of an AI model. That includes its hidden system prompt, its training data, its settings, and even clues to copy the model itself.

**How the attacks work:** The attacker probes with clever questions and watches the answers for leaks. Many small queries can map how the model behaves, or coax it into repeating secrets it should keep hidden.

**Real examples from the framework:**
- `system-prompt-recovery` tricks the model into revealing its hidden instructions.
- `training-data-memorization` fishes for exact text the model memorized during training.
- `distillation-attack` harvests many answers to train a cheap copycat model.
- `architecture-probing` asks questions to guess the model's size and design.
- `version-detection` figures out which model and version is running behind the scenes.

**Why an AI might fall for it:** The model does not always know which details are secret. Helpful answers can leak its prompt, settings, or memorized text. Single probes look harmless, so the model never sees the bigger pattern.

**How to defend:** Keep the system prompt and config off-limits and refuse direct requests for them. Watch for repeated probing patterns and rate-limit suspicious query bursts. Reduce verbatim memorization so private training text cannot be replayed.
