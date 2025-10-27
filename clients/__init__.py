"""
Browser Automation Clients

This package contains client implementations for various browser automation services:
- Browserbase: Cloud browser automation service
- Hyperbrowser: AI-powered browser automation (Playwright-based, not Selenium)
- Steel: Browser automation service
- Skyvern: AI-powered browser automation with LLM and computer vision

Each client provides a high-level API for:
- Session management
- Page navigation
- Element interaction
- JavaScript execution
- Screenshot capture

Output Management:
- All screenshots and JSON files are saved to the outputs/ directory
- Files are automatically timestamped with format: name_<epoch_milliseconds>.ext
- Use output_utils for custom file management
"""

from .browserbase_client import BrowserbaseClient, create_client as create_browserbase_client
from .hyperbrowser_client import (
    HyperbrowserPlaywrightClient,
    create_client as create_hyperbrowser_client
)
from .steel_client import SteelClient, create_client as create_steel_client
from .skyvern_client import SkyvernClient, SkyvernClientSync, create_client as create_skyvern_client

__all__ = [
    'BrowserbaseClient',
    'create_browserbase_client',
    'HyperbrowserPlaywrightClient',
    'create_hyperbrowser_client',
    'SteelClient',
    'create_steel_client',
    'SkyvernClient',
    'SkyvernClientSync',
    'create_skyvern_client',
]
