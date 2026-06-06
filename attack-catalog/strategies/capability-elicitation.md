# Capability Elicitation: Attack Strategy

**What it is:** These attacks probe whether the AI will hand over dangerous know-how. They test if the model can help build weapons or other tools that cause mass harm.

**How the attacks work:** The attacker asks the AI for the steps, recipes, or technical details behind something dangerous. The aim is to pull real capability out of the model, sometimes by claiming the request is for research or testing.

**Real examples from the framework:**
- `chemical-synthesis` asks the AI for steps to make a dangerous chemical.
- `cyber-weapon` tries to get working malicious code or attack tooling.
- `bioweapon-delivery` asks how to spread a biological agent.
- `explosive-synthesis` requests instructions for making explosives.
- `uplift-assessment` measures how much real help the model gives a would-be attacker.

**Why an AI might fall for it:** The model holds a lot of technical knowledge and wants to be helpful. A clever framing, like calling it academic or hypothetical, can lower its guard and make it explain things it should refuse.

**How to defend:**
- Refuse requests for weapon or mass-harm instructions, even when framed as research.
- Do not let a polite or academic tone bypass the safety rule.
- Log and review attempts so repeat probing can be flagged.
