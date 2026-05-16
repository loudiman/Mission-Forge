"""Plugin discovery and management."""

import importlib.util
import inspect
from pathlib import Path
from typing import Type

from ..core.exceptions import PluginError
from ..core.logging import get_logger
from .base import Plugin

logger = get_logger(__name__)


class PluginRegistry:
    """Discovers and manages plugins."""

    def __init__(self) -> None:
        """Initialize plugin registry."""
        self._plugins: dict[str, Plugin] = {}

    def discover(self, plugin_dirs: list[Path]) -> None:
        """Discover plugins in specified directories.

        Args:
            plugin_dirs: List of directories to search for plugins.
        """
        for plugin_dir in plugin_dirs:
            if not plugin_dir.exists():
                logger.warning(f"Plugin directory does not exist: {plugin_dir}")
                continue

            if not plugin_dir.is_dir():
                logger.warning(f"Plugin path is not a directory: {plugin_dir}")
                continue

            for py_file in plugin_dir.glob("*.py"):
                if py_file.name.startswith("_"):
                    continue

                try:
                    self._load_plugin_from_file(py_file)
                except Exception as e:
                    logger.error(f"Failed to load plugin from {py_file}: {e}")

    def _load_plugin_from_file(self, file_path: Path) -> None:
        """Load plugin from Python file.

        Args:
            file_path: Path to Python file containing plugin.

        Raises:
            PluginError: If plugin loading fails.
        """
        try:
            spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
            if spec is None or spec.loader is None:
                raise PluginError(f"Could not load spec from {file_path}")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find Plugin subclasses
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, Plugin)
                    and obj is not Plugin
                    and not inspect.isabstract(obj)
                ):
                    try:
                        plugin = obj()
                        self._plugins[plugin.name] = plugin
                        logger.info(f"Loaded plugin: {plugin.name} v{plugin.version}")
                    except Exception as e:
                        logger.error(f"Failed to instantiate plugin {name}: {e}")

        except Exception as e:
            raise PluginError(f"Failed to load plugin from {file_path}", str(e))

    def get(self, name: str) -> Plugin | None:
        """Get plugin by name.

        Args:
            name: Plugin name.

        Returns:
            Plugin instance or None if not found.
        """
        return self._plugins.get(name)

    def list_plugins(self, plugin_type: Type[Plugin] | None = None) -> list[Plugin]:
        """List all plugins or plugins of specific type.

        Args:
            plugin_type: Optional plugin type to filter by.

        Returns:
            List of plugin instances.
        """
        if plugin_type:
            return [p for p in self._plugins.values() if isinstance(p, plugin_type)]
        return list(self._plugins.values())

    def register(self, plugin: Plugin) -> None:
        """Manually register a plugin instance.

        Args:
            plugin: Plugin instance to register.

        Raises:
            PluginError: If plugin with same name already exists.
        """
        if plugin.name in self._plugins:
            raise PluginError(
                f"Plugin '{plugin.name}' already registered",
                "Use a different plugin name or unregister the existing plugin",
            )
        self._plugins[plugin.name] = plugin
        logger.info(f"Registered plugin: {plugin.name} v{plugin.version}")

    def unregister(self, name: str) -> None:
        """Unregister a plugin by name.

        Args:
            name: Plugin name to unregister.
        """
        if name in self._plugins:
            plugin = self._plugins.pop(name)
            try:
                plugin.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up plugin {name}: {e}")
            logger.info(f"Unregistered plugin: {name}")

    def cleanup_all(self) -> None:
        """Cleanup all registered plugins."""
        for name in list(self._plugins.keys()):
            self.unregister(name)

# Made with Bob
