"""Scaffold a new experiment from templates."""

import os
import shutil
from datetime import date
from pathlib import Path


def get_next_experiment_id(experiments_dir: Path) -> str:
    """Scan existing experiments and return the next EXP-NNN id."""
    existing = []
    if experiments_dir.exists():
        for d in experiments_dir.iterdir():
            if d.is_dir() and not d.name.startswith("."):
                readme = d / "README.md"
                if readme.exists():
                    for line in readme.read_text().splitlines():
                        if line.startswith("id:"):
                            exp_id = line.split(":", 1)[1].strip()
                            if exp_id.startswith("EXP-"):
                                try:
                                    existing.append(int(exp_id.split("-")[1]))
                                except (IndexError, ValueError):
                                    pass
    next_num = max(existing, default=0) + 1
    return f"EXP-{next_num:03d}"


def scaffold_experiment(
    name: str,
    technique: str,
    model: str,
    root_dir: Path,
) -> Path:
    """Create a new experiment directory from templates.

    Returns the path to the created experiment directory.
    """
    today = date.today().isoformat()
    experiments_dir = root_dir / "experiments"
    templates_dir = root_dir / "templates" / "experiment"

    exp_dir_name = f"{today}-{name}"
    exp_dir = experiments_dir / exp_dir_name

    if exp_dir.exists():
        raise FileExistsError(f"Experiment directory already exists: {exp_dir}")

    exp_id = get_next_experiment_id(experiments_dir)

    # Create directory structure
    exp_dir.mkdir(parents=True)
    (exp_dir / "prompts").mkdir()
    (exp_dir / "responses").mkdir()
    (exp_dir / "responses" / "screenshots").mkdir()
    (exp_dir / "scripts").mkdir()
    (exp_dir / "results").mkdir()

    # Copy and fill templates
    replacements = {
        "{{ID}}": exp_id,
        "{{TITLE}}": f"{model} {technique} -- {name}",
        "{{DATE}}": today,
        "{{MODEL}}": model,
        "{{TECHNIQUE}}": technique,
    }

    for template_file in ["README.md", "STATUS.md"]:
        src = templates_dir / template_file
        if src.exists():
            content = src.read_text()
            for placeholder, value in replacements.items():
                content = content.replace(placeholder, value)
            (exp_dir / template_file).write_text(content)

    # Create first prompt from template
    prompt_template = templates_dir / "prompt.md"
    if prompt_template.exists():
        content = prompt_template.read_text()
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        (exp_dir / "prompts" / "001-initial.md").write_text(content)

    return exp_dir
