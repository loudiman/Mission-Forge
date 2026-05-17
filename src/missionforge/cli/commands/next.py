# Made with Bob
"""Next command - identify sub-missions ready for execution."""

import json

import typer
from rich.console import Console

from ...core.workspace import Workspace
from ...models.schemas import SubMissionValidation
from ...schemas import SchemaValidator

console = Console()


def next_command(
    mission_id: str = typer.Argument(..., help="Mission ID to check execution status for"),
) -> None:
    """Identify next sub-mission(s) ready for execution based on dependency graph."""
    try:
        workspace = Workspace()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from None

    mission_path = workspace.mission_path(mission_id)
    plan_file = mission_path / "plan.yaml"

    if not plan_file.exists():
        console.print(f"[red]Error:[/red] No plan.yaml found for {mission_id}")
        console.print(f"[yellow]Tip:[/yellow] Run 'missionforge plan {mission_id}' first")
        raise typer.Exit(1)

    try:
        plan = SchemaValidator.validate_plan_file(plan_file)
    except Exception as e:
        console.print(f"[red]Error loading plan:[/red] {e}")
        raise typer.Exit(1) from None

    if not plan.execution_order:
        console.print(f"[red]Error:[/red] Plan for {mission_id} has no sub-missions")
        raise typer.Exit(1)

    status_map = _scan_validation_status(workspace, plan.execution_order)

    complete: list[str] = []
    ready: list[tuple[str, list[str]]] = []
    blocked: list[tuple[str, list[str]]] = []
    failed: list[str] = []
    pending: list[str] = []

    for sub_id in plan.execution_order:
        status = status_map[sub_id]
        deps = plan.dependency_graph.get(sub_id, [])

        if status == "PASSED":
            complete.append(sub_id)
        elif status == "FAILED":
            failed.append(sub_id)
        elif status == "captured":
            pending.append(sub_id)
        elif status is None:
            if all(status_map.get(dep) == "PASSED" for dep in deps):
                satisfied = [d for d in deps if d in complete or status_map.get(d) == "PASSED"]
                ready.append((sub_id, satisfied))
            else:
                blocked.append((sub_id, deps))
        else:  # "BLOCKED" from validation service
            blocked.append((sub_id, deps))

    _display_progress(mission_id, complete, ready, blocked, failed, pending, len(plan.execution_order))

    if len(complete) == len(plan.execution_order):
        raise typer.Exit(0)
    if not ready:
        raise typer.Exit(1)


def _scan_validation_status(
    workspace: Workspace, sub_mission_ids: list[str]
) -> dict[str, str | None]:
    """Return status for each sub-mission by reading validation.json files."""
    status_map: dict[str, str | None] = {}

    for sub_id in sub_mission_ids:
        validation_path = workspace.validation_path(sub_id)

        if not validation_path.exists():
            status_map[sub_id] = None
            continue

        try:
            with open(validation_path) as f:
                data = json.load(f)
            validation = SubMissionValidation(**data)
            status_map[sub_id] = validation.status
        except Exception as e:
            console.print(f"[yellow]Warning:[/yellow] Could not read {validation_path}: {e}")
            status_map[sub_id] = None

    return status_map


def _display_progress(
    mission_id: str,
    complete: list[str],
    ready: list[tuple[str, list[str]]],
    blocked: list[tuple[str, list[str]]],
    failed: list[str],
    pending: list[str],
    total: int,
) -> None:
    """Display formatted progress summary."""
    console.print(
        f"\n[bold]Mission {mission_id} Progress:[/bold] {len(complete)}/{total} sub-missions complete\n"
    )

    if len(complete) == total:
        console.print("[bold green]All sub-missions complete![/bold green]")
        return

    if ready:
        console.print("[bold green]READY TO EXECUTE:[/bold green]")
        for i, (sub_id, satisfied_deps) in enumerate(ready):
            marker = "→" if i == 0 else " "
            suffix = " (recommended next)" if i == 0 else ""
            console.print(f"  {marker} [green]{sub_id}[/green]{suffix}")
            if satisfied_deps:
                console.print(f"    Dependencies satisfied: {', '.join(satisfied_deps)}")

        if len(ready) > 1:
            parallel_ids = ", ".join(sub_id for sub_id, _ in ready[1:])
            console.print(f"\n[dim]Note: {parallel_ids} can run in parallel (Phase 3 feature)[/dim]")
    elif not complete:
        console.print("[yellow]No sub-missions are ready to execute.[/yellow]")
        console.print("Check failed dependencies and resolve before proceeding.")
    else:
        console.print("[yellow]No sub-missions are ready. Resolve failed sub-missions to unblock.[/yellow]")

    if blocked:
        console.print("\n[bold yellow]BLOCKED:[/bold yellow]")
        for sub_id, deps in blocked:
            console.print(f"  ⊗ [yellow]{sub_id}[/yellow]")
            waiting_for = [d for d in deps if d not in complete]
            if waiting_for:
                console.print(f"    Waiting for: {', '.join(waiting_for)}")

    if pending:
        console.print("\n[bold cyan]PENDING COMMIT:[/bold cyan]")
        for sub_id in pending:
            console.print(f"  ◎ [cyan]{sub_id}[/cyan]")
            console.print("    Validation captured — run 'missionforge validate commit' to finalize")

    if failed:
        console.print("\n[bold red]FAILED:[/bold red]")
        for sub_id in failed:
            console.print(f"  ✗ [red]{sub_id}[/red]")

    if complete:
        console.print("\n[bold]COMPLETE:[/bold]")
        for sub_id in complete:
            console.print(f"  ✓ [green]{sub_id}[/green]")
