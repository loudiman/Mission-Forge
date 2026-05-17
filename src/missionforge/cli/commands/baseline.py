"""Baseline management commands."""

import json

import typer
from rich.console import Console
from rich.table import Table

from ...core.baseline_service import BaselineService
from ...core.exceptions import MissionForgeError

app = typer.Typer(help="Baseline capture and commit commands")
console = Console()


@app.command("capture")
def capture_baseline(
    sub_mission_id: str = typer.Argument(..., help="Sub-mission ID (e.g., MF-001-A)"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing baseline"),
) -> None:
    """Capture baseline metrics from sub-mission definition.

    Creates baseline.todo.json with metric definitions for Bob to fill.
    """
    try:
        service = BaselineService()
        todo_path = service.capture_baseline(sub_mission_id, force=force)

        # Read the created file to display metrics
        with open(todo_path) as f:
            baseline_data = json.load(f)

        metrics = baseline_data.get("metrics", [])

        console.print(f"[green]✓[/green] Baseline captured for {sub_mission_id}")
        console.print(f"\nGenerated: {todo_path}")

        console.print(f"\nMetrics to fill ({len(metrics)}):")
        for metric in metrics:
            metric_id = metric.get("metric_id")
            baseline_target = metric.get("baseline_target")
            target_type = type(baseline_target).__name__
            console.print(f"  • {metric_id} ({target_type})")

        console.print("\n[bold]Next steps:[/bold]")
        console.print("1. Analyze the code in allowed paths")
        console.print("2. Fill metric values in baseline.todo.json")
        console.print(f"3. Run: missionforge baseline commit {sub_mission_id}")

    except MissionForgeError as e:
        console.print(f"[red]Error:[/red] {e.format_error()}")
        raise typer.Exit(1) from e


@app.command("commit")
def commit_baseline(
    sub_mission_id: str = typer.Argument(..., help="Sub-mission ID (e.g., MF-001-A)"),
) -> None:
    """Commit baseline from baseline.todo.json to immutable baseline.json.

    Validates all metrics are filled and creates read-only baseline.json.
    """
    try:
        service = BaselineService()
        baseline_path = service.commit_baseline(sub_mission_id)

        # Read the committed file to display summary
        with open(baseline_path) as f:
            baseline_data = json.load(f)

        metrics = baseline_data.get("metrics", [])

        console.print(f"[green]✓[/green] Baseline committed for {sub_mission_id}")
        console.print(f"\nCommitted: {baseline_path}")

        # Create summary table
        console.print("\n[bold]Baseline Summary:[/bold]")
        table = Table()
        table.add_column("Metric", style="cyan")
        table.add_column("Target", style="yellow")
        table.add_column("Value", style="green")

        for metric in metrics:
            metric_id = metric.get("metric_id")
            baseline_target = metric.get("baseline_target")
            value = metric.get("value")
            table.add_row(
                metric_id,
                str(baseline_target),
                str(value),
            )

        console.print(table)
        console.print("\n[yellow]⚠️  baseline.json is now immutable[/yellow]")

    except MissionForgeError as e:
        console.print(f"[red]Error:[/red] {e.format_error()}")
        raise typer.Exit(1) from e


@app.command("reset")
def reset_baseline(
    sub_mission_id: str = typer.Argument(..., help="Sub-mission ID (e.g., MF-001-A)"),
    force: bool = typer.Option(False, "--force", help="Remove committed baseline.json"),
) -> None:
    """Reset baseline by removing baseline files.

    Removes baseline.todo.json and baseline.json (if --force is used).
    """
    try:
        service = BaselineService()
        service.reset_baseline(sub_mission_id, force=force)

        console.print(f"[green]✓[/green] Baseline reset for {sub_mission_id}")

        if force:
            console.print("\nRemoved:")
            console.print("  • baseline.todo.json (if existed)")
            console.print("  • baseline.json (if existed)")
        else:
            console.print("\nRemoved:")
            console.print("  • baseline.todo.json (if existed)")
            console.print("\nUse --force to also remove committed baseline.json")

    except MissionForgeError as e:
        console.print(f"[red]Error:[/red] {e.format_error()}")
        raise typer.Exit(1) from e


# Made with Bob
