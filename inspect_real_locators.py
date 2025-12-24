"""Enhanced script to inspect actual page structure and find correct locators."""
import sys
import os
import json
from playwright.sync_api import sync_playwright
from config.config import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from pages.login_page import LoginPage

def get_element_info(locator):
    """Get comprehensive info about an element."""
    try:
        info = {
            'tag': locator.evaluate('el => el.tagName.toLowerCase()'),
            'id': locator.get_attribute('id') or '',
            'class': locator.get_attribute('class') or '',
            'name': locator.get_attribute('name') or '',
            'type': locator.get_attribute('type') or '',
            'placeholder': locator.get_attribute('placeholder') or '',
            'aria_label': locator.get_attribute('aria-label') or '',
            'data_testid': locator.get_attribute('data-testid') or '',
            'text': locator.inner_text().strip()[:50] if locator.is_visible() else '',
            'href': locator.get_attribute('href') or '',
            'visible': locator.is_visible(),
        }
        return info
    except:
        return None

def find_best_locator(elements, target_text=None, target_type=None):
    """Find the best locator strategy for elements."""
    locators = []
    for elem_info in elements:
        if not elem_info or not elem_info.get('visible'):
            continue
            
        strategies = []
        
        # Priority 1: data-testid
        if elem_info.get('data_testid'):
            strategies.append(f'[data-testid="{elem_info["data_testid"]}"]')
        
        # Priority 2: ID
        if elem_info.get('id'):
            strategies.append(f'#{elem_info["id"]}')
            strategies.append(f'[id="{elem_info["id"]}"]')
        
        # Priority 3: aria-label
        if elem_info.get('aria_label'):
            strategies.append(f'[aria-label="{elem_info["aria_label"]}"]')
        
        # Priority 4: name attribute
        if elem_info.get('name'):
            strategies.append(f'[name="{elem_info["name"]}"]')
        
        # Priority 5: text content (for buttons, links)
        if elem_info.get('text') and target_text and target_text.lower() in elem_info['text'].lower():
            if elem_info['tag'] in ['button', 'a']:
                strategies.append(f'{elem_info["tag"]}:has-text("{elem_info["text"]}")')
                strategies.append(f'text={elem_info["text"]}')
        
        # Priority 6: placeholder
        if elem_info.get('placeholder'):
            strategies.append(f'[placeholder="{elem_info["placeholder"]}"]')
        
        # Priority 7: class (as fallback)
        if elem_info.get('class'):
            class_parts = elem_info['class'].split()
            for cls in class_parts[:2]:  # First 2 classes
                if cls:
                    strategies.append(f'.{cls}')
        
        if strategies:
            locators.append({
                'strategies': strategies,
                'info': elem_info
            })
    
    return locators

def inspect_page_detailed(page, page_name: str, url: str):
    """Inspect a page in detail and find all locators."""
    print(f"\n{'='*80}")
    print(f"INSPECTING: {page_name}")
    print(f"URL: {url}")
    print(f"{'='*80}\n")
    
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.wait_for_timeout(3000)  # Wait for dynamic content
        
        print(f"Page Title: {page.title()}")
        print(f"Current URL: {page.url}\n")
        
        results = {
            'page_name': page_name,
            'url': page.url,
            'title': page.title(),
            'locators': {}
        }
        
        # Find headers
        print("--- HEADERS ---")
        headers = []
        for tag in ['h1', 'h2', 'h3']:
            elems = page.locator(tag).all()
            for elem in elems[:5]:
                info = get_element_info(elem)
                if info and info['visible']:
                    headers.append(info)
                    print(f"  {tag.upper()}: '{info['text']}'")
        
        if headers:
            results['locators']['header'] = find_best_locator(headers, target_text=page_name)
        
        # Find navigation links
        print("\n--- NAVIGATION LINKS ---")
        nav_links = []
        links = page.locator('a, button').all()
        nav_keywords = ['dashboard', 'tasks', 'reports', 'users', 'branch', 'branches', 'settings', 'logout', 'profile']
        
        for link in links:
            info = get_element_info(link)
            if info and info['visible']:
                text_lower = info['text'].lower()
                href_lower = (info.get('href') or '').lower()
                for keyword in nav_keywords:
                    if keyword in text_lower or keyword in href_lower:
                        nav_links.append((keyword, info))
                        print(f"  {keyword}: '{info['text']}' -> {info.get('href', '')}")
                        break
        
        # Find buttons
        print("\n--- BUTTONS ---")
        buttons = []
        button_elements = page.locator('button, [role="button"]').all()
        button_keywords = ['create', 'add', 'new', 'save', 'cancel', 'delete', 'edit', 'view', 'export', 'filter', 'search', 'next', 'previous']
        
        for btn in button_elements[:20]:
            info = get_element_info(btn)
            if info and info['visible']:
                buttons.append(info)
                text = info['text'][:30] if info['text'] else 'no text'
                print(f"  Button: '{text}' | id: {info.get('id', 'none')} | aria-label: {info.get('aria_label', 'none')}")
        
        # Find input fields
        print("\n--- INPUT FIELDS ---")
        inputs = []
        input_elements = page.locator('input, textarea, select').all()
        
        for inp in input_elements[:15]:
            info = get_element_info(inp)
            if info and info['visible']:
                inputs.append(info)
                inp_type = info.get('type') or info['tag']
                print(f"  {inp_type}: name='{info.get('name', '')}' id='{info.get('id', '')}' placeholder='{info.get('placeholder', '')}'")
        
        # Find tables
        print("\n--- TABLES ---")
        tables = page.locator('table').all()
        if tables:
            print(f"Found {len(tables)} table(s)")
            for i, table in enumerate(tables):
                try:
                    rows = table.locator('tbody tr, tr').count()
                    print(f"  Table {i+1}: {rows} rows")
                except:
                    pass
        
        # Find cards/list items
        print("\n--- CARDS/LIST ITEMS ---")
        card_selectors = [
            '[class*="card"]',
            '[class*="item"]',
            '[class*="row"]',
            'tbody tr',
            '[data-testid*="card"]',
            '[data-testid*="item"]'
        ]
        
        for selector in card_selectors:
            try:
                items = page.locator(selector).all()
                if items and len(items) > 0:
                    print(f"  Found {len(items)} items with selector: {selector}")
                    if len(items) <= 5:
                        for item in items:
                            try:
                                text = item.inner_text().strip()[:50] if item.is_visible() else ''
                                if text:
                                    print(f"    - {text}")
                            except:
                                pass
            except:
                pass
        
        # Find search inputs specifically
        print("\n--- SEARCH INPUTS ---")
        search_inputs = []
        search_selectors = [
            'input[type="search"]',
            'input[placeholder*="search" i]',
            'input[placeholder*="Search" i]',
            'input[name*="search" i]',
            'input[id*="search" i]'
        ]
        
        for selector in search_selectors:
            try:
                elems = page.locator(selector).all()
                for elem in elems:
                    info = get_element_info(elem)
                    if info and info['visible']:
                        search_inputs.append(info)
                        print(f"  Search: {selector} -> id: {info.get('id')} placeholder: {info.get('placeholder')}")
            except:
                pass
        
        # Find pagination
        print("\n--- PAGINATION ---")
        pagination_selectors = [
            '[class*="pagination"]',
            '[data-testid*="pagination"]',
            'button:has-text("Next")',
            'button:has-text("Previous")',
            '[aria-label*="next" i]',
            '[aria-label*="previous" i]'
        ]
        
        for selector in pagination_selectors:
            try:
                elems = page.locator(selector).all()
                if elems:
                    print(f"  Found pagination with: {selector}")
            except:
                pass
        
        # Find action menus
        print("\n--- ACTION MENUS ---")
        action_selectors = [
            '[data-testid*="action"]',
            '[aria-label*="action" i]',
            '[aria-label*="menu" i]',
            'button[aria-label*="more" i]',
            '[class*="menu"]'
        ]
        
        for selector in action_selectors:
            try:
                elems = page.locator(selector).all()
                if elems:
                    print(f"  Found action menu with: {selector}")
            except:
                pass
        
        print(f"\n{'='*80}\n")
        
        return results
        
    except Exception as e:
        print(f"Error inspecting {page_name}: {e}\n")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main inspection function."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()
        
        all_results = {}
        
        try:
            # Login first
            print("="*80)
            print("LOGGING IN...")
            print("="*80)
            login = LoginPage(page)
            login.open()
            page.wait_for_timeout(2000)
            
            # Check login page elements
            print("\n--- LOGIN PAGE ELEMENTS ---")
            email_inputs = page.locator('input[type="email"], input[id*="email" i], input[placeholder*="email" i], input[name*="email" i]').all()
            for inp in email_inputs:
                info = get_element_info(inp)
                if info:
                    print(f"Email input: id='{info.get('id')}' name='{info.get('name')}' placeholder='{info.get('placeholder')}'")
            
            # Try to find the actual email input
            all_inputs = page.locator('input').all()
            print(f"\nTotal inputs on login page: {len(all_inputs)}")
            for inp in all_inputs:
                info = get_element_info(inp)
                if info:
                    print(f"  Input: id='{info.get('id')}' type='{info.get('type')}' placeholder='{info.get('placeholder')}'")
            
            # Find Next button
            next_buttons = page.locator('button').all()
            for btn in next_buttons:
                info = get_element_info(btn)
                if info and 'next' in info.get('text', '').lower():
                    print(f"Next button: '{info['text']}' id='{info.get('id')}'")
            
            login.login(ADMIN_USERNAME, ADMIN_PASSWORD)
            
            # Wait for dashboard
            import time
            start_time = time.time()
            while time.time() - start_time < 20:
                if "/dashboard" in page.url:
                    break
                time.sleep(0.5)
            
            page.wait_for_timeout(3000)
            
            base_url = page.url.split('/dashboard')[0] if '/dashboard' in page.url else page.url
            
            # Inspect different pages
            pages_to_inspect = [
                ("Dashboard", f"{base_url}/dashboard"),
                ("Reports", f"{base_url}/reports"),
                ("Users", f"{base_url}/users"),
                ("Tasks", f"{base_url}/tasks"),
                ("Branch", f"{base_url}/branch"),
                ("Branches", f"{base_url}/branches"),
                ("Settings", f"{base_url}/settings"),
            ]
            
            for page_name, url in pages_to_inspect:
                try:
                    result = inspect_page_detailed(page, page_name, url)
                    if result:
                        all_results[page_name.lower()] = result
                    page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"Error inspecting {page_name}: {e}\n")
            
            # Save results to file
            with open('locator_inspection_results.json', 'w') as f:
                json.dump(all_results, f, indent=2)
            print("\nResults saved to locator_inspection_results.json")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            input("\nPress Enter to close browser...")
            browser.close()

if __name__ == "__main__":
    main()

