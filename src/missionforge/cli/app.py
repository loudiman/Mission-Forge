"""Main CLI application."""

from pathlib import Path

import typer
from rich.console import Console

from ..core.config import MissionForgeConfig
from ..core.exceptions import MissionForgeError
from ..core.logging import setup_logging
from ..core.workspace import Workspace
from .commands import workspace

app = typer.Typer(
    name="missionforge",
    help="AI-assisted mission decomposition and validation",
    add_completion=False,
    rich_markup_mode="rich",
)

console = Console()

# Global state
_workspace: Workspace | None = None
_config: MissionForgeConfig | None = None


def get_workspace() -> Workspace:
    """Get or create workspace instance.

    Returns:
        Workspace instance.
    """
    global _workspace
    if _workspace is None:
        _workspace = Workspace()
    return _workspace


def get_config() -> MissionForgeConfig:
    """Get or create config instance.

    Returns:
        Configuration instance.
    """
    global _config
    if _config is None:
        config_path = MissionForgeConfig.get_default_config_path()
        _config = MissionForgeConfig.load(config_path)
    return _config


# Register command groups
app.add_typer(workspace.app, name="workspace")


@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    log_file: Path | None = typer.Option(None, "--log-file", help="Log to file"),  # noqa: B008
) -> None:
    """MissionForge CLI - AI-assisted mission management."""

    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(level=log_level, log_file=log_file)

    # Store in context for commands
    ctx.obj = {"workspace": get_workspace, "config": get_config, "console": console}


@app.command()
def version() -> None:
    """Show version information."""
    console.print("[bold]MissionForge[/bold] v0.1.0")
    console.print("Python 3.11+ required")


def cli_main() -> None:
    """Entry point with error handling."""
    try:
        app()
    except MissionForgeError as e:
        console.print(e.format_error(), style="bold red")
        raise typer.Exit(1) from e
    except KeyboardInterrupt as e:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        raise typer.Exit(130) from e
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        if "--verbose" in str(e) or "-v" in str(e):
            raise
        raise typer.Exit(1) from e


if __name__ == "__main__":
    cli_main()

# Made with Bob
