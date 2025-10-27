"""
Sample Script 2: Quotes Scraper

This script demonstrates using BrowserbaseClient to:
1. Navigate to quotes.toscrape.com
2. Scrape quotes, authors, and tags from the page
3. Interact with pagination
4. Display and save the results
"""


import os
import json
from clients.utils import output_utils
from dotenv import load_dotenv
from clients.browserbase_client import BrowserbaseClient
from selenium.webdriver.common.by import By
import time

# Load environment variables from .env file
load_dotenv()


def scrape_quotes(num_pages: int = 2):
    """
    Scrape quotes from quotes.toscrape.com

    Args:
        num_pages: Number of pages to scrape (default: 2)
    """
    # Get credentials from environment variables
    api_key = os.getenv("API_KEY_BROWSERBASE")
    project_id = os.getenv("PROJECT_ID_BROWSERBASE")

    if not api_key or not project_id:
        print("Error: Missing API_KEY_BROWSERBASE or PROJECT_ID_BROWSERBASE")
        print("Please set them in your .env file")
        return

    print("=" * 80)
    print("Quotes Scraper Demo")
    print("=" * 80)
    print()

    all_quotes = []

    # Create and use the Browserbase client
    client = BrowserbaseClient(api_key=api_key, project_id=project_id)

    try:
        # Start the browser session
        with client:
            # Navigate to the quotes page
            base_url = "https://quotes.toscrape.com"
            client.navigate(base_url)

            # Wait a moment for the page to load
            time.sleep(2)

            print(f"Page Title: {client.get_title()}")
            print(f"Starting to scrape {num_pages} page(s)...")
            print()

            # Scrape multiple pages
            for page_num in range(1, num_pages + 1):
                print(f"Scraping page {page_num}...")
                print("-" * 80)

                # Find all quote containers
                quote_divs = client.find_elements(By.CLASS_NAME, "quote")

                print(f"Found {len(quote_divs)} quotes on this page")

                # Extract data from each quote
                for idx, quote_div in enumerate(quote_divs, 1):
                    try:
                        # Extract the quote text
                        quote_text = quote_div.find_element(
                            By.CLASS_NAME, "text"
                        ).text

                        # Extract the author
                        author = quote_div.find_element(
                            By.CLASS_NAME, "author"
                        ).text

                        # Extract tags
                        tag_elements = quote_div.find_elements(
                            By.CLASS_NAME, "tag"
                        )
                        tags = [tag.text for tag in tag_elements]

                        # Create quote dictionary
                        quote_data = {
                            "page": page_num,
                            "quote": quote_text,
                            "author": author,
                            "tags": tags
                        }

                        all_quotes.append(quote_data)

                        # Print the quote
                        print(f"\nQuote #{idx}:")
                        print(f"  Text: {quote_text}")
                        print(f"  Author: {author}")
                        print(f"  Tags: {', '.join(tags)}")

                    except Exception as e:
                        print(f"Error extracting quote {idx}: {e}")

                print()
                print(f"Completed scraping page {page_num}")
                print()

                # Try to go to the next page (if not the last page)
                if page_num < num_pages:
                    try:
                        # Find the "Next" button
                        next_button = client.find_element(
                            By.CSS_SELECTOR,
                            "li.next > a"
                        )

                        # Click the next button
                        print("Navigating to next page...")
                        next_button.click()

                        # Wait for the page to load
                        time.sleep(2)

                    except Exception as e:
                        print(f"Could not navigate to next page: {e}")
                        print("This might be the last page.")
                        break

            # Summary
            print("=" * 80)
            print("SCRAPING SUMMARY")
            print("=" * 80)
            print(f"Total quotes scraped: {len(all_quotes)}")
            print(f"Pages scraped: {page_num}")
            print()

            # Get all unique authors
            unique_authors = set(q["author"] for q in all_quotes)
            print(f"Unique authors: {len(unique_authors)}")
            print("Authors:", ", ".join(sorted(unique_authors)))
            print()

            # Get all unique tags
            all_tags = []
            for quote in all_quotes:
                all_tags.extend(quote["tags"])
            unique_tags = set(all_tags)
            print(f"Unique tags: {len(unique_tags)}")
            print("Tags:", ", ".join(sorted(unique_tags)))
            print()

            # Save to JSON file
            with open(output_utils.get_json_path("scraped-quotes"), "w", encoding="utf-8") as f:
                json.dump(all_quotes, f, indent=2, ensure_ascii=False)

            print(f"Quotes saved to outputs folder")
            print()

            # Take a screenshot of the last page
            try:
                client.take_screenshot("quotes-screenshot")
                # Screenshot path is printed by the client
            except Exception as e:
                print(f"Could not save screenshot: {e}")

            print()

            # Demonstrate getting page source
            page_source = client.get_page_source()
            print(f"Page source length: {len(page_source)} characters")
            print()

            # Demonstrate JavaScript execution
            print("Demonstrating JavaScript execution:")
            page_height = client.execute_script("return document.body.scrollHeight;")
            print(f"  Page height: {page_height}px")
            viewport_width = client.execute_script("return window.innerWidth;")
            print(f"  Viewport width: {viewport_width}px")
            print()

            print("=" * 80)
            print("Demo completed successfully!")
            print("=" * 80)

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

    return all_quotes


def scrape_quote_details():
    """
    Alternative demo: Click on author links and scrape author details
    """
    # Get credentials from environment variables
    api_key = os.getenv("API_KEY_BROWSERBASE")
    project_id = os.getenv("PROJECT_ID_BROWSERBASE")

    if not api_key or not project_id:
        print("Error: Missing API_KEY_BROWSERBASE or PROJECT_ID_BROWSERBASE")
        return

    print("=" * 80)
    print("Quote Details Scraper Demo")
    print("=" * 80)
    print()

    client = BrowserbaseClient(api_key=api_key, project_id=project_id)

    try:
        with client:
            # Navigate to the quotes page
            client.navigate("https://quotes.toscrape.com")
            time.sleep(2)

            # Find the first author link and click it
            first_author_link = client.find_element(
                By.CSS_SELECTOR,
                ".quote .author + a"
            )

            author_name = client.find_element(By.CLASS_NAME, "author").text
            print(f"Clicking on author: {author_name}")

            first_author_link.click()
            time.sleep(2)

            # Extract author details
            print()
            print("=" * 80)
            print("AUTHOR DETAILS")
            print("=" * 80)

            try:
                author_title = client.find_element(By.CLASS_NAME, "author-title").text
                print(f"Name: {author_title}")
            except:
                pass

            try:
                author_born = client.find_element(By.CLASS_NAME, "author-born-date").text
                author_location = client.find_element(By.CLASS_NAME, "author-born-location").text
                print(f"Born: {author_born} in {author_location}")
            except:
                pass

            try:
                author_description = client.find_element(By.CLASS_NAME, "author-description").text
                print(f"\nBiography:")
                print(author_description[:300] + "..." if len(author_description) > 300 else author_description)
            except:
                pass

            print()
            print("=" * 80)

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the main scraper
    scrape_quotes(num_pages=2)

    print("\n\n")

    # Uncomment to run the author details demo
    # scrape_quote_details()
