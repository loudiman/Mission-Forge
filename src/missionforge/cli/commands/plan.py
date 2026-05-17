# Made with Bob
"""Plan command - dependency graph resolution and execution order."""

from datetime import UTC, datetime
from pathlib import Path

import pathspec
import typer
import yaml
from rich.console import Console
from rich.panel import Panel

from ...core.workspace import Workspace
from ...models.schemas import ExecutionPlan, SubMission
from ...schemas import SchemaValidator

console = Console()


def plan_command(
    mission_id: str = typer.Argument(..., help="Mission ID to generate execution plan for"),
) -> None:
    """Generate execution plan with dependency graph resolution."""
    try:
        workspace = Workspace()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from None

    mission_path = workspace.mission_path(mission_id)
    mission_file = mission_path / "mission.yaml"

    # Step 1: Load parent mission
    console.print(f"\n[bold cyan]Step 1:[/bold cyan] Loading parent mission {mission_id}...")

    if not mission_file.exists():
        console.print(f"[red]Error:[/red] Mission {mission_id} not found")
        console.print(f"Expected: {mission_file}")
        raise typer.Exit(1)

    try:
        parent_mission = SchemaValidator.validate_parent_mission_file(mission_file)
    except Exception as e:
        console.print(f"[red]Error loading parent mission:[/red] {e}")
        raise typer.Exit(1) from None

    console.print("[green]✓[/green] Parent mission loaded")

    # Step 2: Scan sub-missions
    console.print("\n[bold cyan]Step 2:[/bold cyan] Scanning sub-missions...")

    sub_missions_dir = mission_path / "sub-missions"
    sub_missions = _load_sub_missions(sub_missions_dir)

    if not sub_missions:
        console.print("[red]Error:[/red] No sub-missions found")
        console.print(f"\n[yellow]Tip:[/yellow] Run 'missionforge decompose {mission_id}' first")
        raise typer.Exit(1)

    sub_mission_ids = [sm.id for sm in sub_missions]
    console.print(
        f"[green]✓[/green] Found {len(sub_missions)} sub-missions: {', '.join(sub_mission_ids)}"
    )

    # Step 3: Validate dependencies
    console.print("\n[bold cyan]Step 3:[/bold cyan] Validating dependencies...")

    dep_errors = _validate_all_dependencies(sub_missions)
    parent_errors = _validate_parent_references(sub_missions, mission_id)
    all_errors = dep_errors + parent_errors

    if all_errors:
        error_lines = "\n".join(f"• {e}" for e in all_errors)
        console.print(Panel(error_lines, title="[red]Validation Errors[/red]", border_style="red"))
        raise typer.Exit(1)

    console.print("[green]✓[/green] All dependencies valid")
    console.print("[green]✓[/green] All parent references correct")

    # Build dependency graph and detect cycles
    graph = _build_dependency_graph(sub_missions)

    has_cycle, cycle_path = _detect_cycles(graph)
    if has_cycle:
        cycle_str = " → ".join(cycle_path)
        console.print(
            Panel(
                f"Cycle path:\n  {cycle_str}\n\n"
                "[yellow]To fix:[/yellow] Remove one of these dependencies to break the cycle",
                title="[red]✗ Circular dependency detected![/red]",
                border_style="red",
            )
        )
        console.print("[red]Error:[/red] Cannot generate plan with circular dependencies")
        raise typer.Exit(1)

    console.print("[green]✓[/green] No circular dependencies detected")

    # Step 4: Check path overlaps
    console.print("\n[bold cyan]Step 4:[/bold cyan] Checking path overlaps...")

    overlap_warnings = _check_all_path_overlaps(sub_missions)
    if overlap_warnings:
        for warning in overlap_warnings:
            console.print(f"[yellow]⚠[/yellow] Warning: {warning}")
    else:
        console.print("[green]✓[/green] No path overlaps detected")

    # Step 5: Compute execution order
    console.print("\n[bold cyan]Step 5:[/bold cyan] Computing execution order...")

    try:
        execution_order = _topological_sort(graph)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from None

    console.print("[green]✓[/green] Topological order computed")

    plan = ExecutionPlan(
        mission_id=mission_id,
        decomposition_rationale=parent_mission.decomposition_rationale,
        execution_order=execution_order,
        dependency_graph=graph,
    )
    parallelism = _compute_parallelism_levels(graph, execution_order)

    _display_plan_summary(plan, parallelism)
    _write_plan_file(mission_path, plan, mission_id, parallelism)

    plan_file = mission_path / "plan.yaml"
    console.print(f"\n[green]✓[/green] Plan written to: {plan_file}")


def _load_sub_missions(sub_missions_dir: Path) -> list[SubMission]:
    """Load all valid sub-mission YAML files from directory."""
    sub_missions: list[SubMission] = []

    if not sub_missions_dir.exists():
        return sub_missions

    for sub_file in sorted(sub_missions_dir.glob("*.yaml")):
        try:
            sub_mission = SchemaValidator.validate_sub_mission_file(sub_file)
            sub_missions.append(sub_mission)
        except Exception:
            console.print(f"[yellow]⚠[/yellow] Skipping invalid file: {sub_file.name}")

    return sub_missions


def _build_dependency_graph(sub_missions: list[SubMission]) -> dict[str, list[str]]:
    """Build dependency graph mapping each sub-mission ID to its dependencies."""
    return {sm.id: list(sm.depends_on) for sm in sub_missions}


def _validate_all_dependencies(sub_missions: list[SubMission]) -> list[str]:
    """Validate all dependency references exist. Returns list of error messages."""
    errors: list[str] = []
    all_ids = {sm.id for sm in sub_missions}

    for sub_mission in sub_missions:
        for dep in sub_mission.depends_on:
            if dep not in all_ids:
                errors.append(
                    f"Sub-mission '{sub_mission.id}' depends on "
                    f"non-existent sub-mission '{dep}'"
                )

    return errors


def _validate_parent_references(sub_missions: list[SubMission], parent_id: str) -> list[str]:
    """Validate all sub-missions reference the correct parent. Returns list of error messages."""
    errors: list[str] = []

    for sub_mission in sub_missions:
        if sub_mission.parent != parent_id:
            errors.append(
                f"Sub-mission '{sub_mission.id}' has invalid parent "
                f"reference '{sub_mission.parent}' (expected '{parent_id}')"
            )

    return errors


def _detect_cycles(graph: dict[str, list[str]]) -> tuple[bool, list[str]]:
    """Detect cycles using depth-first search. Returns (has_cycle, cycle_path)."""
    visited: set[str] = set()
    rec_stack: set[str] = set()

    def dfs(node: str, path: list[str]) -> tuple[bool, list[str]]:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                has_cycle, cycle = dfs(neighbor, path.copy())
                if has_cycle:
                    return True, cycle
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                return True, path[cycle_start:] + [neighbor]

        rec_stack.remove(node)
        return False, []

    for node in graph:
        if node not in visited:
            has_cycle, cycle = dfs(node, [])
            if has_cycle:
                return True, cycle

    return False, []


def _topological_sort(graph: dict[str, list[str]]) -> list[str]:
    """Compute topological order using Kahn's algorithm. Raises ValueError if cycle exists."""
    # in_degree = number of unresolved dependencies per node
    in_degree: dict[str, int] = {node: len(graph[node]) for node in graph}

    # successors[A] = nodes that depend on A (must be processed after A)
    successors: dict[str, list[str]] = {node: [] for node in graph}
    for node in graph:
        for dep in graph[node]:
            if dep in successors:
                successors[dep].append(node)

    queue = sorted(node for node in graph if in_degree[node] == 0)
    result: list[str] = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        for successor in successors[node]:
            in_degree[successor] -= 1
            if in_degree[successor] == 0:
                queue.append(successor)
        queue.sort()

    if len(result) != len(graph):
        raise ValueError("Graph contains cycles")

    return result


def _check_all_path_overlaps(sub_missions: list[SubMission]) -> list[str]:
    """Check for overlapping allowed_paths between sub-mission pairs (bidirectional)."""
    warnings: list[str] = []

    for i, sm_a in enumerate(sub_missions):
        if not sm_a.allowed_paths:
            continue
        spec_a = pathspec.PathSpec.from_lines("gitignore", sm_a.allowed_paths)

        for sm_b in sub_missions[i + 1:]:
            if not sm_b.allowed_paths:
                continue

            # Forward: sm_b's concrete paths vs sm_a's patterns
            overlap = any(spec_a.match_file(p) for p in sm_b.allowed_paths)

            # Reverse: sm_a's concrete paths vs sm_b's patterns (catches asymmetric globs)
            if not overlap:
                spec_b = pathspec.PathSpec.from_lines("gitignore", sm_b.allowed_paths)
                overlap = any(spec_b.match_file(p) for p in sm_a.allowed_paths)

            if overlap:
                warnings.append(
                    f"{sm_a.id} and {sm_b.id} have overlapping allowed_paths"
                )

    return warnings


def _compute_parallelism_levels(
    graph: dict[str, list[str]],
    order: list[str],
) -> dict[int, list[str]]:
    """Compute which sub-missions can run in parallel at each level."""
    levels: dict[int, list[str]] = {}
    node_level: dict[str, int] = {}

    for node in order:
        deps = graph.get(node, [])
        level = 0 if not deps else max(node_level[dep] for dep in deps) + 1
        node_level[node] = level
        levels.setdefault(level, []).append(node)

    return levels


def _write_plan_file(
    mission_path: Path,
    plan: ExecutionPlan,
    mission_id: str,
    parallelism: dict[int, list[str]],
) -> None:
    """Write resolved execution plan to plan.yaml."""
    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    header_lines = [
        f"# Generated by missionforge plan {mission_id}",
        f"# Timestamp: {timestamp}",
        "#",
        "# Parallelism analysis (for future Phase 3):",
    ]
    for level in sorted(parallelism.keys()):
        header_lines.append(f"# Level {level}: {', '.join(parallelism[level])}")
    header_lines.append("")

    plan_data: dict = {}
    if plan.mission_id:
        plan_data["mission_id"] = plan.mission_id
    if plan.decomposition_rationale:
        plan_data["decomposition_rationale"] = plan.decomposition_rationale
    plan_data["execution_order"] = plan.execution_order
    plan_data["dependency_graph"] = plan.dependency_graph
    yaml_content = yaml.dump(plan_data, default_flow_style=False, sort_keys=False)

    plan_file = mission_path / "plan.yaml"
    plan_file.write_text("\n".join(header_lines) + "\n" + yaml_content)


def _display_plan_summary(
    plan: ExecutionPlan,
    parallelism: dict[int, list[str]],
) -> None:
    """Display execution plan summary with order and parallelism levels."""
    order_lines = "\n".join(
        f"  {i + 1}. {mid}" for i, mid in enumerate(plan.execution_order)
    )
    level_parts = []
    for lvl, ms in sorted(parallelism.items()):
        if lvl == 0:
            level_parts.append(f"  [green]Ready  [/green] [Level {lvl}]: {', '.join(ms)}")
        else:
            blocked_by = sorted({dep for m in ms for dep in plan.dependency_graph.get(m, [])})
            level_parts.append(
                f"  [yellow]Blocked[/yellow] [Level {lvl}]: {', '.join(ms)}"
                f"  [dim](waiting on: {', '.join(blocked_by)})[/dim]"
            )
    level_lines = "\n".join(level_parts)
    content = (
        f"[bold]Execution Order:[/bold]\n{order_lines}\n\n"
        f"[bold]Parallelism Analysis:[/bold]\n{level_lines}\n\n"
        "[dim]Note: Phase 1 executes sequentially.\n"
        "Parallel execution coming in Phase 3.[/dim]"
    )
    console.print(Panel(content, title="Execution Plan", border_style="green"))
