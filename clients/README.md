# Browser Automation Clients

This directory contains Python client implementations for various browser automation services.

## Available Clients

### 1. Browserbase Client (`browserbase_client.py`)
Cloud-based browser automation service.

**Protocol:** Selenium WebDriver
**Status:** ✅ Working

```python
from clients import BrowserbaseClient

client = BrowserbaseClient(api_key="your_key", project_id="your_project")
with client:
    client.navigate("https://example.com")
    title = client.get_title()
```

### 2. Hyperbrowser Playwright Client (`hyperbrowser_client.py`)
AI-powered browser automation using Playwright.

**Protocol:** Chrome DevTools Protocol (CDP) via WebSocket
**Status:** ✅ Working
**Note:** Hyperbrowser does NOT support Selenium WebDriver. Use Playwright client instead.

```python
from clients import HyperbrowserPlaywrightClient

client = HyperbrowserPlaywrightClient(api_key="your_key")
with client:
    client.navigate("https://example.com")
    user_agent = client.execute_script("return navigator.userAgent;")
```

### 3. Steel Client (`steel_client.py`)
Browser automation service with Playwright support.

**Protocol:** Playwright (CDP)
**Status:** ✅ Working

```python
from clients import SteelClient

client = SteelClient(api_key="your_key")
with client:
    client.navigate("https://example.com")
    content = client.get_page_source()
```

### 4. Hyperbrowser Selenium Client (`hyperbrowser_client.py`)
**Status:** ❌ Not Working - Do Not Use

This client is kept for reference only. Hyperbrowser does not support the Selenium WebDriver protocol.
Use `hyperbrowser_client.py` instead.

**Error:** WebDriver API returns `{"error":"No selenium port available"}`

See `HYPERBROWSER_SELENIUM_ISSUE.md` in the project root for details.

## Common Interface

All working clients share a similar high-level API:

| Method | Description |
|--------|-------------|
| `navigate(url)` | Navigate to a URL |
| `get_page_source()` | Get HTML source code |
| `get_title()` | Get page title |
| `get_current_url()` | Get current URL |
| `find_element(selector)` | Find a single element |
| `find_elements(selector)` | Find multiple elements |
| `wait_for_element(selector, timeout)` | Wait for element to appear |
| `click_element(selector)` | Click an element |
| `type_text(selector, text)` | Type text into an input |
| `execute_script(script)` | Execute JavaScript |
| `take_screenshot(filename)` | Capture screenshot |

## Environment Variables

Set these in your `.env` file:

```bash
# Browserbase
API_KEY_BROWSERBASE=your_api_key_here
PROJECT_ID_BROWSERBASE=your_id_here

# Hyperbrowser
HYPERBROWSER_API_KEY=your_api_key_here

# Steel
STEEL_API_KEY=your_api_key_here

# Scrapeless
SCRAPELESS_API_KEY=your_api_key_here
```

## Installation

Each client requires specific dependencies:

```bash
# Browserbase (Selenium)
pip install selenium python-dotenv

# Hyperbrowser (Playwright)
pip install playwright hyperbrowser python-dotenv
playwright install chromium

# Steel (Playwright)
pip install playwright steel-sdk python-dotenv
playwright install chromium
```

## Usage Examples

See the `samples/` directory for complete working examples of each client.

## Protocol Comparison

| Client | Protocol | Connection Type |
|--------|----------|----------------|
| Browserbase | Selenium WebDriver | HTTP REST API |
| Hyperbrowser | Playwright (CDP) | WebSocket |
| Steel | Playwright (CDP) | WebSocket |

## Troubleshooting

### Hyperbrowser Selenium Error
If you see `KeyError: 'value'` or "No selenium port available" with Hyperbrowser:
- ✅ Use `hyperbrowser_client.py` (Playwright implementation)
- See `HYPERBROWSER_SELENIUM_ISSUE.md` for details

### Connection Timeouts
- Increase timeout values in client initialization
- Check your API keys are valid
- Verify your network connection

### Import Errors
Make sure you've installed all required dependencies and activated your virtual environment.
