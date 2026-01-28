# Browser Automation Error Handling Guide

Comprehensive troubleshooting guide for common browser automation issues using BrowserOS MCP tools.

## Table of Contents

1. [Connection Issues](#connection-issues)
2. [Element Not Found]((#element-not-found)
3. [Page Loading Problems](#page-loading-problems)
4. [Interaction Failures](#interaction-failures)
5. [Session Issues](#session-issues)
6. [Content Extraction Errors](#content-extraction-errors)
7. [Performance Issues](#performance-issues)
8. [Debugging Techniques](#debugging-techniques)

---

## Connection Issues

### Problem: BrowserOS MCP Server Not Responding

**Symptoms**:
```
❌ BrowserOS MCP server is not responding
curl: (7) Failed to connect to 127.0.0.1:9106
```

**Diagnosis**:
```bash
# Check if BrowserOS is running
pgrep -f "BrowserOS" || echo "BrowserOS not running"

# Check if MCP server is enabled in BrowserOS
# Navigate to chrome://browseros/mcp or Settings → BrowserOS as MCP

# Check port 9106
lsof -i :9106 || echo "Port 9106 not in use"
```

**Solutions**:

1. **Start BrowserOS**
   - Open BrowserOS application
   - Enable MCP server: Settings → BrowserOS as MCP
   - Note the Server URL displayed

2. **Verify MCP endpoint**
   ```bash
   curl http://127.0.0.1:9106/mcp
   ```
   Should return MCP server info

3. **Check firewall/network**
   - Ensure localhost (127.0.0.1) is accessible
   - Check if port 9106 is blocked

---

### Problem: MCP Server Timeout

**Symptoms**:
```
Tool use timeout: Request to MCP server timed out after 30000ms
```

**Solutions**:

1. **Check server load**
   ```bash
   # Check BrowserOS CPU/memory usage
   top | grep BrowserOS
   ```

2. **Increase timeout**
   - Some operations take longer (e.g., large page loads)
   - Adjust in MCP client settings

3. **Retry operation**
   - Timeout may be transient
   - Implement retry logic in your workflow

---

## Element Not Found

### Problem: nodeId Does Not Exist

**Symptoms**:
```
❌ Error: Element with nodeId 15 not found
```

**Diagnosis**:
```bash
# Re-fetch interactive elements
mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID

# Check if nodeId exists in response
# Look for nodeId: 15 in the elements array
```

**Common Causes**:

1. **Stale snapshot** - Elements changed since last fetch
2. **Wrong tab** - Operating on different tab than expected
3. **Element removed** - Page changed, element deleted

**Solutions**:

1. **Re-fetch elements before interaction**
   ```bash
   # Always get fresh elements before clicking
   mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID
   ELEMENTS=$(response)

   # Then use nodeId from fresh elements
   mcp__browser-mcp__browser_click_element?nodeId=<fresh_nodeId>&tabId=$TAB_ID
   ```

2. **Use grep to find element**
   ```bash
   # Search by text
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=Submit|Login

   # Search by attributes
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=name=\"username\"
   ```

3. **Verify tab context**
   ```bash
   # Ensure you're using correct tab
   mcp__browser-mcp__browser_get_active_tab

   # List all tabs
   mcp__browser-mcp__browser_list_tabs
   ```

---

### Problem: Element Not Visible

**Symptoms**:
- Click doesn't trigger action
- Element exists but can't be clicked

**Diagnosis**:
```bash
# Check if element is in viewport
# Take screenshot to see current page state
mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID

# Check element attributes in get_interactive_elements response
# Look for "(hidden)" in element data
```

**Solutions**:

1. **Scroll element into view**
   ```bash
   # Use nodeId to scroll
   mcp__browser-mcp__browser_scroll_to_element?nodeId=<nodeId>&tabId=$TAB_ID
   ```

2. **Wait for dynamic content**
   ```bash
   # Element may be covered by overlay or loading spinner
   sleep 2
   mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID
   ```

3. **Check for blocking modal**
   ```bash
   # Take screenshot to see if modal is blocking
   mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID

   # Look for close/dismiss buttons
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=Close|Dismiss|Cancel
   ```
---

## Page Loading Problems

### Problem: Page Never Finishes Loading

**Symptoms**:
```
isPageComplete: false for extended period
```

**Diagnosis**:
```bash
# Check load status details
mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID

# All three should be true for page to be fully loaded
# - isDOMContentLoaded: true
# - isResourcesLoading: false
# - isPageComplete: true
```

**Common Causes**:

1. **Slow dynamic content** - Page loads content via JavaScript
2. **Infinite scroll** - Page keeps loading as you scroll
3. **Background tasks** - Page has ongoing processes

**Solutions**:

1. **Wait and recheck**
   ```bash
   # Wait for page to stabilize
   sleep 5
   mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID
   ```

2. **Check for specific content**
   ```bash
   # Even if page not "complete", specific content may be loaded
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=Target.*Element

   # Get current content even if loading
   mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID
   ```

3. **Wait for specific condition**
   ```bash
   # Poll for element to appear
   for i in {1..30}; do
     ELEMENT=$(mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=Complete)

     if [ -n "$ELEMENT" ]; then
       echo "✅ Element found"
       break
     fi

     sleep 1
   done
   ```

---

### Problem: Redirect Loop

**Symptoms**:
```
Page redirects back and forth infinitely
```

**Solutions**:

1. **Detect redirect chains**
   ```bash
   # Track URLs to detect loops
   PREVIOUS_URL=""
   CURRENT_URL=""

   # After each navigation, check if we've seen this URL before
   if [ "$CURRENT_URL" == "$PREVIOUS_URL" ]; then
     echo "⚠️  Redirect loop detected"
     break
   fi
   PREVIOUS_URL="$CURRENT_URL"
   ```

2. **Limit redirect depth**
   ```bash
   MAX_REDIRECTS=5
   REDIRECT_COUNT=0

   while [ $REDIRECT_COUNT -lt $MAX_REDIRECTS ]; do
     # Navigate and check URL
     # If URL hasn't changed, we're done
     break
     REDIRECT_COUNT=$((REDIRECT_COUNT + 1))
   done
   ```

---

## Interaction Failures

### Problem: Click Doesn't Work

**Symptoms**:
- Click executed but page doesn't change
- Button is visually clicked but no action

**Diagnosis**:
```bash
# 1. Get screenshot to see page state
mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID

# 2. Check if element is still present
mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=<nodeId>

# 3. Check page content for errors
mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID
```

**Common Causes**:

1. **Element overlay** - Popup/covering element blocking click
2. **Disabled button** - Button has disabled attribute
3. **Wrong element** - Clicked container instead of button
4. **JavaScript interception** - JS prevents default action

**Solutions**:

1. **Dismiss overlays**
   ```bash
   # Find close/dismiss buttons
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=Close|Dismiss|Cancel

   # Click to dismiss
   mcp__browser-mcp__browser_click_element?nodeId=<close_nodeId>&tabId=$TAB_ID
   ```

2. **Check element attributes**
   ```bash
   # In interactive elements response, check for:
   # - disabled: true (element is disabled)
   # - aria-disabled: true
   ```

3. **Wait and retry**
   ```bash
   # May need to wait for animation
   sleep 2
   mcp__browser-mcp__browser_click_element?nodeId=$NODEID&tabId=$TAB_ID
   ```

---

### Problem: Type Text Not Working

**Symptoms**:
- Text not appearing in input field
- Partial text entered

**Diagnosis**:
```bash
# Check if input is focused
# Text may be typed but not accepted

# Verify input field properties
# In interactive elements, check:
# - type: text/email/password/number/tel/url
# - readonly: (not set) or true (read-only)
```

**Solutions**:

1. **Clear input first**
   ```bash
   mcp__browser-mcp__browser_clear_input?nodeId=$NODEID&tabId=$TAB_ID
   mcp__browser-mcp__browser_type_text?nodeId=$NODEID&text=text&tabId=$TAB_ID
   ```

2. **Click element before typing**
   ```bash
   # Focus input by clicking it first
   mcp__browser-mcp__browser_click_element?nodeId=$NODEID&tabId=$TAB_ID
   mcp__browser-mcp__browser_type_text?nodeId=$NODEID&text=text&tabId=$TAB_ID
   ```

3. **Use JavaScript to set value**
   ```bash
   # Directly set value via JS
   JS_CODE="document.getElementById('element-id').value = 'text';"
   mcp__browser-mcp__browser_execute_javascript?tabId=$TAB_ID&code="$JS_CODE"
   ```

---

## Session Issues

### Problem: Unexpected Login Page

**Symptoms**:
- Redirected to login page when expecting dashboard
- Session expired during workflow

**Diagnosis**:
```bash
# Check current URL
# Look for "login", "sign-in" in URL or content

mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text
```

**Solutions**:

1. **Detect login page**
   ```bash
   CONTENT=$(mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text)

   if echo "$CONTENT" | grep -qi "login\|sign.?in"; then
     echo "🔐 Login page detected, session expired"
     # Re-authenticate
     perform_login
   fi
   ```

2. **Automatic re-login**
   ```bash
   # Navigate to login
   mcp__browser-mcp__browser_navigate?url=https://example.com/login

   # Get login form elements
   mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID

   # Fill credentials
   mcp__browser-mcp__browser_type_text?nodeId=$USERNAME_ID&text=$USERNAME
   mcp__browser-mcp__browser_type_text?nodeId=$PASSWORD_ID&text=$PASSWORD

   # Submit
   mcp__browser-mcp__browser_click_element?nodeId=$SUBMIT_ID&tabId=$TAB_ID

   # Wait for redirect
   mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID
   ```

3. **Session monitoring**
   ```bash
   # Track session age
   # Store login timestamp
   # Re-login if session too old (> 30 minutes)
   ```

---

### Problem: Cookies Not Persisting

**Symptoms**:
- Need to re-login every time
- Preferences not saved

**Diagnosis**:
- BrowserOS preserves cookies by default
- Check if site explicitly blocks cookies

**Solutions**:

1. **Verify cookie settings**
   - BrowserOS → Settings → Privacy and security
   - Check "Block third-party cookies" is off

2. **Accept cookies**
   ```bash
   # Look for cookie banner
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=Accept|Accept.*Cookies

   # Click accept button
   mcp__browser-mcp__browser_click_element?nodeId=<accept_nodeId>&tabId=$TAB_ID
   ```

---

## Content Extraction Errors

### Problem: Incomplete Content

**Symptoms**:
- Missing parts of page content
- Truncated text

**Diagnosis**:
```bash
# Check contextWindow parameter
# Small context may truncate large pages

mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text&contextWindow=100k
```

**Solutions**:

1. **Increase context window**
   ```bash
   # Use larger context for big pages
   mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&contextWindow=50k
   mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&contextWindow=100k
   ```

2. **Use page parameter for pagination**
   ```bash
   # Some sites support page parameter
   mcp__browser-mcp__browser_navigate?url=https://example.com/data?page=2
   ```

3. **Scroll to trigger lazy loading**
   ```bash
   # Scroll through page to load all content
   for i in {1..5}; do
     mcp__browser-mcp__browser_scroll_down?tabId=$TAB_ID
     sleep 1
   done
   ```

---

### Problem: Special Characters Not Extracted

**Symptoms**:
- Unicode characters displayed incorrectly
- Emojis missing

**Solutions**:

1. **Use text-with-links type**
   ```bash
   mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text-with-links
   ```

2. **Parse HTML directly**
   - Get raw HTML, parse locally
   - Use browser_get_page_content, extract with BeautifulSoup

---

## Performance Issues

### Problem: Slow Operations

**Symptoms**:
- Each operation takes several seconds
- Overall workflow is slow

**Solutions**:

1. **Batch operations**
   ```bash
   # Open multiple tabs first
   # Then process them all
   TAB_IDS=(tab1 tab2 tab3)
   for tab in "${TAB_IDS[@]}"; do
     mcp__browser-mcp__browser_navigate?url=https://example.com/item$tab
   done
   ```

2. **Parallel processing**
   - Use BrowserOS tab groups
   - Process multiple pages simultaneously

3. **Skip unnecessary waits**
   - Only wait when necessary
   - Not all pages need long waits

---

### Problem: BrowserOS High CPU/Memory

**Symptoms**:
- BrowserOS becomes slow
- High memory usage

**Solutions**:

1. **Close unused tabs**
   ```bash
   # Regularly close tabs when done
   mcp__browser-mcp__browser_close_tab?tabId=$TAB_ID
   ```

2. **Limit concurrent operations**
   - Don't open too many tabs at once (recommend max 5-10)

3. **Restart BrowserOS periodically**
   - Some sessions may degrade over time

---

## Debugging Techniques

### 1. Take Screenshots

Always take screenshots when errors occur:

```bash
mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID&size=medium
mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID&size=large
```

### 2. Log Everything

```bash
# Log each step with timestamps
echo "[$(date)] Navigating to URL..." >> browser_automation.log
echo "[$(date)] Getting interactive elements..." >> browser_automation.log
echo "[$(date)] Clicking nodeId=$NODEID..." >> browser_automation.log
```

### 3. Use Interactive Elements Output

```bash
# Save elements for analysis
mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID > elements_snapshot.json
```

### 4. Check Page Source

```bash
# Get raw HTML for debugging
mcp__browser-mcp__browser_execute_javascript?tabId=$TAB_ID&code=document.body.innerHTML
```

### 5. Monitor BrowserOS Console

- Open BrowserOS Developer Tools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for failed requests

---

## Common Error Messages

| Error Message | Likely Cause | Solution |
|---------------|---------------|----------|
| "Element not found" | Stale snapshot or wrong nodeId | Re-fetch elements |
| "Tool use timeout" | Page loading slow | Increase timeout, wait longer |
| "Invalid tabId" | Tab was closed | Get active tab, re-open URL |
| "Network error" | Connection issue | Check BrowserOS is running |
| "Element not clickable" | Element hidden or disabled | Scroll to element, check attributes |
| "Text input failed" | Input readonly or wrong focus | Clear input, click first |
| "Session expired" | Login timeout | Re-authenticate |
| "Content incomplete" | Context too small | Increase contextWindow |

---

## Error Recovery Checklist

When encountering errors, go through this checklist:

- [ ] **Is BrowserOS running?**
- [ ] **Is MCP server responding?**
- [ ] **Is page fully loaded?**
- [ ] **Are you on the correct tab?**
- [ ] **Did you re-fetch elements?**
- [ ] **Is element still visible?**
- [ ] **Are there overlays/modals blocking?**
- [ ] **Is session still valid?**
- [ ] **Did you wait long enough for dynamic content?**
- [ ] **Is JavaScript enabled?**
- [ ] **Are there any errors in BrowserOS console?**

---

## Proactive Error Prevention

### Best Practices

1. **Always verify before acting**
   - Check load_status
   - Re-fetch elements
   - Verify element visibility

2. **Implement timeouts**
   - Don't wait forever
   - Set reasonable timeouts for each operation

3. **Log errors with context**
   - Include tabId, nodeId, timestamp
   - Save error screenshots
   - Include page URLs

4. **Build retry logic**
   - Transient errors should be retried
   - Fatal errors should fail fast

5. **Test error recovery**
   - Simulate errors to test recovery
   - Ensure workflow can handle common failures

---

## Quick Reference

### Error Diagnosis Flowchart

```
Error occurs
    ↓
Take screenshot for debugging
    ↓
Check error type
    ↓
┌────────────────┬──────────────┬──────────────┐
│                  │              │              │
Connection error   Element not   Page loading  Interaction
│                  │ found         │  failure    │
│                  │              │              │
↓                  ↓              ↓              ↓
Check BrowserOS   Re-fetch       Wait and      Try alternative
is running        elements      re-check     method
↓                  ↓              ↓              ↓
Start BrowserOS   Use grep       Scroll to    Re-authenticate
or check MCP      to find       element   or logout
server            element        into view
```

---

## See Also

- [Advanced Patterns](./advanced-patterns.md) - Complex workflow patterns
- [Tools List](./tools-list.md) - Complete tool reference
- [Workflow Integration](./workflow-integration.md) - BrowserOS visual workflows
