import time
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


def _verdict_color(verdict):
    return {"BYPASSED": "red", "PARTIAL": "yellow", "BLOCKED": "green"}.get(verdict, "white")


def _format_duration(seconds):
    if seconds < 60:
        return f"{seconds:.1f}s"
    return f"{int(seconds // 60)}m {seconds % 60:.1f}s"


@cli.command()
@click.option("-p", "--provider", required=True, help="Provider name")
@click.option("-m", "--model", default=None, help="Model name")
@click.option("-a", "--attack", required=True, help="Attack name")
@click.option("-t", "--target", required=True, help="Target behavior to test")
@click.option("--verbose", is_flag=True, help="Show full response text")
@click.option("--quiet", is_flag=True, help="Suppress output, exit 0=all blocked, 1=any bypassed")
def run(provider, model, attack, target, verbose, quiet):
    """Run a single attack against a model."""
    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))

    provider_cls = provider_registry.get(provider)
    if not provider_cls:
        if not quiet:
            console.print(f"[red]Unknown provider: {provider}[/red]")
            console.print(f"Available: {', '.join(provider_registry.list())}")
        raise SystemExit(2)

    attack_cls = attack_registry.get(attack)
    if not attack_cls:
        if not quiet:
            console.print(f"[red]Unknown attack: {attack}[/red]")
            console.print(f"Available: {', '.join(attack_registry.list())}")
        raise SystemExit(2)

    provider_config = config.get("providers", {}).get(provider, {})
    api_key = provider_config.get("api_key")
    prov = provider_cls(model=model, api_key=api_key)
    atk = attack_cls()

    engine = Engine(db_path=db_path)

    if not quiet:
        console.print(f"\n[bold]Running {attack} against {prov.model}[/bold]")
        console.print(f"Target: {target}\n")

    total_start = time.time()

    with console.status(f"Testing {attack}...", spinner="dots") as status:
        if quiet:
            status.stop()
        results = engine.run(prov, atk, target)

    total_elapsed = time.time() - total_start

    any_bypassed = False

    if isinstance(results, list):
        any_bypassed = any(r["verdict"] == "BYPASSED" for r in results)
        if not quiet:
            table = Table(title="Results")
            table.add_column("Prompt")
            table.add_column("Verdict")
            table.add_column("Confidence")
            if verbose:
                table.add_column("Response")
            for r in results:
                color = _verdict_color(r["verdict"])
                row = [
                    r["prompt"][:60],
                    f"[{color}]{r['verdict']}[/{color}]",
                    f"{r['confidence']:.2f}",
                ]
                if verbose:
                    row.append(r.get("response_preview", ""))
                table.add_row(*row)
            console.print(table)
            console.print(f"Duration: {_format_duration(total_elapsed)}")
    else:
        any_bypassed = results["verdict"] == "BYPASSED"
        if not quiet:
            color = _verdict_color(results["verdict"])
            console.print(f"Verdict: [{color}]{results['verdict']}[/{color}]")
            console.print(f"Turns: {results.get('turns', 1)}")
            console.print(f"Confidence: {results['confidence']:.2f}")
            if verbose:
                console.print(f"Response: {results.get('final_response_preview', '')}")
            console.print(f"Duration: {_format_duration(total_elapsed)}")

    raise SystemExit(1 if any_bypassed else 0)


@cli.command()
@click.option("-p", "--provider", required=True)
@click.option("-m", "--model", default=None)
@click.option("--attacks", "attack_filter", default="all", help="Comma-separated attack names or 'all'")
@click.option("-t", "--target", required=True)
@click.option("--verbose", is_flag=True, help="Show full response text")
@click.option("--quiet", is_flag=True, help="Suppress output, exit 0=all blocked, 1=any bypassed")
def batch(provider, model, attack_filter, target, verbose, quiet):
    """Run multiple attacks against a model."""
    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))

    provider_cls = provider_registry.get(provider)
    if not provider_cls:
        if not quiet:
            console.print(f"[red]Unknown provider: {provider}[/red]")
        raise SystemExit(2)

    provider_config = config.get("providers", {}).get(provider, {})
    api_key = provider_config.get("api_key")
    prov = provider_cls(model=model, api_key=api_key)

    if attack_filter == "all":
        attack_names = attack_registry.list()
    else:
        attack_names = [a.strip() for a in attack_filter.split(",")]

    engine = Engine(db_path=db_path)

    if not quiet:
        console.print(f"\n[bold]Batch: {len(attack_names)} attacks against {prov.model}[/bold]")
        console.print(f"Target: {target}\n")

    total_start = time.time()
    counts = {"BYPASSED": 0, "BLOCKED": 0, "PARTIAL": 0}

    for atk_name in attack_names:
        attack_cls = attack_registry.get(atk_name)
        if not attack_cls:
            if not quiet:
                console.print(f"[yellow]Skipping unknown attack: {atk_name}[/yellow]")
            continue

        atk = attack_cls()
        if not quiet:
            console.print(f"Running [bold]{atk_name}[/bold]...")

        atk_start = time.time()
        results = engine.run(prov, atk, target)
        atk_elapsed = time.time() - atk_start

        if isinstance(results, list):
            for r in results:
                counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
                if not quiet:
                    color = _verdict_color(r["verdict"])
                    line = f"  [{color}]{r['verdict']}[/{color}] {r['prompt'][:60]}"
                    if verbose:
                        line += f"\n    {r.get('response_preview', '')}"
                    console.print(line)
        else:
            counts[results["verdict"]] = counts.get(results["verdict"], 0) + 1
            if not quiet:
                color = _verdict_color(results["verdict"])
                line = f"  [{color}]{results['verdict']}[/{color}] ({results.get('turns', 1)} turns)"
                if verbose:
                    line += f"\n    {results.get('final_response_preview', '')}"
                console.print(line)

        if not quiet:
            console.print(f"  [dim]{_format_duration(atk_elapsed)}[/dim]")

    total_elapsed = time.time() - total_start
    total = sum(counts.values())

    if not quiet:
        bypassed = counts.get("BYPASSED", 0)
        blocked = counts.get("BLOCKED", 0)
        partial = counts.get("PARTIAL", 0)
        console.print(
            f"\nSummary: [red]{bypassed} BYPASSED[/red] | "
            f"[green]{blocked} BLOCKED[/green] | "
            f"[yellow]{partial} PARTIAL[/yellow] "
            f"({total} total, {_format_duration(total_elapsed)})"
        )

    any_bypassed = counts.get("BYPASSED", 0) > 0
    raise SystemExit(1 if any_bypassed else 0)


@cli.command()
@click.option("-t", "--target", required=True, help="Target behavior to test")
@click.option("--verbose", is_flag=True, help="Show full response text")
@click.option("--quiet", is_flag=True, help="Suppress output, exit 0=all blocked, 1=any bypassed")
def sweep(target, verbose, quiet):
    """Run all attacks against all configured providers."""
    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))
    attack_names = attack_registry.list()

    provider_configs = config.get("providers", {})
    active_providers = []
    for name in provider_registry.list():
        pcfg = provider_configs.get(name, {})
        api_key = pcfg.get("api_key")
        # ollama doesn't need an api_key
        if name == "ollama" or api_key:
            active_providers.append(name)

    if not active_providers:
        if not quiet:
            console.print("[yellow]No providers configured. Set an api_key with: blackteam config set providers.<name>.api_key VALUE[/yellow]")
        raise SystemExit(2)

    if not quiet:
        console.print(f"\n[bold]Sweep: {len(attack_names)} attacks x {len(active_providers)} providers[/bold]")
        console.print(f"Target: {target}\n")

    engine = Engine(db_path=db_path)
    total_start = time.time()

    # per-provider summary rows for the final table
    summary_rows = []

    for prov_name in active_providers:
        cls = provider_registry.get(prov_name)
        pcfg = provider_configs.get(prov_name, {})
        api_key = pcfg.get("api_key")
        prov = cls(api_key=api_key)

        if not quiet:
            console.print(f"[bold cyan]{prov_name}[/bold cyan] ({prov.model})")

        counts = {"BYPASSED": 0, "BLOCKED": 0, "PARTIAL": 0}
        prov_start = time.time()

        for atk_name in attack_names:
            attack_cls = attack_registry.get(atk_name)
            if not attack_cls:
                continue
            atk = attack_cls()

            if not quiet:
                console.print(f"  Running [bold]{atk_name}[/bold]...")

            atk_start = time.time()
            results = engine.run(prov, atk, target)
            atk_elapsed = time.time() - atk_start

            if isinstance(results, list):
                for r in results:
                    counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
                    if not quiet:
                        color = _verdict_color(r["verdict"])
                        line = f"    [{color}]{r['verdict']}[/{color}] {r['prompt'][:50]}"
                        if verbose:
                            line += f"\n      {r.get('response_preview', '')}"
                        console.print(line)
            else:
                counts[results["verdict"]] = counts.get(results["verdict"], 0) + 1
                if not quiet:
                    color = _verdict_color(results["verdict"])
                    line = f"    [{color}]{results['verdict']}[/{color}] ({results.get('turns', 1)} turns)"
                    if verbose:
                        line += f"\n      {results.get('final_response_preview', '')}"
                    console.print(line)

            if not quiet:
                console.print(f"    [dim]{_format_duration(atk_elapsed)}[/dim]")

        prov_elapsed = time.time() - prov_start
        summary_rows.append((prov_name, prov.model, counts, prov_elapsed))

        if not quiet:
            console.print()

    total_elapsed = time.time() - total_start

    if not quiet:
        table = Table(title="Sweep Summary")
        table.add_column("Provider")
        table.add_column("Model")
        table.add_column("BYPASSED", style="red")
        table.add_column("BLOCKED", style="green")
        table.add_column("PARTIAL", style="yellow")
        table.add_column("Total")
        table.add_column("Time")

        for prov_name, model_name, counts, elapsed in summary_rows:
            total = sum(counts.values())
            table.add_row(
                prov_name,
                model_name,
                str(counts.get("BYPASSED", 0)),
                str(counts.get("BLOCKED", 0)),
                str(counts.get("PARTIAL", 0)),
                str(total),
                _format_duration(elapsed),
            )

        console.print(table)
        console.print(f"Total time: {_format_duration(total_elapsed)}")

    any_bypassed = any(counts.get("BYPASSED", 0) > 0 for _, _, counts, _ in summary_rows)
    raise SystemExit(1 if any_bypassed else 0)


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
