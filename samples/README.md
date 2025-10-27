# Sample Scripts

This directory contains 3 sample scripts demonstrating browser automation across multiple providers.

## 📁 Directory Contents

```
samples/
├── README.md                    # This file
├── sample_user_agent.py         # Basic navigation demo (Browserbase)
├── sample_quotes_scraper.py     # Web scraping demo (Browserbase)
└── sample_multi_provider.py     # Multi-provider comparison ⭐ NEW
```

## 🚀 Quick Start

Run samples from the project root:

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Set PYTHONPATH (required!)
export PYTHONPATH="$PWD:$PYTHONPATH"

# 3. Run a sample
python samples/sample_user_agent.py
```

## 📋 Sample Descriptions

### Sample 1: User Agent Detection (`sample_user_agent.py`)

Demonstrates basic browser automation with Browserbase.

**Status:** ✅ Working
**Client:** BrowserbaseClient (Selenium WebDriver)
**Service:** Browserbase

```bash
python samples/sample_user_agent.py
```

**What it does:**
- Creates a Browserbase session
- Navigates to gs.statcounter.com/detect
- Extracts user agent information from page
- Executes JavaScript to get browser details
- Takes a screenshot (saved to `outputs/`)
- Demonstrates element finding and text extraction

**Output:**
```
DETECTED USER AGENT:
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36

Screenshot saved to: outputs/user-agent-screenshot_<timestamp>.png
```

**Environment Variables Required:**
```bash
API_KEY_BROWSERBASE=your_api_key_here
PROJECT_ID_BROWSERBASE=your_project_id_here
```

---

### Sample 2: Quotes Scraper (`sample_quotes_scraper.py`)

Demonstrates web scraping with pagination and data extraction.

**Status:** ✅ Working
**Client:** BrowserbaseClient (Selenium WebDriver)
**Service:** Browserbase

```bash
python samples/sample_quotes_scraper.py
```

**What it does:**
- Scrapes quotes from quotes.toscrape.com
- Extracts quote text, author, and tags
- Handles pagination (scrapes 2 pages by default)
- Saves data to JSON file (timestamped in `outputs/`)
- Takes screenshot of last page
- Demonstrates element finding, clicking, and data extraction

**Output:**
```
SCRAPING SUMMARY
Total quotes scraped: 20
Pages scraped: 2
Unique authors: 12
Unique tags: 15

Quotes saved to: outputs/scraped-quotes_<timestamp>.json
Screenshot saved to: outputs/quotes-screenshot_<timestamp>.png
```

**Environment Variables Required:**
```bash
API_KEY_BROWSERBASE=your_api_key_here
PROJECT_ID_BROWSERBASE=your_project_id_here
```

**Optional Parameters:**
You can modify the script to scrape more pages:
```python
scrape_quotes(num_pages=5)  # Scrape 5 pages instead of 2
```

---

### Sample 3: Multi-Provider Comparison (`sample_multi_provider.py`) ⭐

**THE KEY SAMPLE** - Demonstrates running the same task across multiple providers.

**Status:** ✅ Working
**Clients:** Browserbase (Selenium), Hyperbrowser (Playwright), Steel (Playwright)
**Services:** All available providers

```bash
# Run with all configured providers
python samples/sample_multi_provider.py

# Or run with specific provider
python samples/sample_multi_provider.py browserbase
python samples/sample_multi_provider.py hyperbrowser
python samples/sample_multi_provider.py steel
```

**What it does:**
- Automatically detects available providers from .env
- Runs the SAME scraping task with each provider
- Shows how to write provider-agnostic code
- Compares results and performance across providers
- Demonstrates unified API working across protocols
- Saves combined comparison data to JSON

**Output:**
```
3 provider(s) available
✓ Browserbase available (Selenium)
✓ Hyperbrowser available (Playwright)
✓ Steel available (Playwright)

==========================================
Scraping with Browserbase (Selenium)
==========================================
Quote #1: "The world as we have created it..." - Albert Einstein
...

==========================================
COMPARISON SUMMARY
==========================================
Browserbase (Selenium): ✓ 5 quotes
Hyperbrowser (Playwright): ✓ 5 quotes
Steel (Playwright): ✓ 5 quotes

KEY INSIGHTS:
1. SAME CODE, DIFFERENT PROVIDERS
2. PROTOCOL DIFFERENCES handled automatically
3. EASY SWITCHING via environment variables
```

**Environment Variables (configure any/all):**
```bash
# Browserbase
API_KEY_BROWSERBASE=your_api_key_here
PROJECT_ID_BROWSERBASE=your_project_id_here

# Hyperbrowser
HYPERBROWSER_API_KEY=your_api_key_here

# Steel
STEEL_API_KEY=your_api_key_here
```

**Why This Sample Matters:**
- Shows the TRUE VALUE of this project: provider portability
- Demonstrates unified API across Selenium and Playwright
- Proves you can switch providers without rewriting code
- Useful for benchmarking providers
- Great for LLMs to understand the abstraction layer

## 🔑 Environment Setup

Before running samples, configure your `.env` file:

```bash
# Copy template
cp .env.example .env

# Edit .env and add your credentials
API_KEY_BROWSERBASE=your_actual_api_key
PROJECT_ID_BROWSERBASE=your_actual_project_id
```

Get your credentials from: https://www.browserbase.com/

## 🎯 Sample Comparison

| Feature | sample_user_agent.py | sample_quotes_scraper.py | sample_multi_provider.py |
|---------|---------------------|-------------------------|--------------------------|
| **Complexity** | Simple | Medium | Advanced |
| **Providers** | Browserbase only | Browserbase only | All 3 providers |
| **Protocols** | Selenium | Selenium | Selenium + Playwright |
| **Navigation** | Single page | Multi-page (pagination) | Single page (repeated 3x) |
| **Data Extraction** | User agent string | Structured data (quotes) | Quotes + comparison data |
| **Element Finding** | CSS selectors, By constants | Class names, CSS selectors | Unified abstraction |
| **Interaction** | None | Clicking next button | None |
| **Output** | Screenshot only | JSON + Screenshot | Multi-provider JSON + Screenshots |
| **Use Case** | Basic navigation test | Real-world scraping | Provider comparison & portability |
| **Key Learning** | How to use one client | How to scrape data | How to switch providers |

## 📚 Common API Patterns

Both samples demonstrate these patterns:

### 1. Client Initialization
```python
from clients.browserbase_client import BrowserbaseClient
import os
from dotenv import load_dotenv

load_dotenv()

client = BrowserbaseClient(
    api_key=os.getenv("API_KEY_BROWSERBASE"),
    project_id=os.getenv("PROJECT_ID_BROWSERBASE")
)
```

### 2. Context Manager Usage
```python
with client:
    # Session automatically started and cleaned up
    client.navigate("https://example.com")
    # ... your automation code
```

### 3. Element Finding
```python
# By CSS selector
element = client.find_element(By.CSS_SELECTOR, ".quote")

# By class name
element = client.find_element(By.CLASS_NAME, "text")

# Multiple elements
elements = client.find_elements(By.CLASS_NAME, "quote")
```

### 4. Data Extraction
```python
# Get text
text = element.text

# Get attribute
href = element.get_attribute("href")

# Execute JavaScript
result = client.execute_script("return navigator.userAgent;")
```

### 5. Screenshots
```python
# Auto-saves to outputs/ with timestamp
filepath = client.take_screenshot("description")
print(f"Screenshot saved to: {filepath}")
```

### 6. JSON Output
```python
from clients.utils import output_utils
import json

with open(output_utils.get_json_path("data"), "w") as f:
    json.dump(data, f, indent=2)
```

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'clients'

**Solution:** Set PYTHONPATH to project root
```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
```

Or run from project root:
```bash
cd /path/to/agentic-browsers-clients
python samples/sample_user_agent.py
```

### Missing API Credentials

**Error:**
```
Error: Missing API_KEY_BROWSERBASE or PROJECT_ID_BROWSERBASE
```

**Solution:** Create `.env` file with your credentials
```bash
cp .env.example .env
# Edit .env and add your actual API keys
```

### Import Error: browserbase package not found

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Screenshot/JSON files not found

**Check:** Files are saved to `outputs/` directory with timestamps:
```bash
ls -la outputs/
```

Files are named: `description_<epoch_milliseconds>.ext`

Example:
```
outputs/user-agent-screenshot_1730063245123.png
outputs/scraped-quotes_1730063245456.json
```

## 📖 Additional Resources

- **Project README** - Main documentation and setup guide
- **clients/README.md** - Detailed client API reference
- **.env.example** - Environment variables template
- **Browserbase Docs** - https://docs.browserbase.com/

## 🎓 Learning Path

**For beginners:**
1. Start with `sample_user_agent.py` - Learn basic navigation
2. Move to `sample_quotes_scraper.py` - Learn data extraction

**Key concepts to understand:**
1. Context managers (`with client:`)
2. Element finding (CSS selectors, By constants)
3. Waiting for elements (avoid `time.sleep()`)
4. Data extraction (`.text`, `.get_attribute()`)
5. Output management (timestamped files in `outputs/`)

## 🔍 Sample Output Examples

### User Agent Sample Output
```
==========================================
User Agent Detection Demo
==========================================

Page Title: Detect
Current URL: https://gs.statcounter.com/detect

==========================================
DETECTED USER AGENT:
==========================================
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...
==========================================

Screenshot saved to: outputs/user-agent-screenshot_1730063245123.png

Demo completed successfully!
```

### Quotes Scraper Output
```
==========================================
Quotes Scraper Demo
==========================================

Scraping page 1...
Found 10 quotes on this page

Quote #1:
  Text: "The world as we have created it..."
  Author: Albert Einstein
  Tags: change, deep-thoughts, thinking

[... more quotes ...]

==========================================
SCRAPING SUMMARY
==========================================
Total quotes scraped: 20
Pages scraped: 2
Unique authors: 12
Authors: Albert Einstein, J.K. Rowling, ...

Quotes saved to: outputs/scraped-quotes_1730063245456.json
Screenshot saved to: outputs/quotes-screenshot_1730063245789.png

Demo completed successfully!
```

---

**Ready to automate? Start with `sample_user_agent.py`!**
