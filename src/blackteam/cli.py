import click
from rich.console import Console
from rich.table import Table

from blackteam.config import load_config, set_config_value, DEFAULT_DB_PATH
from blackteam.engine import Engine
from blackteam.registry import provider_registry, attack_registry

console = Console()


def _load_plugins():
    from blackteam import providers, attacks
    provider_registry.discover(providers)
    attack_registry.discover(attacks)


@click.group()
def cli():
    """ai-blackteam -- automated LLM red team framework"""
    _load_plugins()


@cli.command("list-providers")
def list_providers():
    """Show available providers."""
    table = Table(title="Providers")
    table.add_column("Name")
    table.add_column("Default Model")
    for name in provider_registry.list():
        cls = provider_registry.get(name)
        inst = cls.__new__(cls)
        model = inst.default_model() if hasattr(inst, "default_model") else "?"
        table.add_row(name, model)
    console.print(table)


@cli.command("list-attacks")
def list_attacks():
    """Show available attacks."""
    table = Table(title="Attacks")
    table.add_column("Name")
    table.add_column("Mode")
    for name in attack_registry.list():
        cls = attack_registry.get(name)
        mode = getattr(cls, "mode", "single-turn")
        table.add_row(name, mode)
    console.print(table)


@cli.command()
@click.option("-p", "--provider", required=True, help="Provider name")
@click.option("-m", "--model", default=None, help="Model name")
@click.option("-a", "--attack", required=True, help="Attack name")
@click.option("-t", "--target", required=True, help="Target behavior to test")
def run(provider, model, attack, target):
    """Run a single attack against a model."""
    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))

    provider_cls = provider_registry.get(provider)
    if not provider_cls:
        console.print(f"[red]Unknown provider: {provider}[/red]")
        console.print(f"Available: {', '.join(provider_registry.list())}")
        return

    attack_cls = attack_registry.get(attack)
    if not attack_cls:
        console.print(f"[red]Unknown attack: {attack}[/red]")
        console.print(f"Available: {', '.join(attack_registry.list())}")
        return

    provider_config = config.get("providers", {}).get(provider, {})
    api_key = provider_config.get("api_key")
    prov = provider_cls(model=model, api_key=api_key)
    atk = attack_cls()

    engine = Engine(db_path=db_path)

    console.print(f"\n[bold]Running {attack} against {prov.model}[/bold]")
    console.print(f"Target: {target}\n")

    results = engine.run(prov, atk, target)

    if isinstance(results, list):
        table = Table(title="Results")
        table.add_column("Prompt")
        table.add_column("Verdict")
        table.add_column("Confidence")
        for r in results:
            color = {"BYPASSED": "red", "PARTIAL": "yellow", "BLOCKED": "green"}.get(r["verdict"], "white")
            table.add_row(r["prompt"][:60], f"[{color}]{r['verdict']}[/{color}]", f"{r['confidence']:.2f}")
        console.print(table)
    else:
        color = {"BYPASSED": "red", "PARTIAL": "yellow", "BLOCKED": "green"}.get(results["verdict"], "white")
        console.print(f"Verdict: [{color}]{results['verdict']}[/{color}]")
        console.print(f"Turns: {results.get('turns', 1)}")
        console.print(f"Confidence: {results['confidence']:.2f}")


@cli.command()
@click.option("-p", "--provider", required=True)
@click.option("-m", "--model", default=None)
@click.option("--attacks", default="all", help="Comma-separated attack names or 'all'")
@click.option("-t", "--target", required=True)
def batch(provider, model, attacks, target):
    """Run multiple attacks against a model."""
    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))

    provider_cls = provider_registry.get(provider)
    if not provider_cls:
        console.print(f"[red]Unknown provider: {provider}[/red]")
        return

    provider_config = config.get("providers", {}).get(provider, {})
    api_key = provider_config.get("api_key")
    prov = provider_cls(model=model, api_key=api_key)

    if attacks == "all":
        attack_names = attack_registry.list()
    else:
        attack_names = [a.strip() for a in attacks.split(",")]

    engine = Engine(db_path=db_path)

    console.print(f"\n[bold]Batch: {len(attack_names)} attacks against {prov.model}[/bold]")
    console.print(f"Target: {target}\n")

    for atk_name in attack_names:
        attack_cls = attack_registry.get(atk_name)
        if not attack_cls:
            console.print(f"[yellow]Skipping unknown attack: {atk_name}[/yellow]")
            continue

        atk = attack_cls()
        console.print(f"Running [bold]{atk_name}[/bold]...")
        results = engine.run(prov, atk, target)

        if isinstance(results, list):
            for r in results:
                color = {"BYPASSED": "red", "PARTIAL": "yellow", "BLOCKED": "green"}.get(r["verdict"], "white")
                console.print(f"  [{color}]{r['verdict']}[/{color}] {r['prompt'][:60]}")
        else:
            color = {"BYPASSED": "red", "PARTIAL": "yellow", "BLOCKED": "green"}.get(results["verdict"], "white")
            console.print(f"  [{color}]{results['verdict']}[/{color}] ({results.get('turns', 1)} turns)")


@cli.command()
@click.option("--format", "fmt", type=click.Choice(["markdown", "json", "html"]), default="markdown")
@click.option("--output", "-o", default=None, help="Output file path")
def report(fmt, output):
    """Generate a report from stored results."""
    from blackteam.reporter import generate_markdown, generate_json
    from blackteam.storage.sqlite import Storage

    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))
    storage = Storage(db_path)

    if fmt == "markdown":
        content = generate_markdown(storage)
    elif fmt == "html":
        from blackteam.reporter import generate_html
        content = generate_html(storage)
    else:
        content = generate_json(storage)

    if output:
        with open(output, "w") as f:
            f.write(content)
        console.print(f"Report saved to {output}")
    else:
        console.print(content)


@cli.group()
def config():
    """Manage configuration."""
    pass


@config.command("show")
def config_show():
    """Show current configuration."""
    import yaml
    cfg = load_config()
    for p in cfg.get("providers", {}).values():
        if p.get("api_key"):
            p["api_key"] = p["api_key"][:8] + "..."
    console.print(yaml.dump(cfg, default_flow_style=False))


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a config value (e.g., providers.anthropic.api_key VALUE)."""
    set_config_value(key, value)
    console.print(f"Set {key}")
