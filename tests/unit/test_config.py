"""Unit tests for config module."""

from pathlib import Path

import pytest

from missionforge.core.config import MissionForgeConfig


def test_config_defaults():
    """Test default configuration values."""
    config = MissionForgeConfig()

    assert config.test_timeout == 300
    assert config.test_retry_count == 0
    assert config.log_level == "INFO"
    assert config.log_file is None
    assert config.git_diff_context == 3
    assert config.plugin_dirs == []
    assert config.disabled_plugins == []


def test_config_load_nonexistent_file(tmp_path: Path):
    """Test loading config from nonexistent file uses defaults."""
    config_path = tmp_path / "nonexistent.yaml"
    config = MissionForgeConfig.load(config_path)

    assert config.test_timeout == 300
    assert config.log_level == "INFO"


def test_config_load_from_file(tmp_path: Path):
    """Test loading config from YAML file."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """test_timeout: 600
log_level: DEBUG
git_diff_context: 5
"""
    )

    config = MissionForgeConfig.load(config_path)

    assert config.test_timeout == 600
    assert config.log_level == "DEBUG"
    assert config.git_diff_context == 5
    # Defaults for unspecified values
    assert config.test_retry_count == 0


def test_config_save(tmp_path: Path):
    """Test saving config to file."""
    config = MissionForgeConfig(
        test_timeout=600, log_level="DEBUG", git_diff_context=5
    )

    config_path = tmp_path / "config.yaml"
    config.save(config_path)

    assert config_path.exists()

    # Load and verify
    loaded_config = MissionForgeConfig.load(config_path)
    assert loaded_config.test_timeout == 600
    assert loaded_config.log_level == "DEBUG"
    assert loaded_config.git_diff_context == 5


def test_config_save_creates_parent_dirs(tmp_path: Path):
    """Test that save creates parent directories."""
    config = MissionForgeConfig()
    config_path = tmp_path / "nested" / "dir" / "config.yaml"

    config.save(config_path)

    assert config_path.exists()
    assert config_path.parent.exists()


def test_config_with_plugin_dirs(tmp_path: Path):
    """Test config with plugin directories."""
    plugin_dir1 = tmp_path / "plugins1"
    plugin_dir2 = tmp_path / "plugins2"

    config = MissionForgeConfig(plugin_dirs=[plugin_dir1, plugin_dir2])

    assert len(config.plugin_dirs) == 2
    assert plugin_dir1 in config.plugin_dirs
    assert plugin_dir2 in config.plugin_dirs


def test_config_with_disabled_plugins():
    """Test config with disabled plugins."""
    config = MissionForgeConfig(disabled_plugins=["plugin1", "plugin2"])

    assert len(config.disabled_plugins) == 2
    assert "plugin1" in config.disabled_plugins
    assert "plugin2" in config.disabled_plugins


def test_config_get_default_config_path():
    """Test getting default config path."""
    path = MissionForgeConfig.get_default_config_path()

    assert path == Path.home() / ".missionforge.config.yaml"
    assert path.name == ".missionforge.config.yaml"


def test_config_load_empty_file(tmp_path: Path):
    """Test loading config from empty YAML file."""
    config_path = tmp_path / "empty.yaml"
    config_path.write_text("")

    config = MissionForgeConfig.load(config_path)

    # Should use defaults
    assert config.test_timeout == 300
    assert config.log_level == "INFO"


def test_config_with_log_file(tmp_path: Path):
    """Test config with log file path."""
    log_file = tmp_path / "missionforge.log"
    config = MissionForgeConfig(log_file=log_file)

    assert config.log_file == log_file


def test_config_validation():
    """Test config validation with Pydantic."""
    # Valid config
    config = MissionForgeConfig(test_timeout=100, test_retry_count=3)
    assert config.test_timeout == 100
    assert config.test_retry_count == 3

    # Invalid types should raise validation error
    with pytest.raises(Exception):  # Pydantic ValidationError
        MissionForgeConfig(test_timeout="invalid")

# Made with Bob
