"""
SteelClient - A Python class to interact with Steel.dev remote Chrome browsers

This client provides convenient methods to:
- Access web pages
- Get page source code
- Interact with web elements
- Execute JavaScript
- Take screenshots

Uses Playwright for browser automation, following Steel's official documentation.
"""

import os
from typing import Optional, Dict, Any, List
from playwright.sync_api import sync_playwright, Browser, Page, Playwright

try:
    from steel import Steel
except ImportError as e:
    raise ImportError(
        "The 'steel-sdk' package is required to use SteelClient. "
        "Install it with: pip install steel-sdk"
    ) from e


class SteelClient:
    """
    A high-level client for interacting with Steel remote Chrome browsers using Playwright.

    Usage:
        client = SteelClient(api_key="your-api-key")

        with client:
            client.navigate("https://example.com")
            source = client.get_page_source()
            print(source)
    """

    def __init__(self, api_key: str):
        """
        Initialize the Steel client.

        Args:
            api_key: Steel API key
        """
        if Steel is None:
            raise ImportError("Steel SDK not installed. Install with: pip install steel-sdk")

        self.api_key = api_key
        self.steel = Steel(steel_api_key=api_key)
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.session = None

    def __enter__(self):
        """Context manager entry - starts a browser session"""
        self.start_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes the browser session"""
        self.close_session()

    def start_session(self):
        """Create a new Steel session and initialize Playwright browser"""
        print("Creating Steel session...")

        # Create session (no is_selenium flag needed for Playwright)
        self.session = self.steel.sessions.create()

        print(f"Session created: {self.session.id}")
        print(f"View live session at: {self.session.session_viewer_url}")

        # Connect Playwright to the Steel session
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.connect_over_cdp(
            f"{self.session.websocket_url}&apiKey={self.api_key}"
        )

        print("Connected to browser via Playwright")

        # Create page at existing context to ensure session is recorded
        current_context = self.browser.contexts[0]
        self.page = current_context.new_page()

        print("Page initialized successfully")

    def close_session(self):
        """Close the browser session and cleanup"""
        if self.page:
            try:
                self.page.close()
            except Exception as e:
                print(f"Error closing page: {e}")
            self.page = None

        if self.playwright:
            try:
                self.playwright.stop()
                print("Playwright stopped")
            except Exception as e:
                print(f"Error stopping Playwright: {e}")
            self.playwright = None

        if self.session:
            try:
                self.steel.sessions.release(self.session.id)
                print("Session released")
            except Exception as e:
                print(f"Error releasing session: {e}")

    def navigate(self, url: str, wait_until: str = "networkidle"):
        """
        Navigate to a URL.

        Args:
            url: The URL to navigate to
            wait_until: When to consider navigation succeeded ('load', 'domcontentloaded', 'networkidle')
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        print(f"Navigating to: {url}")
        self.page.goto(url, wait_until=wait_until)
        print(f"Page loaded: {self.page.title()}")

    def get_page_source(self) -> str:
        """
        Get the HTML source code of the current page.

        Returns:
            The page source as a string
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.content()

    def get_current_url(self) -> str:
        """Get the current URL"""
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.url

    def get_title(self) -> str:
        """Get the page title"""
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.title()

    def find_element(self, selector: str):
        """
        Find a single element on the page using CSS selector.

        Args:
            selector: CSS selector string

        Returns:
            Playwright Locator
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.locator(selector).first

    def find_elements(self, selector: str):
        """
        Find multiple elements on the page using CSS selector.

        Args:
            selector: CSS selector string

        Returns:
            Playwright Locator for all matching elements
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.locator(selector)

    def wait_for_element(self, selector: str, timeout: int = 10000):
        """
        Wait for an element to be present on the page.

        Args:
            selector: CSS selector string
            timeout: Maximum time to wait in milliseconds

        Returns:
            Playwright Locator
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        locator = self.page.locator(selector)
        locator.wait_for(timeout=timeout)
        return locator

    def click_element(self, selector: str):
        """
        Find and click an element.

        Args:
            selector: CSS selector string
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        self.page.locator(selector).first.click()

    def type_text(self, selector: str, text: str):
        """
        Find an input element and type text into it.

        Args:
            selector: CSS selector string
            text: The text to type
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        locator = self.page.locator(selector).first
        locator.clear()
        locator.fill(text)

    def execute_script(self, script: str) -> Any:
        """
        Execute JavaScript in the browser.

        Args:
            script: The JavaScript code to execute

        Returns:
            The return value of the script
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.evaluate(script)

    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Take a screenshot of the current page.

        Args:
            name: Base name for the screenshot file (default: "screenshot")
                 The file will be saved as outputs/name_<timestamp>.png

        Returns:
            The absolute path where the screenshot was saved
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        from .output_utils import get_screenshot_path

        filepath = get_screenshot_path(name)
        self.page.screenshot(path=filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath

    def get_element_text(self, selector: str) -> str:
        """
        Get the text content of an element.

        Args:
            selector: CSS selector string

        Returns:
            The text content of the element
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.locator(selector).first.text_content()

    def get_element_attribute(self, selector: str, attribute: str) -> str:
        """
        Get an attribute value of an element.

        Args:
            selector: CSS selector string
            attribute: The attribute name

        Returns:
            The attribute value
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.locator(selector).first.get_attribute(attribute)

    def scroll_to_element(self, selector: str):
        """
        Scroll to make an element visible.

        Args:
            selector: CSS selector string
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        self.page.locator(selector).first.scroll_into_view_if_needed()

    def get_cookies(self) -> List[Dict]:
        """Get all cookies"""
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.context.cookies()

    def add_cookie(self, cookie_dict: Dict):
        """Add a cookie"""
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        self.page.context.add_cookies([cookie_dict])

    def delete_all_cookies(self):
        """Delete all cookies"""
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        self.page.context.clear_cookies()


# Convenience function for quick usage
def create_client(api_key: Optional[str] = None) -> SteelClient:
    """
    Create a SteelClient using environment variables or provided credentials.

    Args:
        api_key: Steel API key (defaults to STEEL_API_KEY env var)

    Returns:
        SteelClient instance
    """
    api_key = api_key or os.getenv("STEEL_API_KEY")

    if not api_key:
        raise ValueError("API key not provided and STEEL_API_KEY not set")

    return SteelClient(api_key=api_key)
