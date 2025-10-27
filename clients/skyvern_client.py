"""
SkyvernClient - A Python class to interact with Skyvern AI for browser automation

This client provides convenient methods to:
- Create and run browser automation tasks
- Extract structured data from websites
- Execute complex workflows with LLM assistance
"""

import os
import asyncio
from typing import Optional, Dict, Any, List

try:
    from skyvern import Skyvern
    SKYVERN_AVAILABLE = True
except ImportError:
    Skyvern = None
    SKYVERN_AVAILABLE = False


class SkyvernClient:
    """
    A high-level client for interacting with Skyvern AI browser automation.

    Skyvern uses LLMs and computer vision to automate browser-based workflows.
    This client provides methods for creating and running automation tasks.

    Usage:
        client = SkyvernClient(api_key="your-api-key")

        # Run a simple task
        result = await client.run_task(
            url="https://example.com",
            prompt="Find and extract the main heading"
        )
        print(result)
    """

    def __init__(self, api_key: Optional[str] = None, cdp_url: Optional[str] = None):
        """
        Initialize the Skyvern client.

        Args:
            api_key: Skyvern API key (for cloud deployment)
            cdp_url: Chrome DevTools Protocol URL (for remote browser)
        """
        if not SKYVERN_AVAILABLE:
            raise ImportError("Skyvern SDK not installed. Install with: pip install skyvern")

        self.api_key = api_key
        self.cdp_url = cdp_url

        # Initialize Skyvern client
        if cdp_url:
            self.client = Skyvern(cdp_url=cdp_url)
        else:
            self.client = Skyvern()

    async def run_task(
        self,
        url: str,
        prompt: str,
        data_extraction_schema: Optional[Dict[str, Any]] = None,
        max_steps: Optional[int] = None,
        error_code_mapping: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create and run a browser automation task.

        Args:
            url: The starting URL for the task
            prompt: Natural language description of what to do
            data_extraction_schema: JSON schema for structured data extraction
            max_steps: Maximum number of steps to take (default: auto)
            error_code_mapping: Map error codes to custom messages

        Returns:
            Dictionary containing task results and extracted data
        """
        print(f"Running Skyvern task...")
        print(f"  URL: {url}")
        print(f"  Prompt: {prompt}")

        task_params = {
            "url": url,
            "prompt": prompt
        }

        if data_extraction_schema:
            task_params["data_extraction_schema"] = data_extraction_schema

        if max_steps:
            task_params["max_steps"] = max_steps

        if error_code_mapping:
            task_params["error_code_mapping"] = error_code_mapping

        try:
            result = await self.client.run_task(**task_params)
            print("Task completed successfully")
            return result
        except Exception as e:
            print(f"Error running task: {e}")
            raise

    async def extract_data(
        self,
        url: str,
        prompt: str,
        schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Navigate to a URL and extract structured data.

        Args:
            url: The URL to navigate to
            prompt: Description of what data to extract
            schema: JSON schema defining the data structure

        Returns:
            Extracted data matching the schema
        """
        print(f"Extracting data from {url}...")

        return await self.run_task(
            url=url,
            prompt=prompt,
            data_extraction_schema=schema
        )

    async def automate_workflow(
        self,
        url: str,
        steps: List[str]
    ) -> Dict[str, Any]:
        """
        Execute a multi-step workflow.

        Args:
            url: Starting URL
            steps: List of prompts describing each step

        Returns:
            Results from the workflow execution
        """
        print(f"Running workflow with {len(steps)} steps...")

        # Combine steps into a single prompt
        combined_prompt = " Then, ".join(steps)

        return await self.run_task(
            url=url,
            prompt=combined_prompt
        )

    async def scrape_with_schema(
        self,
        url: str,
        fields: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Scrape specific fields from a webpage.

        Args:
            url: The URL to scrape
            fields: Dictionary mapping field names to descriptions
                   e.g., {"title": "string", "price": "number"}

        Returns:
            Dictionary with extracted field values
        """
        # Build JSON schema from fields
        schema = {
            "type": "object",
            "properties": {
                field_name: {"type": field_type}
                for field_name, field_type in fields.items()
            }
        }

        prompt = f"Extract the following information: {', '.join(fields.keys())}"

        return await self.extract_data(url, prompt, schema)


# Convenience function for quick usage
def create_client(api_key: Optional[str] = None, cdp_url: Optional[str] = None) -> SkyvernClient:
    """
    Create a SkyvernClient using environment variables or provided credentials.

    Args:
        api_key: Skyvern API key (defaults to SKYVERN_API_KEY env var)
        cdp_url: Chrome DevTools Protocol URL (optional)

    Returns:
        SkyvernClient instance
    """
    api_key = api_key or os.getenv("SKYVERN_API_KEY")

    if not api_key and not cdp_url:
        raise ValueError("API key not provided and SKYVERN_API_KEY not set")

    return SkyvernClient(api_key=api_key, cdp_url=cdp_url)


# Synchronous wrapper for easier testing
class SkyvernClientSync:
    """Synchronous wrapper around SkyvernClient for easier testing"""

    def __init__(self, api_key: Optional[str] = None, cdp_url: Optional[str] = None):
        self.client = SkyvernClient(api_key=api_key, cdp_url=cdp_url)

    def run_task(self, url: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Run a task synchronously"""
        return asyncio.run(self.client.run_task(url, prompt, **kwargs))

    def extract_data(self, url: str, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data synchronously"""
        return asyncio.run(self.client.extract_data(url, prompt, schema))

    def scrape_with_schema(self, url: str, fields: Dict[str, str]) -> Dict[str, Any]:
        """Scrape with schema synchronously"""
        return asyncio.run(self.client.scrape_with_schema(url, fields))
