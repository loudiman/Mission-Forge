"""Custom exception hierarchy for MissionForge."""


class MissionForgeError(Exception):
    """Base exception for all MissionForge errors."""

    def __init__(self, message: str, suggestion: str | None = None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(message)

    def format_error(self) -> str:
        """Format error with suggestion."""
        msg = f"❌ {self.message}"
        if self.suggestion:
            msg += f"\n💡 Suggestion: {self.suggestion}"
        return msg


class WorkspaceNotFoundError(MissionForgeError):
    """Raised when .missionforge workspace not found."""

    def __init__(self, path: str):
        super().__init__(
            f"No .missionforge workspace found from {path}",
            "Run 'missionforge workspace init <mission-id>' to create a workspace",
        )


class InvalidMissionIDError(MissionForgeError):
    """Raised when mission ID format is invalid."""

    def __init__(self, mission_id: str):
        super().__init__(
            f"Invalid mission ID: {mission_id}",
            "Mission IDs must match pattern: [A-Z]{{2,4}}-\\d{{3}}[A-Z]? (e.g., MF-001, FG-042A)",
        )


class ValidationError(MissionForgeError):
    """Raised when validation fails."""

    pass


class GitOperationError(MissionForgeError):
    """Raised when git operation fails."""

    pass


class TestExecutionError(MissionForgeError):
    """Raised when test execution fails."""

    pass


class ConfigurationError(MissionForgeError):
    """Raised when configuration is invalid."""

    pass


class PluginError(MissionForgeError):
    """Raised when plugin operation fails."""

    pass


# Made with Bob
