"""
HyperbrowserPlaywrightClient - A Python class to interact with Hyperbrowser using Playwright

This client uses Playwright (CDP protocol) instead of Selenium since Hyperbrowser
does not support the WebDriver protocol.

This client provides convenient methods to:
- Access web pages
- Get page source code
- Interact with web elements
- Execute JavaScript
- Take screenshots
"""

import os
from typing import Optional
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext

try:
    from hyperbrowser import Hyperbrowser
except ImportError as e:
    raise ImportError(
        "The 'hyperbrowser' package is required to use HyperbrowserPlaywrightClient. "
        "Install it with: pip install hyperbrowser"
    ) from e


class HyperbrowserPlaywrightClient:
    """
    A high-level client for interacting with Hyperbrowser using Playwright.

    Usage:
        client = HyperbrowserPlaywrightClient(api_key="your-api-key")

        with client:
            client.navigate("https://example.com")
            source = client.get_page_source()
            print(source)
    """

    def __init__(self, api_key: str):
        """
        Initialize the Hyperbrowser Playwright client.

        Args:
            api_key: Hyperbrowser API key
        """
        self.api_key = api_key
        self.hb = Hyperbrowser(api_key=api_key)
        self.session = None
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def __enter__(self):
        """Context manager entry - starts a browser session"""
        self.start_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes the browser session"""
        self.close_session()

    def start_session(self):
        """Create a new Hyperbrowser session and initialize Playwright"""
        print("Creating Hyperbrowser session...")
        self.session = self.hb.sessions.create()

        print(f"Session created: {self.session.id}")
        print(f"WebSocket endpoint: {self.session.ws_endpoint}")

        # Initialize Playwright
        self.playwright = sync_playwright().start()

        # Connect to the browser via CDP
        self.browser = self.playwright.chromium.connect_over_cdp(self.session.ws_endpoint)

        # Get the default context or create a new one
        if self.browser.contexts:
            self.context = self.browser.contexts[0]
        else:
            self.context = self.browser.new_context()

        # Get the first page or create a new one
        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

        print("Playwright initialized successfully")

    def close_session(self):
        """Close the browser session and cleanup"""
        if self.page:
            print("Closing page...")
            self.page.close()
            self.page = None

        if self.browser:
            print("Closing browser...")
            self.browser.close()
            self.browser = None

        if self.playwright:
            self.playwright.stop()
            self.playwright = None

        if self.session:
            try:
                self.hb.sessions.stop(self.session.id)
                print("Session stopped")
            except Exception as e:
                print(f"Error stopping session: {e}")

    def navigate(self, url: str):
        """
        Navigate to a URL.

        Args:
            url: The URL to navigate to
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        print(f"Navigating to: {url}")
        self.page.goto(url)
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
            selector: CSS selector to locate the element

        Returns:
            ElementHandle if found
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.query_selector(selector)

    def find_elements(self, selector: str):
        """
        Find multiple elements on the page using CSS selector.

        Args:
            selector: CSS selector to locate the elements

        Returns:
            List of ElementHandles
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.query_selector_all(selector)

    def wait_for_element(self, selector: str, timeout: int = 10000):
        """
        Wait for an element to be present on the page.

        Args:
            selector: CSS selector to locate the element
            timeout: Maximum time to wait in milliseconds

        Returns:
            ElementHandle if found within timeout
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.wait_for_selector(selector, timeout=timeout)

    def click_element(self, selector: str):
        """
        Find and click an element.

        Args:
            selector: CSS selector to locate the element
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        self.page.click(selector)

    def type_text(self, selector: str, text: str):
        """
        Find an input element and type text into it.

        Args:
            selector: CSS selector to locate the element
            text: The text to type
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        self.page.fill(selector, text)

    def execute_script(self, script: str):
        """
        Execute JavaScript in the browser.

        Args:
            script: The JavaScript code to execute (should be a function expression or statement)

        Returns:
            The return value of the script
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        # Playwright expects a function expression, not a bare return statement
        # If the script starts with "return ", wrap it in a function
        if script.strip().startswith("return "):
            script = f"() => {{ {script} }}"

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
            selector: CSS selector to locate the element

        Returns:
            The text content of the element
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        element = self.page.query_selector(selector)
        if element:
            return element.text_content() or ""
        return ""

    def get_element_attribute(self, selector: str, attribute: str) -> str:
        """
        Get an attribute value of an element.

        Args:
            selector: CSS selector to locate the element
            attribute: The attribute name

        Returns:
            The attribute value
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.page.get_attribute(selector, attribute) or ""

    def scroll_to_element(self, selector: str):
        """
        Scroll to make an element visible.

        Args:
            selector: CSS selector to locate the element
        """
        if not self.page:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        element = self.page.query_selector(selector)
        if element:
            element.scroll_into_view_if_needed()


# Convenience function for quick usage
def create_client(api_key: Optional[str] = None) -> HyperbrowserPlaywrightClient:
    """
    Create a HyperbrowserPlaywrightClient using environment variables or provided credentials.

    Args:
        api_key: Hyperbrowser API key (defaults to HYPERBROWSER_API_KEY env var)

    Returns:
        HyperbrowserPlaywrightClient instance
    """
    api_key = api_key or os.getenv("HYPERBROWSER_API_KEY")

    if not api_key:
        raise ValueError("API key not provided and HYPERBROWSER_API_KEY not set")

    return HyperbrowserPlaywrightClient(api_key=api_key)
