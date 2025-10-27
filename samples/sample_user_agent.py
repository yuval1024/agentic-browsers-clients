"""
Sample Script 1: User Agent Detection

This script demonstrates using BrowserbaseClient to:
1. Navigate to whatismybrowser.com
2. Access the page
3. Extract the user agent information
4. Display the results
"""


import os
from dotenv import load_dotenv
from clients.browserbase_client import BrowserbaseClient
from selenium.webdriver.common.by import By
import time

# Load environment variables from .env file
load_dotenv()


def detect_user_agent():
    """
    Navigate to whatismybrowser.com and extract user agent information
    """
    # Get credentials from environment variables
    api_key = os.getenv("API_KEY_BROWSERBASE")
    project_id = os.getenv("PROJECT_ID_BROWSERBASE")

    if not api_key or not project_id:
        print("Error: Missing API_KEY_BROWSERBASE or PROJECT_ID_BROWSERBASE")
        print("Please set them in your .env file")
        return

    print("=" * 80)
    print("User Agent Detection Demo")
    print("=" * 80)
    print()

    # Create and use the Browserbase client
    client = BrowserbaseClient(api_key=api_key, project_id=project_id)

    try:
        # Start the browser session
        with client:
            # Navigate to the user agent detection page
            url = "https://gs.statcounter.com/detect"
            client.navigate(url)

            # Wait a moment for the page to fully load
            time.sleep(3)

            # Get the page title
            print(f"Page Title: {client.get_title()}")
            print(f"Current URL: {client.get_current_url()}")
            print()

            # Extract user agent string
            try:
                # The user agent is displayed in a div with class "string-major"
                user_agent_element = client.wait_for_element(
                    By.CSS_SELECTOR,
                    ".string-major",
                    timeout=10
                )
                user_agent = user_agent_element.text
                print("=" * 80)
                print("DETECTED USER AGENT:")
                print("=" * 80)
                print(user_agent)
                print("=" * 80)
                print()

            except Exception as e:
                print(f"Could not extract user agent from page element: {e}")
                print("Trying alternative method...")

                # Alternative: get user agent via JavaScript
                user_agent = client.execute_script("return navigator.userAgent;")
                print("=" * 80)
                print("USER AGENT (via JavaScript):")
                print("=" * 80)
                print(user_agent)
                print("=" * 80)
                print()

            # Extract additional browser information
            try:
                print("Additional Browser Information:")
                print("-" * 80)

                # Try to get browser name
                try:
                    browser_name = client.find_element(
                        By.CSS_SELECTOR,
                        ".browser-name"
                    ).text
                    print(f"Browser Name: {browser_name}")
                except:
                    pass

                # Try to get browser version
                try:
                    browser_version = client.find_element(
                        By.CSS_SELECTOR,
                        ".browser-version"
                    ).text
                    print(f"Browser Version: {browser_version}")
                except:
                    pass

                # Try to get OS information
                try:
                    os_name = client.find_element(
                        By.CSS_SELECTOR,
                        ".os-name"
                    ).text
                    print(f"Operating System: {os_name}")
                except:
                    pass

            except Exception as e:
                print(f"Could not extract additional info: {e}")

            print("-" * 80)
            print()

            # Get some page source to demonstrate the functionality
            page_source = client.get_page_source()
            print(f"Page source length: {len(page_source)} characters")
            print()

            # Take a screenshot
            try:
                client.take_screenshot("user-agent-screenshot")
                # Screenshot path is printed by the client
            except Exception as e:
                print(f"Could not save screenshot: {e}")

            print()
            print("=" * 80)
            print("Demo completed successfully!")
            print("=" * 80)

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    detect_user_agent()
