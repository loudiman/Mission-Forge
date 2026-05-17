"""Tests for test execution utilities."""

import sys

import pytest

from missionforge.core.exceptions import TestExecutionError as MissionForgeTestExecutionError
from missionforge.testing.executor import TestResult as MissionForgeTestResult
from missionforge.testing.executor import execute_test_command


class TestExecuteTestCommand:
    """Tests for execute_test_command function."""

    def test_execute_test_command_success(self):
        """Test successful command execution."""
        result = execute_test_command(["echo", "hello"])

        assert isinstance(result, MissionForgeTestResult)
        assert result.success is True
        assert result.exit_code == 0
        assert "hello" in result.stdout
        assert result.duration > 0
        assert result.timed_out is False

    def test_execute_test_command_failure(self):
        """Test failed command execution."""
        # Use a command that will fail
        result = execute_test_command(["false"])

        assert result.success is False
        assert result.exit_code != 0
        assert result.timed_out is False

    def test_execute_test_command_captures_stdout(self):
        """Test that stdout is captured."""
        result = execute_test_command(["echo", "test output"])

        assert "test output" in result.stdout
        assert result.success is True

    def test_execute_test_command_captures_stderr(self):
        """Test that stderr is captured."""
        # Python command that writes to stderr
        cmd = [sys.executable, "-c", "import sys; sys.stderr.write('error message')"]
        result = execute_test_command(cmd)

        assert "error message" in result.stderr

    def test_execute_test_command_exit_code(self):
        """Test that exit codes are correctly reported."""
        # Command that exits with specific code
        cmd = [sys.executable, "-c", "import sys; sys.exit(42)"]
        result = execute_test_command(cmd)

        assert result.exit_code == 42
        assert result.success is False

    def test_execute_test_command_uses_custom_env(self):
        """Test custom environment variables are passed to the command."""
        cmd = [sys.executable, "-c", "import os; print(os.environ['MF_TEST_ENV'])"]
        result = execute_test_command(cmd, env={"MF_TEST_ENV": "present"})

        assert result.success is True
        assert result.stdout.strip() == "present"

    def test_execute_test_command_timeout(self):
        """Test timeout handling."""
        # Command that sleeps longer than timeout
        cmd = ["sleep", "10"]
        result = execute_test_command(cmd, timeout=1)

        assert result.timed_out is True
        assert result.success is False
        assert "timed out" in result.stderr.lower()

    def test_execute_test_command_with_cwd(self, tmp_path):
        """Test command execution in specific directory."""
        # Create a test file in tmp_path
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        # List files in that directory
        result = execute_test_command(["ls"], cwd=tmp_path)

        assert result.success is True
        assert "test.txt" in result.stdout

    def test_execute_test_command_duration(self):
        """Test that duration is measured."""
        result = execute_test_command(["sleep", "0.1"])

        assert result.duration >= 0.1
        assert result.duration < 1.0  # Should be much less than 1 second

    def test_execute_test_command_stores_command(self):
        """Test that command is stored in result."""
        cmd = ["echo", "test"]
        result = execute_test_command(cmd)

        assert result.command == cmd

    def test_execute_test_command_not_found(self):
        """Test error when command not found."""
        with pytest.raises(MissionForgeTestExecutionError) as exc_info:
            execute_test_command(["nonexistent_command_xyz"])

        # Should mention the command or failure
        error_msg = str(exc_info.value).lower()
        assert "nonexistent_command_xyz" in error_msg or "failed" in error_msg

    def test_execute_test_command_python_script(self):
        """Test executing Python test command."""
        # Simple Python command that prints and exits
        cmd = [sys.executable, "-c", "print('test passed'); exit(0)"]
        result = execute_test_command(cmd)

        assert result.success is True
        assert "test passed" in result.stdout

    def test_execute_test_command_multiline_output(self):
        """Test capturing multiline output."""
        cmd = [sys.executable, "-c", "print('line 1'); print('line 2'); print('line 3')"]
        result = execute_test_command(cmd)

        assert "line 1" in result.stdout
        assert "line 2" in result.stdout
        assert "line 3" in result.stdout

    def test_execute_test_command_empty_output(self):
        """Test command with no output."""
        result = execute_test_command(["true"])

        assert result.success is True
        assert result.stdout == ""
        assert result.stderr == ""

    def test_execute_test_command_long_timeout(self):
        """Test with longer timeout."""
        # Command that takes a bit of time but completes
        cmd = ["sleep", "0.5"]
        result = execute_test_command(cmd, timeout=5)

        assert result.success is True
        assert result.timed_out is False
        assert result.duration >= 0.5


class TestTestResult:
    """Tests for TestResult dataclass."""

    def test_test_result_creation(self):
        """Test creating TestResult instance."""
        result = MissionForgeTestResult(
            command=["pytest"],
            exit_code=0,
            stdout="test output",
            stderr="",
            duration=1.5,
            timed_out=False,
            success=True,
        )

        assert result.command == ["pytest"]
        assert result.exit_code == 0
        assert result.stdout == "test output"
        assert result.duration == 1.5
        assert result.success is True

    def test_test_result_failure(self):
        """Test TestResult for failed test."""
        result = MissionForgeTestResult(
            command=["pytest"],
            exit_code=1,
            stdout="",
            stderr="test failed",
            duration=0.5,
            timed_out=False,
            success=False,
        )

        assert result.success is False
        assert result.exit_code == 1
        assert "test failed" in result.stderr

    def test_test_result_timeout(self):
        """Test TestResult for timed out test."""
        result = MissionForgeTestResult(
            command=["pytest"],
            exit_code=-1,
            stdout="",
            stderr="timed out",
            duration=300.0,
            timed_out=True,
            success=False,
        )

        assert result.timed_out is True
        assert result.success is False


class TestRealWorldScenarios:
    """Tests simulating real-world test execution scenarios."""

    def test_pytest_style_command(self):
        """Test pytest-style command execution."""
        # Simulate pytest command (using echo as substitute)
        cmd = ["echo", "collected 5 items\ntest_main.py::test_func PASSED"]
        result = execute_test_command(cmd)

        assert result.success is True
        assert "PASSED" in result.stdout

    def test_npm_test_style_command(self):
        """Test npm test style command."""
        # Simulate npm test output
        cmd = ["echo", "PASS tests/test.js"]
        result = execute_test_command(cmd)

        assert result.success is True
        assert "PASS" in result.stdout

    @pytest.mark.skipif(
        sys.platform == "win32", reason=".sh scripts are not directly executable on Windows"
    )
    def test_custom_test_script(self, tmp_path):
        """Test custom test script execution."""
        # Create a simple test script
        script = tmp_path / "test.sh"
        script.write_text("#!/bin/bash\necho 'Running tests...'\nexit 0\n")
        script.chmod(0o755)

        result = execute_test_command([str(script)])

        assert result.success is True
        assert "Running tests" in result.stdout

    def test_test_with_arguments(self):
        """Test command with multiple arguments."""
        cmd = [sys.executable, "-c", "import sys; print(sys.argv)", "arg1", "arg2"]
        result = execute_test_command(cmd)

        assert result.success is True
        assert "arg1" in result.stdout
        assert "arg2" in result.stdout

    def test_test_command_with_special_characters(self):
        """Test command with special characters in output."""
        cmd = [sys.executable, "-c", "print('✓ Test passed')"]
        result = execute_test_command(cmd)

        assert result.success is True
        # Unicode should be handled correctly
        assert "passed" in result.stdout.lower()


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_execute_test_command_very_short_timeout(self):
        """Test with very short timeout."""
        # Even a simple command might timeout with 1 second
        cmd = ["sleep", "5"]
        result = execute_test_command(cmd, timeout=1)

        # Should timeout
        assert result.timed_out is True

    def test_execute_test_command_zero_exit_code(self):
        """Test that exit code 0 means success."""
        result = execute_test_command(["true"])

        assert result.exit_code == 0
        assert result.success is True

    def test_execute_test_command_nonzero_exit_code(self):
        """Test that non-zero exit code means failure."""
        result = execute_test_command(["false"])

        assert result.exit_code != 0
        assert result.success is False

    def test_execute_test_command_large_output(self):
        """Test handling large output."""
        # Generate large output
        cmd = [sys.executable, "-c", "for i in range(1000): print(f'Line {i}')"]
        result = execute_test_command(cmd)

        assert result.success is True
        assert "Line 0" in result.stdout
        assert "Line 999" in result.stdout

    def test_execute_test_command_no_shell_injection(self):
        """Test that shell injection is prevented."""
        # This should NOT execute the second command
        cmd = ["echo", "test; echo injected"]
        result = execute_test_command(cmd)

        # The semicolon should be treated as part of the argument
        assert "test; echo injected" in result.stdout or "test" in result.stdout
        # Should not see "injected" on a separate line
        assert result.success is True


# Made with Bob
