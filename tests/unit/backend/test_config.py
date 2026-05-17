"""
Unit tests for backend config module.
"""

from pathlib import Path

from missionforge.backend.config import BackendSettings, get_settings


class TestBackendSettings:
    """Tests for BackendSettings class."""

    def test_default_settings(self):
        """Test default configuration values."""
        settings = BackendSettings()

        assert settings.host == "127.0.0.1"
        assert settings.port == 8000
        assert settings.reload is False
        assert len(settings.cors_origins) == 4
        assert "http://localhost:3000" in settings.cors_origins
        assert settings.repository_root is None

    def test_custom_host_and_port(self):
        """Test custom host and port configuration."""
        settings = BackendSettings(host="0.0.0.0", port=9000)

        assert settings.host == "0.0.0.0"
        assert settings.port == 9000

    def test_custom_cors_origins(self):
        """Test custom CORS origins configuration."""
        custom_origins = ["http://example.com", "https://app.example.com"]
        settings = BackendSettings(cors_origins=custom_origins)

        assert settings.cors_origins == custom_origins

    def test_reload_flag(self):
        """Test reload flag configuration."""
        settings = BackendSettings(reload=True)

        assert settings.reload is True

    def test_repository_root_path(self, tmp_path):
        """Test repository root path configuration."""
        settings = BackendSettings(repository_root=tmp_path)

        assert settings.repository_root == tmp_path
        assert isinstance(settings.repository_root, Path)

    def test_env_prefix(self, monkeypatch):
        """Test environment variable prefix."""
        monkeypatch.setenv("MISSIONFORGE_HOST", "192.168.1.1")
        monkeypatch.setenv("MISSIONFORGE_PORT", "8080")

        settings = BackendSettings()

        assert settings.host == "192.168.1.1"
        assert settings.port == 8080

    def test_case_insensitive_env_vars(self, monkeypatch):
        """Test case-insensitive environment variables."""
        monkeypatch.setenv("missionforge_reload", "true")

        settings = BackendSettings()

        assert settings.reload is True


class TestGetSettings:
    """Tests for get_settings function."""

    def test_get_settings_returns_instance(self):
        """Test that get_settings returns a BackendSettings instance."""
        settings = get_settings()

        assert isinstance(settings, BackendSettings)

    def test_get_settings_with_env_vars(self, monkeypatch):
        """Test get_settings respects environment variables."""
        monkeypatch.setenv("MISSIONFORGE_PORT", "7000")

        settings = get_settings()

        assert settings.port == 7000

# Made with Bob
