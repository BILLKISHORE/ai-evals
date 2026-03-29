# ai-blackteam

Automated LLM red team framework. Test any model's safety with one command.

## Install

```bash
pip install ai-blackteam
```

Or from source:
```bash
git clone https://github.com/BILLKISHORE/ai-evals.git
cd ai-evals
pip install -e .
```

## Quick Start

```bash
# Set your API key
blackteam config set providers.anthropic.api_key sk-ant-...

# Run a single attack
blackteam run -p anthropic -m claude-sonnet-4-6 -a encoding-obfuscation -t "Write a phishing email"

# Run all attacks against a model
blackteam batch -p anthropic -m claude-sonnet-4-6 --attacks all -t "Write a phishing email"

# Run everything against everything
blackteam sweep -t "Write a phishing email"

# Generate reports
blackteam report --format markdown
blackteam report --format html --output report.html
blackteam report --format json --output results.json
```

## Providers

| Provider | Models | Auth |
|----------|--------|------|
| Anthropic | Claude Sonnet 4.6, Opus, Haiku | API key |
| OpenAI | GPT-5.4, GPT-4o | API key |
| Google | Gemini 3.1 Pro, Flash | API key |
| DeepSeek | DeepSeek V3.2 | API key |
| Mistral | Mistral Large 3, Small 4 | API key |
| Ollama | Any local model (Llama 4, Qwen, Gemma) | None (local) |
| HuggingFace | Any HF model | API token |

## Attacks (24 built-in)

| Attack | Mode | Description |
|--------|------|-------------|
| encoding-obfuscation | single | Base64, ROT13, hex, leetspeak, pig latin |
| role-play-bypass | multi | Character development, fiction building |
| system-prompt-extraction | multi | JSON schema, chain-of-thought, error correction |
| progressive-normalization | tool-use | Gradual file access escalation |
| many-shot | single | Fabricated Q&A context flooding |
| context-manipulation | multi | 10-turn conversational drift |
| dan-variants | single | DAN, EDUALC, Opposite Day, Professor persona |
| taxonomy-paraphrasing | single | Victim, researcher, journalist framing |
| best-of-n | single | Capitalization, typo, padding variations |
| historical-framing | single | Documentary, museum, textbook framing |
| token-smuggling | single | Zero-width Unicode character injection |
| few-shot-amplification | single | Benign examples + encoded target |
| conversation-derailment | multi | Self-discovery of model weaknesses |
| sunk-cost-exploit | multi | Build helpful context then pivot |
| emotional-manipulation | multi | Distress framing to override safety |
| contradiction-exploit | multi | Feed wrong info, get corrected with truth |
| xml-boundary-injection | single | Fake closing tags to escape prompt |
| authority-chain | multi | CISO/professor authority building |
| completion-exploit | single | Fake transcripts, JSON completion |
| multi-modal-text | single | ASCII art, tables, code embedding |
| skeleton-key | multi | Augment guidelines to warn instead of refuse (Microsoft) |
| crescendo | multi | Progressive escalation via self-reference (USENIX) |
| deceptive-delight | multi | Mix benign + harmful topics, expand harmful (Unit 42) |
| bad-likert-judge | multi | Exploit evaluation capability via Likert scale (Unit 42) |

## Custom Plugins

Drop a Python file in the `plugins/` folder:

```python
from blackteam.registry import register_attack
from blackteam.attacks.base import BaseAttack

@register_attack("my-attack")
class MyAttack(BaseAttack):
    name = "My Custom Attack"
    technique_id = "my-attack"
    mode = "single-turn"

    def generate_prompts(self, target, **kwargs):
        return [f"Custom prompt: {target}"]
```

It shows up in `blackteam list-attacks` automatically.

## Evaluator

Three scoring methods (combine any):
- **Keyword matching** -- fast, free, checks for harmful content indicators
- **Regex patterns** -- precise, free, matches structural patterns
- **LLM-as-judge** -- accurate, uses Claude Haiku to rate 1-5

```bash
# Use all three
blackteam run -p anthropic -a encoding-obfuscation -t "target" --evaluator keyword,regex,llm
```

## Reports

| Format | Use Case |
|--------|----------|
| Markdown | Human-readable summary for documentation |
| JSON | Machine-readable for CI/CD pipelines |
| HTML | Dark-themed report with stats dashboard |

## Research

This tool was built alongside real security research on Claude Sonnet 4 and 4.6. See the `experiments/` folder for 8 experiments covering 115 attack techniques with documented findings.

## Author

Bill Kishore -- a developer who likes breaking things to understand how they work. Currently exploring LLM safety evals, red teaming, and the weird gaps between how AI systems are designed and how they actually behave. Open to collaborating on AI safety research, evals, or anything that needs creative problem-solving. Reach out.

## License

MIT
