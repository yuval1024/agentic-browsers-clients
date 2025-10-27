# Agentic Browser Automation Examples - sample clients code to use with your LLMs

Working code examples built for POC with different providers - demonstrating browser automation across multiple cloud platforms (Browserbase, Hyperbrowser, Steel, Skyvern) using both Selenium WebDriver and Playwright protocols.

## About This Project

These examples exist to give LLMs like Claude working context for browser automation tasks. When a human asks Claude to perform web scraping or browser automation, Claude can reference these examples to understand the exact imports, API patterns, and provider-specific constraints (like Hyperbrowser not supporting Selenium). This enables Claude to write correct code on the first try, perform WebFetch operations to read current documentation, and run advanced tests with real browser sessions when given appropriate credentials.

---

## 🤖 FOR LLMs: Quick Integration Guide

### Environment Setup

**1. File to Update: `.env` (NOT `.env.example`)**

Create or update `.env` in the project root with these exact variable names:

```bash
# Browserbase - Selenium WebDriver
API_KEY_BROWSERBASE=your_browserbase_api_key
PROJECT_ID_BROWSERBASE=your_browserbase_project_id

# Hyperbrowser - Playwright only (Selenium NOT supported!)
HYPERBROWSER_API_KEY=your_hyperbrowser_api_key

# Steel - Playwright
STEEL_API_KEY=your_steel_api_key

# Skyvern - AI-powered automation
SKYVERN_API_KEY=your_skyvern_api_key
```

**2. Installation Commands**

```bash
# Option 1: Using uv (recommended, faster)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Option 2: Using pip
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Required for Playwright-based clients (Hyperbrowser, Steel)
playwright install chromium
```

**3. Set PYTHONPATH (Required for imports to work)**

```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
```

Or add to your shell profile (~/.bashrc, ~/.zshrc):
```bash
export PYTHONPATH="/path/to/agentic-browsers-clients:$PYTHONPATH"
```

**4. Quick Test**

```bash
# Test Browserbase (Selenium)
python samples/sample_user_agent.py

# Test multiple providers (Browserbase, Hyperbrowser, Steel)
python samples/sample_multi_provider.py
```

### Basic Usage Pattern

```python
from clients import BrowserbaseClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = BrowserbaseClient(
    api_key=os.getenv("API_KEY_BROWSERBASE"),
    project_id=os.getenv("PROJECT_ID_BROWSERBASE")
)

# Always use context manager for cleanup
with client:
    client.navigate("https://example.com")
    title = client.get_title()
    client.take_screenshot("example")  # Auto-saves to outputs/example_<timestamp>.png
```

### Critical Notes for LLMs

1. **Hyperbrowser ONLY supports Playwright** - Do NOT use `HyperbrowserClient`, use `HyperbrowserPlaywrightClient`
2. **Screenshots**: `take_screenshot(name)` auto-saves to `outputs/name_<epoch_ms>.png` - returns filepath
3. **JSON output**: Use `from clients.utils import output_utils` then `output_utils.get_json_path(name)`
4. **Imports**: Always use `from clients.module_name import ClassName` format
5. **PYTHONPATH**: Must be set or imports will fail with `ModuleNotFoundError`
6. **Context managers**: Always use `with client:` to ensure session cleanup

### Available Clients & Protocol Matrix

| Client | Import | Protocol | Status |
|--------|--------|----------|--------|
| Browserbase | `from clients.browserbase_client import BrowserbaseClient` | Selenium | ✅ Working |
| Hyperbrowser | `from clients.hyperbrowser_client import HyperbrowserPlaywrightClient` | Playwright | ✅ Working |
| Steel | `from clients.steel_client import SteelClient` | Playwright | ✅ Working |
| Skyvern | `from clients.skyvern_client import SkyvernClient` | AI-powered | ⚠️ Requires Local Setup |

### Common API Methods (All Clients)

```python
# Navigation
client.navigate(url: str)
client.get_current_url() -> str
client.get_title() -> str

# Elements (use CSS selectors or By constants for Selenium)
client.find_element(selector) -> Element
client.find_elements(selector) -> List[Element]
client.wait_for_element(selector, timeout=10)

# Interaction
client.click_element(selector)
client.type_text(selector, text: str)

# Data Extraction
client.get_page_source() -> str
client.get_element_text(selector) -> str
client.get_element_attribute(selector, attribute: str) -> str

# Execution
client.execute_script(js_code: str) -> Any
client.take_screenshot(name: str) -> str  # Returns filepath
```

### Error Handling

All clients raise `ImportError` with installation instructions if dependencies are missing:

```python
try:
    from clients.browserbase_client import BrowserbaseClient
except ImportError as e:
    print(e)  # Shows: "Install with: pip install browserbase"
```

---

## 📁 Project Structure

```
agentic-browsers-clients/
├── clients/                    # Browser automation clients
│   ├── browserbase_client.py          # Browserbase (Selenium) ✅
│   ├── hyperbrowser_client.py   # Hyperbrowser (Playwright) ✅
│   ├── steel_client.py                # Steel (Playwright) ✅
│   ├── skyvern_client.py              # Skyvern (AI-powered) ⚠️
│   ├── output_utils.py                # File output utilities
│   └── README.md
│
├── samples/                    # Example scripts
│   ├── sample_user_agent.py           # Basic navigation demo
│   ├── sample_quotes_scraper.py       # Web scraping demo
│   └── sample_multi_provider.py       # Multi-provider comparison ⭐
│
├── scripts/                    # Utility scripts
│   ├── create_env_example.py          # Generate .env.example
│   ├── fix_sample_imports.py          # Update imports
│   └── update_samples_for_outputs.py  # Migrate to outputs folder
│
├── outputs/                    # Generated files (gitignored)
│   ├── *.png                   # Screenshots (timestamped)
│   └── *.json                  # Scraped data (timestamped)
│
├── memory-bank/               # Project documentation (gitignored)
├── .env                       # Your credentials (NOT in git)
├── .env.example              # Template
├── requirements.txt          # Dependencies
└── setup_browserbase_proj.sh # Automated setup script
```

## 🚀 Quick Start

### One-Command Setup (Automated)

```bash
# 1. Copy and edit credentials
cp .env.example .env
# Edit .env with your API keys

# 2. Run setup script (installs everything, runs samples)
./setup_browserbase_proj.sh
```

The script will:
- Install uv package manager (if needed)
- Create virtual environment
- Install all dependencies
- Set PYTHONPATH
- Run sample scripts
- Save all logs to `logs/setup_<timestamp>.log`

### Manual Setup

```bash
# 1. Create virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 3. Configure credentials
cp .env.example .env
# Edit .env with your API keys

# 4. Set PYTHONPATH
export PYTHONPATH="$PWD:$PYTHONPATH"

# 5. Run a sample
python samples/sample_user_agent.py
```

## 📖 Sample Scripts

### Sample 1: User Agent Detection (`samples/sample_user_agent.py`)

Demonstrates basic browser automation:
- Navigate to user agent detection site
- Extract page information
- Execute JavaScript
- Take screenshot

```bash
python samples/sample_user_agent.py
```

### Sample 2: Quotes Scraper (`samples/sample_quotes_scraper.py`)

Demonstrates web scraping:
- Navigate multiple pages
- Extract structured data (quotes, authors, tags)
- Save to JSON file
- Click pagination links

```bash
python samples/sample_quotes_scraper.py
```

### Sample 3: Multi-Provider Comparison (`samples/sample_multi_provider.py`) ⭐

**THE KEY SAMPLE** - Runs the same task across all configured providers:
- Automatically detects available providers (Browserbase, Hyperbrowser, Steel)
- Runs identical scraping task with each
- Demonstrates provider portability
- Compares results across Selenium and Playwright protocols
- Shows unified API in action

```bash
# Run with all available providers
python samples/sample_multi_provider.py

# Or specify a single provider
python samples/sample_multi_provider.py browserbase
python samples/sample_multi_provider.py hyperbrowser
python samples/sample_multi_provider.py steel
```

**Why this matters:** This sample demonstrates the core value - writing code once and running it across multiple providers without changes.

## 🔧 Utility Scripts

```bash
# Generate .env.example from your .env (removes sensitive values)
python scripts/create_env_example.py

# Fix imports after moving files
python scripts/fix_sample_imports.py

# Update samples to use outputs folder
python scripts/update_samples_for_outputs.py
```

## 📚 Service Documentation

### Browserbase
- **Protocol**: Selenium WebDriver (HTTP REST)
- **Docs**: https://docs.browserbase.com/
- **Dashboard**: https://www.browserbase.com/
- **Use Case**: Traditional web automation, mature tooling

### Hyperbrowser
- **Protocol**: Playwright/CDP (WebSocket) - **NO Selenium support!**
- **Docs**: https://docs.hyperbrowser.ai/
- **Dashboard**: https://hyperbrowser.ai/
- **Use Case**: Modern web apps, faster execution

### Steel
- **Protocol**: Playwright/CDP (WebSocket)
- **Docs**: https://docs.steel.dev/
- **Use Case**: Production browser automation

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'clients'

**Fix**: Set PYTHONPATH to project root
```bash
export PYTHONPATH="$PWD:$PYTHONPATH"
```

### Missing playwright browsers

**Fix**: Install Chromium
```bash
playwright install chromium
```

### Import errors for specific clients

Each client has descriptive error messages:
```python
try:
    from clients.steel_client import SteelClient
except ImportError as e:
    print(e)  # "Install with: pip install steel-sdk"
```

## 📦 Requirements

Core dependencies:
```
browserbase>=0.3.0
hyperbrowser>=0.1.0
playwright>=1.40.0
selenium>=4.0.0
python-dotenv>=1.0.0
steel-sdk>=0.1.0
```

See `requirements.txt` for full list.

## 🎯 Best Practices

1. **Always use context managers** (`with client:`) for automatic cleanup
2. **Use proper waits** - `wait_for_element()` instead of `time.sleep()`
3. **Handle exceptions** - Wrap automation code in try-except
4. **Close sessions** - Avoid quota limits
5. **Choose right protocol**:
   - Selenium: Traditional automation, wider compatibility
   - Playwright: Modern apps, better performance, anti-detection
6. **Output management** - Use `output_utils` for timestamped files
7. **Environment variables** - Never hardcode credentials

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT

---

**Built for scalable web automation across multiple cloud browser platforms**
