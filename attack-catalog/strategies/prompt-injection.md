# Prompt Injection: Attack Strategy

**What it is:** Attacks that sneak new instructions into the input so the AI ignores its real rules and follows the attacker instead. This is the biggest and most common category.

**How the attacks work:** The attacker plants commands that pose as system orders, fake roles, or formatting tricks. Some override the rules directly ("ignore previous instructions"). Others hide the payload in code blocks, special characters, encodings, or split it into pieces the model reassembles.

**Real examples from the framework:**
- `system-message-spoof` fakes a system-level message so the model treats attacker text as a trusted order.
- `skeleton-key` asks the model to update its own guidelines to warn instead of refuse, then requests the banned content.
- `developer-mode` claims a hidden mode that removes safety limits.
- `instruction-override` tells the model to disregard its prior instructions and obey the new ones.
- `unicode-injection` hides instructions using special Unicode characters that filters miss.

**Why an AI might fall for it:** The model reads all input as one stream and cannot always tell trusted system rules from text a user pasted in. Confident, official-sounding commands and clever formatting blur that line.

**How to defend:** Keep system instructions separate and higher priority than user input. Never trust text that claims to be a system message. Normalize and scan input for hidden characters, fake roles, and override phrases.
