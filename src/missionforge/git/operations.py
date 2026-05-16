"""Git operations using safe subprocess calls (no GitPython)."""

from pathlib import Path
from typing import Optional

from ..core.exceptions import GitOperationError
from ..utils.subprocess_utils import run_command


def run_git_command(
    args: list[str], cwd: Optional[Path] = None, check: bool = True
) -> str:
    """Run git command safely via subprocess.

    Args:
        args: Git command arguments (without 'git' prefix).
        cwd: Working directory for git command.
        check: Whether to raise exception on non-zero exit code.

    Returns:
        Command stdout as string.

    Raises:
        GitOperationError: If git command fails.
    """
    cmd = ["git"] + args

    try:
        result = run_command(cmd, cwd=cwd, check=check, timeout=30)
        return result.stdout.strip()
    except Exception as e:
        raise GitOperationError(
            f"Git command failed: {' '.join(cmd)}", f"Error: {str(e)}"
        )


def get_changed_files(base_ref: str = "HEAD", cwd: Optional[Path] = None) -> list[Path]:
    """Get list of changed files since base_ref.

    Args:
        base_ref: Git reference to compare against (default: HEAD).
        cwd: Working directory.

    Returns:
        List of changed file paths.
    """
    output = run_git_command(["diff", "--name-only", base_ref], cwd=cwd)

    if not output:
        return []

    files = [Path(line) for line in output.split("\n") if line]
    return files


def get_repo_root(cwd: Optional[Path] = None) -> Path:
    """Get git repository root directory.

    Args:
        cwd: Working directory.

    Returns:
        Path to repository root.

    Raises:
        GitOperationError: If not in a git repository.
    """
    output = run_git_command(["rev-parse", "--show-toplevel"], cwd=cwd)
    return Path(output)


def is_git_repo(cwd: Optional[Path] = None) -> bool:
    """Check if directory is a git repository.

    Args:
        cwd: Working directory to check.

    Returns:
        True if directory is in a git repository.
    """
    try:
        run_git_command(["rev-parse", "--git-dir"], cwd=cwd, check=True)
        return True
    except GitOperationError:
        return False


def get_current_branch(cwd: Optional[Path] = None) -> str:
    """Get current git branch name.

    Args:
        cwd: Working directory.

    Returns:
        Current branch name.
    """
    output = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
    return output


def get_diff(
    base_ref: str = "HEAD",
    file_path: Optional[Path] = None,
    context_lines: int = 3,
    cwd: Optional[Path] = None,
) -> str:
    """Get git diff output.

    Args:
        base_ref: Git reference to compare against.
        file_path: Specific file to diff (None for all files).
        context_lines: Number of context lines in diff.
        cwd: Working directory.

    Returns:
        Diff output as string.
    """
    args = ["diff", f"-U{context_lines}", base_ref]
    if file_path:
        args.append(str(file_path))

    return run_git_command(args, cwd=cwd)


def has_uncommitted_changes(cwd: Optional[Path] = None) -> bool:
    """Check if repository has uncommitted changes.

    Args:
        cwd: Working directory.

    Returns:
        True if there are uncommitted changes.
    """
    try:
        output = run_git_command(["status", "--porcelain"], cwd=cwd)
        return bool(output)
    except GitOperationError:
        return False


def get_commit_hash(ref: str = "HEAD", cwd: Optional[Path] = None) -> str:
    """Get commit hash for a reference.

    Args:
        ref: Git reference (default: HEAD).
        cwd: Working directory.

    Returns:
        Full commit hash.
    """
    return run_git_command(["rev-parse", ref], cwd=cwd)

# Made with Bob
