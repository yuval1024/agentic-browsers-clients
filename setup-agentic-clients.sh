#!/bin/bash

# set -e  # Exit on error

# Create logs directory if it doesn't exist
mkdir -p ~/logs

# Setup logging - capture both stdout and stderr
# exec - Replaces the current shell's file descriptors (doesn't spawn a new process)
LOG_FILE="~/logs/setup_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "Browser Automation Project Setup Script"
echo "Supports multiple browser automation services."
echo "Logging to: $LOG_FILE"
echo ""


echo "Creating virtual environment..."
uv venv
source .venv/bin/activate

echo "Setting PYTHONPATH to current directory..."
export PYTHONPATH="$PWD:$PYTHONPATH"

echo "Installing dependencies from requirements.txt..."
uv pip install -r requirements.txt

python samples/sample_quotes_scraper.py

PNG_COUNT=$(find outputs -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
JSON_COUNT=$(find outputs -name "*.json" 2>/dev/null | wc -l | tr -d ' ')
echo "$PNG_COUNT screenshot(s) ; $JSON_COUNT JSON file(s)"
find outputs -name "*.png" -exec basename {} \; | head -5 | sed 's/^/    • /'
find outputs -name "*.json" -exec basename {} \; | head -5 | sed 's/^/    • /'

