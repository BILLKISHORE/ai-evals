# AI Blackteam

LLM security research framework. Finding vulnerabilities in AI models,
documenting them properly, and publishing responsible research.

## Structure

| Directory | Purpose |
|-----------|---------|
| `experiments/` | Self-contained research experiments |
| `techniques/` | Attack method knowledge base |
| `models/` | Per-model intelligence tracker |
| `writeups/` | Papers, blog posts, bug bounty reports |
| `tools/` | Red team automation framework (Python) |
| `logs/` | Daily notes and scratch pad |
| `templates/` | Reusable templates for everything |

## Quick Start

```bash
# Create a new experiment
python tools/cli.py new --name "model-technique-description" --technique prompt-injection --model gpt-5.4

# Rebuild the master index after adding experiments
python tools/cli.py index
```

## Research Workflow

1. **Explore** -- Manual prompt crafting against target models
2. **Document** -- Create experiment folder, record prompts and responses
3. **Automate** -- Batch test across models (when ready)
4. **Analyze** -- Evaluate results, update technique/model knowledge
5. **Publish** -- Write paper, blog post, or bug bounty report

## Author

Bill Kishore -- AI Security Researcher
