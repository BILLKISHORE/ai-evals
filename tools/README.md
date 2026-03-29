# AI Blackteam -- Tools

Python automation framework for LLM red teaming.

## Setup

```bash
cd tools
pip install -r requirements.txt
```

## CLI Usage

```bash
# Create a new experiment
python cli.py new --name "description" --technique prompt-injection --model gpt-5.4

# Rebuild the master index
python cli.py index
```

## Configuration

Edit `config.yaml` for provider settings. Set API keys as environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."
```

## Architecture

- `redteam/providers/base.py` -- Abstract base class for model providers
- `redteam/attacks/base.py` -- Abstract base class for attack techniques
- `generators/` -- Utility scripts for scaffolding and indexing
- `cli.py` -- Command-line interface
