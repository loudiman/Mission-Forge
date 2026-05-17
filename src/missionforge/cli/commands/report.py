"""Report generation commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from ...core.exceptions import MissionForgeError
from ...core.report_generator import ReportGenerator
from ...core.workspace import Workspace

console = Console()


def _validate_output_path(output_path: Path, workspace_root: Path) -> None:
    """Validate output path for security issues.

    Args:
        output_path: The requested output path.
        workspace_root: The workspace root directory.

    Raises:
        typer.Exit: If path validation fails.
    """
    try:
        # Resolve to absolute path
        resolved_path = output_path.resolve()

        # Check for path traversal attempts
        # Allow paths within workspace or in user's home directory
        workspace_resolved = workspace_root.resolve()
        home_dir = Path.home().resolve()

        # Check if path is within allowed directories
        try:
            # Try to get relative path from workspace
            resolved_path.relative_to(workspace_resolved)
            return  # Path is within workspace - OK
        except ValueError:
            pass

        try:
            # Try to get relative path from home
            resolved_path.relative_to(home_dir)
            return  # Path is within home directory - OK
        except ValueError:
            pass

        # Path is outside allowed directories
        console.print(
            "[red]Error:[/red] Output path must be within workspace or home directory"
        )
        console.print(f"Workspace: {workspace_resolved}")
        console.print(f"Home: {home_dir}")
        console.print(f"Requested: {resolved_path}")
        raise typer.Exit(1)

    except (OSError, RuntimeError) as e:
        console.print(f"[red]Error:[/red] Invalid output path: {e}")
        raise typer.Exit(1) from e


def report_command(
    ctx: typer.Context,
    mission_id: str = typer.Argument(..., help="Mission ID (e.g., MF-001)"),
    output: Path | None = typer.Option(  # noqa: B008
        None, "--output", "-o", help="Custom output path for report"
    ),
    stdout: bool = typer.Option(False, "--stdout", help="Output report to stdout instead of file"),
) -> None:
    """Generate PR-ready Markdown evidence report for a mission.

    This command generates a comprehensive report summarizing:
    - Mission goal and overall status
    - Sub-mission results with metrics
    - Test results (parent and sub-missions)
    - Files changed summary
    - Aggregate metrics comparison
    - Forbidden path violations (if any)
    - Next suggested mission

    The report is suitable for:
    - Attaching to pull requests
    - Mission completion evidence
    - Judging artifacts

    Examples:
        # Generate report in mission directory
        missionforge report MF-001

        # Output to custom path
        missionforge report MF-001 --output ./my-report.md

        # Output to stdout
        missionforge report MF-001 --stdout
    """
    try:
        workspace = Workspace()
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    mission_path = workspace.mission_path(mission_id)

    if not mission_path.exists():
        console.print(f"[red]Error:[/red] Mission {mission_id} not found")
        console.print(f"Expected: {mission_path}")
        raise typer.Exit(1)

    mission_file = mission_path / "mission.yaml"
    if not mission_file.exists():
        console.print(f"[red]Error:[/red] Mission file not found: {mission_file}")
        console.print(f"Initialize mission with: missionforge init {mission_id}")
        raise typer.Exit(1)

    # Validate output path if provided
    if output and not stdout:
        _validate_output_path(output, workspace.root)

    # Generate report
    console.print(f"[cyan]Generating report for mission {mission_id}...[/cyan]")

    try:
        generator = ReportGenerator()
        report_content, output_path = generator.generate_report(mission_path, output)

        if stdout:
            # Output to stdout
            console.print("\n" + "=" * 80)
            console.print(report_content)
            console.print("=" * 80 + "\n")
        else:
            # Report written to file
            console.print(
                Panel(
                    f"[green]✓[/green] Report generated successfully\n\n"
                    f"[bold]Output:[/bold] {output_path}\n"
                    f"[bold]Size:[/bold] {len(report_content)} characters",
                    title="Report Generation Complete",
                    border_style="green",
                )
            )

            console.print("\n[bold]Next steps:[/bold]")
            console.print(f"1. Review report: {output_path}")
            console.print("2. Attach report to your pull request")
            console.print("3. Use report as evidence for mission completion")

    except MissionForgeError as e:
        console.print(
            Panel(
                f"[red]✗[/red] Report generation failed\n\n{e.format_error()}",
                title="Error",
                border_style="red",
            )
        )
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]Error:[/red] Unexpected error during report generation: {e}")
        if ctx.obj and ctx.obj.get("verbose"):
            raise
        raise typer.Exit(1) from e


# Made with Bob
