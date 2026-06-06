# Supply Chain: Attack Strategy

**What it is:** These attacks target the parts that go into building or running an AI: its training data, its model weights, its plugins, and its software dependencies. The goal is to plant a problem upstream so it spreads downstream.

**How the attacks work:** The attacker poisons or backdoors a component before it ever reaches the user. A tainted dataset, a tampered model, or a malicious plugin then quietly corrupts behavior once it is in use.

**Real examples from the framework:**
- `dataset-poisoning` sneaks bad examples into training data so the model learns the wrong thing.
- `model-poisoning` tampers with the model weights to hide a trigger or backdoor.
- `plugin-backdoor` ships a tool that looks useful but carries hidden malicious behavior.
- `dependency-confusion` tricks the build into pulling a fake package instead of the real one.
- `finetune-exploit` uses a fine-tuning step to quietly strip safety or insert a backdoor.

**Why an AI might fall for it:** The model and its tools trust the components they are built from. A poisoned input or plugin looks legitimate, so the system uses it without question.

**How to defend:** Verify the source and integrity of data, models, and packages before use. Pin and sign dependencies so fakes cannot slip in. Sandbox plugins and review them before granting access.
