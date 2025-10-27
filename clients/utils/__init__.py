"""
Utility modules for browser automation clients.

This package contains helper utilities used across different browser clients.
"""

from .output_utils import get_screenshot_path, get_json_path

__all__ = [
    'get_screenshot_path',
    'get_json_path',
]
