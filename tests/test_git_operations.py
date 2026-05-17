"""Tests for git operations module."""

import subprocess
from pathlib import Path

import pytest

from missionforge.core.exceptions import GitOperationError
from missionforge.git.operations import (
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
)


@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary git repository for testing."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=repo_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"], cwd=repo_path, check=True, capture_output=True
    )

    return repo_path


@pytest.fixture
def git_repo_with_commit(git_repo):
    """Create a git repository with an initial commit."""
    # Create and commit a file
    test_file = git_repo / "initial.txt"
    test_file.write_text("initial content")

    subprocess.run(["git", "add", "initial.txt"], cwd=git_repo, check=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"], cwd=git_repo, check=True, capture_output=True
    )

    return git_repo


class TestIsGitRepo:
    """Tests for is_git_repo function."""

    def test_is_git_repo_valid(self, git_repo):
        """Test that valid git repo is detected."""
        assert is_git_repo(git_repo) is True

    def test_is_git_repo_invalid(self, tmp_path):
        """Test that non-git directory returns False."""
        non_repo = tmp_path / "not_a_repo"
        non_repo.mkdir()
        assert is_git_repo(non_repo) is False

    def test_is_git_repo_from_subdirectory(self, git_repo):
        """Test detection from subdirectory."""
        subdir = git_repo / "subdir"
        subdir.mkdir()
        assert is_git_repo(subdir) is True


class TestGetRepoRoot:
    """Tests for get_repo_root function."""

    def test_get_repo_root_from_root(self, git_repo):
        """Test getting repo root from repository root."""
        root = get_repo_root(git_repo)
        assert root == git_repo

    def test_get_repo_root_from_subdirectory(self, git_repo):
        """Test getting repo root from subdirectory."""
        subdir = git_repo / "deep" / "nested" / "dir"
        subdir.mkdir(parents=True)

        root = get_repo_root(subdir)
        assert root == git_repo

    def test_get_repo_root_not_in_repo(self, tmp_path):
        """Test error when not in a git repository."""
        non_repo = tmp_path / "not_a_repo"
        non_repo.mkdir()

        with pytest.raises(GitOperationError):
            get_repo_root(non_repo)


class TestGetCurrentBranch:
    """Tests for get_current_branch function."""

    def test_get_current_branch(self, git_repo_with_commit):
        """Test getting current branch name."""
        branch = get_current_branch(git_repo_with_commit)
        # Default branch is usually 'main' or 'master'
        assert branch in ["main", "master"]

    def test_get_current_branch_after_checkout(self, git_repo_with_commit):
        """Test getting branch name after creating and checking out new branch."""
        subprocess.run(
            ["git", "checkout", "-b", "feature-branch"],
            cwd=git_repo_with_commit,
            check=True,
            capture_output=True,
        )

        branch = get_current_branch(git_repo_with_commit)
        assert branch == "feature-branch"


class TestGetStatus:
    """Tests for get_status function."""

    def test_get_status_empty_repo(self, git_repo):
        """Test status in empty repository."""
        status = get_status(git_repo)

        assert isinstance(status, GitStatus)
        assert len(status.staged) == 0
        assert len(status.unstaged) == 0
        assert len(status.untracked) == 0
        assert len(status.deleted) == 0
        assert len(status.renamed) == 0

    def test_get_status_with_staged_files(self, git_repo):
        """Test status with staged files."""
        # Create and stage a file
        test_file = git_repo / "staged.txt"
        test_file.write_text("staged content")
        subprocess.run(["git", "add", "staged.txt"], cwd=git_repo, check=True)

        status = get_status(git_repo)

        assert len(status.staged) == 1
        assert status.staged[0].name == "staged.txt"
        assert len(status.unstaged) == 0
        assert len(status.untracked) == 0

    def test_get_status_with_untracked_files(self, git_repo):
        """Test status with untracked files."""
        # Create untracked file
        test_file = git_repo / "untracked.txt"
        test_file.write_text("untracked content")

        status = get_status(git_repo)

        assert len(status.untracked) == 1
        assert status.untracked[0].name == "untracked.txt"
        assert len(status.staged) == 0
        assert len(status.unstaged) == 0

    def test_get_status_mixed_changes(self, git_repo_with_commit):
        """Test status with multiple types of changes."""
        # Staged file
        staged_file = git_repo_with_commit / "staged.txt"
        staged_file.write_text("staged")
        subprocess.run(["git", "add", "staged.txt"], cwd=git_repo_with_commit, check=True)

        # Untracked file
        untracked_file = git_repo_with_commit / "untracked.txt"
        untracked_file.write_text("untracked")

        status = get_status(git_repo_with_commit)

        # Should have staged files (at least staged.txt)
        assert len(status.staged) >= 1
        assert any("staged" in str(f) for f in status.staged)

        # Should have untracked files
        assert len(status.untracked) >= 1
        assert any("untracked" in str(f) for f in status.untracked)

    def test_get_status_with_rename_and_unstaged_modification(self, git_repo_with_commit):
        """Test renamed files can also be reported as unstaged modifications."""
        subprocess.run(
            ["git", "mv", "initial.txt", "renamed.txt"],
            cwd=git_repo_with_commit,
            check=True,
        )
        (git_repo_with_commit / "renamed.txt").write_text("renamed and modified")

        status = get_status(git_repo_with_commit)

        assert status.renamed == {Path("initial.txt"): Path("renamed.txt")}
        assert Path("renamed.txt") in status.staged
        assert Path("renamed.txt") in status.unstaged

    def test_get_status_with_staged_delete(self, git_repo_with_commit):
        """Test staged deleted files are categorized once."""
        (git_repo_with_commit / "initial.txt").unlink()
        subprocess.run(["git", "add", "initial.txt"], cwd=git_repo_with_commit, check=True)

        status = get_status(git_repo_with_commit)

        assert status.deleted == [Path("initial.txt")]
        assert status.staged == [Path("initial.txt")]
        assert status.unstaged == []


class TestGetChangedFiles:
    """Tests for get_changed_files function."""

    def test_get_changed_files_no_changes(self, git_repo_with_commit):
        """Test with no changes since HEAD."""
        files = get_changed_files(cwd=git_repo_with_commit)
        assert len(files) == 0

    def test_get_changed_files_with_changes(self, git_repo_with_commit):
        """Test with uncommitted changes."""
        # Modify file
        test_file = git_repo_with_commit / "initial.txt"
        test_file.write_text("modified content")

        files = get_changed_files(cwd=git_repo_with_commit)

        assert len(files) == 1
        assert files[0].name == "initial.txt"

    def test_get_changed_files_new_file(self, git_repo_with_commit):
        """Test with new file."""
        # Create and stage new file
        new_file = git_repo_with_commit / "new.txt"
        new_file.write_text("new content")
        subprocess.run(["git", "add", "new.txt"], cwd=git_repo_with_commit, check=True)

        files = get_changed_files(cwd=git_repo_with_commit)

        assert len(files) == 1
        assert files[0].name == "new.txt"


class TestGetChangedFilesDetailed:
    """Tests for get_changed_files_detailed function."""

    def test_get_changed_files_detailed_no_changes(self, git_repo_with_commit):
        """Test with no changes."""
        changes = get_changed_files_detailed(cwd=git_repo_with_commit)

        assert changes["added"] == []
        assert changes["modified"] == []
        assert changes["deleted"] == []
        assert changes["renamed"] == []

    def test_get_changed_files_detailed_with_modifications(self, git_repo_with_commit):
        """Test with modified files."""
        # Modify and stage file
        test_file = git_repo_with_commit / "initial.txt"
        test_file.write_text("modified content")
        subprocess.run(["git", "add", "initial.txt"], cwd=git_repo_with_commit, check=True)

        changes = get_changed_files_detailed(cwd=git_repo_with_commit)

        assert len(changes["modified"]) == 1
        assert changes["modified"][0].name == "initial.txt"

    def test_get_changed_files_detailed_with_additions(self, git_repo_with_commit):
        """Test with added files."""
        # Create and stage new file
        new_file = git_repo_with_commit / "new.txt"
        new_file.write_text("new content")
        subprocess.run(["git", "add", "new.txt"], cwd=git_repo_with_commit, check=True)

        changes = get_changed_files_detailed(cwd=git_repo_with_commit)

        assert len(changes["added"]) == 1
        assert changes["added"][0].name == "new.txt"


class TestGetDiff:
    """Tests for get_diff function."""

    def test_get_diff_no_changes(self, git_repo_with_commit):
        """Test diff with no changes."""
        diff = get_diff(cwd=git_repo_with_commit)
        assert diff == ""

    def test_get_diff_with_changes(self, git_repo_with_commit):
        """Test diff with changes."""
        # Modify file
        test_file = git_repo_with_commit / "initial.txt"
        test_file.write_text("modified content")

        diff = get_diff(cwd=git_repo_with_commit)

        assert "initial.txt" in diff
        assert "modified content" in diff

    def test_get_diff_specific_file(self, git_repo_with_commit):
        """Test diff for specific file."""
        # Modify file
        test_file = git_repo_with_commit / "initial.txt"
        test_file.write_text("modified content")

        diff = get_diff(file_path=Path("initial.txt"), cwd=git_repo_with_commit)

        assert "initial.txt" in diff

    def test_get_diff_file_path_starting_with_dash(self, git_repo_with_commit):
        """Test diff treats dash-prefixed paths as paths, not options."""
        weird_file = git_repo_with_commit / "-weird.txt"
        weird_file.write_text("original\n")
        subprocess.run(["git", "add", "--", "-weird.txt"], cwd=git_repo_with_commit, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Add weird file"],
            cwd=git_repo_with_commit,
            check=True,
            capture_output=True,
        )
        weird_file.write_text("modified\n")

        diff = get_diff(file_path=Path("-weird.txt"), cwd=git_repo_with_commit)

        assert "-weird.txt" in diff
        assert "modified" in diff


class TestGetDiffStats:
    """Tests for get_diff_stats function."""

    def test_get_diff_stats_no_changes(self, git_repo_with_commit):
        """Test stats with no changes."""
        stats = get_diff_stats(cwd=git_repo_with_commit)

        assert stats["files_changed"] == 0
        assert stats["insertions"] == 0
        assert stats["deletions"] == 0

    def test_get_diff_stats_with_changes(self, git_repo_with_commit):
        """Test stats with changes."""
        # Modify file
        test_file = git_repo_with_commit / "initial.txt"
        test_file.write_text("line 1\nline 2\nline 3\n")

        stats = get_diff_stats(cwd=git_repo_with_commit)

        assert stats["files_changed"] >= 1
        assert stats["insertions"] >= 0
        assert stats["deletions"] >= 0


class TestHasUncommittedChanges:
    """Tests for has_uncommitted_changes function."""

    def test_has_uncommitted_changes_false(self, git_repo_with_commit):
        """Test with no uncommitted changes."""
        assert has_uncommitted_changes(git_repo_with_commit) is False

    def test_has_uncommitted_changes_true(self, git_repo_with_commit):
        """Test with uncommitted changes."""
        # Modify file
        test_file = git_repo_with_commit / "initial.txt"
        test_file.write_text("modified content")

        assert has_uncommitted_changes(git_repo_with_commit) is True

    def test_has_uncommitted_changes_with_untracked(self, git_repo_with_commit):
        """Test with untracked files."""
        # Create untracked file
        new_file = git_repo_with_commit / "untracked.txt"
        new_file.write_text("untracked")

        assert has_uncommitted_changes(git_repo_with_commit) is True


class TestGetCommitHash:
    """Tests for get_commit_hash function."""

    def test_get_commit_hash_head(self, git_repo_with_commit):
        """Test getting HEAD commit hash."""
        commit_hash = get_commit_hash(cwd=git_repo_with_commit)

        # Git commit hashes are 40 characters (SHA-1)
        assert len(commit_hash) == 40
        assert all(c in "0123456789abcdef" for c in commit_hash)

    def test_get_commit_hash_specific_ref(self, git_repo_with_commit):
        """Test getting commit hash for specific reference."""
        # Get hash for HEAD
        head_hash = get_commit_hash("HEAD", cwd=git_repo_with_commit)

        # Get hash for branch
        branch = get_current_branch(git_repo_with_commit)
        branch_hash = get_commit_hash(branch, cwd=git_repo_with_commit)

        # Should be the same
        assert head_hash == branch_hash


# Made with Bob
