# BrowserOS MCP Tools - Complete List

Complete reference for all 31 BrowserOS MCP tools available for browser automation.

## Navigation Tools

### browser_navigate
Navigate to a URL in the specified or current tab.

**Parameters**:
- `url` (required): The URL to navigate to
- `tabId` (optional): Tab ID to navigate in (defaults to active tab)

**Example**:
```bash
mcp__browser-mcp__browser_navigate?url=https://example.com
```

### browser_open_tab
Open a new browser tab with optional URL.

**Parameters**:
- `url` (optional): URL to open in new tab
- `active` (optional): Whether to make the new tab active (default: true)

**Example**:
```bash
mcp__browser-mcp__browser_open_tab?url=https://example.com
```

### browser_close_tab
Close a specific browser tab by ID.

**Parameters**:
- `tabId` (required): ID of the tab to close

**Example**:
```bash
mcp__browser-mcp__browser_close_tab?tabId=1697399534
```

---

## Tab Management Tools

### browser_switch_tab
Switch to (activate) a specific tab.

**Parameters**:
- `tabId` (required): ID of the tab to switch to
- `windowId` (optional): Window ID for routing

### browser_list_tabs
List all open browser tabs.

**Returns**: Array of tab information including IDs, URLs, titles

### browser_group_tabs
Group multiple tabs together.

**Parameters**:
- `tabIds` (required): Array of tab IDs to group
- `title` (optional): Title for the tab group
- `color` (optional): Color for the tab group

### browser_ungroup_tabs
Remove tabs from their groups.

**Parameters**:
- `tabIds` (required): Array of tab IDs to ungroup

### browser_get_active_tab
Get information about the currently active browser tab.

---

## Scrolling Tools

### browser_scroll_down
Scroll the page down by one viewport height.

**Parameters**:
- `tabId` (required): Tab ID to scroll

### browser_scroll_up
Scroll the page up by one viewport height.

**Parameters**:
- `tabId` (required): Tab ID to scroll

### browser_scroll_to_element
Scroll to bring an element into view.

**Parameters**:
- `nodeId` (required): Node ID of the element to scroll to
- `tabId` (required): Tab ID containing the element

---

## Interaction Tools

### browser_click_element
Click an element by its nodeId (from interactive elements snapshot).

**Parameters**:
- `tabId` (required): Tab containing the element
- `nodeId` (required): Node ID from get_interactive_elements
- `windowId` (optional): Window ID for routing

**Example**:
```bash
# First get elements to find nodeId
mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534

# Then click using nodeId
mcp__browser-mcp__browser_click_element?nodeId=15&tabId=1697399534
```

### browser_type_text
Type text into an input element.

**Parameters**:
- `nodeId` (required): Node ID of the input element
- `text` (required): Text to type into the element
- `tabId` (required): Tab ID containing the element

**Example**:
```bash
mcp__browser-mcp__browser_type_text?nodeId=15&text=user@example.com&tabId=1697399534
```

### browser_clear_input
Clear text from an input element.

**Parameters**:
- `nodeId` (required): Node ID of the input element
- `tabId` (required): Tab ID containing the element

### browser_send_keys
Send keyboard keys to the active tab.

**Parameters**:
- `tabId` (required): Tab ID to send keys to
- `key` (required): Key to send (Enter, Delete, Escape, Arrow keys, etc.)

**Available keys**: Enter, Delete, Backspace, Tab, Escape, ArrowUp, ArrowDown, ArrowLeft, ArrowRight, Home, End, PageUp, PageDown

---

## Content Extraction Tools

### browser_get_page_content
Extract text or text with links from the page.

**Parameters**:
- `tabId` (required): Tab ID to extract content from
- `type`: Content type - "text" or "text-with-links"
- `contextWindow`: Context size - "20k", "30k", "50k", "100k" (default: "20k")
- `options` (optional): Additional extraction options

**Example**:
```bash
# Get plain text
mcp__browser-mcp__browser_get_page_content?tabId=1697399534&type=text

# Get text with links preserved
mcp__browser-mcp__browser_get_page_content?tabId=1697399534&type=text-with-links

# Get with larger context
mcp__browser-mcp__browser_get_page_content?tabId=1697399534&type=text&contextWindow=50k
```

### browser_get_interactive_elements
Get a snapshot of all interactive elements on the page (buttons, links, inputs).

**Parameters**:
- `tabId` (required): Tab ID to snapshot
- `simplified` (optional): Use simplified format (default: false)

**Returns**: Detailed list of all clickable elements with nodeIds

**Example**:
```bash
mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534

# Simplified format
mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534&simplified=true
```

### browser_grep_interactive_elements
Search interactive elements using regex patterns (case insensitive).

**Parameters**:
- `tabId` (required): Tab ID to search
- `pattern` (required): Regex pattern to match (supports | for OR)
- `context` (optional): Number of elements to show before/after match (default: 2)
- `windowId` (optional): Window ID for routing

**Example**:
```bash
# Find all buttons
mcp__browser-mcp__browser_grep_interactive_elements?tabId=1697399534&pattern=button|submit

# Find login/submit elements
mcp__browser-mcp__browser_grep_interactive_elements?tabId=1697399534&pattern=login|signin|submit

# Find email inputs
mcp__browser-mcp__browser_grep_interactive_elements?tabId=1697399534&pattern=email
```

---

## Screenshot Tools

### browser_get_screenshot
Capture a screenshot of the page.

**Parameters**:
- `tabId` (required): Tab ID to capture
- `size` (optional): Size preset - "small", "medium", "large"
- `showHighlights` (optional): Show element highlights
- `width` (optional): Exact width in pixels (overrides size)
- `height` (optional): Exact height in pixels (overrides size)

**Example**:
```bash
# Medium screenshot
mcp__browser-mcp__browser_get_screenshot?tabId=1697399534&size=medium

# Custom size
mcp__browser-mcp__browser_get_screenshot?tabId=1697399534&width=1200&height=800

# With element highlights
mcp__browser-mcp__browser_get_screenshot?tabId=1697399534&showHighlights=true
```

### browser_get_screenshot_pointer
Capture a screenshot with a pointer overlay on a specific element.

**Parameters**:
- `tabId` (required): Tab ID to capture
- `nodeId` (required): Node ID to show pointer over
- `size` (optional): Size preset
- `pointerLabel` (optional): Label to show with pointer

**Example**:
```bash
mcp__browser-mcp__browser_get_screenshot_pointer?tabId=1697399534&nodeId=15&pointerLabel=Click
```

---

## Bookmarks Tools

### browser_get_bookmarks
Get all bookmarks from the browser.

**Parameters**:
- `folderId` (optional): Folder ID to get bookmarks from (omit for all)

### browser_create_bookmark
Create a new bookmark.

**Parameters**:
- `title` (required): Bookmark title
- `url` (required): Bookmark URL
- `parentId` (optional): Parent folder ID

### browser_remove_bookmark
Remove a bookmark by ID.

**Parameters**:
- `bookmarkId` (required): ID of the bookmark to remove

---

## History Tools

### browser_get_recent_history
Get most recent browser history items.

**Parameters**:
- `count` (optional): Number of recent items (default: 20)

### browser_search_history
Search browser history by text query.

**Parameters**:
- `query` (required): Search query
- `maxResults` (optional): Maximum results (default: 100)

---

## Window Management

### browser_create_window
Create a new browser window.

**Parameters**:
- `url` (optional): URL to open in the new window (defaults to about:blank)
- `incognito` (optional): Create an incognito window
- `focused` (optional): Whether to focus the new window (default: true)

### browser_close_window
Close a browser window by its windowId.

**Parameters**:
- `windowId` (required): ID of the window to close

---

## Load Status

### browser_get_load_status
Check if a page has finished loading.

**Parameters**:
- `tabId` (required): Tab ID to check

**Returns**: Load status details:
- `isDOMContentLoaded`: Boolean
- `isResourcesLoading`: Boolean
- `isPageComplete`: Boolean

**Example**:
```bash
mcp__browser-mcp__browser_get_load_status?tabId=1697399534

# Check if page is fully loaded before proceeding
if isPageComplete == true; then
  # Safe to interact
fi
```

---

## Quick Reference Cheatsheet

### Common Workflows

#### 1. Navigate and Extract
```bash
# Navigate
mcp__browser-mcp__browser_navigate?url=https://example.com
tabId=$(response.tabId)

# Wait for load
mcp__browser-mcp__browser_get_load_status?tabId=$tabId

# Extract content
mcp__browser-mcp__browser_get_page_content?tabId=$tabId
```

#### 2. Find and Click
```bash
# Get elements
mcp__browser-mcp__browser_get_interactive_elements?tabId=$tabId

# Find submit button using grep
mcp__browser-mcp__browser_grep_interactive_elements?tabId=$tabId&pattern=submit

# Click by nodeId
mcp__browser-mcp__browser_click_element?nodeId=<nodeId>&tabId=$tabId
```

#### 3. Fill Form
```bash
# Get elements to find input nodeIds
mcp__browser-mcp__browser_get_interactive_elements?tabId=$tabId

# Fill inputs
mcp__browser-mcp__browser_type_text?nodeId=12&text=user@example.com
mcp__browser-mcp__browser_type_text?nodeId=15&text=password123

# Submit
mcp__browser-mcp__browser_click_element?nodeId=20
```

#### 4. Search and Extract
```bash
# Navigate
mcp__browser-mcp__browser_navigate?url=https://example.com

# Get content
content=$(mcp__browser-mcp__browser_get_page_content?tabId=$tabId)

# Search for prices
mcp__browser-mcp__browser_grep_interactive_elements?tabId=$tabId&pattern=\$[\d,]+\.\d{2}
```

---

## Tool Parameters Quick Reference

| Tool | Required Params | Optional Params | Returns |
|------|----------------|-----------------|---------|
| browser_navigate | url | tabId | tabId, url |
| browser_open_tab | - | url, active | tabId |
| browser_close_tab | tabId | - | - |
| browser_switch_tab | tabId | windowId | - |
| browser_list_tabs | - | windowId | tabs array |
| browser_scroll_down | tabId | - | - |
| browser_scroll_up | tabId | - | - |
| browser_scroll_to_element | nodeId, tabId | - | - |
| browser_click_element | nodeId, tabId | windowId | - |
| browser_type_text | nodeId, text, tabId | - | - |
| browser_clear_input | nodeId, tabId | - | - |
| browser_send_keys | tabId, key | - | - |
| browser_get_page_content | tabId | type, contextWindow, options | content |
| browser_get_interactive_elements | tabId | simplified | elements array |
| browser_grep_interactive_elements | tabId, pattern | context | matches |
| browser_get_screenshot | tabId | size, showHighlights, width, height | - |
| browser_get_load_status | tabId | - | status object |
| browser_get_bookmarks | - | folderId | bookmarks array |
| browser_create_bookmark | title, url | parentId | - |
| browser_remove_bookmark | bookmarkId | - | - |
| browser_get_recent_history | - | count | history array |
| browser_search_history | query | maxResults | results |
| browser_create_window | - | url, incognito, focused | windowId, tabId |
| browser_close_window | windowId | - | - |

---

## Response Formats

### browser_get_interactive_elements Response

```json
{
  "content": "INTERACTIVE ELEMENTS (Snapshot ID: 17):",
  "elements": [
    {
      "nodeId": 1,
      "type": "C",
      "tag": "a",
      "name": "Gmail",
      "text": "Gmail ",
      "attributes": {
        "href": "https://mail.google.com/mail"
      }
    },
    {
      "nodeId": 12,
      "type": "T",
      "tag": "input",
      "placeholder": "Google",
      "attributes": {
        "type": "text"
      }
    }
  ]
}
```

**Legend**:
- `<C>` - Clickable element
- `<T>` - Typeable/input element
- `(hidden)` - Element is out of viewport
- Indentation shows DOM depth

---

## Best Practices

1. **Always get fresh snapshots** - Elements change after navigation
2. **Use nodeId not coordinates** - More reliable
3. **Check load_status** - Wait for page to fully load
4. **Use grep for finding** - Faster than manual scanning
5. **Screenshot on errors** - Helps debugging
6. **Re-verify after actions** - Confirm success
7. **Handle failures gracefully** - Retry, recover, report

---

## See Also

- [Advanced Patterns](./advanced-patterns.md) - Complex automation workflows
- [Error Handling Guide](./error-handling.md) - Troubleshooting
- [Workflow Integration](./workflow-integration.md) - BrowserOS visual workflows
