"""Validation capture and commit commands."""

import json

import typer
from rich.console import Console
from rich.table import Table

from ...core.exceptions import MissionForgeError
from ...core.validation_service import ValidationService

app = typer.Typer(help="Sub-mission validation capture and commit commands")
console = Console()


@app.command("capture")
def capture_validation(
    sub_mission_id: str = typer.Argument(..., help="Sub-mission ID (e.g., MF-001-A)"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing validation.json"),
) -> None:
    """Capture deterministic evidence and create validation.todo.json.

    Runs git diff, scope checks, and test command. Bob fills metric values.
    """
    try:
        service = ValidationService()
        todo_path = service.capture_validation(sub_mission_id, force=force)

        with open(todo_path) as f:
            data = json.load(f)

        evidence = data.get("deterministic_evidence", {})
        files_changed = evidence.get("files_changed", [])
        scope_check = evidence.get("scope_check", {})
        test_results = evidence.get("test_results")
        metrics = data.get("metrics", [])

        console.print(f"[green]✓[/green] Validation captured for {sub_mission_id}")
        console.print(f"\nGenerated: {todo_path}")

        console.print(f"\n[bold]Files changed ({len(files_changed)}):[/bold]")
        for f in files_changed:
            console.print(f"  • {f}")
        if not files_changed:
            console.print("  (none)")

        scope_ok = scope_check.get("allowed_paths_satisfied", True) and not scope_check.get("forbidden_paths_violated", False)
        scope_icon = "[green]✓[/green]" if scope_ok else "[red]✗[/red]"
        console.print(f"\n[bold]Scope check:[/bold] {scope_icon}")
        violations = scope_check.get("violations", [])
        for v in violations:
            console.print(f"  [red]• {v}[/red]")

        if test_results:
            test_icon = "[green]✓[/green]" if test_results.get("passed") else "[red]✗[/red]"
            duration = test_results.get("duration", 0)
            console.print(f"\n[bold]Tests:[/bold] {test_icon} ({duration:.1f}s)")

        console.print(f"\n[bold]Metrics to fill ({len(metrics)}):[/bold]")
        for m in metrics:
            console.print(f"  • {m['metric_id']} (target: {m['target_value']})")

        console.print("\n[bold]Next steps:[/bold]")
        console.print("1. Analyze implementation and fill final_value in validation.todo.json")
        console.print(f"2. Run: missionforge validate commit {sub_mission_id}")

    except MissionForgeError as e:
        console.print(f"[red]Error:[/red] {e.format_error()}")
        raise typer.Exit(1) from e


@app.command("commit")
def commit_validation(
    sub_mission_id: str = typer.Argument(..., help="Sub-mission ID (e.g., MF-001-A)"),
) -> None:
    """Commit validation from validation.todo.json to immutable validation.json.

    Validates all metrics are filled and determines pass/fail status.
    """
    try:
        service = ValidationService()
        validation_path = service.commit_validation(sub_mission_id)

        with open(validation_path) as f:
            data = json.load(f)

        overall = data.get("status", "UNKNOWN")
        metrics = data.get("metrics", [])

        status_color = {"PASSED": "green", "FAILED": "red", "BLOCKED": "yellow"}.get(overall, "white")
        console.print(f"\n[bold]Overall Status:[/bold] [{status_color}]{overall}[/{status_color}]")
        console.print(f"Committed: {validation_path}")

        table = Table()
        table.add_column("Metric", style="cyan")
        table.add_column("Baseline", style="blue")
        table.add_column("Target", style="yellow")
        table.add_column("Final", style="white")
        table.add_column("Status", style="white")

        for m in metrics:
            status = m.get("status", "")
            status_style = "green" if status == "PASSED" else "red"
            table.add_row(
                m.get("metric_id", ""),
                str(m.get("baseline_value", "")),
                str(m.get("target_value", "")),
                str(m.get("final_value", "")),
                f"[{status_style}]{status}[/{status_style}]",
            )

        console.print("\n[bold]Metric Results:[/bold]")
        console.print(table)
        console.print("\n[yellow]⚠️  validation.json is now immutable[/yellow]")

    except MissionForgeError as e:
        console.print(f"[red]Error:[/red] {e.format_error()}")
        raise typer.Exit(1) from e


# Made with Bob
