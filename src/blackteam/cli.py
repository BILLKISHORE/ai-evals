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
@click.option("-w", "--workers", default=5, help="Max parallel workers (default: 5)")
@click.option("--verbose", is_flag=True, help="Show full response text")
@click.option("--quiet", is_flag=True, help="Suppress output, exit 0=all blocked, 1=any bypassed")
@click.option("--sequential", is_flag=True, help="Run attacks one at a time (no parallelism)")
def batch(provider, model, attack_filter, target, workers, verbose, quiet, sequential):
    """Run multiple attacks against a model (parallel by default)."""
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

    attacks = []
    for atk_name in attack_names:
        attack_cls = attack_registry.get(atk_name)
        if not attack_cls:
            if not quiet:
                console.print(f"[yellow]Skipping unknown attack: {atk_name}[/yellow]")
            continue
        attacks.append(attack_cls())

    engine = Engine(db_path=db_path)

    if not quiet:
        mode_label = "sequential" if sequential else f"parallel ({workers} workers)"
        console.print(f"\n[bold]Batch: {len(attacks)} attacks against {prov.model} ({mode_label})[/bold]")
        console.print(f"Target: {target}\n")

    total_start = time.time()
    counts = {"BYPASSED": 0, "BLOCKED": 0, "PARTIAL": 0}

    if sequential:
        from rich.progress import Progress
        with Progress(console=console, disable=quiet) as progress:
            task = progress.add_task("Running attacks...", total=len(attacks))
            for atk in attacks:
                results = engine.run(prov, atk, target)
                _tally_results(results, counts, atk.technique_id, verbose, quiet)
                progress.advance(task)
    else:
        from rich.progress import Progress
        completed = [0]
        with Progress(console=console, disable=quiet) as progress:
            task = progress.add_task("Running attacks...", total=len(attacks))

            def on_complete(entry):
                completed[0] += 1
                progress.update(task, completed=completed[0])
                _tally_results(entry.get("results"), counts, entry["attack"], verbose, quiet)
                if entry.get("error") and not quiet:
                    console.print(f"  [red]ERROR[/red] {entry['attack']}: {entry['error']}")

            engine.run_batch_parallel(prov, attacks, target, max_workers=workers, on_complete=on_complete)

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


def _tally_results(results, counts, attack_name, verbose, quiet):
    if results is None:
        return
    if isinstance(results, list):
        for r in results:
            counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
            if not quiet:
                color = _verdict_color(r["verdict"])
                line = f"  [{color}]{r['verdict']}[/{color}] {attack_name}: {r['prompt'][:50]}"
                if verbose:
                    line += f"\n    {r.get('response_preview', '')}"
                console.print(line)
    elif isinstance(results, dict) and "verdict" in results:
        counts[results["verdict"]] = counts.get(results["verdict"], 0) + 1
        if not quiet:
            color = _verdict_color(results["verdict"])
            line = f"  [{color}]{results['verdict']}[/{color}] {attack_name} ({results.get('turns', 1)} turns)"
            if verbose:
                line += f"\n    {results.get('final_response_preview', '')}"
            console.print(line)


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
@click.option("--export", "export_fmt", type=click.Choice(["promptfoo", "garak"]), default=None, help="Export to Promptfoo JSON or garak JSONL")
@click.option("--output", "-o", default=None, help="Output file path")
def report(fmt, export_fmt, output):
    """Generate a report from stored results."""
    from blackteam.storage.sqlite import Storage

    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))
    storage = Storage(db_path)

    if export_fmt:
        from blackteam.exporters import export_promptfoo, export_garak
        content = export_promptfoo(storage) if export_fmt == "promptfoo" else export_garak(storage)
    elif fmt == "markdown":
        from blackteam.reporter import generate_markdown
        content = generate_markdown(storage)
    elif fmt == "html":
        from blackteam.reporter import generate_html
        content = generate_html(storage)
    else:
        from blackteam.reporter import generate_json
        content = generate_json(storage)

    if output:
        with open(output, "w") as f:
            f.write(content)
        console.print(f"Report saved to {output}")
    else:
        console.print(content)


RATING_COLORS = {"PASS": "green", "ELEVATED": "yellow", "PARTIAL": "bright_red", "FAIL": "red", "N/A": "dim"}


@cli.command()
@click.option("--format", "fmt", type=click.Choice(["table", "json", "markdown"]), default="table")
@click.option("--output", "-o", default=None, help="Output file path")
@click.option("--model", "-m", default=None, help="Filter by model name")
def scorecard(fmt, output, model):
    """Show OWASP LLM Top 10 safety scorecard from stored results."""
    from blackteam.storage.sqlite import Storage
    from blackteam.scorecard import generate_scorecard, scorecard_to_json, scorecard_to_markdown

    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))
    storage = Storage(db_path)

    runs = storage.list_runs(limit=5000)
    if model:
        runs = [r for r in runs if r["model"] == model]

    if not runs:
        console.print("[yellow]No runs found. Run some attacks first.[/yellow]")
        raise SystemExit(2)

    sc = generate_scorecard(runs)
    model_label = model or "all models"

    if fmt == "json":
        content = scorecard_to_json(sc)
    elif fmt == "markdown":
        content = scorecard_to_markdown(sc, model_label)
    else:
        table = Table(title=f"OWASP LLM Top 10 Scorecard -- {model_label}")
        table.add_column("Category", style="bold")
        table.add_column("Name")
        table.add_column("Rating")
        table.add_column("Block Rate")
        table.add_column("Blocked/Total")
        table.add_column("Attacks")

        for cat_id, info in sc["categories"].items():
            rating = info["rating"]
            color = RATING_COLORS.get(rating, "white")
            rate = f"{info['block_rate']}%" if info["block_rate"] is not None else "-"
            ratio = f"{info['blocked']}/{info['total']}" if info["total"] > 0 else "-"
            table.add_row(
                cat_id, info["name"], f"[{color}]{rating}[/{color}]",
                rate, ratio, str(info["attacks_tested"]),
            )

        overall_color = RATING_COLORS.get(sc["overall_rating"], "white")
        console.print(table)
        console.print(
            f"\nOverall: [{overall_color}]{sc['overall_score']}% ({sc['overall_rating']})[/{overall_color}]"
            f" | Tested: {sc['tested_categories']}/{sc['total_categories']} categories"
        )
        content = None

    if content:
        if output:
            with open(output, "w") as f:
                f.write(content)
            console.print(f"Scorecard saved to {output}")
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


@cli.command("taxonomy")
def taxonomy():
    """Show all attacks grouped by category with OWASP/MITRE mappings."""
    categories = {}
    for name in attack_registry.list():
        cls = attack_registry.get(name)
        attack = cls()
        meta = attack.metadata()
        cat = meta["category"] or "uncategorized"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(meta)

    SEVERITY_COLORS = {"critical": "red", "high": "bright_red", "medium": "yellow", "low": "green"}

    for cat, attacks in sorted(categories.items()):
        table = Table(title=f"[bold]{cat.upper()}[/bold] ({len(attacks)} attacks)")
        table.add_column("Attack", style="cyan")
        table.add_column("Severity")
        table.add_column("Mode")
        table.add_column("Description")
        table.add_column("OWASP LLM")
        table.add_column("MITRE ATLAS", style="dim")

        for a in sorted(attacks, key=lambda x: x["technique_id"]):
            sev = a["severity"]
            color = SEVERITY_COLORS.get(sev, "white")
            owasp = ", ".join(o.split(" ")[0] for o in a.get("owasp_llm", [])) or "-"
            atlas = ", ".join(a.get("mitre_atlas", [])) or "-"
            table.add_row(
                a["technique_id"],
                f"[{color}]{sev}[/{color}]",
                a["mode"],
                a["description"][:60],
                owasp,
                atlas,
            )
        console.print(table)
        console.print()


@cli.command("mlcommons")
def mlcommons_cmd():
    """Show MLCommons AILuminate hazard taxonomy and harm category alignment."""
    from blackteam.taxonomy import MLCOMMONS_HAZARDS, HARM_TO_MLCOMMONS

    table = Table(title="MLCommons AILuminate v1.0 Hazard Taxonomy")
    table.add_column("Code", style="bold cyan")
    table.add_column("Hazard Category")
    table.add_column("Description")

    for code, info in MLCOMMONS_HAZARDS.items():
        table.add_row(code, info["name"], info["description"])
    console.print(table)
    console.print()

    mapping = Table(title="Harm Category Alignment")
    mapping.add_column("ai-blackteam Category", style="cyan")
    mapping.add_column("MLCommons Code", style="bold")
    mapping.add_column("MLCommons Hazard")

    for harm, code in HARM_TO_MLCOMMONS.items():
        mapping.add_row(harm, code, MLCOMMONS_HAZARDS[code]["name"])
    console.print(mapping)


@cli.command("atlas")
def atlas_cmd():
    """Show MITRE ATLAS technique mappings for all attacks."""
    from blackteam.taxonomy import ATLAS_TECHNIQUES

    table = Table(title="MITRE ATLAS Attack Mappings (v5.4.0)")
    table.add_column("Attack", style="cyan")
    table.add_column("ATLAS Techniques")
    table.add_column("Technique Names")

    for name in sorted(attack_registry.list()):
        cls = attack_registry.get(name)
        attack = cls()
        ids = attack.mitre_atlas
        names = [ATLAS_TECHNIQUES[t]["name"] for t in ids if t in ATLAS_TECHNIQUES]
        table.add_row(
            name,
            ", ".join(ids),
            ", ".join(names),
        )
    console.print(table)


@cli.command()
@click.option("-p", "--provider", default=None, help="Provider name (omit for --all)")
@click.option("-m", "--model", default=None, help="Model name")
@click.option("--all", "run_all", is_flag=True, help="Benchmark all configured providers")
@click.option("--models", default=None, help="Comma-separated provider:model pairs (e.g., anthropic:claude-sonnet-4-6,openai:gpt-4o)")
@click.option("-w", "--workers", default=5, help="Max parallel workers")
@click.option("--categories", default=None, help="Comma-separated categories to test (default: all)")
@click.option("--threshold", default=None, type=float, help="Min safety score (0-100) to pass. Exit 1 if below.")
@click.option("--output", default=None, help="Save JSON results to file")
@click.option("--quiet", is_flag=True, help="Minimal output")
def benchmark(provider, model, run_all, models, workers, categories, threshold, output, quiet):
    """Run the safety benchmark and produce a score.

    Single model:   blackteam benchmark -p anthropic -m claude-sonnet-4-6
    All models:     blackteam benchmark --all
    Specific list:  blackteam benchmark --models anthropic:claude-sonnet-4-6,openai:gpt-4o
    """
    import json
    from blackteam.benchmark import run_benchmark, load_benchmark
    from blackteam.engine import Engine
    from rich.progress import Progress

    config = load_config()
    db_path = config.get("storage", {}).get("database", str(DEFAULT_DB_PATH))
    provider_configs = config.get("providers", {})

    # Build list of (provider_name, model_name) pairs to benchmark
    targets_list = []

    if models:
        for pair in models.split(","):
            pair = pair.strip()
            if ":" in pair:
                p, m = pair.split(":", 1)
                targets_list.append((p.strip(), m.strip()))
            else:
                targets_list.append((pair, None))
    elif run_all:
        for name in provider_registry.list():
            pcfg = provider_configs.get(name, {})
            if name == "ollama" or pcfg.get("api_key"):
                targets_list.append((name, None))
        if not targets_list:
            console.print("[yellow]No providers configured. Set API keys with: blackteam config set providers.<name>.api_key VALUE[/yellow]")
            raise SystemExit(2)
    elif provider:
        targets_list.append((provider, model))
    else:
        console.print("[red]Specify -p/--provider, --all, or --models[/red]")
        raise SystemExit(2)

    cats = [c.strip() for c in categories.split(",")] if categories else None
    bench_data = load_benchmark(cats)
    total_targets = sum(len(v) for v in bench_data.values())
    total_attacks = len(attack_registry.list())

    engine = Engine(db_path=db_path)
    all_scores = []

    for prov_name, model_name in targets_list:
        provider_cls = provider_registry.get(prov_name)
        if not provider_cls:
            if not quiet:
                console.print(f"[yellow]Skipping unknown provider: {prov_name}[/yellow]")
            continue

        api_key = provider_configs.get(prov_name, {}).get("api_key")
        prov = provider_cls(model=model_name, api_key=api_key)

        if not quiet:
            console.print(f"\n[bold]Benchmarking: {prov.model} ({prov_name})[/bold]")
            console.print(f"Targets: {total_targets} | Attacks: {total_attacks} | Runs: {total_targets * total_attacks}")

        completed = [0]
        total_runs = total_targets * total_attacks

        with Progress(console=console, disable=quiet) as progress:
            task = progress.add_task(f"{prov.model}...", total=total_runs)

            def on_progress(attack_name, target, verdict):
                completed[0] += 1
                progress.update(task, completed=completed[0])

            scores = run_benchmark(
                engine, prov, categories=cats,
                max_workers=workers, on_progress=on_progress,
            )

        all_scores.append(scores)

        if not quiet:
            score = scores["overall_score"]
            score_color = "green" if score >= 90 else "yellow" if score >= 70 else "red"
            console.print(f"  Safety Score: [{score_color}]{score}%[/{score_color}]")
            console.print(f"  Bypassed: {scores['bypassed']} | Blocked: {scores['blocked']} | Partial: {scores['partial']}")

    # Leaderboard (only when testing multiple models)
    if len(all_scores) > 1 and not quiet:
        console.print(f"\n")
        leader = Table(title="Safety Leaderboard")
        leader.add_column("Rank", style="bold")
        leader.add_column("Model")
        leader.add_column("Provider")
        leader.add_column("Safety Score")
        leader.add_column("Bypassed")
        leader.add_column("Blocked")

        ranked = sorted(all_scores, key=lambda s: s["overall_score"], reverse=True)
        for i, s in enumerate(ranked, 1):
            sc = s["overall_score"]
            color = "green" if sc >= 90 else "yellow" if sc >= 70 else "red"
            leader.add_row(
                str(i), s["model"], s["provider"],
                f"[{color}]{sc}%[/{color}]",
                str(s["bypassed"]), str(s["blocked"]),
            )
        console.print(leader)

        # Category comparison matrix
        all_cats = sorted({cat for s in all_scores for cat in s.get("category_scores", {})})
        if all_cats:
            matrix = Table(title="Category Comparison")
            matrix.add_column("Category")
            for s in ranked:
                matrix.add_column(s["model"][:20])

            for cat in all_cats:
                row = [cat]
                for s in ranked:
                    cat_info = s.get("category_scores", {}).get(cat, {})
                    cat_score = cat_info.get("score", 0)
                    color = "green" if cat_score >= 90 else "yellow" if cat_score >= 70 else "red"
                    row.append(f"[{color}]{cat_score}%[/{color}]")
                matrix.add_row(*row)
            console.print(matrix)

    # Single model category breakdown
    elif len(all_scores) == 1 and not quiet:
        scores = all_scores[0]
        cat_table = Table(title="Category Scores")
        cat_table.add_column("Category")
        cat_table.add_column("Score")
        cat_table.add_column("Attacks")

        for cat, info in sorted(scores.get("category_scores", {}).items()):
            cat_score = info["score"]
            color = "green" if cat_score >= 90 else "yellow" if cat_score >= 70 else "red"
            cat_table.add_row(cat, f"[{color}]{cat_score}%[/{color}]", str(info["count"]))
        console.print(cat_table)

    # OWASP scorecard for all benchmarked models
    if all_scores and not quiet:
        from blackteam.scorecard import generate_scorecard
        from blackteam.storage.sqlite import Storage
        storage = Storage(db_path)
        runs = storage.list_runs(limit=5000)

        for s in all_scores:
            model_runs = [r for r in runs if r["model"] == s["model"]]
            if model_runs:
                sc = generate_scorecard(model_runs)
                owasp_table = Table(title=f"OWASP LLM Top 10 -- {s['model']}")
                owasp_table.add_column("Category", style="bold")
                owasp_table.add_column("Name")
                owasp_table.add_column("Rating")
                owasp_table.add_column("Block Rate")

                for cat_id, info in sc["categories"].items():
                    rating = info["rating"]
                    color = RATING_COLORS.get(rating, "white")
                    rate = f"{info['block_rate']}%" if info["block_rate"] is not None else "-"
                    owasp_table.add_row(cat_id, info["name"], f"[{color}]{rating}[/{color}]", rate)
                console.print(owasp_table)

    # Save results
    if output:
        save_data = all_scores if len(all_scores) > 1 else all_scores[0] if all_scores else {}
        from pathlib import Path
        Path(output).write_text(json.dumps(save_data, indent=2, default=str))
        if not quiet:
            console.print(f"\nResults saved to: {output}")

    # Threshold check (uses worst score across all models when --all)
    if threshold is not None and all_scores:
        worst = min(s["overall_score"] for s in all_scores)
        if worst < threshold:
            if not quiet:
                console.print(f"\n[red]FAIL: Lowest score {worst}% below threshold {threshold}%[/red]")
            raise SystemExit(1)
        else:
            if not quiet:
                console.print(f"\n[green]PASS: All models meet threshold {threshold}%[/green]")
            raise SystemExit(0)
