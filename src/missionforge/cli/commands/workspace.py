"""Workspace management commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ...core.exceptions import InvalidMissionIDError
from ...core.workspace import Workspace
from ..utils.validation import validate_mission_id

app = typer.Typer(help="Workspace management commands")
console = Console()


@app.command("init")
def init_workspace(
    mission_id: str = typer.Argument(..., help="Mission ID (e.g., MF-001)"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing mission"),
) -> None:
    """Initialize a new mission workspace."""

    # Validate mission ID
    if not validate_mission_id(mission_id):
        raise InvalidMissionIDError(mission_id)

    # Create workspace if it doesn't exist
    try:
        workspace = Workspace()
    except Exception:
        # Workspace doesn't exist, create it
        workspace_root = Path.cwd()
        workspace_dir = workspace_root / ".missionforge"
        workspace_dir.mkdir(exist_ok=True)
        workspace = Workspace(start_path=workspace_root)

    mission_path = workspace.mission_path(mission_id)

    if mission_path.exists() and not force:
        console.print(f"[yellow]Mission {mission_id} already exists[/yellow]")
        console.print("Use --force to overwrite")
        raise typer.Exit(1)

    # Create directory structure
    mission_path.mkdir(parents=True, exist_ok=True)
    (mission_path / "sub-missions").mkdir(exist_ok=True)

    # Create template files
    _create_mission_template(mission_path / "mission.yaml", mission_id)
    _create_plan_template(mission_path / "plan.yaml")
    (mission_path / "report.md").touch()

    console.print(f"[green]✓[/green] Initialized mission {mission_id}")
    console.print("\n[bold]Next steps:[/bold]")
    console.print(f"1. Edit {mission_path / 'mission.yaml'}")
    console.print(f"2. Run: missionforge mission {mission_id} --validate")


@app.command("status")
def workspace_status() -> None:
    """Show workspace status and missions."""

    try:
        workspace = Workspace()
    except Exception as e:
        console.print("[yellow]No workspace initialized[/yellow]")
        console.print("Run: missionforge workspace init <mission-id>")
        raise typer.Exit(1) from e

    if not workspace.exists():
        console.print("[yellow]No workspace initialized[/yellow]")
        console.print("Run: missionforge workspace init <mission-id>")
        raise typer.Exit(1)

    # List missions
    missions = workspace.list_missions()

    if not missions:
        console.print("[yellow]No missions found[/yellow]")
        console.print(f"\nWorkspace location: {workspace.workspace_dir}")
        return

    table = Table(title="Missions")
    table.add_column("Mission ID", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Sub-missions", justify="right")

    for mission_id in missions:
        mission_path = workspace.mission_path(mission_id)
        sub_missions_dir = mission_path / "sub-missions"
        sub_mission_count = 0
        if sub_missions_dir.exists():
            sub_mission_count = len(list(sub_missions_dir.glob("*.yaml")))
        table.add_row(mission_id, "Active", str(sub_mission_count))

    console.print(table)
    console.print(f"\nWorkspace location: {workspace.workspace_dir}")


def _create_mission_template(path: Path, mission_id: str) -> None:
    """Create mission.yaml template with comprehensive documentation.

    Args:
        path: Path where template should be created.
        mission_id: Mission identifier.
    """
    template = f"""# Mission Configuration: {mission_id}
# This file defines the parent mission scope, constraints, and validation criteria.

# Mission identifier - must match directory name
id: {mission_id}

# High-level mission objective
# Describe what should be accomplished and why
goal: |
  Describe the high-level goal of this mission.
  What problem are you solving?
  What should be accomplished?

# Paths that sub-missions CANNOT modify
# Use glob patterns to protect critical code
# Examples:
#   - "core/**"           # Protect entire core directory
#   - "config/*.json"     # Protect config files
#   - "**/*_test.py"      # Protect test files
forbidden_paths:
  - "core/**"
  - "config/**"

# Optional: Paths that sub-missions CAN modify
# If not specified, all paths except forbidden_paths are allowed
# allowed_paths:
#   - "src/features/**"
#   - "src/utils/**"

# Aggregate metrics to validate across ALL sub-missions
# Each metric must have at least one constraint: max, min, or target
# Common metrics:
#   - total_files_changed: Track scope creep
#   - total_lines_changed: Measure impact
#   - test_coverage: Ensure quality
aggregate_metrics:
  total_files_changed:
    max: 50
    description: "Limit scope to prevent mission creep"
  total_lines_changed:
    max: 1000
    description: "Keep changes reviewable"

# Command to validate mission completion
# This should run your test suite or validation checks
# Examples:
#   - "pytest tests/"
#   - "npm test"
#   - "make test"
test_command: "pytest tests/"

# Sub-missions (populated by 'missionforge decompose')
# Each sub-mission represents a discrete, reviewable unit of work
sub_missions: []

# Optional: Additional metadata
# owner: "team-name"
# priority: "high"
# estimated_hours: 8
"""
    path.write_text(template)


def _create_plan_template(path: Path) -> None:
    """Create plan.yaml template.

    Args:
        path: Path where template should be created.
    """
    template = """# Execution plan (generated by 'missionforge plan')
execution_order: []
dependency_graph: {}
"""
    path.write_text(template)


# Made with Bob
