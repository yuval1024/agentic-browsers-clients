"""
Output utilities for managing screenshots and JSON files

Provides functions to generate timestamped filenames and ensure the outputs directory exists.
"""

import time
from pathlib import Path


# Get the project root directory (parent of clients folder)
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def ensure_outputs_dir():
    """
    Ensure the outputs directory exists.
    Creates it if it doesn't exist.
    """
    OUTPUTS_DIR.mkdir(exist_ok=True)


def get_timestamped_filename(name: str, extension: str) -> str:
    """
    Generate a timestamped filename in the outputs directory.

    Args:
        name: Base name for the file (e.g., "screenshot", "quotes")
        extension: File extension without dot (e.g., "png", "json")

    Returns:
        Absolute path to the file with format: outputs/name_<epoch_milliseconds>.ext

    Example:
        >>> get_timestamped_filename("screenshot", "png")
        '/path/to/outputs/screenshot_1698765432123.png'
    """
    ensure_outputs_dir()

    # Get current time in milliseconds
    timestamp_ms = int(time.time() * 1000)

    # Create filename
    filename = f"{name}_{timestamp_ms}.{extension}"

    # Return absolute path
    return str(OUTPUTS_DIR / filename)


def get_output_path(filename: str) -> str:
    """
    Get absolute path for a file in the outputs directory.

    Args:
        filename: Name of the file

    Returns:
        Absolute path to the file in outputs directory

    Example:
        >>> get_output_path("my_file.json")
        '/path/to/outputs/my_file.json'
    """
    ensure_outputs_dir()
    return str(OUTPUTS_DIR / filename)


# Convenience functions for common file types
def get_screenshot_path(name: str = "screenshot") -> str:
    """
    Get timestamped path for a screenshot file.

    Args:
        name: Base name for the screenshot (default: "screenshot")

    Returns:
        Absolute path to PNG file in outputs directory
    """
    return get_timestamped_filename(name, "png")


def get_json_path(name: str = "data") -> str:
    """
    Get timestamped path for a JSON file.

    Args:
        name: Base name for the JSON file (default: "data")

    Returns:
        Absolute path to JSON file in outputs directory
    """
    return get_timestamped_filename(name, "json")


def get_log_path(name: str = "log") -> str:
    """
    Get timestamped path for a log file.

    Args:
        name: Base name for the log file (default: "log")

    Returns:
        Absolute path to log file in outputs directory
    """
    return get_timestamped_filename(name, "log")


# Initialize outputs directory when module is imported
ensure_outputs_dir()
