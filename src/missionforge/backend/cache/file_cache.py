import os
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

class FileCache:
    """A simple cache that invalidates based on file mtime."""
    
    def __init__(self):
        self._cache: Dict[str, Tuple[float, Any]] = {}
        
    def get(self, file_path: Path, loader: Callable[[Path], Any]) -> Any:
        """
        Get data from cache or load it if missing/stale.
        
        Args:
            file_path: Path to the file
            loader: Function to load the file if not in cache
            
        Returns:
            The parsed file contents
        """
        path_str = str(file_path)
        
        try:
            current_mtime = os.path.getmtime(file_path)
        except OSError:
            # If file doesn't exist or can't be read, let the loader handle it
            return loader(file_path)
            
        cached = self._cache.get(path_str)
        if cached is not None:
            cached_mtime, cached_data = cached
            if current_mtime == cached_mtime:
                return cached_data
                
        # Cache miss or stale
        data = loader(file_path)
        self._cache[path_str] = (current_mtime, data)
        return data
        
    def clear(self):
        """Clear all cached entries."""
        self._cache.clear()

# Global instance
file_cache = FileCache()
