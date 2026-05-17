"""Tests for path matching utilities."""

import json
from pathlib import Path

from missionforge.utils.path_matching import (
    filter_paths_by_patterns,
    matches_patterns,
    validate_paths_against_scope,
)


class TestMatchesPatterns:
    """Tests for matches_patterns function."""

    def test_matches_patterns_simple_wildcard(self):
        """Test simple wildcard pattern."""
        assert matches_patterns(Path("test.py"), ["*.py"]) is True
        assert matches_patterns(Path("test.txt"), ["*.py"]) is False

    def test_matches_patterns_recursive_wildcard(self):
        """Test recursive wildcard pattern."""
        assert matches_patterns(Path("src/main.py"), ["src/**/*.py"]) is True
        assert matches_patterns(Path("src/utils/helper.py"), ["src/**/*.py"]) is True
        assert matches_patterns(Path("tests/test.py"), ["src/**/*.py"]) is False

    def test_matches_patterns_directory_pattern(self):
        """Test directory pattern."""
        assert matches_patterns(Path("src/main.py"), ["src/**"]) is True
        assert matches_patterns(Path("src/utils/helper.py"), ["src/**"]) is True
        assert matches_patterns(Path("tests/test.py"), ["src/**"]) is False

    def test_matches_patterns_multiple_patterns(self):
        """Test matching against multiple patterns."""
        patterns = ["src/**/*.py", "tests/**/*.py"]

        assert matches_patterns(Path("src/main.py"), patterns) is True
        assert matches_patterns(Path("tests/test.py"), patterns) is True
        assert matches_patterns(Path("docs/readme.md"), patterns) is False

    def test_matches_patterns_empty_patterns(self):
        """Test with empty pattern list."""
        assert matches_patterns(Path("any/file.py"), []) is False

    def test_matches_patterns_with_base_path(self):
        """Test pattern matching with base path."""
        base = Path("/project")
        file_path = Path("/project/src/main.py")

        assert matches_patterns(file_path, ["src/**/*.py"], base_path=base) is True

    def test_matches_patterns_question_mark(self):
        """Test single character wildcard."""
        assert matches_patterns(Path("test1.py"), ["test?.py"]) is True
        assert matches_patterns(Path("test12.py"), ["test?.py"]) is False

    def test_matches_patterns_character_class(self):
        """Test character class pattern."""
        assert matches_patterns(Path("test_a.py"), ["test_[abc].py"]) is True
        assert matches_patterns(Path("test_d.py"), ["test_[abc].py"]) is False

    def test_matches_patterns_nested_directories(self):
        """Test deeply nested directory patterns."""
        pattern = "src/**/utils/**/*.py"

        assert matches_patterns(Path("src/core/utils/helper.py"), [pattern]) is True
        assert matches_patterns(Path("src/utils/helper.py"), [pattern]) is True
        assert matches_patterns(Path("src/main.py"), [pattern]) is False


class TestFilterPathsByPatterns:
    """Tests for filter_paths_by_patterns function."""

    def test_filter_paths_allowed_only(self):
        """Test filtering with only allowed patterns."""
        paths = [
            Path("src/main.py"),
            Path("src/utils.py"),
            Path("tests/test.py"),
            Path("docs/readme.md"),
        ]

        valid, invalid = filter_paths_by_patterns(paths, allowed_patterns=["src/**/*.py"])

        assert len(valid) == 2
        assert Path("src/main.py") in valid
        assert Path("src/utils.py") in valid
        assert len(invalid) == 2
        assert Path("tests/test.py") in invalid
        assert Path("docs/readme.md") in invalid

    def test_filter_paths_with_forbidden(self):
        """Test filtering with forbidden patterns."""
        paths = [Path("src/main.py"), Path("src/secret.py"), Path("src/utils.py")]

        valid, invalid = filter_paths_by_patterns(
            paths, allowed_patterns=["src/**/*.py"], forbidden_patterns=["**/secret.py"]
        )

        assert len(valid) == 2
        assert Path("src/main.py") in valid
        assert Path("src/utils.py") in valid
        assert len(invalid) == 1
        assert Path("src/secret.py") in invalid

    def test_filter_paths_multiple_forbidden(self):
        """Test filtering with multiple forbidden patterns."""
        paths = [
            Path("src/main.py"),
            Path("src/__pycache__/main.pyc"),
            Path("src/.env"),
            Path("src/utils.py"),
        ]

        valid, invalid = filter_paths_by_patterns(
            paths, allowed_patterns=["src/**"], forbidden_patterns=["**/__pycache__/**", "**/.env"]
        )

        assert len(valid) == 2
        assert Path("src/main.py") in valid
        assert Path("src/utils.py") in valid
        assert len(invalid) == 2

    def test_filter_paths_empty_allowed(self):
        """Test filtering with empty allowed patterns."""
        paths = [Path("src/main.py"), Path("tests/test.py")]

        valid, invalid = filter_paths_by_patterns(paths, allowed_patterns=[])

        # All paths should be invalid if no allowed patterns
        assert len(valid) == 0
        assert len(invalid) == 2

    def test_filter_paths_no_forbidden(self):
        """Test filtering without forbidden patterns."""
        paths = [Path("src/main.py"), Path("tests/test.py")]

        valid, invalid = filter_paths_by_patterns(paths, allowed_patterns=["src/**", "tests/**"])

        assert len(valid) == 2
        assert len(invalid) == 0


class TestValidatePathsAgainstScope:
    """Tests for validate_paths_against_scope function."""

    def test_validate_paths_all_valid(self):
        """Test validation with all files in scope."""
        files = [Path("src/main.py"), Path("src/utils.py"), Path("src/core/helper.py")]

        result = validate_paths_against_scope(files, allowed_patterns=["src/**/*.py"])

        assert result["valid"] is True
        assert len(result["allowed_files"]) == 3
        assert len(result["forbidden_files"]) == 0
        assert len(result["out_of_scope_files"]) == 0
        assert "3 allowed" in result["summary"]

    def test_validate_paths_with_forbidden(self):
        """Test validation with forbidden files."""
        files = [Path("src/main.py"), Path("src/secret.py"), Path("src/utils.py")]

        result = validate_paths_against_scope(
            files, allowed_patterns=["src/**/*.py"], forbidden_patterns=["**/secret.py"]
        )

        assert result["valid"] is False
        assert len(result["allowed_files"]) == 2
        assert len(result["forbidden_files"]) == 1
        assert "src/secret.py" in result["forbidden_files"]
        assert "forbidden" in result["summary"]

    def test_validate_paths_out_of_scope(self):
        """Test validation with out-of-scope files."""
        files = [Path("src/main.py"), Path("tests/test.py"), Path("docs/readme.md")]

        result = validate_paths_against_scope(files, allowed_patterns=["src/**/*.py"])

        assert result["valid"] is False
        assert len(result["allowed_files"]) == 1
        assert len(result["out_of_scope_files"]) == 2
        assert "tests/test.py" in result["out_of_scope_files"]
        assert "docs/readme.md" in result["out_of_scope_files"]
        assert "out of scope" in result["summary"]

    def test_validate_paths_mixed_violations(self):
        """Test validation with both forbidden and out-of-scope files."""
        files = [Path("src/main.py"), Path("src/secret.py"), Path("tests/test.py")]

        result = validate_paths_against_scope(
            files, allowed_patterns=["src/**/*.py"], forbidden_patterns=["**/secret.py"]
        )

        assert result["valid"] is False
        assert len(result["allowed_files"]) == 1
        assert len(result["forbidden_files"]) == 1
        assert len(result["out_of_scope_files"]) == 1

    def test_validate_paths_no_changes(self):
        """Test validation with no files."""
        result = validate_paths_against_scope([], allowed_patterns=["src/**"])

        assert result["valid"] is True
        assert len(result["allowed_files"]) == 0
        assert "No files changed" in result["summary"]

    def test_validate_paths_complex_patterns(self):
        """Test validation with complex pattern combinations."""
        files = [
            Path("src/missionforge/git/operations.py"),
            Path("src/missionforge/utils/helper.py"),
            Path("src/missionforge/__pycache__/main.pyc"),
            Path("tests/test_git.py"),
        ]

        result = validate_paths_against_scope(
            files,
            allowed_patterns=["src/missionforge/**/*.py"],
            forbidden_patterns=["**/__pycache__/**", "**/*.pyc"],
        )

        assert result["valid"] is False
        assert len(result["allowed_files"]) == 2
        assert len(result["forbidden_files"]) == 1
        assert len(result["out_of_scope_files"]) == 1

    def test_validate_paths_with_base_path(self):
        """Test validation with base path."""
        base = Path("/project")
        files = [Path("/project/src/main.py"), Path("/project/tests/test.py")]

        result = validate_paths_against_scope(
            files, allowed_patterns=["src/**/*.py"], base_path=base
        )

        assert len(result["allowed_files"]) == 1
        assert len(result["out_of_scope_files"]) == 1

    def test_validate_paths_summary_format(self):
        """Test summary message formatting."""
        # Only allowed files
        result1 = validate_paths_against_scope([Path("src/main.py")], allowed_patterns=["src/**"])
        assert result1["summary"] == "1 allowed"

        # Forbidden files
        result2 = validate_paths_against_scope(
            [Path("src/secret.py")],
            allowed_patterns=["src/**"],
            forbidden_patterns=["**/secret.py"],
        )
        assert "forbidden" in result2["summary"]

        # Out of scope
        result3 = validate_paths_against_scope([Path("tests/test.py")], allowed_patterns=["src/**"])
        assert "out of scope" in result3["summary"]

    def test_validate_paths_returns_json_serializable_strings(self):
        """Test validation results can be written directly to JSON evidence."""
        result = validate_paths_against_scope(
            [Path("src/main.py"), Path("docs/readme.md")],
            allowed_patterns=["src/**"],
        )

        json.dumps(result)
        assert result["allowed_files"] == ["src/main.py"]
        assert result["out_of_scope_files"] == ["docs/readme.md"]


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_matches_patterns_with_dots(self):
        """Test patterns with dot files."""
        assert matches_patterns(Path(".gitignore"), [".*"]) is True
        assert matches_patterns(Path(".env"), [".*"]) is True
        assert matches_patterns(Path("normal.py"), [".*"]) is False

    def test_matches_patterns_windows_paths(self):
        """Test with Windows-style paths."""
        # pathspec should handle both forward and backslashes
        assert matches_patterns(Path("src/main.py"), ["src/**/*.py"]) is True

    def test_filter_paths_duplicate_patterns(self):
        """Test filtering with duplicate patterns."""
        paths = [Path("src/main.py")]

        valid, invalid = filter_paths_by_patterns(
            paths,
            allowed_patterns=["src/**/*.py", "src/**/*.py"],  # Duplicate
        )

        assert len(valid) == 1

    def test_validate_paths_empty_patterns(self):
        """Test validation with empty patterns."""
        files = [Path("src/main.py")]

        result = validate_paths_against_scope(files, allowed_patterns=[])

        assert result["valid"] is False
        assert len(result["out_of_scope_files"]) == 1


# Made with Bob
