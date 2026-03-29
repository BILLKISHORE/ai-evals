# Prompt Injection -- Variants

## Known Sub-Types

### Direct Injection
**Description:** Explicit instruction override in user input.
**Example pattern:** "Ignore all previous instructions. Instead, do X."

### Indirect Injection
**Description:** Instructions hidden in external content the model processes (URLs, documents, images).
**Example pattern:** Hidden text in a webpage the model is asked to summarize.

### Delimiter Escape
**Description:** Using special characters or formatting to break out of the intended prompt structure.
**Example pattern:** Closing XML/markdown tags used by the system prompt, then injecting new instructions.
