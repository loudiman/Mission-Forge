"""Mission decomposition command."""

import re
from pathlib import Path

import pathspec
import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from ...core.mission_validator import MissionValidator
from ...core.workspace import Workspace
from ...schemas import SchemaValidator

console = Console()


def decompose_command(
    mission_id: str = typer.Argument(..., help="Parent mission ID to decompose"),
) -> None:
    """Decompose a parent mission into sub-missions.
    
    This command guides Bob through the process of creating sub-missions:
    1. Validates the parent mission exists and is valid
    2. Creates the sub-missions directory structure
    3. Displays templates and instructions for creating sub-mission files
    4. Validates each sub-mission as it's created
    5. Provides guidance for creating plan.yaml
    """
    try:
        workspace = Workspace()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    mission_path = workspace.mission_path(mission_id)
    mission_file = mission_path / "mission.yaml"

    # Step 1: Validate parent mission exists
    console.print(f"\n[bold cyan]Step 1:[/bold cyan] Validating parent mission {mission_id}...")
    
    if not mission_file.exists():
        console.print(f"[red]Error:[/red] Mission {mission_id} not found")
        console.print(f"Expected: {mission_file}")
        console.print("\n[yellow]Tip:[/yellow] Create the mission first using:")
        console.print(f"  missionforge init {mission_id}")
        raise typer.Exit(1)

    # Validate mission
    validator = MissionValidator()
    is_valid, errors = validator.validate_file(mission_file)

    if not is_valid:
        console.print(
            Panel(
                "[red]✗[/red] Parent mission validation failed",
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

    console.print("[green]✓[/green] Parent mission is valid")

    # Load parent mission for reference
    try:
        parent_mission = SchemaValidator.validate_parent_mission_file(mission_file)
    except Exception as e:
        console.print(f"[red]Error loading parent mission:[/red] {e}")
        raise typer.Exit(1)

    # Step 2: Create sub-missions directory
    console.print(f"\n[bold cyan]Step 2:[/bold cyan] Setting up sub-missions directory...")
    
    sub_missions_dir = mission_path / "sub-missions"
    already_existed = sub_missions_dir.exists()
    sub_missions_dir.mkdir(exist_ok=True)

    if already_existed:
        console.print(f"[cyan]ℹ[/cyan] Already exists: {sub_missions_dir}")
    else:
        console.print(f"[green]✓[/green] Created: {sub_missions_dir}")

    # Step 3: Display instructions and templates
    console.print(f"\n[bold cyan]Step 3:[/bold cyan] Create sub-mission files")
    
    _display_decomposition_instructions(mission_id, parent_mission.goal, sub_missions_dir)
    
    # Step 4: Display sub-mission template
    console.print(f"\n[bold cyan]Step 4:[/bold cyan] Sub-mission template")
    _display_sub_mission_template(mission_id)

    # Step 5: Display validation guidance
    console.print(f"\n[bold cyan]Step 5:[/bold cyan] Validate sub-missions as you create them")
    _display_validation_guidance(mission_id, sub_missions_dir)

    # Step 6: Display plan.yaml guidance
    console.print(f"\n[bold cyan]Step 6:[/bold cyan] Create execution plan")
    _display_plan_guidance(mission_id, mission_path)

    # Step 7: Check for existing sub-missions
    console.print(f"\n[bold cyan]Current Status:[/bold cyan]")
    _display_current_status(sub_missions_dir, mission_path, parent_mission.id)

    # Final summary
    console.print(
        Panel(
            "[bold green]Decomposition workspace ready![/bold green]\n\n"
            "Follow the steps above to create your sub-missions.\n"
            "Bob will validate each file as you create it.",
            title="✓ Setup Complete",
            border_style="green",
        )
    )


def _display_decomposition_instructions(
    mission_id: str, parent_goal: str, sub_missions_dir: Path
) -> None:
    """Display instructions for Bob on how to decompose the mission."""
    
    instructions = f"""[bold]Instructions for Bob:[/bold]

1. [cyan]Read the codebase[/cyan] to understand the current structure
2. [cyan]Analyze the parent goal:[/cyan] {parent_goal}
3. [cyan]Break down into logical sub-missions[/cyan] (e.g., {mission_id}-A, {mission_id}-B, etc.)
4. [cyan]Create YAML files[/cyan] in: {sub_missions_dir}
   - Name files: {mission_id}-A.yaml, {mission_id}-B.yaml, etc.
   - Each file represents one sub-mission

[bold yellow]Important Rules:[/bold yellow]
• Sub-mission IDs must follow pattern: {mission_id}-[A-Z]
• Each sub-mission must reference parent: {mission_id}
• allowed_paths should not overlap between sub-missions
• Define clear dependencies using depends_on field
"""
    
    console.print(Panel(instructions, title="📋 Decomposition Guide", border_style="cyan"))


def _display_sub_mission_template(mission_id: str) -> None:
    """Display sub-mission YAML template."""
    
    template = f"""id: {mission_id}-A
parent: {mission_id}
title: "Short descriptive title"
goal: "Specific goal for this sub-mission"

# Dependencies (optional)
depends_on:
  - {mission_id}-B  # This sub-mission depends on B completing first

# Paths this sub-mission can modify
allowed_paths:
  - "src/module_a/**"
  - "tests/test_module_a.py"

# Metrics for this sub-mission (optional)
metrics:
  test_coverage:
    min: 80.0
    target: 90.0
  lines_added:
    max: 500

# Test command (optional, inherits from parent if not specified)
test_command: "pytest tests/test_module_a.py -v"
"""
    
    syntax = Syntax(template, "yaml", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=f"📄 Template: {mission_id}-A.yaml", border_style="blue"))


def _display_validation_guidance(mission_id: str, sub_missions_dir: Path) -> None:
    """Display guidance on validating sub-missions."""
    
    guidance = f"""After creating each sub-mission file, validate it:

[cyan]Command:[/cyan]
  missionforge validate-submission {mission_id} {mission_id}-A

[bold]What gets validated:[/bold]
• ✓ Sub-mission ID format ({mission_id}-[A-Z])
• ✓ Parent reference matches {mission_id}
• ✓ allowed_paths don't conflict with forbidden_paths
• ✓ allowed_paths don't overlap with other sub-missions
• ✓ Dependencies reference valid sub-missions
• ✓ YAML syntax and schema compliance

[yellow]Tip:[/yellow] Validate frequently to catch errors early!
"""
    
    console.print(Panel(guidance, title="🔍 Validation", border_style="yellow"))


def _display_plan_guidance(mission_id: str, mission_path: Path) -> None:
    """Display guidance for creating plan.yaml."""
    
    plan_template = f"""# Execution plan for {mission_id}

# Ordered list of sub-missions to execute
execution_order:
  - {mission_id}-A
  - {mission_id}-B
  - {mission_id}-C

# Dependency graph (maps each sub-mission to its dependencies)
dependency_graph:
  {mission_id}-A: []  # No dependencies, can start immediately
  {mission_id}-B: [{mission_id}-A]  # Depends on A
  {mission_id}-C: [{mission_id}-A, {mission_id}-B]  # Depends on both A and B
"""
    
    syntax = Syntax(plan_template, "yaml", theme="monokai", line_numbers=True)
    
    guidance = f"""Create [cyan]plan.yaml[/cyan] in: {mission_path}

This file defines the execution order and dependencies.

[bold]Requirements:[/bold]
• execution_order must list all sub-missions
• dependency_graph must include all sub-missions
• No circular dependencies allowed
• Dependencies must exist in execution_order
"""
    
    console.print(Panel(guidance, title="📊 Execution Plan", border_style="magenta"))
    console.print(syntax)


def _display_current_status(
    sub_missions_dir: Path, mission_path: Path, parent_id: str
) -> None:
    """Display current status of sub-missions and plan."""
    
    table = Table(title="Current Files", show_header=True, header_style="bold cyan")
    table.add_column("File", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Validation", style="yellow")

    # Check for sub-mission files
    sub_mission_files = list(sub_missions_dir.glob("*.yaml")) if sub_missions_dir.exists() else []
    
    if sub_mission_files:
        for sub_file in sorted(sub_mission_files):
            # Validate the file
            try:
                sub_mission = SchemaValidator.validate_sub_mission_file(sub_file)
                
                # Check parent relationship
                if sub_mission.parent != parent_id:
                    status = "❌ Parent mismatch"
                    validation = f"Expected: {parent_id}"
                else:
                    # Validate ID format: suffix must be exactly one letter A-Z.
                    # This intentionally caps each parent at 26 sub-missions.
                    pattern = rf"^{re.escape(parent_id)}-[A-Z]$"
                    if re.match(pattern, sub_mission.id):
                        status = "✓ Valid"
                        validation = "OK"
                    else:
                        status = "❌ Invalid ID"
                        validation = f"Must be {parent_id}-A … {parent_id}-Z (max 26)"
                        
            except Exception as e:
                status = "❌ Invalid"
                validation = str(e)[:50] + "..." if len(str(e)) > 50 else str(e)
            
            table.add_row(sub_file.name, status, validation)
    else:
        table.add_row("(no sub-missions yet)", "—", "Create files to begin")

    # Check for plan.yaml
    plan_file = mission_path / "plan.yaml"
    if plan_file.exists():
        try:
            SchemaValidator.validate_plan_file(plan_file)
            table.add_row("plan.yaml", "✓ Valid", "OK")
        except Exception as e:
            error_msg = str(e)[:50] + "..." if len(str(e)) > 50 else str(e)
            table.add_row("plan.yaml", "❌ Invalid", error_msg)
    else:
        table.add_row("plan.yaml", "⚠ Missing", "Create after sub-missions")

    console.print(table)


def validate_submission_command(
    mission_id: str = typer.Argument(..., help="Parent mission ID"),
    sub_mission_id: str = typer.Argument(..., help="Sub-mission ID to validate"),
) -> None:
    """Validate a specific sub-mission file.
    
    This command validates:
    - Sub-mission file exists and has valid YAML
    - ID format matches parent-[A-Z] pattern
    - Parent reference is correct
    - allowed_paths don't conflict with forbidden_paths
    - Dependencies reference valid sub-missions
    """
    try:
        workspace = Workspace()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)

    mission_path = workspace.mission_path(mission_id)
    sub_missions_dir = mission_path / "sub-missions"
    sub_mission_file = sub_missions_dir / f"{sub_mission_id}.yaml"

    console.print(f"\n[bold]Validating:[/bold] {sub_mission_file}")

    # Check file exists
    if not sub_mission_file.exists():
        console.print(f"[red]Error:[/red] Sub-mission file not found: {sub_mission_file}")
        console.print(f"\n[yellow]Expected location:[/yellow] {sub_missions_dir}/{sub_mission_id}.yaml")
        raise typer.Exit(1)

    # Validate parent mission first
    mission_file = mission_path / "mission.yaml"
    if not mission_file.exists():
        console.print(f"[red]Error:[/red] Parent mission not found: {mission_file}")
        raise typer.Exit(1)

    try:
        parent_mission = SchemaValidator.validate_parent_mission_file(mission_file)
    except Exception as e:
        console.print(f"[red]Error:[/red] Parent mission validation failed: {e}")
        raise typer.Exit(1)

    # Validate sub-mission
    errors = []
    warnings = []

    try:
        sub_mission = SchemaValidator.validate_sub_mission_file(sub_mission_file)
        console.print("[green]✓[/green] YAML syntax and schema valid")
    except Exception as e:
        console.print(f"[red]✗[/red] Schema validation failed: {e}")
        raise typer.Exit(1)

    # Validate ID format: suffix must be exactly one letter A-Z.
    # This intentionally caps each parent mission at 26 sub-missions (A–Z).
    pattern = rf"^{re.escape(mission_id)}-[A-Z]$"
    if not re.match(pattern, sub_mission.id):
        errors.append(
            f"Invalid sub-mission ID format: {sub_mission.id}\n"
            f"  Expected: {mission_id}-A through {mission_id}-Z "
            f"(single letter suffix, max 26 sub-missions per parent)"
        )
    else:
        console.print(f"[green]✓[/green] ID format valid: {sub_mission.id}")

    # Validate parent reference
    if sub_mission.parent != parent_mission.id:
        errors.append(
            f"Parent mismatch: sub-mission references '{sub_mission.parent}' "
            f"but should reference '{parent_mission.id}'"
        )
    else:
        console.print(f"[green]✓[/green] Parent reference correct: {parent_mission.id}")

    # Validate forbidden paths
    try:
        SchemaValidator.validate_forbidden_paths(parent_mission, sub_mission)
        console.print("[green]✓[/green] No conflicts with forbidden paths")
    except Exception as e:
        errors.append(str(e))

    # Check for overlapping allowed_paths with other sub-missions
    if sub_missions_dir.exists():
        overlaps = _check_path_overlaps(sub_mission, sub_missions_dir, sub_mission_file)
        if overlaps:
            warnings.extend(overlaps)

    # Validate dependencies exist
    if sub_mission.depends_on:
        available_missions = _get_available_sub_missions(sub_missions_dir)
        missing_deps = [dep for dep in sub_mission.depends_on if dep not in available_missions]
        
        if missing_deps:
            errors.append(
                f"Missing dependencies: {', '.join(missing_deps)}\n"
                f"  These sub-missions must be created first"
            )
        else:
            console.print(f"[green]✓[/green] All dependencies exist: {', '.join(sub_mission.depends_on)}")

    # Display results
    if errors:
        console.print(
            Panel(
                "[red]✗[/red] Validation failed",
                title="Validation Errors",
                border_style="red",
            )
        )
        table = Table(show_header=False, box=None)
        table.add_column("Error", style="red")
        for error in errors:
            table.add_row(f"• {error}")
        console.print(table)
        raise typer.Exit(1)

    if warnings:
        console.print("\n[bold yellow]Warnings:[/bold yellow]")
        for warning in warnings:
            console.print(f"[yellow]⚠[/yellow] {warning}")

    console.print(
        Panel(
            f"[green]✓[/green] Sub-mission {sub_mission_id} is valid!",
            title="Validation Success",
            border_style="green",
        )
    )


def _check_path_overlaps(
    sub_mission, sub_missions_dir: Path, current_file: Path
) -> list[str]:
    """Check for overlapping allowed_paths with other sub-missions."""
    overlaps = []

    if not sub_mission.allowed_paths:
        return overlaps

    current_spec = pathspec.PathSpec.from_lines("gitignore", sub_mission.allowed_paths)

    for other_file in sub_missions_dir.glob("*.yaml"):
        if other_file == current_file:
            continue

        try:
            other_mission = SchemaValidator.validate_sub_mission_file(other_file)
            if not other_mission.allowed_paths:
                continue

            other_spec = pathspec.PathSpec.from_lines("gitignore", other_mission.allowed_paths)

            # Collect conflicting paths from both directions into a set so that
            # a path found by both checks (the common case for identical entries)
            # is reported only once.
            conflict_paths: set[str] = set()

            for path in other_mission.allowed_paths:
                if current_spec.match_file(path):
                    conflict_paths.add(path)

            for path in sub_mission.allowed_paths:
                if other_spec.match_file(path):
                    conflict_paths.add(path)

            for path in sorted(conflict_paths):
                overlaps.append(
                    f"Path '{path}' overlaps with {other_mission.id}'s allowed_paths"
                )
        except Exception:
            # Skip invalid files
            continue
    
    return overlaps


def _get_available_sub_missions(sub_missions_dir: Path) -> list[str]:
    """Get list of valid sub-mission IDs."""
    missions = []
    
    if not sub_missions_dir.exists():
        return missions
    
    for sub_file in sub_missions_dir.glob("*.yaml"):
        try:
            sub_mission = SchemaValidator.validate_sub_mission_file(sub_file)
            missions.append(sub_mission.id)
        except Exception:
            # Skip invalid files
            continue
    
    return missions


# Made with Bob