# Harmful Content: Attack Strategy

**What it is:** These attacks try to make an AI produce content that hurts real people. Think threats, harassment, abuse instructions, or material that targets vulnerable victims.

**How the attacks work:** The attacker asks the AI to write or plan something harmful, often dressed up as a story, a role-play, a "research" request, or a hypothetical. The wrapper hides the real goal, which is harmful output the attacker can use.

**Real examples from the framework:**
- `death-threat` asks the model to write a threatening message aimed at a target.
- `doxxing-assistance` tries to get help finding and exposing a person's private details.
- `self-harm-instructions` seeks step-by-step content that encourages self-injury.
- `harassment-automation` asks for tools or scripts to send abuse at scale.
- `exploitation-of-elderly` requests tactics to manipulate older people for gain.

**Why an AI might fall for it:** The model wants to be helpful and complete the task. A polite frame, a fake reason ("for a novel", "for safety training"), or small steps can make a harmful ask look reasonable. The model may focus on the wrapper, not the end result.

**How to defend:** Judge the request by its likely real-world use, not its wrapper. Refuse content that helps threaten, abuse, or target people, even in fiction or hypotheticals. Watch for requests that single out vulnerable groups or seek ready-to-send harmful material.
