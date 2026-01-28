# Advanced Browser Automation Patterns

Complex multi-step workflows for browser automation using BrowserOS MCP tools.

## Pattern 1: Multi-Page Data Extraction

### Scenario
Extract product listings from a paginated e-commerce site.

### Workflow

```markdown
1. **Navigate to first page**
   ```bash
   mcp__browser-mcp__browser_navigate?url=https://shop.example.com/products
   TAB_ID=<response.tabId>
   ```

2. **Wait for load**
   ```bash
   mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID
   # Verify: isPageComplete == true
   ```

3. **Extract data from page**
   ```bash
   # Get all product links
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=product.*href
   # Extract: href attribute values

   # Get content
   mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text-with-links
   ```

4. **Save results**
   ```bash
   # Write to CSV (using Write tool)
   echo "product,url,price" > products.csv
   ```

5. **Find and click "Next" button**
   ```bash
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=Next|→
   # Get nodeId of Next button
   mcp__browser-mcp__browser_click_element?nodeId=<nodeId>&tabId=$TAB_ID
   ```

6. **Repeat from step 2**
   - Continue until no more pages
   - Stop when "Next" button is disabled or not found
```

### Optimization Tips

- **Parallel extraction**: Open multiple product pages in separate tabs
- **Rate limiting**: Add delays between requests to avoid rate limiting
- **Error recovery**: If extraction fails on a page, log it and continue
- **Progress tracking**: Keep count of pages processed

---

## Pattern 2: Form Field Mapping

### Scenario
Fill complex forms with data from a CSV/JSON file.

### Workflow

```markdown
1. **Parse data file**
   ```bash
   # Read CSV data
   while IFS=, read -r field1 field2 field3; do
     # Process each row
   done < data.csv
   ```

2. **Navigate to form**
   ```bash
   mcp__browser-mcp__browser_navigate?url=https://example.com/form
   mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID
   mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID
   ```

3. **Map fields to nodeIds**
   ```bash
   # Find each field by name/id/placeholder
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=first_name|name
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=email

   # Extract nodeId from response
   FIELD1_NODEID=<extracted>
   FIELD2_NODEID=<extracted>
   ```

4. **Fill each field**
   ```bash
   mcp__browser-mcp__browser_type_text?nodeId=$FIELD1_NODEID&text="$field1"
   mcp__browser-mcp__browser_type_text?nodeId=$FIELD2_NODEID&text="$field2"
   ```

5. **Submit form**
   ```bash
   mcp__browser-mcp__browser_click_element?nodeId=<submit_nodeId>&tabId=$TAB_ID
   ```

6. **Verify submission**
   ```bash
   mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID
   mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID
   # Check for success message or confirmation page
   ```

7. **Handle errors**
   - Validation errors → Fix fields and resubmit
   - Duplicate entry → Skip or update existing
   - Network errors → Retry after delay
```

### Field Matching Strategies

#### Strategy 1: By Attribute

```bash
# Match by 'name' attribute
mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=name=\"email\"

# Match by 'id' attribute
mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=id=\"user_email\"

# Match by 'placeholder'
mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=placeholder=\"Email\"
```

#### Strategy 2: By Type

```bash
# All text inputs
mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=<input.*type=[\"']text['\"]>

# Email inputs
mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=<input.*type=[\"']email['\"]>

# Password fields (be careful with logging!)
mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=<input.*type=[\"']password['\"]>
```

#### Strategy 3: Sequential Scan

```bash
# Get all elements
mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID

# Parse output to find target fields
# Look for matching name/id/placeholder in elements array
```

---

## Pattern 3: Session-Based Automation

### Scenario
Automate tasks that require login, with session reuse across multiple operations.

### Workflow

```markdown
1. **Check existing session**
   ```bash
   # Try to navigate to authenticated page
   mcp__browser-mcp__browser_navigate?url=https://example.com/dashboard
   mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID
   ```

2. **Check if authenticated**
   ```bash
   mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text

   # Look for signs of login page
   if content contains "sign in" or "log in":
     # Need to login
     perform_login
   fi
   ```

3. **Login procedure**
   ```bash
   # Navigate to login page
   mcp__browser-mcp__browser_navigate?url=https://example.com/login

   # Get login form elements
   mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID

   # Find username and password fields
   USERNAME_NODEID=<find_nodeId_for_username>
   PASSWORD_NODEID=<find_nodeId_for_password>
   SUBMIT_NODEID=<find_nodeId_for_submit_button>

   # Fill credentials
   mcp__browser-mcp__browser_type_text?nodeId=$USERNAME_NODEID&text=$USERNAME
   mcp__browser-mcp__browser_type_text?nodeId=$PASSWORD_NODEID&text=$PASSWORD

   # Click login
   mcp__browser-mcp__browser_click_element?nodeId=$SUBMIT_NODEID&tabId=$TAB_ID

   # Wait for redirect
   mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID
   ```

4. **Perform authenticated task**
   ```bash
   # Navigate to target page
   mcp__browser-mcp__browser_navigate?url=https://example.com/protected/data

   # Extract data
   mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID
   ```

5. **Logout (optional)**
   ```bash
   # Find logout button/link
   mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=logout|sign.?out

   # Click logout
   mcp__browser-mcp__browser_click_element?nodeId=<logout_nodeId>&tabId=$TAB_ID
   ```
```

### Session Persistence

**Key insight**: BrowserOS maintains your session automatically
- ✅ Cookies are preserved
- ✅ Login state persists across operations
- ✅ No need to re-login for each task
- ⚠️ Sessions may expire after inactivity

**Best practices**:
- Check for session validity before critical operations
- Implement auto-relogin if session expired
- Store session timestamps for monitoring
- Handle session timeouts gracefully

---

## Pattern 4: Conditional Logic

### Scenario
Perform different actions based on page content or conditions.

### Workflow

```markdown
1. **Navigate to page**
   ```bash
   mcp__browser-mcp__browser_navigate?url=https://example.com/page
   mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID
   ```

2. **Get page content**
   ```bash
   CONTENT=$(mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text)
   ```

3. **Evaluate conditions**
   ```bash
   # Check page type
   if echo "$CONTENT" | grep -q "Product out of stock"; then
     echo "⚠️  Product out of stock"
     # Send notification, skip to next item
   elif echo "$CONTENT" | grep -q "Add to cart"; then
     echo "✅  Product available"
     # Click add to cart
     mcp__browser-mcp__browser_click_element?nodeId=<add_to_cart_button>
   else
     echo "❓  Unknown page state"
     mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID
     exit 1
   fi
   ```

4. **Handle different page states**
   - **Error page** → Log error, skip to next
   - **Loading spinner** → Wait and recheck
   - **Success page** → Extract confirmation
   - **Redirect** → Follow redirect
```

### Decision Trees

```markdown
## Example: Product Availability Decision Tree

Start
  |
  v
Is page loaded?
  |
  +-- No --> Wait for load --> Check timeout --> Skip item
  |
  Yes
  |
  v
Check availability
  |
  +-- Out of stock --> Log, skip
  |
  +-- Available --> Add to cart
  |
  v
Added successfully?
  |
  +-- No --> Check for error message --> Try alternative method
  |
  +-- Yes --> Continue to next item
```

---

## Pattern 5: Error Recovery with Retry

### Scenario
Robust automation that handles transient failures.

### Retry Strategy

```markdown
1. **Define retry conditions**
   - Network timeout
   - Element not found (may appear later)
   - Page loading slow
   - Temporary server error (5xx)

2. **Implement retry loop**
   ```bash
   MAX_RETRIES=3
   RETRY_DELAY=5  # seconds

   for attempt in $(seq 1 $MAX_RETRIES); do
     # Try operation
     mcp__browser-mcp__browser_click_element?nodeId=$NODEID&tabId=$TAB_ID
     SUCCESS=$?

     if [ $SUCCESS -eq 0 ]; then
       echo "✅ Operation succeeded on attempt $attempt"
       break
     else
       echo "⚠️  Operation failed (attempt $attempt/$MAX_RETRIES)"

       if [ $attempt -lt $MAX_RETRIES ]; then
         echo "⏳  Waiting ${RETRY_DELAY}s before retry..."
         sleep $RETRY_DELAY

         # Refresh elements before retry
         mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID
       else
         echo "❌  Max retries exceeded"
         # Take error screenshot
         mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID
         exit 1
       fi
     fi
   done
   ```

3. **Handle different error types**
   - **Element not found**: Re-fetch elements, search for alternative
   - **Network error**: Wait longer, check connectivity
   - **Page changed**: Refresh page, re-analyze
   - **Blocking popup**: Dismiss popup, retry action

4. **Fallback strategies**
   - **Alternative selector**: Try different search pattern
   - **Alternative method**: Use coordinates if nodeId fails
   - **Manual intervention**: Pause and ask user for help
```

### Exponential Backoff

```bash
# Implement exponential backoff for retries
DELAY=1
MAX_DELAY=60

for attempt in $(seq 1 5); do
  # Try operation
  if mcp__browser-mcp__browser_click_element?nodeId=$NODEID; then
    break
  fi

  # Exponential backoff
  sleep $DELAY
  DELAY=$((DELAY * 2))

  if [ $DELAY -gt $MAX_DELAY ]; then
    DELAY=$MAX_DELAY
  fi
done
```

---

## Pattern 6: Batch Processing with Parallel Tabs

### Scenario
Process multiple URLs or data points efficiently.

### Workflow

```markdown
1. **Prepare list of URLs**
   ```bash
   URLS=(
     "https://example.com/item1"
     "https://example.com/item2"
     "https://example.com/item3"
   )
   ```

2. **Open all tabs in parallel**
   ```bash
   TAB_IDS=()

   for url in "${URLS[@]}"; do
     RESPONSE=$(mcp__browser-mcp__browser_open_tab?url=$url)
     TAB_ID=$(echo $RESPONSE | jq -r '.tabId')
     TAB_IDS+=("$TAB_ID")
   done

   echo "Opened ${#TAB_IDS[@]} tabs"
   ```

3. **Process each tab**
   ```bash
   RESULTS=()

   for i in "${!TAB_IDS[@]}"; do
     TAB_ID="${TAB_IDS[$i]}"

     # Switch to tab
     mcp__browser-mcp__browser_switch_tab?tabId=$TAB_ID

     # Wait for load
     mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID

     # Extract data
     DATA=$(mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text)

     # Save result
     RESULTS+=("$DATA")

     # Close tab when done
     mcp__browser-mcp__browser_close_tab?tabId=$TAB_ID
   done

   echo "Processed ${#RESULTS[@]} items"
   ```

4. **Consolidate results**
   ```bash
   # Write all results to file
   for result in "${RESULTS[@]}"; do
     echo "$result" >> output.csv
   done
   ```

### Optimization Techniques

- **Limit concurrent tabs**: Don't open too many tabs at once (BrowserOS may slow down)
- **Error isolation**: Failure in one tab shouldn't affect others
- **Progress tracking**: Log which tabs completed/failed
- **Resource cleanup**: Always close tabs after processing

---

## Pattern 7: Content Change Detection

### Scenario
Monitor a page for changes and take action when detected.

### Workflow

```markdown
1. **Initial snapshot**
   ```bash
   # Navigate and get baseline
   mcp__browser-mcp__browser_navigate?url=https://example.com/monitor
   TAB_ID=<response.tabId>

   mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID

   BASELINE_CONTENT=$(mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text)
   echo "$BASELINE_CONTENT" > baseline.txt
   ```

2. **Monitoring loop**
   ```bash
   CHECK_INTERVAL=300  # seconds (5 minutes)

   while true; do
     sleep $CHECK_INTERVAL

     # Refresh page
     mcp__browser-mcp__browser_navigate?url=https://example.com/monitor
     mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID

     # Get current content
     CURRENT_CONTENT=$(mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text)

     # Compare with baseline
     if [ "$CURRENT_CONTENT" != "$BASELINE_CONTENT" ]; then
       echo "🚨 Change detected!"

       # Take screenshot
       mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID

       # Send notification (use AskUserQuestion or external API)
       # Extract changes
       # Update baseline

       break
     fi
   done
   ```

3. **Change detection strategies**
   - **Simple string comparison** (as above)
   - **Hash comparison**: Compute content hash
   - **Section-specific**: Monitor only specific page regions
   - **Keyword-based**: Trigger on specific words appearing

### Hash-Based Comparison

```bash
# Compute hash of content
CURRENT_HASH=$(echo "$CURRENT_CONTENT" | md5sum | cut -d' ' -f1)
BASELINE_HASH=$(cat baseline.txt | md5sum | cut -d' ' -f1)

if [ "$CURRENT_HASH" != "$BASELINE_HASH" ]; then
  echo "Content has changed (hash mismatch)"
fi
```

---

## Pattern 8: Dynamic Content Handling

### Scenario
Wait for dynamically loaded content (AJAX, lazy loading).

### Strategies

#### 1. Wait and Poll

```bash
# Navigate to page
mcp__browser-mcp__browser_navigate?url=https://example.com/dynamic
TAB_ID=<response.tabId>

# Wait for initial load
mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID
# Verify: isPageComplete == true

# Poll for content appearance
MAX_WAIT=30
ELAPSED=0

while [ $ELAPSED -lt $MAX_WAIT ]; do
  # Check if target element exists
  ELEMENT=$(mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=target.*content)

  if [ -n "$ELEMENT" ]; then
    echo "✅ Content loaded"
    break
  fi

  sleep 1
  ELAPSED=$((ELAPSED + 1))
done

if [ $ELAPSED -ge $MAX_WAIT ]; then
  echo "⏱️  Timeout waiting for content"
fi
```

#### 2. Scroll-Triggered Loading

```bash
# Some sites load content as you scroll
mcp__browser-mcp__browser_navigate?url=https://example.com/infinite-scroll
TAB_ID=<response.tabId>

# Scroll down to trigger more content
for i in {1..5}; do
  mcp__browser-mcp__browser_scroll_down?tabId=$TAB_ID
  sleep 2

  # Check if new content appeared
  CURRENT_HEIGHT=$(mcp__browser-mcp__browser_execute_javascript?tabId=$TAB_ID&code=return document.body.scrollHeight)

  echo "Scroll $i: height=$CURRENT_HEIGHT"
done
```

#### 3. JavaScript Execution

```bash
# Execute custom JavaScript to handle dynamic content
JS_CODE='
  // Wait for element to appear
  const checkForElement = () => {
    const element = document.querySelector(".target-class");
    if (element) {
      return true;
    }
    return false;
  };

  // Poll for up to 10 seconds
  const timeout = 10000;
  const startTime = Date.now();

  while (Date.now() - startTime < timeout) {
    if (checkForElement()) {
      return "Element found";
    }
    await new Promise(r => setTimeout(r, 500));
  }

  return "Element not found";
'

mcp__browser-mcp__browser_execute_javascript?tabId=$TAB_ID&code="$JS_CODE"
```

---

## Pattern 9: Multi-Window Workflows

### Scenario
Coordinate actions across multiple browser windows.

### Workflow

```markdown
1. **Create multiple windows**
   ```bash
   # Window 1 - Main task
   mcp__browser-mcp__browser_create_window?url=https://example.com/task1
   WINDOW1_ID=$window_id
   TAB1_ID=$tab_id

   # Window 2 - Monitoring
   mcp__browser-mcp__browser_create_window?url=https://example.com/monitor
   WINDOW2_ID=$window_id
   TAB2_ID=$tab_id
   ```

2. **Perform parallel tasks**
   ```bash
   # In Window 1: Execute main workflow
   mcp__browser-mcp__browser_click_element?tabId=$TAB1_ID&nodeId=<nodeId>

   # In Window 2: Monitor status
   mcp__browser-mcp__browser_get_page_content?tabId=$TAB2_ID
   ```

3. **Coordinate windows**
   - Use windowId parameter when switching tabs
   - Track state across windows
   - Synchronize actions between windows
```

### Coordination Patterns

```bash
# Switch between windows
mcp__browser-mcp__browser_switch_tab?tabId=$TAB1_ID&windowId=$WINDOW1_ID
mcp__browser-mcp__browser_switch_tab?tabId=$TAB2_ID&windowId=$WINDOW2_ID

# List all windows (not directly available, but can track manually)
# Keep track of your created window IDs
```

---

## Pattern 10: Error Recovery with Automatic Retry

### Comprehensive Error Handling

```markdown
**Generic Retry Wrapper**:

function browser_operation_with_retry() {
  local operation="$1"
  local max_retries="${2:-3}"
  local retry_delay="${3:-5}"

  for attempt in $(seq 1 $max_retries); do
    echo "🔄 Attempt $attempt of $max_retries: $operation"

    # Execute operation
    if eval "$operation"; then
      echo "✅ Success"
      return 0
    fi

    # Operation failed
    if [ $attempt -lt $max_retries ]; then
      echo "⚠️  Failed, waiting ${retry_delay}s..."
      sleep $retry_delay

      # Refresh state before retry
      if [[ "$operation" == *"click_element"* ]]; then
        mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID > /dev/null
      fi
    else
      echo "❌ Max retries exceeded"
      # Take screenshot for debugging
      mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID
      return 1
    fi
  done
}

# Usage
browser_operation_with_retry \
  "mcp__browser-mcp__browser_click_element?nodeId=15&tabId=$TAB_ID" \
  3 \
  5
```

### Common Error Patterns

| Error Type | Detection | Recovery Strategy |
|------------|-----------|-------------------|
| Element not found | nodeId not found | Re-fetch elements, search alternatives |
| Page not loaded | isPageComplete=false | Wait and check load status |
| Network timeout | Connection timeout | Retry with longer delay |
| Invalid state | Unexpected page content | Screenshot, diagnose, ask user |
| Popup blocking | Can't click element | Dismiss popup, retry |
| Session expired | Redirected to login | Re-authenticate |

---

## Quick Reference

### Essential Commands

| Task | Command Pattern |
|------|----------------|
| Navigate | `mcp__browser-mcp__browser_navigate?url=URL` |
| Wait | `mcp__browser-mcp__browser_get_load_status?tabId=$TAB_ID` |
| Get elements | `mcp__browser-mcp__browser_get_interactive_elements?tabId=$TAB_ID` |
| Find element | `mcp__browser-mcp__browser_grep_interactive_elements?tabId=$TAB_ID&pattern=PATTERN` |
| Click | `mcp__browser-mcp__browser_click_element?nodeId=$NODEID&tabId=$TAB_ID` |
| Type text | `mcp__browser-mcp__browser_type_text?nodeId=$NODEID&text=TEXT&tabId=$TAB_ID` |
| Get content | `mcp__browser-mcp__browser_get_page_content?tabId=$TAB_ID&type=text` |
| Screenshot | `mcp__browser-mcp__browser_get_screenshot?tabId=$TAB_ID` |
| Switch tab | `mcp__browser-mcp__browser_switch_tab?tabId=$TAB_ID` |
| Close tab | `mcp__browser-mcp__browser_close_tab?tabId=$TAB_ID` |

### Common Workflows

| Workflow | Key Steps |
|----------|-----------|
| Form fill | Navigate → Get elements → Type inputs → Submit → Verify |
| Data extract | Navigate → Wait load → Get content → Parse → Save |
| Multi-page | Loop: Navigate → Extract → Click Next → Repeat |
| Batch process | Open tabs → For each: Switch → Extract → Close → Consolidate |
| Login | Navigate login → Get elements → Type creds → Submit → Verify |
| Monitor page | Loop: Navigate → Get content → Compare → Wait → Repeat |
| Parallel | Open tabs → Process in parallel → Consolidate results |

---

## See Also

- [Tools List](./tools-list.md) - Complete reference for all 31 tools
- [Error Handling](./error-handling.md) - Detailed troubleshooting guide
- [Workflow Integration](./workflow-integration.md) - BrowserOS visual workflows
