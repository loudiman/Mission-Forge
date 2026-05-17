"""Test command execution utilities."""

import time
from dataclasses import dataclass
from pathlib import Path

from ..core.exceptions import MissionForgeError, TestExecutionError
from ..utils.subprocess_utils import run_command


@dataclass
class TestResult:
    """Test execution result.

    Attributes:
        command: Command that was executed.
        exit_code: Process exit code (0 = success).
        stdout: Standard output from the test command.
        stderr: Standard error from the test command.
        duration: Execution time in seconds.
        timed_out: Whether the command timed out.
        success: Whether the test passed (exit_code == 0 and not timed_out).
    """

    command: list[str]
    exit_code: int
    stdout: str
    stderr: str
    duration: float
    timed_out: bool
    success: bool


def execute_test_command(
    command: list[str],
    cwd: Path | None = None,
    timeout: int = 300,
    env: dict[str, str] | None = None,
) -> TestResult:
    """Execute test command and capture results.

    Safely executes test commands without shell injection vulnerabilities.
    Captures complete stdout/stderr for evidence generation.

    Args:
        command: Test command as list (e.g., ["pytest", "-v", "tests/"]).
        cwd: Working directory for test execution.
        timeout: Timeout in seconds (default: 300 = 5 minutes).
        env: Environment variables (merged with os.environ if provided).

    Returns:
        TestResult with complete execution details.

    Raises:
        TestExecutionError: If command cannot be executed (not found, etc.).

    Examples:
        >>> result = execute_test_command(["pytest", "tests/"])
        >>> print(f"Tests {'passed' if result.success else 'failed'}")
        >>> print(f"Exit code: {result.exit_code}")
        >>> print(f"Duration: {result.duration:.2f}s")

        >>> # With timeout
        >>> result = execute_test_command(
        ...     ["pytest", "tests/"],
        ...     timeout=60
        ... )

        >>> # Different working directory
        >>> result = execute_test_command(
        ...     ["npm", "test"],
        ...     cwd=Path("frontend")
        ... )
    """
    start_time = time.time()
    timed_out = False
    exit_code = -1
    stdout = ""
    stderr = ""

    try:
        # Run command without check=True to capture non-zero exit codes
        result = run_command(
            command,
            cwd=cwd,
            check=False,  # Don't raise on non-zero exit
            timeout=timeout,
            capture_output=True,
            env=env,
        )
        exit_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr

    except MissionForgeError as e:
        error_msg = str(e).lower()

        # Check if it's a timeout
        if "timed out" in error_msg or "timeout" in error_msg:
            timed_out = True
            exit_code = -1
            stdout = ""
            stderr = f"Command timed out after {timeout}s"
        else:
            # Re-raise as TestExecutionError for other errors
            raise TestExecutionError(
                f"Failed to execute test command: {' '.join(command)}", str(e)
            ) from e

    duration = time.time() - start_time
    success = exit_code == 0 and not timed_out

    return TestResult(
        command=command,
        exit_code=exit_code,
        stdout=stdout,
        stderr=stderr,
        duration=duration,
        timed_out=timed_out,
        success=success,
    )


# Made with Bob
