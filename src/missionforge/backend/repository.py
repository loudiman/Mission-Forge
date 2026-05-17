"""
Mission Repository

Handles reading and parsing mission data from .missionforge/ directory.
"""

import json
from pathlib import Path

import yaml

from missionforge.core.exceptions import MissionForgeError

from .cache.file_cache import file_cache


class RepositoryError(MissionForgeError):
    """Raised when repository operations fail."""
    pass


class MissionRepository:
    """
    Repository for reading mission data from .missionforge/ directory.

    This class provides methods to discover and read mission files,
    parse YAML and JSON data, and navigate the mission structure.
    """

    def __init__(self, root_path: Path | None = None):
        """
        Initialize the mission repository.

        Args:
            root_path: Root directory containing .missionforge/.
                      If None, searches upward from current directory.

        Raises:
            RepositoryError: If .missionforge/ directory cannot be found
        """
        self.root_path = root_path or self._find_repository_root()
        self.missionforge_dir = self.root_path / ".missionforge"

        if not self.missionforge_dir.exists():
            raise RepositoryError(
                f"No .missionforge directory found at {self.root_path}"
            )

    @staticmethod
    def _find_repository_root() -> Path:
        """
        Find repository root by searching upward for .missionforge/ directory.

        Returns:
            Path: Repository root directory

        Raises:
            RepositoryError: If no .missionforge/ directory found
        """
        current = Path.cwd()

        # Search upward through parent directories
        for parent in [current] + list(current.parents):
            if (parent / ".missionforge").exists():
                return parent

        raise RepositoryError(
            "Could not find .missionforge directory in current path or parents"
        )

    def list_missions(self) -> list[str]:
        """
        List all parent mission IDs.

        Returns:
            List of mission IDs (e.g., ['MF-001', 'MF-002'])
        """
        missions_dir = self.missionforge_dir / "missions"
        if not missions_dir.exists():
            return []

        return sorted([
            d.name for d in missions_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ])

    def read_mission_yaml(self, mission_id: str) -> dict | None:
        """
        Read and parse mission.yaml for a parent mission.
        """
        mission_file = (
            self.missionforge_dir / "missions" / mission_id / "mission.yaml"
        )
        if not mission_file.exists():
            return None

        def _loader(path: Path) -> dict:
            try:
                with open(path, encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise RepositoryError(f"Invalid YAML in {mission_id}: {e}") from e

        return file_cache.get(mission_file, _loader)

    def read_sub_mission_yaml(self, mission_id: str, sub_id: str) -> dict | None:
        """
        Read and parse sub-mission.yaml.
        """
        sub_file = (
            self.missionforge_dir / "missions" / mission_id / "sub-missions" / f"{sub_id}.yaml"
        )
        if not sub_file.exists():
            return None

        def _loader(path: Path) -> dict:
            try:
                with open(path, encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except yaml.YAMLError as e:
                raise RepositoryError(f"Invalid YAML in {sub_id}: {e}") from e

        return file_cache.get(sub_file, _loader)

    def read_report(self, mission_id: str) -> str | None:
        """
        Read mission report markdown.
        """
        report_file = (
            self.missionforge_dir / "missions" / mission_id / "report.md"
        )
        if not report_file.exists():
            return None

        def _loader(path: Path) -> str:
            with open(path, encoding="utf-8") as f:
                return f.read()

        return file_cache.get(report_file, _loader)

    def read_json_file(self, file_path: Path) -> dict:
        """
        Read and parse a JSON file.
        """
        if not file_path.exists():
            raise RepositoryError(f"File not found: {file_path}")

        def _loader(path: Path) -> dict:
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                raise RepositoryError(f"Invalid JSON in {file_path}: {e}") from e

        return file_cache.get(file_path, _loader)
