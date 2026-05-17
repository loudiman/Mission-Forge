"""Git operations module."""

from .operations import (
    GitStatus,
    get_changed_files,
    get_changed_files_detailed,
    get_commit_hash,
    get_current_branch,
    get_diff,
    get_diff_stats,
    get_repo_root,
    get_status,
    has_uncommitted_changes,
    is_git_repo,
    run_git_command,
)

__all__ = [
    "GitStatus",
    "get_changed_files",
    "get_changed_files_detailed",
    "get_commit_hash",
    "get_current_branch",
    "get_diff",
    "get_diff_stats",
    "get_repo_root",
    "get_status",
    "has_uncommitted_changes",
    "is_git_repo",
    "run_git_command",
]

# Made with Bob
