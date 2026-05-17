"""
Backend-specific exceptions.

Custom exception classes for the MissionForge backend API.
"""

from missionforge.core.exceptions import MissionForgeError


class BackendError(MissionForgeError):
    """Base exception for backend errors."""
    pass


class APIError(BackendError):
    """Raised when API operations fail."""
    pass


class DataNotFoundError(BackendError):
    """Raised when requested data is not found."""
    
    def __init__(self, resource: str, identifier: str):
        """
        Initialize data not found error.
        
        Args:
            resource: Type of resource (e.g., 'mission', 'sub-mission')
            identifier: Resource identifier
        """
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier}")


class InvalidDataError(BackendError):
    """Raised when data validation fails."""
    pass

# Made with Bob
