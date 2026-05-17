"""Base classes for MissionForge plugins."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class Plugin(ABC):
    """Base class for all plugins."""

    name: str
    version: str
    description: str

    @abstractmethod
    def initialize(self, config: dict[str, Any]) -> None:
        """Initialize plugin with configuration.

        Args:
            config: Plugin configuration dictionary.
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        pass


class ValidatorPlugin(Plugin):
    """Base class for custom validators."""

    @abstractmethod
    def validate(self, data: BaseModel) -> list[str]:
        """Validate data and return list of error messages.

        Args:
            data: Data model to validate.

        Returns:
            List of validation error messages (empty if valid).
        """
        pass


class MetricCollectorPlugin(Plugin):
    """Base class for custom metric collectors."""

    @abstractmethod
    def collect(self, mission_id: str) -> dict[str, Any]:
        """Collect metrics for a mission.

        Args:
            mission_id: Mission identifier.

        Returns:
            Dictionary of collected metrics.
        """
        pass


class FormatterPlugin(Plugin):
    """Base class for custom report formatters."""

    @abstractmethod
    def format(self, data: dict[str, Any]) -> str:
        """Format report data to string.

        Args:
            data: Report data dictionary.

        Returns:
            Formatted report as string.
        """
        pass


class CommandPlugin(Plugin):
    """Base class for custom CLI commands."""

    @abstractmethod
    def register(self, app: Any) -> None:
        """Register command with Typer app.

        Args:
            app: Typer application instance.
        """
        pass


# Made with Bob
