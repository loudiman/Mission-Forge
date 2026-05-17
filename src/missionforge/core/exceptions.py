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


class BaselineAlreadyExistsError(MissionForgeError):
    """Raised when baseline already committed."""

    def __init__(self, sub_mission_id: str, baseline_path: str):
        super().__init__(
            f"Baseline already exists for {sub_mission_id} at {baseline_path}",
            "Use 'missionforge baseline reset <id> --force' to remove and re-capture",
        )


class BaselineNotCapturedError(MissionForgeError):
    """Raised when trying to commit without capture."""

    def __init__(self, sub_mission_id: str):
        super().__init__(
            f"No baseline.todo.json found for {sub_mission_id}",
            "Run 'missionforge baseline capture <id>' first to generate baseline.todo.json",
        )


class BaselineValidationError(MissionForgeError):
    """Raised when baseline validation fails."""

    pass


class BaselineIncompleteError(MissionForgeError):
    """Raised when baseline has unfilled values."""

    def __init__(self, sub_mission_id: str, unfilled_metrics: list[str]):
        metrics_list = "\n  • ".join(unfilled_metrics)
        super().__init__(
            f"Baseline for {sub_mission_id} has unfilled metric values:\n  • {metrics_list}",
            "Fill all metric values in baseline.todo.json before committing",
        )


# Made with Bob
