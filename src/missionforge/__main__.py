"""Entry point for python -m missionforge."""

# Import logging first to suppress harmless hashlib errors
from .core import logging  # noqa: F401

from .cli.app import cli_main

if __name__ == "__main__":
    cli_main()

# Made with Bob
