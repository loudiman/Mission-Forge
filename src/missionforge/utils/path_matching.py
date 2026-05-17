"""Path matching utilities using glob patterns."""

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pathspec

from ..core.exceptions import ValidationError


def matches_patterns(
    file_path: Path, patterns: Sequence[str], base_path: Path | None = None
) -> bool:
    """Check if file path matches any of the glob patterns.

    Supports gitignore-style patterns including:
    - ** for recursive directory matching
    - * for single-level wildcard
    - ? for single character wildcard
    - [abc] for character classes

    Args:
        file_path: Path to check.
        patterns: List of glob patterns (e.g., ["src/**/*.py", "tests/**"]).
        base_path: Base path for relative pattern matching. If provided,
                  file_path will be made relative to base_path.

    Returns:
        True if path matches any pattern, False otherwise.

    Examples:
        >>> matches_patterns(Path("src/main.py"), ["src/**/*.py"])
        True
        >>> matches_patterns(Path("tests/test.py"), ["src/**"])
        False
        >>> matches_patterns(Path("src/utils/helper.py"), ["src/**/*.py"])
        True
    """
    if not patterns:
        return False

    try:
        spec = pathspec.PathSpec.from_lines("gitignore", patterns)

        # Convert to relative path if base_path provided
        if base_path:
            try:
                relative_path = file_path.relative_to(base_path)
                path_str = str(relative_path)
            except ValueError:
                # file_path is not relative to base_path
                path_str = str(file_path)
        else:
            path_str = str(file_path)

        return spec.match_file(path_str)
    except Exception as e:
        raise ValidationError(
            f"Failed to match path against patterns: {file_path}", f"Error: {str(e)}"
        ) from e


def filter_paths_by_patterns(
    paths: Sequence[Path],
    allowed_patterns: Sequence[str],
    forbidden_patterns: Sequence[str] | None = None,
    base_path: Path | None = None,
) -> tuple[list[Path], list[Path]]:
    """Filter paths by allowed and forbidden patterns.

    A path is valid if:
    1. It matches at least one allowed pattern, AND
    2. It does NOT match any forbidden pattern

    Args:
        paths: Paths to filter.
        allowed_patterns: Patterns that paths must match.
        forbidden_patterns: Patterns that paths must NOT match.
        base_path: Base path for relative pattern matching.

    Returns:
        Tuple of (valid_paths, invalid_paths).

    Examples:
        >>> valid, invalid = filter_paths_by_patterns(
        ...     [Path("src/main.py"), Path("tests/test.py")],
        ...     allowed_patterns=["src/**"],
        ...     forbidden_patterns=["**/__pycache__/**"]
        ... )
        >>> print(valid)  # [Path("src/main.py")]
        >>> print(invalid)  # [Path("tests/test.py")]
    """
    forbidden_patterns = forbidden_patterns or []
    valid_paths: list[Path] = []
    invalid_paths: list[Path] = []

    for path in paths:
        # Check if path matches forbidden patterns
        if forbidden_patterns and matches_patterns(path, forbidden_patterns, base_path):
            invalid_paths.append(path)
            continue

        # Check if path matches allowed patterns
        if allowed_patterns and matches_patterns(path, allowed_patterns, base_path):
            valid_paths.append(path)
        else:
            invalid_paths.append(path)

    return valid_paths, invalid_paths


def validate_paths_against_scope(
    changed_files: Sequence[Path],
    allowed_patterns: Sequence[str],
    forbidden_patterns: Sequence[str] | None = None,
    base_path: Path | None = None,
) -> dict[str, Any]:
    """Validate changed files against allowed/forbidden patterns.

    Provides detailed validation results for the validation workflow.

    Args:
        changed_files: Files to validate.
        allowed_patterns: Patterns defining allowed scope.
        forbidden_patterns: Patterns defining forbidden scope.
        base_path: Base path for relative pattern matching.

    Returns:
        Dictionary with validation results:
        {
            "valid": bool,  # True if all files are valid
            "allowed_files": list[str],  # Files matching allowed patterns
            "forbidden_files": list[str],  # Files matching forbidden patterns
            "out_of_scope_files": list[str],  # Files not matching any allowed pattern
            "summary": str  # Human-readable summary
        }

    Examples:
        >>> result = validate_paths_against_scope(
        ...     [Path("src/main.py"), Path("src/secret.py")],
        ...     allowed_patterns=["src/**/*.py"],
        ...     forbidden_patterns=["**/secret.py"]
        ... )
        >>> print(result["valid"])  # False
        >>> print(result["forbidden_files"])  # [Path("src/secret.py")]
    """
    forbidden_patterns = forbidden_patterns or []
    allowed_files: list[str] = []
    forbidden_files: list[str] = []
    out_of_scope_files: list[str] = []

    for file_path in changed_files:
        # Check forbidden patterns first
        if forbidden_patterns and matches_patterns(file_path, forbidden_patterns, base_path):
            forbidden_files.append(str(file_path))
            continue

        # Check allowed patterns
        if allowed_patterns and matches_patterns(file_path, allowed_patterns, base_path):
            allowed_files.append(str(file_path))
        else:
            out_of_scope_files.append(str(file_path))

    # Validation passes if no forbidden or out-of-scope files
    valid = len(forbidden_files) == 0 and len(out_of_scope_files) == 0

    # Generate summary
    summary_parts = []
    if allowed_files:
        summary_parts.append(f"{len(allowed_files)} allowed")
    if forbidden_files:
        summary_parts.append(f"{len(forbidden_files)} forbidden")
    if out_of_scope_files:
        summary_parts.append(f"{len(out_of_scope_files)} out of scope")

    summary = ", ".join(summary_parts) if summary_parts else "No files changed"

    return {
        "valid": valid,
        "allowed_files": allowed_files,
        "forbidden_files": forbidden_files,
        "out_of_scope_files": out_of_scope_files,
        "summary": summary,
    }


# Made with Bob
