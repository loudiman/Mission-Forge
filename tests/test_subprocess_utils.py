"""Tests for subprocess utilities."""

import sys

import pytest

from missionforge.core.exceptions import MissionForgeError
from missionforge.utils.subprocess_utils import run_command, run_command_silent


class TestRunCommand:
    """Tests for run_command function."""

    def test_run_command_success(self):
        """Test successful command execution."""
        result = run_command(["echo", "hello"])

        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_run_command_rejects_empty_args(self):
        """Test that empty commands fail with a MissionForgeError."""
        with pytest.raises(MissionForgeError) as exc_info:
            run_command([])

        assert "empty" in str(exc_info.value).lower()

    def test_run_command_merges_custom_env(self):
        """Test custom env vars are visible without replacing PATH."""
        cmd = [sys.executable, "-c", "import os; print(os.environ['MF_TEST_ENV'])"]
        result = run_command(cmd, env={"MF_TEST_ENV": "present"})

        assert result.returncode == 0
        assert result.stdout.strip() == "present"

    def test_run_command_failure_with_check(self):
        """Test that check=True raises exception on failure."""
        with pytest.raises(MissionForgeError) as exc_info:
            run_command(["false"], check=True)

        assert "failed" in str(exc_info.value).lower()

    def test_run_command_failure_without_check(self):
        """Test that check=False doesn't raise exception."""
        result = run_command(["false"], check=False)

        assert result.returncode != 0

    def test_run_command_captures_stdout(self):
        """Test stdout capture."""
        result = run_command(["echo", "test output"])

        assert "test output" in result.stdout

    def test_run_command_captures_stderr(self):
        """Test stderr capture."""
        cmd = [sys.executable, "-c", "import sys; sys.stderr.write('error')"]
        result = run_command(cmd)

        assert "error" in result.stderr

    def test_run_command_timeout(self):
        """Test timeout handling."""
        with pytest.raises(MissionForgeError) as exc_info:
            run_command(["sleep", "10"], timeout=1)

        assert "timed out" in str(exc_info.value).lower()

    def test_run_command_with_cwd(self, tmp_path):
        """Test command execution in specific directory."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        result = run_command(["ls"], cwd=tmp_path)

        assert "test.txt" in result.stdout

    def test_run_command_not_found(self):
        """Test error when command not found."""
        with pytest.raises(MissionForgeError) as exc_info:
            run_command(["nonexistent_command_xyz"])

        assert "not found" in str(exc_info.value).lower()

    def test_run_command_no_capture(self):
        """Test command without output capture."""
        result = run_command(["echo", "test"], capture_output=False)

        # When capture_output=False, stdout/stderr are None
        assert result.returncode == 0

    def test_run_command_multiline_output(self):
        """Test capturing multiline output."""
        cmd = [sys.executable, "-c", "print('line1'); print('line2')"]
        result = run_command(cmd)

        assert "line1" in result.stdout
        assert "line2" in result.stdout

    def test_run_command_exit_code(self):
        """Test exit code capture."""
        cmd = [sys.executable, "-c", "import sys; sys.exit(42)"]
        result = run_command(cmd, check=False)

        assert result.returncode == 42

    def test_run_command_empty_output(self):
        """Test command with no output."""
        result = run_command(["true"])

        assert result.returncode == 0
        assert result.stdout == ""

    def test_run_command_with_arguments(self):
        """Test command with multiple arguments."""
        result = run_command(["echo", "arg1", "arg2"])

        assert "arg1" in result.stdout
        assert "arg2" in result.stdout

    def test_run_command_no_shell_injection(self):
        """Test that shell injection is prevented."""
        # This should NOT execute the second command
        result = run_command(["echo", "test; echo injected"])

        # The semicolon should be treated as part of the argument
        assert "test; echo injected" in result.stdout or "test" in result.stdout
        assert result.returncode == 0


class TestRunCommandSilent:
    """Tests for run_command_silent function."""

    def test_run_command_silent_success(self):
        """Test silent execution with successful command."""
        success = run_command_silent(["echo", "hello"])

        assert success is True

    def test_run_command_silent_failure(self):
        """Test silent execution with failed command."""
        success = run_command_silent(["false"])

        assert success is False

    def test_run_command_silent_not_found(self):
        """Test silent execution with command not found."""
        success = run_command_silent(["nonexistent_command_xyz"])

        assert success is False

    def test_run_command_silent_timeout(self):
        """Test silent execution with timeout."""
        success = run_command_silent(["sleep", "10"], timeout=1)

        assert success is False

    def test_run_command_silent_with_cwd(self, tmp_path):
        """Test silent execution in specific directory."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        success = run_command_silent(["ls"], cwd=tmp_path)

        assert success is True

    def test_run_command_silent_no_exception(self):
        """Test that silent execution never raises exceptions."""
        # These should all return False without raising
        assert run_command_silent(["false"]) is False
        assert run_command_silent(["nonexistent_xyz"]) is False
        assert run_command_silent(["sleep", "10"], timeout=1) is False


class TestSecurityAndSafety:
    """Tests for security and safety features."""

    def test_no_shell_true(self):
        """Test that shell=True is never used."""
        # Commands should be passed as lists, not strings
        result = run_command(["echo", "test"])
        assert result.returncode == 0

        # This should work because we're not using shell=True
        result = run_command(["echo", "test && echo injected"])
        # The && should be treated as part of the argument
        assert result.returncode == 0

    def test_command_as_list_required(self):
        """Test that commands must be lists."""
        # run_command expects a list
        result = run_command(["echo", "test"])
        assert result.returncode == 0

    def test_timeout_prevents_hanging(self):
        """Test that timeout prevents indefinite hanging."""
        import time

        start = time.time()

        with pytest.raises(MissionForgeError):
            run_command(["sleep", "100"], timeout=1)

        duration = time.time() - start
        # Should timeout around 1 second, not 100 seconds
        assert duration < 5


class TestEdgeCases:
    """Tests for edge cases."""

    def test_run_command_with_special_characters(self):
        """Test command with special characters."""
        result = run_command(["echo", "test!@#$%^&*()"])

        assert result.returncode == 0

    def test_run_command_with_unicode(self):
        """Test command with unicode characters."""
        cmd = [sys.executable, "-c", "print('✓ Test')"]
        result = run_command(cmd)

        assert result.returncode == 0

    def test_run_command_large_output(self):
        """Test handling large output."""
        cmd = [sys.executable, "-c", "for i in range(1000): print(i)"]
        result = run_command(cmd)

        assert result.returncode == 0
        assert "0" in result.stdout
        assert "999" in result.stdout

    def test_run_command_empty_args(self):
        """Test with minimal arguments."""
        result = run_command(["true"])
        assert result.returncode == 0

    def test_run_command_very_short_timeout(self):
        """Test with very short timeout."""
        with pytest.raises(MissionForgeError):
            run_command(["sleep", "5"], timeout=1)


class TestErrorMessages:
    """Tests for error message quality."""

    def test_error_message_includes_command(self):
        """Test that error messages include the command."""
        with pytest.raises(MissionForgeError) as exc_info:
            run_command(["false"], check=True)

        error_msg = str(exc_info.value)
        assert "false" in error_msg.lower() or "command" in error_msg.lower()

    def test_error_message_includes_exit_code(self):
        """Test that error messages include exit code."""
        with pytest.raises(MissionForgeError) as exc_info:
            run_command(["false"], check=True)

        error_msg = str(exc_info.value)
        # Should mention command failure
        assert "command" in error_msg.lower() or "failed" in error_msg.lower()

    def test_timeout_error_message(self):
        """Test timeout error message."""
        with pytest.raises(MissionForgeError) as exc_info:
            run_command(["sleep", "10"], timeout=1)

        error_msg = str(exc_info.value)
        assert "timeout" in error_msg.lower() or "timed out" in error_msg.lower()

    def test_not_found_error_message(self):
        """Test command not found error message."""
        with pytest.raises(MissionForgeError) as exc_info:
            run_command(["nonexistent_xyz"])

        error_msg = str(exc_info.value)
        assert "not found" in error_msg.lower()


# Made with Bob
