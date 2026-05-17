"""
Unit tests for backend repository module.
"""

import json
from pathlib import Path

import pytest
import yaml

from missionforge.backend.repository import MissionRepository, RepositoryError


class TestMissionRepository:
    """Tests for MissionRepository class."""
    
    def test_init_with_valid_path(self, tmp_path):
        """Test repository initialization with valid .missionforge directory."""
        # Create .missionforge directory
        missionforge_dir = tmp_path / ".missionforge"
        missionforge_dir.mkdir()
        
        repo = MissionRepository(root_path=tmp_path)
        
        assert repo.root_path == tmp_path
        assert repo.missionforge_dir == missionforge_dir
    
    def test_init_without_missionforge_dir(self, tmp_path):
        """Test repository initialization fails without .missionforge directory."""
        with pytest.raises(RepositoryError, match="No .missionforge directory found"):
            MissionRepository(root_path=tmp_path)
    
    def test_find_repository_root_in_current_dir(self, tmp_path, monkeypatch):
        """Test finding repository root in current directory."""
        missionforge_dir = tmp_path / ".missionforge"
        missionforge_dir.mkdir()
        
        monkeypatch.chdir(tmp_path)
        
        root = MissionRepository._find_repository_root()
        assert root == tmp_path
    
    def test_find_repository_root_in_parent_dir(self, tmp_path, monkeypatch):
        """Test finding repository root in parent directory."""
        missionforge_dir = tmp_path / ".missionforge"
        missionforge_dir.mkdir()
        
        subdir = tmp_path / "subdir" / "nested"
        subdir.mkdir(parents=True)
        
        monkeypatch.chdir(subdir)
        
        root = MissionRepository._find_repository_root()
        assert root == tmp_path
    
    def test_find_repository_root_not_found(self, tmp_path, monkeypatch):
        """Test finding repository root fails when not found."""
        monkeypatch.chdir(tmp_path)
        
        with pytest.raises(RepositoryError, match="Could not find .missionforge"):
            MissionRepository._find_repository_root()
    
    def test_list_missions_empty(self, tmp_path):
        """Test listing missions when directory is empty."""
        missionforge_dir = tmp_path / ".missionforge"
        missionforge_dir.mkdir()
        
        repo = MissionRepository(root_path=tmp_path)
        missions = repo.list_missions()
        
        assert missions == []
    
    def test_list_missions_with_missions(self, tmp_path):
        """Test listing missions with multiple mission directories."""
        missionforge_dir = tmp_path / ".missionforge"
        missions_dir = missionforge_dir / "missions"
        missions_dir.mkdir(parents=True)
        
        # Create mission directories
        (missions_dir / "MF-001").mkdir()
        (missions_dir / "MF-002").mkdir()
        (missions_dir / ".hidden").mkdir()  # Should be ignored
        
        repo = MissionRepository(root_path=tmp_path)
        missions = repo.list_missions()
        
        assert sorted(missions) == ["MF-001", "MF-002"]
    
    def test_read_mission_yaml_success(self, tmp_path):
        """Test reading mission YAML file successfully."""
        missionforge_dir = tmp_path / ".missionforge"
        mission_dir = missionforge_dir / "missions" / "MF-001"
        mission_dir.mkdir(parents=True)
        
        mission_data = {
            "id": "MF-001",
            "goal": "Test mission",
            "forbidden_paths": ["core/**"],
        }
        
        mission_file = mission_dir / "mission.yaml"
        with open(mission_file, "w") as f:
            yaml.dump(mission_data, f)
        
        repo = MissionRepository(root_path=tmp_path)
        data = repo.read_mission_yaml("MF-001")
        
        assert data == mission_data
    
    def test_read_mission_yaml_not_found(self, tmp_path):
        """Test reading mission YAML fails when file not found."""
        missionforge_dir = tmp_path / ".missionforge"
        missionforge_dir.mkdir()
        
        repo = MissionRepository(root_path=tmp_path)
        
        with pytest.raises(RepositoryError, match="Mission file not found"):
            repo.read_mission_yaml("MF-999")
    
    def test_read_mission_yaml_invalid(self, tmp_path):
        """Test reading mission YAML fails with invalid YAML."""
        missionforge_dir = tmp_path / ".missionforge"
        mission_dir = missionforge_dir / "missions" / "MF-001"
        mission_dir.mkdir(parents=True)
        
        mission_file = mission_dir / "mission.yaml"
        with open(mission_file, "w") as f:
            f.write("invalid: yaml: content: [")
        
        repo = MissionRepository(root_path=tmp_path)
        
        with pytest.raises(RepositoryError, match="Invalid YAML"):
            repo.read_mission_yaml("MF-001")
    
    def test_read_json_file_success(self, tmp_path):
        """Test reading JSON file successfully."""
        missionforge_dir = tmp_path / ".missionforge"
        missionforge_dir.mkdir()
        
        json_file = tmp_path / "test.json"
        json_data = {"key": "value", "number": 42}
        
        with open(json_file, "w") as f:
            json.dump(json_data, f)
        
        repo = MissionRepository(root_path=tmp_path)
        data = repo.read_json_file(json_file)
        
        assert data == json_data
    
    def test_read_json_file_not_found(self, tmp_path):
        """Test reading JSON file fails when file not found."""
        missionforge_dir = tmp_path / ".missionforge"
        missionforge_dir.mkdir()
        
        repo = MissionRepository(root_path=tmp_path)
        
        with pytest.raises(RepositoryError, match="File not found"):
            repo.read_json_file(tmp_path / "nonexistent.json")
    
    def test_read_json_file_invalid(self, tmp_path):
        """Test reading JSON file fails with invalid JSON."""
        missionforge_dir = tmp_path / ".missionforge"
        missionforge_dir.mkdir()
        
        json_file = tmp_path / "invalid.json"
        with open(json_file, "w") as f:
            f.write("{invalid json content")
        
        repo = MissionRepository(root_path=tmp_path)
        
        with pytest.raises(RepositoryError, match="Invalid JSON"):
            repo.read_json_file(json_file)

# Made with Bob
