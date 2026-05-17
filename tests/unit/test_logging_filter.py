"""Test logging filter for hashlib blake2 errors."""

import logging


def test_blake2_error_filter():
    """Test that blake2 hashlib errors are filtered out."""
    # Import logging module to ensure filter is applied
    from missionforge.core import logging as mf_logging  # noqa: F401

    # Create a test logger
    logger = logging.getLogger()

    # Create a test handler to capture log records
    class TestHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.records = []

        def emit(self, record):
            self.records.append(record)

    test_handler = TestHandler()
    logger.addHandler(test_handler)

    # Try to log a blake2 error message (should be filtered)
    logger.error("code for hash blake2b was not found.")

    # Try to log a normal error message (should not be filtered)
    logger.error("This is a normal error message")

    # Clean up
    logger.removeHandler(test_handler)

    # Verify that only the normal error was captured
    assert len(test_handler.records) == 1
    assert "normal error" in test_handler.records[0].getMessage()
    assert "blake2" not in test_handler.records[0].getMessage()


def test_blake2s_error_filter():
    """Test that blake2s hashlib errors are also filtered out."""
    from missionforge.core import logging as mf_logging  # noqa: F401

    logger = logging.getLogger()

    class TestHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.records = []

        def emit(self, record):
            self.records.append(record)

    test_handler = TestHandler()
    logger.addHandler(test_handler)

    # Try to log a blake2s error message (should be filtered)
    logger.error("code for hash blake2s was not found.")

    # Clean up
    logger.removeHandler(test_handler)

    # Verify that the blake2s error was filtered
    assert len(test_handler.records) == 0


def test_other_errors_not_filtered():
    """Test that other error messages are not filtered."""
    from missionforge.core import logging as mf_logging  # noqa: F401

    logger = logging.getLogger()

    class TestHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.records = []

        def emit(self, record):
            self.records.append(record)

    test_handler = TestHandler()
    test_handler.setLevel(logging.DEBUG)  # Capture all levels
    logger.addHandler(test_handler)

    # Temporarily set logger level to DEBUG to capture all messages
    original_level = logger.level
    logger.setLevel(logging.DEBUG)

    # Log various error messages that should NOT be filtered
    logger.error("File not found")
    logger.error("Invalid configuration")
    logger.warning("This is a warning")
    logger.info("This is info")

    # Restore original level
    logger.setLevel(original_level)

    # Clean up
    logger.removeHandler(test_handler)

    # Verify all messages were captured
    assert len(test_handler.records) == 4


# Made with Bob
