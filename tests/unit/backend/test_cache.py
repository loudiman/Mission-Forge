import os
import pytest
from pathlib import Path
from src.missionforge.backend.cache.file_cache import FileCache

def test_file_cache(tmp_path):
    cache = FileCache()
    test_file = tmp_path / "test.txt"
    test_file.write_text("v1")
    
    loader_calls = 0
    def loader(path: Path):
        nonlocal loader_calls
        loader_calls += 1
        with open(path, "r") as f:
            return f.read()
            
    # First access - cache miss
    data1 = cache.get(test_file, loader)
    assert data1 == "v1"
    assert loader_calls == 1
    
    # Second access - cache hit
    data2 = cache.get(test_file, loader)
    assert data2 == "v1"
    assert loader_calls == 1
    
    # Modify file
    import time
    # Sleep a bit to ensure mtime changes
    time.sleep(0.01)
    test_file.write_text("v2")
    
    # Third access - cache miss (mtime changed)
    data3 = cache.get(test_file, loader)
    assert data3 == "v2"
    assert loader_calls == 2
    
    cache.clear()
    
    # Fourth access - cache miss (cleared)
    data4 = cache.get(test_file, loader)
    assert data4 == "v2"
    assert loader_calls == 3

def test_file_cache_missing_file():
    cache = FileCache()
    missing_file = Path("/nonexistent/file.txt")
    
    loader_calls = 0
    def loader(path: Path):
        nonlocal loader_calls
        loader_calls += 1
        return "fallback"
        
    data = cache.get(missing_file, loader)
    assert data == "fallback"
    assert loader_calls == 1
