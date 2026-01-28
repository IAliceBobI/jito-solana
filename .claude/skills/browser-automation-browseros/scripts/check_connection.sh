#!/usr/bin/env bash
# Check BrowserOS MCP server connection

echo "Checking BrowserOS MCP server at http://127.0.0.1:9106/mcp..."

if curl -s http://127.0.0.1:9106/mcp > /dev/null 2>&1; then
    echo "✅ BrowserOS MCP server is running"
    echo ""
    echo "Testing MCP connection..."
    curl -s http://127.0.0.1:9106/mcp | head -20
    exit 0
else
    echo "❌ BrowserOS MCP server is not responding"
    echo ""
    echo "Troubleshooting:"
    echo "1. Ensure BrowserOS application is open"
    echo "2. Check BrowserOS MCP server is enabled"
    echo "3. Verify server is running on port 9106"
    echo ""
    echo "Start BrowserOS and enable MCP server in:"
    echo "Settings → BrowserOS as MCP"
    exit 1
fi
