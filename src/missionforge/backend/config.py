"""
Backend Configuration

Manages configuration settings for the MissionForge backend API server.
"""

from pathlib import Path

from pydantic_settings import BaseSettings


class BackendSettings(BaseSettings):
    """Backend API server configuration settings."""

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False

    # CORS settings
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Repository settings
    repository_root: Path | None = None

    class Config:
        """Pydantic configuration."""
        env_prefix = "MISSIONFORGE_"
        case_sensitive = False


def get_settings() -> BackendSettings:
    """
    Get backend settings instance.

    Returns:
        BackendSettings: Configuration settings
    """
    return BackendSettings()

# Made with Bob
