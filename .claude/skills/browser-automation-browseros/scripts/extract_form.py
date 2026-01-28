#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["beautifulsoup4", "lxml"]
# ///

"""
Extract form fields from HTML content.
Usage: cat page.html | extract_form.py
"""

from bs4 import BeautifulSoup
import sys
import json
from typing import List, Dict, Any

def extract_forms(html_content: str) -> List[Dict[str, Any]]:
    """Extract form fields from HTML content"""
    soup = BeautifulSoup(html_content, 'lxml')
    forms = soup.find_all('form')

    results = []
    for i, form in enumerate(forms):
        form_data = {
            'form_index': i,
            'action': form.get('action', ''),
            'method': form.get('method', 'GET'),
            'fields': []
        }

        # Extract all input fields
        for field in form.find_all(['input', 'textarea', 'select']):
            field_info = {
                'name': field.get('name'),
                'type': field.get('type', 'text'),
                'id': field.get('id'),
                'value': field.get('value', ''),
                'placeholder': field.get('placeholder', ''),
                'required': field.has_attr('required'),
                'maxlength': field.get('maxlength'),
            }
            form_data['fields'].append(field_info)

        # Extract textarea content
        for textarea in form.find_all('textarea'):
            textarea_info = {
                'name': textarea.get('name'),
                'type': 'textarea',
                'id': textarea.get('id'),
                'value': textarea.get_text(strip=True),
            }
            form_data['fields'].append(textarea_info)

        # Extract select options
        for select in form.find_all('select'):
            options = []
            for option in select.find_all('option'):
                options.append({
                    'value': option.get('value', ''),
                    'text': option.get_text(strip=True),
                    'selected': option.has_attr('selected')
                })

            select_info = {
                'name': select.get('name'),
                'type': 'select',
                'id': select.get('id'),
                'options': options
            }
            form_data['fields'].append(select_info)

        results.append(form_data)

    return results

def print_forms(forms: List[Dict[str, Any]]) -> None:
    """Print forms in readable format"""
    for form in forms:
        print(f"\n=== Form {form['form_index']} ===")
        print(f"Action: {form['action']}")
        print(f"Method: {form['method']}")
        print(f"\nFields ({len(form['fields'])} total):")

        for field in form['fields']:
            if field['type'] == 'select':
                print(f"\n  📋 {field['name']} (select):")
                for option in field.get('options', []):
                    selected = " ✓" if option['selected'] else ""
                    print(f"    - {option['value']}: {option['text']}{selected}")
            else:
                required = " (required)" if field.get('required') else ""
                print(f"  📝 {field['name']} ({field['type']}){required}:")
                print(f"     Value: {field.get('value', '(empty)')}")
                print(f"     ID: {field.get('id', '(no id)')}")

if __name__ == "__main__":
    if sys.stdin.isatty():
        # Interactive mode - show usage
        print("BrowserOS Form Extractor")
        print("\nUsage:")
        print("  cat page.html | extract_form.py")
        print("  mcp__browser-mcp__browser_get_page_content | extract_form.py")
        print("\nOr pipe from BrowserOS page content:")
        print("  # Get page content and pipe to script")
        sys.exit(0)
    else:
        # Pipe mode - process HTML
        html = sys.stdin.read()
        forms = extract_forms(html)
        print_forms(forms)
