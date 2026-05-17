"""Git operations using safe subprocess calls (no GitPython)."""

from dataclasses import dataclass
from pathlib import Path

from ..core.exceptions import GitOperationError
from ..utils.subprocess_utils import run_command


@dataclass
class GitStatus:
    """Structured git status information.

    Attributes:
        staged: Files in staging area (index).
        unstaged: Modified files not yet staged.
        untracked: Files not tracked by git.
        deleted: Deleted files.
        renamed: Renamed files (old_path -> new_path).
    """

    staged: list[Path]
    unstaged: list[Path]
    untracked: list[Path]
    deleted: list[Path]
    renamed: dict[Path, Path]


def _append_unique(paths: list[Path], path: Path) -> None:
    """Append path if it is not already present."""
    if path not in paths:
        paths.append(path)


def run_git_command(args: list[str], cwd: Path | None = None, check: bool = True) -> str:
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
        raise GitOperationError(f"Git command failed: {' '.join(cmd)}", f"Error: {str(e)}") from e


def get_changed_files(base_ref: str = "HEAD", cwd: Path | None = None) -> list[Path]:
    """Get list of diff-tracked changed files since base_ref.

    Untracked files are not included. Use get_status() for validation workflows
    that need staged, unstaged, and untracked files.

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


def get_repo_root(cwd: Path | None = None) -> Path:
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


def is_git_repo(cwd: Path | None = None) -> bool:
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


def get_current_branch(cwd: Path | None = None) -> str:
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
    file_path: Path | None = None,
    context_lines: int = 3,
    cwd: Path | None = None,
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
        args.append("--")
        args.append(str(file_path))

    return run_git_command(args, cwd=cwd)


def has_uncommitted_changes(cwd: Path | None = None) -> bool:
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


def get_commit_hash(ref: str = "HEAD", cwd: Path | None = None) -> str:
    """Get commit hash for a reference.

    Args:
        ref: Git reference (default: HEAD).
        cwd: Working directory.

    Returns:
        Full commit hash.
    """
    return run_git_command(["rev-parse", ref], cwd=cwd)


def get_status(cwd: Path | None = None) -> GitStatus:
    """Get detailed git status with file categorization.

    Uses git status --porcelain=v1 for reliable machine-readable parsing.

    Args:
        cwd: Working directory.

    Returns:
        GitStatus with categorized file lists.

    Examples:
        >>> status = get_status()
        >>> print(f"Staged: {len(status.staged)}")
        >>> print(f"Unstaged: {len(status.unstaged)}")
        >>> print(f"Untracked: {len(status.untracked)}")
    """
    output = run_git_command(["status", "--porcelain"], cwd=cwd)

    staged: list[Path] = []
    unstaged: list[Path] = []
    untracked: list[Path] = []
    deleted: list[Path] = []
    renamed: dict[Path, Path] = {}

    if not output:
        return GitStatus(
            staged=staged, unstaged=unstaged, untracked=untracked, deleted=deleted, renamed=renamed
        )

    for line in output.split("\n"):
        if not line:
            continue

        # Porcelain format: XY filename
        # X = index status (staged), Y = working tree status (unstaged)
        # There's always a space at position 2, filename starts at position 3
        if len(line) < 4:
            continue

        index_status = line[0]
        worktree_status = line[1]
        # Skip the space at position 2, filename starts at 3
        filepath = line[3:]

        # Handle renamed/copied files (format: "R  old -> new" or "RM old -> new")
        if index_status in "RC":
            if " -> " in filepath:
                old_path, new_path = filepath.split(" -> ", 1)
                current_path = Path(new_path.strip())
                renamed[Path(old_path.strip())] = current_path
                _append_unique(staged, current_path)
                if worktree_status == "D":
                    _append_unique(deleted, current_path)
                    _append_unique(unstaged, current_path)
                elif worktree_status in "MARC":
                    _append_unique(unstaged, current_path)
            continue

        # Untracked files
        if index_status == "?" and worktree_status == "?":
            untracked.append(Path(filepath))
            continue

        # Deleted files (check both index and worktree)
        if index_status == "D":
            _append_unique(deleted, Path(filepath))
            _append_unique(staged, Path(filepath))
        if worktree_status == "D":
            _append_unique(deleted, Path(filepath))
            _append_unique(unstaged, Path(filepath))

        # Staged files (index has changes)
        if index_status in "MARC" and index_status != " ":
            _append_unique(staged, Path(filepath))

        # Unstaged files (working tree has changes)
        if worktree_status in "MARC" and worktree_status != " ":
            _append_unique(unstaged, Path(filepath))

    return GitStatus(
        staged=staged, unstaged=unstaged, untracked=untracked, deleted=deleted, renamed=renamed
    )


def get_changed_files_detailed(
    base_ref: str = "HEAD", cwd: Path | None = None
) -> dict[str, list[Path]]:
    """Get diff-tracked changed files categorized by change type.

    Untracked files are not included. Use get_status() when validation needs
    staged, unstaged, and untracked files.

    Args:
        base_ref: Git reference to compare against (default: HEAD).
        cwd: Working directory.

    Returns:
        Dictionary with keys: 'added', 'modified', 'deleted', 'renamed'.

    Examples:
        >>> changes = get_changed_files_detailed()
        >>> print(f"Added: {len(changes['added'])}")
        >>> print(f"Modified: {len(changes['modified'])}")
    """
    output = run_git_command(["diff", "--name-status", base_ref], cwd=cwd)

    added: list[Path] = []
    modified: list[Path] = []
    deleted: list[Path] = []
    renamed: list[Path] = []

    if not output:
        return {"added": added, "modified": modified, "deleted": deleted, "renamed": renamed}

    for line in output.split("\n"):
        if not line:
            continue

        parts = line.split("\t", 1)
        if len(parts) < 2:
            continue

        status = parts[0][0]  # First character is the status
        filepath = parts[1]

        if status == "A":
            added.append(Path(filepath))
        elif status == "M":
            modified.append(Path(filepath))
        elif status == "D":
            deleted.append(Path(filepath))
        elif status == "R":
            # Renamed files have format: "R\told_name\tnew_name"
            if "\t" in filepath:
                renamed.append(Path(filepath.split("\t")[1]))
            else:
                renamed.append(Path(filepath))

    return {"added": added, "modified": modified, "deleted": deleted, "renamed": renamed}


def get_diff_stats(base_ref: str = "HEAD", cwd: Path | None = None) -> dict[str, int]:
    """Get diff statistics.

    Args:
        base_ref: Git reference to compare against (default: HEAD).
        cwd: Working directory.

    Returns:
        Dictionary with keys: 'files_changed', 'insertions', 'deletions'.

    Examples:
        >>> stats = get_diff_stats()
        >>> print(f"Files changed: {stats['files_changed']}")
        >>> print(f"+{stats['insertions']} -{stats['deletions']}")
    """
    output = run_git_command(["diff", "--shortstat", base_ref], cwd=cwd)

    files_changed = 0
    insertions = 0
    deletions = 0

    if output:
        # Parse format: "X files changed, Y insertions(+), Z deletions(-)"
        parts = output.split(",")

        for part in parts:
            part = part.strip()
            if "file" in part:
                files_changed = int(part.split()[0])
            elif "insertion" in part:
                insertions = int(part.split()[0])
            elif "deletion" in part:
                deletions = int(part.split()[0])

    return {"files_changed": files_changed, "insertions": insertions, "deletions": deletions}


# Made with Bob
