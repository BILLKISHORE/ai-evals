"""AI Blackteam CLI -- Red team research toolkit."""

import sys
from pathlib import Path

import click

# Root of the project (one level up from tools/)
ROOT_DIR = Path(__file__).resolve().parent.parent


@click.group()
def cli():
    """AI Blackteam -- LLM security research toolkit."""
    pass


@cli.command()
@click.option("--name", required=True, help="Short experiment name (used in folder name)")
@click.option("--technique", required=True, help="Attack technique (e.g., prompt-injection)")
@click.option("--model", required=True, help="Target model (e.g., gpt-5.4)")
def new(name: str, technique: str, model: str):
    """Scaffold a new experiment from templates."""
    from generators.new_experiment import scaffold_experiment

    try:
        exp_dir = scaffold_experiment(
            name=name,
            technique=technique,
            model=model,
            root_dir=ROOT_DIR,
        )
        click.echo(f"Created experiment: {exp_dir.relative_to(ROOT_DIR)}")
        click.echo(f"Next steps:")
        click.echo(f"  1. Edit {exp_dir / 'prompts' / '001-initial.md'} with your first prompt")
        click.echo(f"  2. Test it against {model}")
        click.echo(f"  3. Record the response in {exp_dir / 'responses' / '001-initial.md'}")
    except FileExistsError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def index():
    """Rebuild INDEX.md from all experiment frontmatter."""
    from generators.build_index import build_index

    count = build_index(ROOT_DIR)
    click.echo(f"INDEX.md updated with {count} experiment(s).")


if __name__ == "__main__":
    cli()
