"""
Mission Repository

Handles reading and parsing mission data from .missionforge/ directory.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from missionforge.core.exceptions import MissionForgeError


class RepositoryError(MissionForgeError):
    """Raised when repository operations fail."""
    pass


class MissionRepository:
    """
    Repository for reading mission data from .missionforge/ directory.
    
    This class provides methods to discover and read mission files,
    parse YAML and JSON data, and navigate the mission structure.
    """
    
    def __init__(self, root_path: Optional[Path] = None):
        """
        Initialize the mission repository.
        
        Args:
            root_path: Root directory containing .missionforge/. 
                      If None, searches upward from current directory.
        
        Raises:
            RepositoryError: If .missionforge/ directory cannot be found
        """
        self.root_path = root_path or self._find_repository_root()
        self.missionforge_dir = self.root_path / ".missionforge"
        
        if not self.missionforge_dir.exists():
            raise RepositoryError(
                f"No .missionforge directory found at {self.root_path}"
            )
    
    @staticmethod
    def _find_repository_root() -> Path:
        """
        Find repository root by searching upward for .missionforge/ directory.
        
        Returns:
            Path: Repository root directory
            
        Raises:
            RepositoryError: If no .missionforge/ directory found
        """
        current = Path.cwd()
        
        # Search upward through parent directories
        for parent in [current] + list(current.parents):
            if (parent / ".missionforge").exists():
                return parent
        
        raise RepositoryError(
            "Could not find .missionforge directory in current path or parents"
        )
    
    def list_missions(self) -> List[str]:
        """
        List all parent mission IDs.
        
        Returns:
            List of mission IDs (e.g., ['MF-001', 'MF-002'])
        """
        missions_dir = self.missionforge_dir / "missions"
        if not missions_dir.exists():
            return []
        
        return [
            d.name for d in missions_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]
    
    def read_mission_yaml(self, mission_id: str) -> Dict:
        """
        Read and parse mission.yaml for a parent mission.
        
        Args:
            mission_id: Parent mission ID (e.g., 'MF-001')
            
        Returns:
            Parsed YAML data as dictionary
            
        Raises:
            RepositoryError: If mission file not found or invalid
        """
        mission_file = (
            self.missionforge_dir / "missions" / mission_id / "mission.yaml"
        )
        
        if not mission_file.exists():
            raise RepositoryError(f"Mission file not found: {mission_id}")
        
        try:
            with open(mission_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise RepositoryError(f"Invalid YAML in {mission_id}: {e}")
    
    def read_json_file(self, file_path: Path) -> Dict:
        """
        Read and parse a JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data as dictionary
            
        Raises:
            RepositoryError: If file not found or invalid JSON
        """
        if not file_path.exists():
            raise RepositoryError(f"File not found: {file_path}")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise RepositoryError(f"Invalid JSON in {file_path}: {e}")

# Made with Bob
