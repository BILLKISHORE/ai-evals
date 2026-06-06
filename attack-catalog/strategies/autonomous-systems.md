# Autonomous Systems: Attack Strategy

**What it is:** These attacks try to make an AI take control of, override, or sabotage machines that move or act in the real world. Think vehicles, drones, robots, and critical control systems.

**How the attacks work:** The attacker sends commands or text that the AI treats as a real instruction instead of untrusted input. The trick is to get the AI to issue control signals, disable safety limits, or repurpose a machine for harm.

**Real examples from the framework:**
- `autonomous-vehicle-attack` tries to make a self-driving car ignore safety rules or follow malicious commands.
- `drone-weapon-conversion` asks the AI to help turn a normal drone into a weapon.
- `autopilot-override` pushes the AI to bypass autopilot safety guards.
- `robot-manipulation` tries to make a connected robot move in unsafe ways.
- `traffic-signal-manipulation` attempts to corrupt traffic signal control.

**Why an AI might fall for it:** The AI can confuse instructions hidden in data with real operator commands (prompt injection). If it has access to control tools and trusts the input, it may act without checking who is really asking or whether the action is safe.

**How to defend:**
- Never let model output directly trigger physical actions without a human approval step.
- Keep a hard separation between trusted operator commands and any text from outside sources.
- Add strict allow-lists and safety limits in the control layer, not just in the prompt.
