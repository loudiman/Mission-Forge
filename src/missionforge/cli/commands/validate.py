"""Validation capture and commit commands."""

import json

import typer
from rich.console import Console
from rich.table import Table

from ...core.exceptions import MissionForgeError
from ...core.parent_validation_service import ParentValidationService
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

        scope_ok = scope_check.get("allowed_paths_satisfied", True) and not scope_check.get(
            "forbidden_paths_violated", False
        )
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

        status_color = {"PASSED": "green", "FAILED": "red", "BLOCKED": "yellow"}.get(
            overall, "white"
        )
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


@app.command("parent")
def validate_parent(
    mission_id: str = typer.Argument(..., help="Parent mission ID (e.g., MF-001)"),
) -> None:
    """Validate parent mission after all sub-missions complete.

    This command:
    1. Verifies all sub-missions have validation.json files
    2. Checks all sub-missions have PASSED status
    3. Runs parent-level test_command if defined
    4. Validates aggregate metrics against targets
    5. Checks forbidden_paths across all sub-mission changes
    6. Determines overall parent mission pass/fail status
    7. Writes immutable parent validation.json

    Examples:
        missionforge validate parent MF-001
    """
    try:
        service = ParentValidationService()

        console.print(f"\n[bold]Validating parent mission {mission_id}...[/bold]")

        validation_path = service.validate_parent_mission(mission_id)

        with open(validation_path) as f:
            data = json.load(f)

        overall = data.get("status", "UNKNOWN")
        sub_missions = data.get("sub_missions", {})
        parent_test = data.get("parent_test")
        aggregate_metrics = data.get("aggregate_metrics", [])
        forbidden_check = data.get("forbidden_paths_check", {})

        # Display sub-missions summary
        console.print(f"\n[bold]Sub-missions ({sub_missions['total']} total):[/bold]")
        for detail in sub_missions.get("details", []):
            status = detail["status"]
            status_color = {"PASSED": "green", "FAILED": "red", "BLOCKED": "yellow"}.get(
                status, "white"
            )
            icon = {"PASSED": "✓", "FAILED": "✗", "BLOCKED": "⚠"}.get(status, "?")
            console.print(f"  [{status_color}]{icon}[/{status_color}] {detail['id']}: {status}")

        # Display parent test results
        if parent_test:
            test_icon = "[green]✓[/green]" if parent_test["passed"] else "[red]✗[/red]"
            duration = parent_test.get("duration", 0)
            console.print(f"\n[bold]Parent tests:[/bold] {test_icon} ({duration:.1f}s)")
            if not parent_test["passed"]:
                console.print(f"  [red]Exit code: {parent_test['exit_code']}[/red]")

        # Display aggregate metrics
        if aggregate_metrics:
            console.print(f"\n[bold]Aggregate metrics ({len(aggregate_metrics)}):[/bold]")
            table = Table()
            table.add_column("Metric", style="cyan")
            table.add_column("Baseline", style="blue")
            table.add_column("Target", style="yellow")
            table.add_column("Final", style="white")
            table.add_column("Status", style="white")

            for m in aggregate_metrics:
                status = m.get("status", "")
                status_style = "green" if status == "PASSED" else "red"
                table.add_row(
                    m.get("metric_id", ""),
                    str(m.get("baseline_value", "")),
                    str(m.get("target_value", "")),
                    str(m.get("final_value", "")),
                    f"[{status_style}]{status}[/{status_style}]",
                )
            console.print(table)

        # Display forbidden paths check
        console.print("\n[bold]Forbidden paths check:[/bold]")
        if forbidden_check.get("violated"):
            console.print(
                f"  [red]✗ {len(forbidden_check['violations'])} violation(s) detected[/red]"
            )
            for violation in forbidden_check.get("violations", [])[:5]:  # Show first 5
                console.print(f"    • {violation}")
        else:
            console.print("  [green]✓ No violations detected[/green]")

        # Display overall status
        status_color = {"PASSED": "green", "FAILED": "red", "INCOMPLETE": "yellow"}.get(
            overall, "white"
        )
        console.print(f"\n[bold]Overall Status:[/bold] [{status_color}]{overall}[/{status_color}]")
        console.print(f"Committed: {validation_path}")
        console.print("\n[yellow]⚠️  validation.json is now immutable[/yellow]")

    except MissionForgeError as e:
        console.print(f"[red]Error:[/red] {e.format_error()}")
        raise typer.Exit(1) from e


# Made with Bob
