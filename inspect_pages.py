"""Script to inspect actual page structure and find correct locators."""
import sys
import os
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from pages.login_page import LoginPage

def inspect_page(page, page_name: str, url: str):
    """Inspect a page and print its structure."""
    print(f"\n{'='*80}")
    print(f"INSPECTING: {page_name}")
    print(f"URL: {url}")
    print(f"{'='*80}\n")
    
    page.goto(url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # Get page title
    print(f"Page Title: {page.title()}")
    print(f"Current URL: {page.url}\n")
    
    # Find navigation elements
    print("--- NAVIGATION ELEMENTS ---")
    nav_selectors = [
        'nav',
        '[role="navigation"]',
        'aside',
        '.sidebar',
        '[class*="nav"]',
        '[class*="menu"]',
        '[class*="sidebar"]'
    ]
    
    for selector in nav_selectors:
        elements = page.locator(selector).all()
        if elements:
            print(f"\nFound {len(elements)} element(s) with selector: {selector}")
            for i, elem in enumerate(elements[:3]):  # Show first 3
                try:
                    text = elem.inner_text()[:100] if elem.is_visible() else "[hidden]"
                    print(f"  [{i+1}] Text: {text}")
                except:
                    pass
    
    # Find links
    print("\n--- LINKS ---")
    links = page.locator('a').all()
    print(f"Total links found: {len(links)}")
    link_texts = []
    for link in links[:20]:  # First 20 links
        try:
            if link.is_visible():
                text = link.inner_text().strip()
                href = link.get_attribute('href') or ''
                if text or href:
                    link_texts.append((text, href))
                    print(f"  Link: '{text}' -> {href}")
        except:
            pass
    
    # Find buttons
    print("\n--- BUTTONS ---")
    buttons = page.locator('button').all()
    print(f"Total buttons found: {len(buttons)}")
    for button in buttons[:15]:  # First 15 buttons
        try:
            if button.is_visible():
                text = button.inner_text().strip()
                aria_label = button.get_attribute('aria-label') or ''
                btn_id = button.get_attribute('id') or ''
                if text or aria_label:
                    print(f"  Button: '{text}' | aria-label: '{aria_label}' | id: '{btn_id}'")
        except:
            pass
    
    # Find main content areas
    print("\n--- MAIN CONTENT ---")
    main_selectors = ['main', '[role="main"]', '.content', '.main-content', '[class*="content"]']
    for selector in main_selectors:
        elements = page.locator(selector).all()
        if elements:
            print(f"Found {len(elements)} element(s) with selector: {selector}")
    
    # Find headers
    print("\n--- HEADERS ---")
    for tag in ['h1', 'h2', 'h3']:
        headers = page.locator(tag).all()
        if headers:
            print(f"\n{tag.upper()} elements:")
            for header in headers[:5]:
                try:
                    if header.is_visible():
                        text = header.inner_text().strip()
                        print(f"  '{text}'")
                except:
                    pass
    
    # Find tables
    print("\n--- TABLES ---")
    tables = page.locator('table').all()
    if tables:
        print(f"Found {len(tables)} table(s)")
        for i, table in enumerate(tables):
            try:
                rows = table.locator('tr').count()
                cols = table.locator('th, td').count()
                print(f"  Table {i+1}: {rows} rows, {cols} cells")
            except:
                pass
    
    # Find inputs
    print("\n--- INPUT FIELDS ---")
    inputs = page.locator('input, textarea, select').all()
    print(f"Total inputs found: {len(inputs)}")
    for inp in inputs[:10]:
        try:
            if inp.is_visible():
                inp_type = inp.get_attribute('type') or inp.tag_name()
                inp_name = inp.get_attribute('name') or ''
                inp_id = inp.get_attribute('id') or ''
                inp_placeholder = inp.get_attribute('placeholder') or ''
                print(f"  {inp_type}: name='{inp_name}' id='{inp_id}' placeholder='{inp_placeholder}'")
        except:
            pass
    
    print(f"\n{'='*80}\n")

def main():
    """Main inspection function."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Login first
            print("Logging in...")
            login = LoginPage(page)
            login.open()
            login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
            page.wait_for_url("**/dashboard**", timeout=15000)
            page.wait_for_timeout(3000)
            
            base_url = page.url.split('/dashboard')[0]
            
            # Inspect different pages
            pages_to_inspect = [
                ("Dashboard", f"{base_url}/dashboard"),
                ("Reports", f"{base_url}/reports"),
                ("Users", f"{base_url}/users"),
                ("Tasks", f"{base_url}/tasks"),
                ("Branch", f"{base_url}/branch"),
                ("Settings", f"{base_url}/settings"),
            ]
            
            for page_name, url in pages_to_inspect:
                try:
                    inspect_page(page, page_name, url)
                    page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"Error inspecting {page_name}: {e}\n")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            input("\nPress Enter to close browser...")
            browser.close()

if __name__ == "__main__":
    main()

