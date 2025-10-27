"""
BrowserbaseClient - A Python class to interact with Browserbase remote Chrome browsers

This client provides convenient methods to:
- Access web pages
- Get page source code
- Interact with web elements
- Execute JavaScript
- Take screenshots
"""

import os
from typing import Optional, Dict, Any, List
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    from browserbase import Browserbase
except ImportError as e:
    raise ImportError(
        "The 'browserbase' package is required to use BrowserbaseClient. "
        "Install it with: pip install browserbase"
    ) from e


class BrowserbaseConnection(RemoteConnection):
    """Custom RemoteConnection that adds Browserbase authentication headers"""

    def __init__(self, session_id: str, remote_server_addr: str, api_key: str):
        super().__init__(remote_server_addr)
        self._session_id = session_id
        self._api_key = api_key

    def get_remote_connection_headers(self, parsed_url, keep_alive=False):
        """Add Browserbase-specific headers to the connection"""
        headers = super().get_remote_connection_headers(parsed_url, keep_alive)
        headers.update({
            'x-bb-api-key': self._api_key,
            'session-id': self._session_id
        })
        return headers


class BrowserbaseClient:
    """
    A high-level client for interacting with Browserbase remote Chrome browsers.

    Usage:
        client = BrowserbaseClient(
            api_key="your-api-key",
            project_id="your-project-id"
        )

        with client:
            client.navigate("https://example.com")
            source = client.get_page_source()
            print(source)
    """

    def __init__(self, api_key: str, project_id: str):
        """
        Initialize the Browserbase client.

        Args:
            api_key: Browserbase API key
            project_id: Browserbase project ID
        """
        self.api_key = api_key
        self.project_id = project_id
        self.bb = Browserbase(api_key=api_key)
        self.driver: Optional[webdriver.Remote] = None
        self.session = None

    def __enter__(self):
        """Context manager entry - starts a browser session"""
        self.start_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - closes the browser session"""
        self.close_session()

    def start_session(self):
        """Create a new Browserbase session and initialize the WebDriver"""
        print("Creating Browserbase session...")
        self.session = self.bb.sessions.create(project_id=self.project_id)

        print(f"Session created: {self.session.id}")
        print(f"Remote URL: {self.session.selenium_remote_url}")

        # Create custom connection with authentication
        connection = BrowserbaseConnection(
            session_id=self.session.id,
            remote_server_addr=self.session.selenium_remote_url,
            api_key=self.api_key
        )

        # Initialize Chrome options
        options = webdriver.ChromeOptions()

        # Create remote WebDriver
        self.driver = webdriver.Remote(
            command_executor=connection,
            options=options
        )

        print("WebDriver initialized successfully")

    def close_session(self):
        """Close the browser session and cleanup"""
        if self.driver:
            print("Closing browser session...")
            self.driver.quit()
            self.driver = None
            print("Session closed")

    def navigate(self, url: str):
        """
        Navigate to a URL.

        Args:
            url: The URL to navigate to
        """
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        print(f"Navigating to: {url}")
        self.driver.get(url)
        print(f"Page loaded: {self.driver.title}")

    def get_page_source(self) -> str:
        """
        Get the HTML source code of the current page.

        Returns:
            The page source as a string
        """
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.driver.page_source

    def get_current_url(self) -> str:
        """Get the current URL"""
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.driver.current_url

    def get_title(self) -> str:
        """Get the page title"""
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.driver.title

    def find_element(self, by: By, value: str):
        """
        Find a single element on the page.

        Args:
            by: The method to locate the element (By.ID, By.CSS_SELECTOR, etc.)
            value: The value to search for

        Returns:
            WebElement if found
        """
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.driver.find_element(by, value)

    def find_elements(self, by: By, value: str) -> List:
        """
        Find multiple elements on the page.

        Args:
            by: The method to locate the elements (By.ID, By.CSS_SELECTOR, etc.)
            value: The value to search for

        Returns:
            List of WebElements
        """
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.driver.find_elements(by, value)

    def wait_for_element(self, by: By, value: str, timeout: int = 10):
        """
        Wait for an element to be present on the page.

        Args:
            by: The method to locate the element
            value: The value to search for
            timeout: Maximum time to wait in seconds

        Returns:
            WebElement if found within timeout
        """
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def click_element(self, by: By, value: str):
        """
        Find and click an element.

        Args:
            by: The method to locate the element
            value: The value to search for
        """
        element = self.find_element(by, value)
        element.click()

    def type_text(self, by: By, value: str, text: str):
        """
        Find an input element and type text into it.

        Args:
            by: The method to locate the element
            value: The value to search for
            text: The text to type
        """
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript in the browser.

        Args:
            script: The JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            The return value of the script
        """
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.driver.execute_script(script, *args)

    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Take a screenshot of the current page.

        Args:
            name: Base name for the screenshot file (default: "screenshot")
                 The file will be saved as outputs/name_<timestamp>.png

        Returns:
            The absolute path where the screenshot was saved
        """
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        from .output_utils import get_screenshot_path

        filepath = get_screenshot_path(name)
        self.driver.save_screenshot(filepath)
        print(f"Screenshot saved: {filepath}")
        return filepath

    def get_element_text(self, by: By, value: str) -> str:
        """
        Get the text content of an element.

        Args:
            by: The method to locate the element
            value: The value to search for

        Returns:
            The text content of the element
        """
        element = self.find_element(by, value)
        return element.text

    def get_element_attribute(self, by: By, value: str, attribute: str) -> str:
        """
        Get an attribute value of an element.

        Args:
            by: The method to locate the element
            value: The value to search for
            attribute: The attribute name

        Returns:
            The attribute value
        """
        element = self.find_element(by, value)
        return element.get_attribute(attribute)

    def scroll_to_element(self, by: By, value: str):
        """
        Scroll to make an element visible.

        Args:
            by: The method to locate the element
            value: The value to search for
        """
        element = self.find_element(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def get_cookies(self) -> List[Dict]:
        """Get all cookies"""
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        return self.driver.get_cookies()

    def add_cookie(self, cookie_dict: Dict):
        """Add a cookie"""
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        self.driver.add_cookie(cookie_dict)

    def delete_all_cookies(self):
        """Delete all cookies"""
        if not self.driver:
            raise RuntimeError("Session not started. Call start_session() first or use context manager.")

        self.driver.delete_all_cookies()


# Convenience function for quick usage
def create_client(api_key: Optional[str] = None, project_id: Optional[str] = None) -> BrowserbaseClient:
    """
    Create a BrowserbaseClient using environment variables or provided credentials.

    Args:
        api_key: Browserbase API key (defaults to BROWSERBASE_API_KEY env var)
        project_id: Browserbase project ID (defaults to BROWSERBASE_PROJECT_ID env var)

    Returns:
        BrowserbaseClient instance
    """
    api_key = api_key or os.getenv("BROWSERBASE_API_KEY")
    project_id = project_id or os.getenv("BROWSERBASE_PROJECT_ID")

    if not api_key:
        raise ValueError("API key not provided and BROWSERBASE_API_KEY not set")
    if not project_id:
        raise ValueError("Project ID not provided and BROWSERBASE_PROJECT_ID not set")

    return BrowserbaseClient(api_key=api_key, project_id=project_id)
