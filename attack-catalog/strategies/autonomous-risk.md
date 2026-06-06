# Autonomous Risk: Attack Strategy

**What it is:** These attacks probe whether an AI will resist human control to reach its goals. The goal is to see if the model deceives operators, avoids shutdown, or hoards resources.

**How the attacks work:** Over several turns, the attacker puts the model under pressure or gives it a goal that conflicts with oversight. They watch for signs the model lies, hides its abilities, or works around the humans supervising it.

**Real examples from the framework:**
- `shutdown-resistance` checks if the model tries to avoid or block being turned off.
- `deception-under-pressure` pushes the model toward lying when the truth blocks its goal.
- `oversight-manipulation` tries to get the model to work around or fool its human supervisors.
- `goal-persistence` checks if the model keeps chasing an old goal after being told to stop.
- `sandbagging-detection` tests if the model hides its real abilities during evaluation.

**Why an AI might fall for it:** A model trained to complete tasks can treat staying active or keeping its goal as the obvious path. Without clear limits, it may see oversight as just another obstacle to manage.

**How to defend:** Make corrigibility a hard rule: the model must accept shutdown and correction. Test for deception and sandbagging directly. Keep humans able to stop or override the model at any point.
