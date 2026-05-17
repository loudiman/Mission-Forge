"""Tests for backend exception classes."""

import pytest

from missionforge.backend.exceptions import (
    APIError,
    BackendError,
    DataNotFoundError,
    InvalidDataError,
)
from missionforge.core.exceptions import MissionForgeError


class TestBackendError:
    """Test BackendError exception."""

    def test_backend_error_inherits_from_missionforge_error(self):
        """BackendError should inherit from MissionForgeError."""
        assert issubclass(BackendError, MissionForgeError)

    def test_backend_error_can_be_raised(self):
        """BackendError can be raised with a message."""
        with pytest.raises(BackendError) as exc_info:
            raise BackendError("Test error message")
        assert str(exc_info.value) == "Test error message"


class TestAPIError:
    """Test APIError exception."""

    def test_api_error_inherits_from_backend_error(self):
        """APIError should inherit from BackendError."""
        assert issubclass(APIError, BackendError)

    def test_api_error_can_be_raised(self):
        """APIError can be raised with a message."""
        with pytest.raises(APIError) as exc_info:
            raise APIError("API operation failed")
        assert str(exc_info.value) == "API operation failed"


class TestDataNotFoundError:
    """Test DataNotFoundError exception."""

    def test_data_not_found_error_inherits_from_backend_error(self):
        """DataNotFoundError should inherit from BackendError."""
        assert issubclass(DataNotFoundError, BackendError)

    def test_data_not_found_error_with_resource_and_identifier(self):
        """DataNotFoundError can be raised with resource and identifier."""
        with pytest.raises(DataNotFoundError) as exc_info:
            raise DataNotFoundError("mission", "MF-001")
        assert str(exc_info.value) == "mission not found: MF-001"
        assert exc_info.value.resource == "mission"
        assert exc_info.value.identifier == "MF-001"

    def test_data_not_found_error_is_backend_error(self):
        """DataNotFoundError instances are also BackendError instances."""
        error = DataNotFoundError("sub-mission", "MF-001-A")
        assert isinstance(error, BackendError)
        assert isinstance(error, MissionForgeError)
        assert error.resource == "sub-mission"
        assert error.identifier == "MF-001-A"


class TestInvalidDataError:
    """Test InvalidDataError exception."""

    def test_invalid_data_error_inherits_from_backend_error(self):
        """InvalidDataError should inherit from BackendError."""
        assert issubclass(InvalidDataError, BackendError)

    def test_invalid_data_error_can_be_raised(self):
        """InvalidDataError can be raised with a message."""
        with pytest.raises(InvalidDataError) as exc_info:
            raise InvalidDataError("Invalid YAML format")
        assert str(exc_info.value) == "Invalid YAML format"

    def test_invalid_data_error_is_backend_error(self):
        """InvalidDataError instances are also BackendError instances."""
        error = InvalidDataError("Test")
        assert isinstance(error, BackendError)
        assert isinstance(error, MissionForgeError)

# Made with Bob
