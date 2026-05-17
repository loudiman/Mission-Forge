"""Shared pytest fixtures and configuration."""

import subprocess

import pytest


@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary git repository for testing.

    This fixture creates a clean git repository with basic configuration.
    """
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
    """Create a git repository with an initial commit.

    This fixture extends git_repo by adding an initial commit.
    """
    # Create and commit a file
    test_file = git_repo / "initial.txt"
    test_file.write_text("initial content")

    subprocess.run(["git", "add", "initial.txt"], cwd=git_repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"], cwd=git_repo, check=True, capture_output=True
    )

    return git_repo


# Made with Bob
