"""Mission management commands."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ...core.mission_validator import MissionValidator
from ...core.workspace import Workspace

console = Console()


def mission_command(
    ctx: typer.Context,
    mission_id: str | None = typer.Argument(None, help="Mission ID"),
    validate: bool = typer.Option(False, "--validate", help="Validate parent mission configuration"),
) -> None:
    """Manage a mission."""
    # "validate" is a reserved compatibility alias — safe because valid mission IDs
    # must match [A-Z]+-\d+ (e.g. MF-001), so this keyword can never be a real ID.
    if mission_id == "validate":
        if not ctx.args:
            console.print("[red]Error:[/red] Mission ID is required")
            raise typer.Exit(1)
        _validate_mission(ctx.args[0])
        return

    if validate:
        if mission_id is None:
            console.print("[red]Error:[/red] Mission ID is required with --validate")
            raise typer.Exit(1)
        _validate_mission(mission_id)
        return

    console.print("[yellow]No mission action specified[/yellow]")
    console.print("Run: missionforge mission <mission-id> --validate")
    raise typer.Exit(1)


def _validate_mission(mission_id: str) -> None:
    """Validate parent mission configuration."""

    try:
        workspace = Workspace()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    mission_path = workspace.mission_path(mission_id)
    mission_file = mission_path / "mission.yaml"

    if not mission_file.exists():
        console.print(f"[red]Error:[/red] Mission {mission_id} not found")
        console.print(f"Expected: {mission_file}")
        raise typer.Exit(1)

    # Validate mission
    validator = MissionValidator()
    is_valid, errors = validator.validate_file(mission_file)

    if is_valid:
        console.print(
            Panel(
                f"[green]✓[/green] Mission {mission_id} is valid",
                title="Validation Success",
                border_style="green",
            )
        )
        console.print("\n[bold]Next steps:[/bold]")
        console.print(f"1. Run: missionforge decompose {mission_id}")
        console.print("2. Or manually edit sub-missions in mission.yaml")
    else:
        console.print(
            Panel(
                "[red]✗[/red] Mission validation failed",
                title="Validation Errors",
                border_style="red",
            )
        )

        table = Table(show_header=False, box=None)
        table.add_column("Error", style="red")

        for error in errors:
            table.add_row(f"• {error}")

        console.print(table)
        console.print(f"\n[yellow]Fix errors in:[/yellow] {mission_file}")
        raise typer.Exit(1)


# Made with Bob
