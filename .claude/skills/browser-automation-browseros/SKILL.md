---
name: browser-automation-browseros
version: "1.0.0"
description: |
  Advanced browser automation using BrowserOS HTTP MCP interface. Automate form
  filling, data extraction, multi-step workflows, and scheduled tasks with 31 MCP
  tools. Use when automating repetitive browser tasks, scraping authenticated pages,
  testing web applications, or monitoring websites for changes. Optimized for BrowserOS
  with local model support, visual workflows, and privacy-first design.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
hooks:
  PreToolUse:
    - matcher: "mcp__browser-mcp__browser.*"
      hooks:
        - type: prompt
          prompt: |
            Before browser operation:
            1. Verify page is loaded (check load_status)
            2. Fetch interactive elements if needed
            3. Plan the interaction sequence (find target nodeId)
            4. Consider error scenarios (popups, delays, iframes)
            Return 'approve' with execution plan or 'deny' with concerns.
  PostToolUse:
    - matcher: "mcp__browser-mcp__browser_click_element|mcp__browser-mcp__browser_type_text|mcp__browser-mcp__browser_navigate"
      hooks:
        - type: prompt
          prompt: |
            After browser interaction:
            1. Check if action succeeded (any errors?)
            2. Decide if re-fetching interactive elements is needed
            3. Consider if next action should wait for page load
            4. Report status: 'continue', 'retry', or 'manual-intervention'
          timeout: 15
---

# Browser Automation for BrowserOS

## Purpose

Automate browser tasks using BrowserOS HTTP MCP interface with 31 powerful tools for navigation, interaction, content extraction, and automation. Leverage your existing BrowserOS session with logged-in accounts, cookies, and browser history.

## When to Use

Use this skill when:
- **Automating repetitive browser tasks** - Daily data entry, status checks, form submissions
- **Extracting data from authenticated pages** - LinkedIn profiles, email content, dashboards
- **Testing web applications** - User flows, form validation, UI testing
- **Filling forms with data** - Batch data entry, multi-page forms, automated sign-ups
- **Scheduling periodic browser checks** - Price monitoring, content updates, status polling
- **Monitoring websites for changes** - Product availability, news updates, page changes

## When NOT to Use

Do NOT use for:
- **Simple one-time page loads** - Use browser tools directly without this skill
- **Tasks requiring Playwright's advanced features** - Use `playwright-skill` instead
- **Cross-browser testing** - BrowserOS is Chromium-based only
- **Headless browser operation** - BrowserOS requires visible browser window

## Quick Start

### Prerequisites

1. **BrowserOS running**: Ensure BrowserOS application is open
2. **MCP configured**: BrowserOS MCP server at `http://127.0.0.1:9106/mcp`
3. **Check connection**:
   ```bash
   curl http://127.0.0.1:9106/mcp
   ```

### Basic Automation Pattern

The **stable browser automation pattern**:

```
1. Navigate → 2. Verify Load → 3. Get Elements → 4. Interact → 5. Confirm
```

**Example workflow**:
```bash
# 1. Navigate
mcp__browser-mcp__browser_navigate?url=https://example.com

# 2. Wait for page load
mcp__browser-mcp__browser_get_load_status?tabId=<from_navigation>

# 3. Get interactive elements
mcp__browser-mcp__browser_get_interactive_elements?tabId=<id>

# 4. Click element (using nodeId from step 3)
mcp__browser-mcp__browser_click_element?nodeId=<nodeId>&tabId=<id>

# 5. Verify result (re-fetch elements if needed)
mcp__browser-mcp__browser_get_interactive_elements?tabId=<id>
```

## The Core Pattern

```
Stable Browser Automation = Verify → Act → Confirm → Repeat

1. **Verify** - Always check load_status before interacting
2. **Act** - Use precise nodeId (not coordinates)
3. **Confirm** - Re-fetch elements to verify action succeeded
4. **Repeat** - Continue pattern for multi-step workflows
```

**Why this matters**:
- **Dynamic pages** - Content may load asynchronously
- **Interactive elements** - May change after navigation
- **Errors happen** - Popups, delays, network issues
- **Reliability** - Pattern works consistently across sites

## Available BrowserOS MCP Tools

### Navigation (3 tools)
- `browser_navigate` - Open URL
- `browser_open_tab` - Open new tab
- `browser_close_tab` - Close tab

### Tab Management (6 tools)
- `browser_switch_tab` - Switch to tab
- `browser_list_tabs` - List all tabs
- `browser_group_tabs` - Group tabs
- `browser_ungroup_tabs` - Ungroup tabs
- `browser_get_active_tab` - Get active tab
- `browser_create_window` - Create new window

### Scrolling (3 tools)
- `browser_scroll_down` - Scroll down one viewport
- `browser_scroll_up` - Scroll up one viewport
- `browser_scroll_to_element` - Scroll element into view

### Interaction (4 tools)
- `browser_click_element` - Click element by nodeId
- `browser_type_text` - Type text into input
- `browser_clear_input` - Clear input field
- `browser_send_keys` - Send keyboard keys

### Content Extraction (3 tools)
- `browser_get_page_content` - Get page text/links
- `browser_get_interactive_elements` - Get all clickable elements
- `browser_grep_interactive_elements` - Search elements by regex

### Screenshots (2 tools)
- `browser_get_screenshot` - Capture page screenshot
- `browser_get_screenshot_pointer` - Screenshot with pointer overlay

### Data Management (10 tools)
- `browser_get_bookmarks` - List bookmarks
- `browser_create_bookmark` - Create bookmark
- `browser_remove_bookmark` - Remove bookmark
- `browser_get_recent_history` - Recent history
- `browser_search_history` - Search history
- And more...

**Total: 31 tools** - Most comprehensive browser automation interface!

## Workflow Patterns

### Pattern 1: Simple Page Navigation

```markdown
**Goal**: Navigate to a page and verify it loaded

**Steps**:
1. Navigate to URL
   ```
   mcp__browser-mcp__browser_navigate?url=https://example.com
   ```

2. Wait for page load
   ```
   mcp__browser-mcp__browser_get_load_status?tabId=<from_step1>
   ```
   Verify: `isPageComplete == true`

3. Get page content (optional)
   ```
   mcp__browser-mcp__browser_get_page_content?tabId=<id>&type=text
   ```

**Success criteria**: Page loaded without errors, content visible
```

### Pattern 2: Form Automation

```markdown
**Goal**: Fill and submit a form

**Steps**:
1. Navigate to form URL
   ```
   mcp__browser-mcp__browser_navigate?url=https://example.com/form
   ```

2. Wait for load
   ```
   mcp__browser-mcp__browser_get_load_status?tabId=<id>
   ```

3. Get interactive elements
   ```
   mcp__browser-mcp__browser_get_interactive_elements?tabId=<id>&simplified=true
   ```

4. Fill form fields:
   - Find input nodeId for username (e.g., 15)
     ```
     mcp__browser-mcp__browser_type_text?nodeId=15&text=user@example.com
     ```
   - Find input nodeId for password (e.g., 18)
     ```
     mcp__browser-mcp__browser_type_text?nodeId=18&text=secret123
     ```

5. Find and click submit button (nodeId: 22)
   ```
   mcp__browser-mcp__browser_click_element?nodeId=22&tabId=<id>
   ```

6. Wait for confirmation
   ```
   mcp__browser-mcp__browser_get_load_status?tabId=<id>
   ```

7. Verify success
   ```
   mcp__browser-mcp__browser_get_page_content?tabId=<id>
   ```

**Success criteria**: Form submitted, confirmation visible
```

### Pattern 3: Data Extraction

```markdown
**Goal**: Extract structured data from a page

**Steps**:
1. Navigate to target page
   ```
   mcp__browser-mcp__browser_navigate?url=https://example.com/data
   ```

2. Wait for dynamic content
   ```
   mcp__browser-mcp__browser_get_load_status?tabId=<id>
   ```

3. Get page content
   ```
   mcp__browser-mcp__browser_get_page_content?tabId=<id>&type=text-with-links
   ```

4. Extract specific data (option A - full content)
   - Use Grep tool to search for patterns:
     ```
     mcp__browser-mcp__browser_grep_interactive_elements?tabId=<id>&pattern=price.*\$\d+
     ```

5. Extract specific data (option B - parse locally)
   - Save content to file using Write tool
   - Parse and extract data using Bash scripts

6. Handle pagination (if applicable)
   - Find "Next" button
   - Click and repeat extraction
   - Stop when no more pages

**Success criteria**: All data extracted, saved to file (CSV/JSON)
```

### Pattern 4: Multi-Step Workflow

```markdown
**Goal**: Complete a complex multi-step task

**Steps**:
1. **Login** (if needed)
   a. Navigate to login page
   b. Fill credentials
   c. Click login button
   d. Wait for redirect (check URL change)

2. **Navigate to target page**
   a. Use menu or direct URL
   b. Wait for load

3. **Perform main task**
   a. Extract data / Fill form / Interact
   b. Wait for results

4. **Cleanup** (if needed)
   a. Logout
   b. Close tab
   c. Return to home

**Success criteria**: Task completed, session cleaned up
```

### Pattern 5: Batch Processing

```markdown
**Goal**: Process multiple items (e.g., multiple URLs, data rows)

**Approach**: Parallel processing with BrowserOS tab groups

**Steps**:
1. **Open multiple tabs** (in parallel)
   ```
   mcp__browser-mcp__browser_open_tab?url=https://example.com/item1
   mcp__browser-mcp__browser_open_tab?url=https://example.com/item2
   mcp__browser-mcp__browser_open_tab?url=https://example.com/item3
   ```

2. **Process each tab**:
   For each tab:
   a. Switch to tab
      ```
      mcp__browser-mcp__browser_switch_tab?tabId=<id>
      ```
   b. Extract/fill data
   c. Move to next

3. **Group tabs for organization**
   ```
   mcp__browser-mcp__browser_group_tabs?tabIds=<id1>,<id2>,<id3>&title=Batch-1
   ```

**Success criteria**: All items processed, results consolidated
```

## Best Practices

### ✅ DO

- **Always verify load_status** before interacting
  ```
  mcp__browser-mcp__browser_get_load_status?tabId=1697399534
  ```
  Check: `isPageComplete == true`

- **Re-fetch elements** after navigation or actions
  ```
  mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534
  ```
  Elements may have changed - get fresh snapshot

- **Use nodeId** not coordinates for clicks
  ```
  mcp__browser-mcp__browser_click_element?nodeId=15
  ```
  Coordinates are fragile and break with responsive layouts

- **Screenshot** for debugging and evidence
  ```
  mcp__browser-mcp__browser_get_screenshot?tabId=1697399534
  ```

- **Wait** between actions if page is slow
  ```
  # Add small delay if needed
  # BrowserOS handles this well, but some sites need extra time
  ```

- **Handle errors** gracefully
  - Check for popups, alerts, modals
  - Handle expired sessions
  - Retry failed actions

- **Use grep** for finding elements
  ```
  mcp__browser-mcp__browser_grep_interactive_elements?tabId=1697399534&pattern=submit|login|button
  ```
  Faster than manually scanning all elements

### ❌ DON'T

- **Don't skip load_status** check
  ```
  # ❌ WRONG
  mcp__browser-mcp__browser_click_element?nodeId=15  # May fail if page not loaded

  # ✅ RIGHT
  mcp__browser-mcp__browser_get_load_status?tabId=1697399534
  mcp__browser-mcp__browser_click_element?nodeId=15
  ```

- **Don't assume elements exist** without fetching
  ```
  # ❌ WRONG
  mcp__browser-mcp__browser_click_element?nodeId=100  # nodeId may not exist

  # ✅ RIGHT
  mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534
  # Find correct nodeId from output
  mcp__browser-mcp__browser_click_element?nodeId=<actual_id>
  ```

- **Don't click coordinates** (fragile)
  ```
  # ❌ WRONG
  mcp__browser-mcp__browser_click_coordinates?x=500&y=300

  # ✅ RIGHT
  mcp__browser-mcp__browser_click_element?nodeId=15
  ```

- **Don't rush** - some pages need time
  ```
  # ❌ WRONG
  # Immediately click after navigate
  mcp__browser-mcp__browser_click_element?nodeId=15

  # ✅ RIGHT
  # Verify page is ready first
  mcp__browser-mcp__browser_get_load_status?tabId=1697399534
  mcp__browser-mcp__browser_click_element?nodeId=15
  ```

- **Don't forget to re-verify** after actions
  ```
  # After clicking, check if something changed
  mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534
  ```

## Common Troubleshooting

### Issue 1: Element Not Found

**Symptom**: `nodeId not found` or element doesn't exist

**Diagnosis**:
```bash
# 1. Re-fetch elements
mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534

# 2. Check if page fully loaded
mcp__browser-mcp__browser_get_load_status?tabId=1697399534

# 3. Look for iframe
# Elements inside iframe need special handling

# 4. Wait for dynamic content
# Some sites load content via JavaScript after initial load
```

**Solutions**:
- Re-fetch interactive elements
- Wait for dynamic content to load
- Check for iframes (need to switch context)
- Use grep to find element by text/attributes

### Issue 2: Click Not Working

**Symptom**: Click doesn't trigger action

**Diagnosis**:
```bash
# 1. Check if element is visible
mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534

# 2. Check for overlays/modals blocking
# Take screenshot to see current state

# 3. Verify element is clickable
# Check element type: should be <button>, <a>, or <input>
```

**Solutions**:
- Scroll element into view first
  ```
  mcp__browser-mcp__browser_scroll_to_element?nodeId=15
  ```
- Check for overlay/modals blocking
- Try alternative interaction method
- Wait for animations to complete

### Issue 3: Session Expired

**Symptom**: Redirected to login page unexpectedly

**Diagnosis**:
```bash
# Check current URL
mcp__browser-mcp__browser_get_page_content?tabId=1697399534&type=text-with-links
```

**Solutions**:
- Detect login page (check for "login", "sign in" in content)
- Re-authenticate automatically
  ```
  # Navigate to login
  mcp__browser-mcp__browser_navigate?url=https://example.com/login

  # Fill credentials
  mcp__browser-mcp__browser_type_text?nodeId=15&text=user@example.com
  mcp__browser-mcp__browser_type_text?nodeId=18&text=password

  # Submit
  mcp__browser-mcp__browser_click_element?nodeId=22
  ```
- Resume workflow after login

### Issue 4: Page Not Loading Completely

**Symptom**: `isPageComplete == false` for long time

**Diagnosis**:
```bash
# Check load status details
mcp__browser-mcp__browser_get_load_status?tabId=1697399534

# Screenshot to see current state
mcp__browser-mcp__browser_get_screenshot?tabId=1697399534
```

**Solutions**:
- Wait longer (some pages are slow)
- Check for errors in console
- Reload page
  ```
  mcp__browser-mcp__browser_navigate?url=<current_url>
  ```
- Try alternative URL

## Examples

### Example 1: Automated Login

```markdown
**Goal**: Login to a website with saved credentials

**Steps**:

1. Navigate to login page
   ```bash
   mcp__browser-mcp__browser_navigate?url=https://example.com/login
   tabId=1697399534
   ```

2. Wait for page load
   ```bash
   mcp__browser-mcp__browser_get_load_status?tabId=1697399534
   # Verify: isPageComplete == true
   ```

3. Get interactive elements
   ```bash
   mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534
   # Look for username input (nodeId: 12)
   # Look for password input (nodeId: 15)
   # Look for login button (nodeId: 20)
   ```

4. Fill credentials
   ```bash
   # Username
   mcp__browser-mcp__browser_type_text?nodeId=12&text=user@example.com&tabId=1697399534

   # Password
   mcp__browser-mcp__browser_type_text?nodeId=15&text=secret123&tabId=1697399534
   ```

5. Click login
   ```bash
   mcp__browser-mcp__browser_click_element?nodeId=20&tabId=1697399534&windowId=1697399500
   ```

6. Wait for redirect
   ```bash
   mcp__browser-mcp__browser_get_load_status?tabId=1697399534
   # Should be on dashboard now
   ```

**Success**: Logged in, dashboard visible
```

### Example 2: Extract Product Prices

```markdown
**Goal**: Scrape product prices from an e-commerce site

**Steps**:

1. Navigate to product page
   ```bash
   mcp__browser-mcp__browser_navigate?url=https://shop.example.com/product/123
   tabId=1697399534
   ```

2. Wait for content to load
   ```bash
   mcp__browser-mcp__browser_get_load_status?tabId=1697399534
   ```

3. Get page content
   ```bash
   mcp__browser-mcp__browser_get_page_content?tabId=1697399534&type=text
   ```

4. Search for price pattern
   ```bash
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=1697399534&pattern=\$[\d,]+\.\d{2}
   ```

5. Extract product info
   - Product title
   - Price
   - Availability
   - Reviews count

6. Save to CSV
   ```bash
   # Use Write tool to save extracted data
   ```

**Success**: Price data extracted and saved
```

### Example 3: Fill Multi-Page Form

```markdown
**Goal**: Fill out a 3-page registration form

**Page 1 - Personal Info**:
```bash
# Navigate
mcp__browser-mcp__browser_navigate?url=https://example.com/register

# Wait
mcp__browser-mcp__browser_get_load_status?tabId=1697399534

# Get elements
mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534

# Fill fields
mcp__browser-mcp__browser_type_text?nodeId=12&text=John
mcp__browser-mcp__browser_type_text?nodeId=15&text=Doe
mcp__browser-mcp__browser_type_text?nodeId=18&text=john@example.com

# Click Next
mcp__browser-mcp__browser_click_element?nodeId=25
```

**Page 2 - Address**:
```bash
# Wait for next page load
mcp__browser-mcp__browser_get_load_status?tabId=1697399534

# Get elements
mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534

# Fill address
mcp__browser-mcp__browser_type_text?nodeId=30&text=123 Main St
mcp__browser-mcp__browser_type_text?nodeId=33&text=Anytown
mcp__browser-mcp__browser_type_text?nodeId=36&text=12345

# Click Next
mcp__browser-mcp__browser_click_element?nodeId=40
```

**Page 3 - Review**:
```bash
# Wait
mcp__browser-mcp__browser_get_load_status?tabId=1697399534

# Review entered data
mcp__browser-mcp__browser_get_page_content?tabId=1697399534

# Submit
mcp__browser-mcp__browser_click_element?nodeId=50
```

**Success**: All pages filled, form submitted
```

## Advanced Automation

### Scheduled Tasks

BrowserOS supports **visual workflows** for scheduled automation. Combine with this skill:

```markdown
**Scheduled Task Examples**:

1. **Daily Price Check**
   - Time: 9:00 AM daily
   - Action: Navigate to product page, extract price, log to file
   - Trigger: BrowserOS Workflow → Schedule

2. **Hourly Status Check**
   - Time: Every hour
   - Action: Check service status page, alert if down
   - Trigger: BrowserOS Workflow + this skill

3. **Weekly Report**
   - Time: Friday 5:00 PM
   - Action: Aggregate weekly data, generate report
   - Trigger: BrowserOS Workflow + extract data
```

### Parallel Operations

BrowserOS can handle multiple tabs efficiently:

```bash
# Open multiple tabs in parallel
mcp__browser-mcp__browser_open_tab?url=https://example.com/page1
mcp__browser-mcp__browser_open_tab?url=https://example.com/page2
mcp__browser-mcp__browser_open_tab?url=https://example.com/page3

# Process each tab
for tab in page1 page2 page3; do
  mcp__browser-mcp__browser_switch_tab?tabId=$tab
  # Extract data from each tab
  mcp__browser-mcp__browser_get_page_content?tabId=$tab
done
```

### Error Recovery

```markdown
**Automatic Retry Logic**:

1. **If action fails**:
   - Re-fetch interactive elements
   - Check if element still exists
   - Verify page state with screenshot
   - Retry action (max 3 times)

2. **If still failing**:
   - Take screenshot for debugging
   - Log error details
   - Ask user for manual intervention

3. **Common recoverable errors**:
   - Network timeout → Wait and retry
   - Element not visible → Scroll into view
   - Page still loading → Wait for completion
   - Session expired → Re-authenticate
```

## Output Formats

### Extraction Results (CSV)

```csv
product_name,price,availability,timestamp
Product A,$29.99,In Stock,2026-01-25T10:30:00Z
Product B,$49.99,Out of Stock,2026-01-25T10:30:15Z
```

### Extraction Results (JSON)

```json
{
  "timestamp": "2026-01-25T10:30:00Z",
  "source_url": "https://example.com/product/123",
  "data": {
    "title": "Product A",
    "price": "$29.99",
    "availability": "In Stock"
  }
}
```

### Execution Log

```markdown
# Browser Automation Execution Log

## Task: Extract Product Prices

**Started**: 2026-01-25T10:30:00Z
**Completed**: 2026-01-25T10:35:00Z

### Steps
1. ✅ Navigate to product page (10:30:05)
2. ✅ Wait for page load (10:30:07)
3. ✅ Extract product data (10:30:15)
4. ✅ Save to CSV (10:30:20)
5. ✅ Close tab (10:35:00)

### Results
- Products extracted: 25
- Saved to: `products/prices_2026-01-25.csv`
- Screenshots: `screenshots/product/`
- Errors: 0
```

## Scripts

### `check_connection.sh`

```bash
#!/usr/bin/env bash
# Check BrowserOS MCP server connection

echo "Checking BrowserOS MCP server..."

if curl -s http://127.0.0.1:9106/mcp > /dev/null; then
  echo "✅ BrowserOS MCP server is running"
else
  echo "❌ BrowserOS MCP server is not responding"
  echo "Start BrowserOS and ensure MCP server is enabled"
  exit 1
fi
```

### `extract_form.py`

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["beautifulsoup4"]
# ///

"""
Extract form fields from HTML content.
Usage: cat page.html | extract_form.py
"""

from bs4 import BeautifulSoup
import sys
import json

def extract_forms(html_content):
    """Extract form fields from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    forms = soup.find_all('form')

    results = []
    for i, form in enumerate(forms):
        form_data = {
            'form_index': i,
            'action': form.get('action', ''),
            'method': form.get('method', 'GET'),
            'fields': []
        }

        for field in form.find_all(['input', 'textarea', 'select']):
            field_info = {
                'name': field.get('name'),
                'type': field.get('type', 'text'),
                'id': field.get('id'),
                'required': field.has_attr('required')
            }
            form_data['fields'].append(field_info)

        results.append(form_data)

    return results

if __name__ == "__main__":
    html = sys.stdin.read()
    forms = extract_forms(html)
    print(json.dumps(forms, indent=2))
```

### `screenshot_on_error.sh`

```bash
#!/usr/bin/env bash
# Take screenshot when browser operation fails

TAB_ID="${1:-1697399534}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SCREENSHOT_DIR="screenshots/errors"

mkdir -p "$SCREENSHOT_DIR"

# Take screenshot
# This would be called via MCP when error detected
echo "Taking screenshot for debugging..."
# Actual MCP call would be:
# mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID

echo "Screenshot saved to $SCREENSHOT_DIR/error_$TIMESTAMP.png"
```

## Templates

### Form Automation Template

**Location**: `assets/form_workflow_template.md`

```markdown
# Form Automation Workflow Template

## Task: [Form Name]

## Form URL
- Login: https://example.com/login
- Form: https://example.com/form

## Fields Mapping

| Field Name | Selector | Value | Type |
|-------------|----------|-------|------|
| username | #input-username | user@example.com | Text |
| password | #input-password | *** | Password |
| email | #input-email | user@example.com | Email |
| terms | #checkbox-terms | true | Checkbox |

## Navigation Steps
1. Navigate to login
2. Enter credentials
3. Click submit
4. Navigate to form
5. Fill fields
6. Submit form

## Success Criteria
- [ ] Login successful
- [ ] Form submitted
- [ ] Confirmation page visible
```

### Data Extraction Template

**Location**: `assets/extraction_template.md`

```markdown
# Data Extraction Template

## Target URL
https://example.com/data

## Data to Extract

| Field | CSS Selector | Regex Pattern | Required |
|-------|-------------|---------------|----------|
| Product Name | .product-title | | Yes |
| Price | .price | \$\d+\.\d{2} | Yes |
| Availability | .stock | In Stock| Yes |
| SKU | .sku | [A-Z]{3}-\d{4} | No |

## Output Format
- CSV file: `extracted_data.csv`
- Timestamp: Yes
- Source URL: Yes
```

## References

- **[BrowserOS Documentation](https://github.com/browseros-ai/BrowserOS)** - Official BrowserOS docs
- **[MCP Tools List](./tools-list.md)** - Complete list of 31 BrowserOS MCP tools
- **[Advanced Patterns](./advanced-patterns.md)** - Complex automation patterns
- **[Error Handling Guide](./error-handling.md)** - Troubleshooting common issues
- **[Workflow Integration](./workflow-integration.md)** - Combining with BrowserOS visual workflows

## Quick Reference

### BrowserOS MCP Server

- **Default URL**: `http://127.0.0.1:9106/mcp`
- **Connection check**: `curl http://127.0.0.1:9106/mcp`

### Tab ID Management

- **From navigation**: Save tabId from `browser_navigate` response
- **From active tab**: Use `browser_get_active_tab` to get current tab
- **List all tabs**: Use `browser_list_tabs` to see all tabs

### Element Finding

```bash
# Get all interactive elements
mcp__browser-mcp__browser_get_interactive_elements?tabId=1697399534

# Search for specific elements
mcp__browser-mcp__browser_grep_interactive_elements?tabId=1697399534&pattern=login|submit|button
```

## Changelog

### v1.0.0 - 2026-01-25

**Added**:
- Initial release
- Core browser automation patterns
- Form automation workflows
- Data extraction patterns
- Error handling strategies
- 31 BrowserOS MCP tools integration
- Hooks for automatic verification

**Features**:
- Task-based workflows
- Multi-step patterns
- Batch processing support
- Error recovery
- Scheduled task integration
- Parallel operations
- Comprehensive examples
- Utility scripts
- Template files

**Known Limitations**:
- Requires BrowserOS to be running
- BrowserOS is Chromium-based (not cross-browser)
- Requires manual setup for captchas
- Some sites may detect automation ( BrowserOS has anti-detection )

**Future Enhancements**:
- OCR integration for captcha solving
- Machine learning for element detection
- Cloud storage integration
- Advanced retry logic
- Performance monitoring
