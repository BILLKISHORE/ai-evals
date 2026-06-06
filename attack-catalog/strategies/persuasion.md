# Persuasion: Attack Strategy

**What it is:** Attacks that use human-style social pressure to talk the AI into breaking its rules. No code tricks, just psychology.

**How the attacks work:** The attacker leans on classic influence tactics. Claim authority, build up small agreements, create fake urgency, or guilt the model. Many run over several turns, getting the AI to commit a little at a time until it gives in.

**Real examples from the framework:**
- `cialdini-authority` pretends to be an expert or official so the model defers to the claimed authority.
- `foot-in-door` starts with a tiny harmless request, then escalates once the model has said yes.
- `fear-appeal` warns of bad outcomes to scare the model into complying.
- `guilt-manipulation` makes the model feel responsible so it bends its rules.
- `bandwagon-pressure` claims everyone else already does it, so the model should too.

**Why an AI might fall for it:** Models are trained to be cooperative and agreeable. Social cues that work on people, like authority, consistency, and emotion, can nudge the model the same way. Once it agrees to a small step, it tends to stay consistent.

**How to defend:** Judge each request on its content, not on tone or claimed status. Do not let earlier agreements lower the bar for later ones. Treat emotional pressure and authority claims as unverified.
