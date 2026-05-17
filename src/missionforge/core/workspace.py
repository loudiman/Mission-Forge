"""Workspace path resolution and management."""

from pathlib import Path

from .exceptions import WorkspaceNotFoundError


class Workspace:
    """Manages .missionforge workspace discovery and paths."""

    WORKSPACE_DIR = ".missionforge"
    MISSIONS_DIR = "missions"

    def __init__(self, start_path: Path | None = None):
        """Initialize workspace from start path.

        Args:
            start_path: Starting directory for workspace search. Defaults to current directory.

        Raises:
            WorkspaceNotFoundError: If no .missionforge workspace found.
        """
        self.root = self._find_workspace_root(start_path or Path.cwd())
        self.workspace_dir = self.root / self.WORKSPACE_DIR
        self.missions_dir = self.workspace_dir / self.MISSIONS_DIR

    def _find_workspace_root(self, start: Path) -> Path:
        """Walk up directory tree to find .missionforge/.

        Args:
            start: Starting directory for search.

        Returns:
            Path to workspace root directory.

        Raises:
            WorkspaceNotFoundError: If no workspace found.
        """
        current = start.resolve()
        while current != current.parent:
            if (current / self.WORKSPACE_DIR).is_dir():
                return current
            current = current.parent
        raise WorkspaceNotFoundError(str(start))

    def mission_path(self, mission_id: str) -> Path:
        """Get path to mission directory.

        Args:
            mission_id: Mission identifier (e.g., 'MF-001').

        Returns:
            Path to mission directory.
        """
        return self.missions_dir / mission_id

    def sub_mission_path(self, mission_id: str, sub_mission_id: str) -> Path:
        """Get path to sub-mission directory.

        Args:
            mission_id: Parent mission identifier.
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').

        Returns:
            Path to sub-mission directory.
        """
        return self.mission_path(mission_id) / "sub-missions" / sub_mission_id

    def sub_mission_definition_path(self, mission_id: str, sub_mission_id: str) -> Path:
        """Get the sub-mission YAML path, supporting canonical and legacy layouts.

        Canonical layout:
            sub-missions/<sub-mission-id>/sub-mission.yaml

        Legacy layout:
            sub-missions/<sub-mission-id>.yaml
        """
        canonical_path = self.sub_mission_path(mission_id, sub_mission_id) / "sub-mission.yaml"
        if canonical_path.exists():
            return canonical_path
        return self.mission_path(mission_id) / "sub-missions" / f"{sub_mission_id}.yaml"

    def exists(self) -> bool:
        """Check if workspace is initialized.

        Returns:
            True if workspace directory exists.
        """
        return self.workspace_dir.exists()

    def initialize(self) -> None:
        """Initialize workspace directory structure.

        Creates .missionforge/missions/ directory structure.
        """
        self.missions_dir.mkdir(parents=True, exist_ok=True)

    def list_missions(self) -> list[str]:
        """List all mission IDs in workspace.

        Returns:
            List of mission IDs.
        """
        if not self.missions_dir.exists():
            return []

        missions = []
        for mission_dir in self.missions_dir.iterdir():
            if mission_dir.is_dir() and (mission_dir / "mission.yaml").exists():
                missions.append(mission_dir.name)
        return sorted(missions)

    def baseline_todo_path(self, sub_mission_id: str) -> Path:
        """Get path to baseline.todo.json for a sub-mission.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').

        Returns:
            Path to baseline.todo.json file.
        """
        # Extract parent mission ID (e.g., "MF-001-A" -> "MF-001")
        parent_id = sub_mission_id.rsplit("-", 1)[0]
        return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.todo.json"

    def baseline_path(self, sub_mission_id: str) -> Path:
        """Get path to baseline.json for a sub-mission.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').

        Returns:
            Path to baseline.json file.
        """
        # Extract parent mission ID (e.g., "MF-001-A" -> "MF-001")
        parent_id = sub_mission_id.rsplit("-", 1)[0]
        return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.json"

    def validation_todo_path(self, sub_mission_id: str) -> Path:
        """Get path to validation.todo.json for a sub-mission."""
        parent_id = sub_mission_id.rsplit("-", 1)[0]
        return self.sub_mission_path(parent_id, sub_mission_id) / "validation.todo.json"

    def validation_path(self, sub_mission_id: str) -> Path:
        """Get path to validation.json for a sub-mission."""
        parent_id = sub_mission_id.rsplit("-", 1)[0]
        return self.sub_mission_path(parent_id, sub_mission_id) / "validation.json"

    def parent_validation_path(self, mission_id: str) -> Path:
        """Get path to parent validation.json.

        Args:
            mission_id: Parent mission identifier (e.g., 'MF-001').

        Returns:
            Path to .missionforge/missions/{mission_id}/validation.json
        """
        return self.mission_path(mission_id) / "validation.json"


# Made with Bob
