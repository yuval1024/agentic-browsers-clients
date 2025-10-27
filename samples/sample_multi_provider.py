"""
Sample Script 3: Multi-Provider Demonstration

This script demonstrates running the SAME task across multiple browser automation providers:
- Browserbase (Selenium)
- Hyperbrowser (Playwright)
- Steel (Playwright)

This shows:
1. How to write provider-agnostic code
2. How easy it is to switch between providers
3. Performance/behavior differences between providers
4. The unified API working across different protocols
"""

import os
import json
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List
from clients.utils import output_utils

# Import all available clients
from clients.browserbase_client import BrowserbaseClient
from clients.hyperbrowser_client import HyperbrowserPlaywrightClient
from clients.steel_client import SteelClient

# For Selenium-based clients
from selenium.webdriver.common.by import By

# Load environment variables
load_dotenv()


class BrowserProvider:
    """Wrapper to provide unified interface across all clients"""

    def __init__(self, name: str, client):
        self.name = name
        self.client = client
        self.protocol = "Selenium" if hasattr(client, 'driver') else "Playwright"

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, *args):
        return self.client.__exit__(*args)

    def navigate(self, url: str):
        return self.client.navigate(url)

    def get_title(self) -> str:
        return self.client.get_title()

    def find_elements(self, selector: str) -> List:
        """Find elements - handles both Selenium and Playwright selectors"""
        if self.protocol == "Selenium":
            return self.client.find_elements(By.CLASS_NAME, selector.replace(".", ""))
        else:
            # Playwright uses CSS selectors
            return self.client.find_elements(selector)

    def get_element_text(self, element) -> str:
        """Get text from element - unified interface"""
        if self.protocol == "Selenium":
            return element.text
        else:
            return self.client.get_element_text(element)

    def click_element(self, selector: str):
        """Click element by selector"""
        return self.client.click_element(selector)

    def take_screenshot(self, name: str) -> str:
        return self.client.take_screenshot(name)


def get_available_providers() -> Dict[str, BrowserProvider]:
    """
    Initialize all available browser providers based on environment variables.

    Returns:
        Dictionary of provider name -> BrowserProvider wrapper
    """
    providers = {}

    # Browserbase (Selenium)
    if os.getenv("API_KEY_BROWSERBASE") and os.getenv("PROJECT_ID_BROWSERBASE"):
        client = BrowserbaseClient(
            api_key=os.getenv("API_KEY_BROWSERBASE"),
            project_id=os.getenv("PROJECT_ID_BROWSERBASE")
        )
        providers["browserbase"] = BrowserProvider("Browserbase", client)
        print("✓ Browserbase available (Selenium)")

    # Hyperbrowser (Playwright)
    if os.getenv("HYPERBROWSER_API_KEY"):
        client = HyperbrowserPlaywrightClient(
            api_key=os.getenv("HYPERBROWSER_API_KEY")
        )
        providers["hyperbrowser"] = BrowserProvider("Hyperbrowser", client)
        print("✓ Hyperbrowser available (Playwright)")

    # Steel (Playwright)
    if os.getenv("STEEL_API_KEY"):
        client = SteelClient(
            api_key=os.getenv("STEEL_API_KEY")
        )
        providers["steel"] = BrowserProvider("Steel", client)
        print("✓ Steel available (Playwright)")

    return providers


def scrape_quotes_with_provider(provider: BrowserProvider, max_quotes: int = 10) -> List[Dict[str, Any]]:
    """
    Scrape quotes using any provider - demonstrates unified API.

    Args:
        provider: BrowserProvider wrapper
        max_quotes: Maximum number of quotes to scrape

    Returns:
        List of quote dictionaries
    """
    print(f"\n{'='*80}")
    print(f"Scraping with {provider.name} ({provider.protocol})")
    print(f"{'='*80}\n")

    quotes = []

    with provider:
        # Navigate to quotes site
        provider.navigate("https://quotes.toscrape.com")

        # Get page title
        title = provider.get_title()
        print(f"Page title: {title}")

        # Find and extract quotes - handle protocol differences
        if provider.protocol == "Selenium":
            # Selenium approach - returns list of elements
            quote_elements = provider.client.find_elements(By.CLASS_NAME, "quote")
            print(f"Found {len(quote_elements)} quotes on page")

            for idx, quote_elem in enumerate(quote_elements[:max_quotes], 1):
                try:
                    text = quote_elem.find_element(By.CLASS_NAME, "text").text
                    author = quote_elem.find_element(By.CLASS_NAME, "author").text
                    tag_elements = quote_elem.find_elements(By.CLASS_NAME, "tag")
                    tags = [tag.text for tag in tag_elements]

                    quote_data = {
                        "quote": text,
                        "author": author,
                        "tags": tags,
                        "provider": provider.name,
                        "protocol": provider.protocol
                    }
                    quotes.append(quote_data)
                    print(f"Quote #{idx}: {text[:50]}... - {author}")

                except Exception as e:
                    print(f"Error extracting quote {idx}: {e}")
                    continue

        else:
            # Playwright approach - use page API directly
            # Count quotes
            quote_count = provider.client.page.locator(".quote").count()
            print(f"Found {quote_count} quotes on page")

            # Extract each quote
            for idx in range(min(quote_count, max_quotes)):
                try:
                    quote_locator = provider.client.page.locator(".quote").nth(idx)
                    text = quote_locator.locator(".text").inner_text()
                    author = quote_locator.locator(".author").inner_text()
                    tag_locators = quote_locator.locator(".tag")
                    tag_count = tag_locators.count()
                    tags = [tag_locators.nth(i).inner_text() for i in range(tag_count)]

                    quote_data = {
                        "quote": text,
                        "author": author,
                        "tags": tags,
                        "provider": provider.name,
                        "protocol": provider.protocol
                    }
                    quotes.append(quote_data)
                    print(f"Quote #{idx + 1}: {text[:50]}... - {author}")

                except Exception as e:
                    print(f"Error extracting quote {idx + 1}: {e}")
                    continue

        # Take screenshot
        screenshot_name = f"quotes-{provider.name.lower()}"
        screenshot_path = provider.take_screenshot(screenshot_name)
        print(f"\nScreenshot saved: {screenshot_path}")

    print(f"\n✓ Scraped {len(quotes)} quotes with {provider.name}")

    return quotes


def compare_providers(providers: Dict[str, BrowserProvider]):
    """
    Run the same scraping task across all providers and compare results.

    Args:
        providers: Dictionary of available providers
    """
    print("\n" + "="*80)
    print("MULTI-PROVIDER QUOTES SCRAPING COMPARISON")
    print("="*80)

    if not providers:
        print("\n❌ No providers available!")
        print("Please configure at least one provider in your .env file:")
        print("  - API_KEY_BROWSERBASE + PROJECT_ID_BROWSERBASE")
        print("  - HYPERBROWSER_API_KEY")
        print("  - STEEL_API_KEY")
        return

    print(f"\n{len(providers)} provider(s) available")
    print()

    all_results = {}

    # Run scraping with each provider
    for name, provider in providers.items():
        try:
            quotes = scrape_quotes_with_provider(provider, max_quotes=5)
            all_results[name] = quotes
        except Exception as e:
            print(f"\n❌ Error with {name}: {e}")
            import traceback
            traceback.print_exc()
            all_results[name] = []

    # Summary comparison
    print("\n" + "="*80)
    print("COMPARISON SUMMARY")
    print("="*80)

    for name, quotes in all_results.items():
        if quotes:
            provider_name = quotes[0]["provider"]
            protocol = quotes[0]["protocol"]
            print(f"\n{provider_name} ({protocol}):")
            print(f"  ✓ Scraped {len(quotes)} quotes")
            print(f"  ✓ Authors: {', '.join(set(q['author'] for q in quotes))}")
        else:
            print(f"\n{name}:")
            print(f"  ❌ No quotes scraped")

    # Save combined results
    output_file = output_utils.get_json_path("multi-provider-comparison")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Combined results saved to: {output_file}")

    # Key insights
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    print("\n1. SAME CODE, DIFFERENT PROVIDERS")
    print("   The scraping logic works across Selenium and Playwright clients")

    print("\n2. PROTOCOL DIFFERENCES")
    print("   - Selenium: Uses By.CLASS_NAME, element.text")
    print("   - Playwright: Uses CSS selectors, locator API")

    print("\n3. UNIFIED WRAPPER")
    print("   BrowserProvider class handles protocol differences")
    print("   Your code doesn't need to know which provider it's using")

    print("\n4. EASY SWITCHING")
    print("   Change providers by switching environment variables")
    print("   No code changes needed!")

    print("\n" + "="*80)


def demo_single_provider(provider_name: str):
    """
    Demo using a single specific provider.

    Args:
        provider_name: Name of provider (browserbase, hyperbrowser, steel)
    """
    providers = get_available_providers()

    if provider_name not in providers:
        print(f"❌ Provider '{provider_name}' not available or not configured")
        print(f"Available providers: {', '.join(providers.keys())}")
        return

    provider = providers[provider_name]
    quotes = scrape_quotes_with_provider(provider, max_quotes=10)

    # Save results
    output_file = output_utils.get_json_path(f"quotes-{provider_name}")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Results saved to: {output_file}")


if __name__ == "__main__":
    import sys

    # Check command line arguments
    if len(sys.argv) > 1:
        # Run with specific provider
        provider_name = sys.argv[1].lower()
        print(f"\nRunning with single provider: {provider_name}\n")
        demo_single_provider(provider_name)
    else:
        # Run comparison across all available providers
        print("\nRunning multi-provider comparison...")
        print("(To use a single provider, run: python samples/sample_multi_provider.py <provider>)")
        print("Available: browserbase, hyperbrowser, steel\n")

        providers = get_available_providers()
        compare_providers(providers)

    print("\n✓ Demo complete!\n")
