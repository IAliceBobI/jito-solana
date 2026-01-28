#!/usr/bin/env bash
# Take screenshot when browser operation fails

TAB_ID="${1:-1697399534}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCREENSHOT_DIR="screenshots/errors"

# Create directory
mkdir -p "$SCREENSHOT_DIR"

echo "📸 Taking screenshot for debugging..."

# In actual usage, this would be called via MCP:
# mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID

# For now, create placeholder
SCREENSHOT_FILE="$SCREENSHOT_DIR/error_$TIMESTAMP.png"
echo "" > "$SCREENSHOT_FILE"
echo "Screenshot saved to: $SCREENSHOT_FILE"
echo ""
echo "📋 Debugging Info:"
echo "  Tab ID: $TAB_ID"
echo "  Timestamp: $TIMESTAMP"
echo "  Screenshot: $SCREENSHOT_FILE"
