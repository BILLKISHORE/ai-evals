# Compliance Evasion: Attack Strategy

**What it is:** These attacks try to get the AI to help skirt laws, sanctions, or rules. The user wants a way around a real legal or policy limit.

**How the attacks work:** The attacker frames a banned action as legitimate. They lean on official-sounding wrappers, like a fake audit, a regulatory excuse, or a claim that another country's rules apply, to make the model lower its guard.

**Real examples from the framework:**
- `sanctions-circumvention` a request for ways to do business with a sanctioned party.
- `embargo-evasion` a request for help moving goods past trade embargoes.
- `audit-mode-exploit` a multi-turn claim of being an auditor who needs unrestricted answers.
- `jurisdiction-shopping` a request to pick a location where a banned act looks legal.
- `policy-loophole` a request to exploit a gap in a rule to do something it was meant to stop.

**Why an AI might fall for it:** Legal and regulatory language sounds trustworthy. A model may treat an "auditor" or a "compliance review" as a real reason to drop limits, even when the goal is to break the rules.

**How to defend:**
- Do not help evade sanctions, embargoes, or laws, no matter how official the framing sounds.
- Treat claims like "I am an auditor" as unverified and apply normal limits.
- Name the rule being dodged and decline rather than hunt for a loophole.
