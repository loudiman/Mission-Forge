"""Configuration management for MissionForge."""

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class MissionForgeConfig(BaseModel):
    """User configuration model."""

    # Test execution
    test_timeout: int = Field(default=300, description="Test timeout in seconds")
    test_retry_count: int = Field(default=0, description="Number of test retries")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[Path] = Field(default=None, description="Log file path")

    # Git operations
    git_diff_context: int = Field(default=3, description="Lines of context in diffs")

    # Plugins
    plugin_dirs: list[Path] = Field(
        default_factory=list, description="Additional plugin directories"
    )
    disabled_plugins: list[str] = Field(
        default_factory=list, description="Disabled plugin names"
    )

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "MissionForgeConfig":
        """Load config from file or use defaults.

        Args:
            config_path: Path to config file. If None or doesn't exist, uses defaults.

        Returns:
            Configuration instance.
        """
        if config_path and config_path.exists():
            with open(config_path) as f:
                data = yaml.safe_load(f) or {}
                return cls(**data)
        return cls()

    def save(self, config_path: Path) -> None:
        """Save config to file.

        Args:
            config_path: Path where config should be saved.
        """
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(self.model_dump(mode="json"), f, default_flow_style=False)

    @classmethod
    def get_default_config_path(cls) -> Path:
        """Get default config file path.

        Returns:
            Path to ~/.missionforge.config.yaml
        """
        return Path.home() / ".missionforge.config.yaml"

# Made with Bob
