"""Safe subprocess execution utilities."""

import os
import subprocess
from pathlib import Path

from ..core.exceptions import MissionForgeError


def run_command(
    args: list[str],
    cwd: Path | None = None,
    check: bool = True,
    timeout: int = 30,
    capture_output: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run command safely via subprocess.

    NEVER uses shell=True to prevent shell injection attacks.

    Args:
        args: Command and arguments as list (e.g., ["git", "status"]).
        cwd: Working directory for command execution.
        check: Whether to raise exception on non-zero exit code.
        timeout: Command timeout in seconds.
        capture_output: Whether to capture stdout/stderr.
        env: Environment variables to merge with the current process environment.

    Returns:
        CompletedProcess instance with result.

    Raises:
        MissionForgeError: If command fails or times out.
    """
    if not args:
        raise MissionForgeError(
            "Cannot run empty command",
            "Provide a command name and optional arguments as a non-empty list",
        )

    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=check,
            timeout=timeout,
            env=merged_env,
        )
        return result
    except subprocess.CalledProcessError as e:
        raise MissionForgeError(
            f"Command failed: {' '.join(args)}",
            f"Exit code: {e.returncode}\nError: {e.stderr}",
        ) from e
    except subprocess.TimeoutExpired as e:
        raise MissionForgeError(
            f"Command timed out after {timeout}s: {' '.join(args)}",
            "Consider increasing timeout or checking system state",
        ) from e
    except FileNotFoundError as e:
        raise MissionForgeError(
            f"Command not found: {args[0]}",
            f"Ensure {args[0]} is installed and in PATH",
        ) from e


def run_command_silent(
    args: list[str],
    cwd: Path | None = None,
    timeout: int = 30,
) -> bool:
    """Run command and return success status without raising exceptions.

    Args:
        args: Command and arguments as list.
        cwd: Working directory for command execution.
        timeout: Command timeout in seconds.

    Returns:
        True if command succeeded (exit code 0), False otherwise.
    """
    try:
        result = run_command(args, cwd=cwd, check=False, timeout=timeout)
        return result.returncode == 0
    except MissionForgeError:
        return False


# Made with Bob
