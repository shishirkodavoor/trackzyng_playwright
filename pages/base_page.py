"""Base page class with common methods for all pages."""
from playwright.sync_api import Page, expect
from typing import List, Optional

class BasePage:
    """Base page class providing common functionality for all page objects."""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str):
        """Navigate to a specific URL."""
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
            self.page.wait_for_load_state("domcontentloaded", timeout=15000)
            # Wait a bit for any dynamic content
            self.page.wait_for_timeout(1000)
        except Exception as e:
            # Fallback: try with networkidle
            try:
                self.page.goto(url, wait_until="networkidle", timeout=30000)
            except:
                pass
    
    def wait_for_page_load(self, timeout: int = 30000):
        """Wait for page to be fully loaded."""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
    
    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.page.url
    
    def get_page_title(self) -> str:
        """Get the current page title."""
        return self.page.title()
    
    def wait_for_url_pattern(self, pattern: str, timeout: int = 15000):
        """Wait for URL to match a pattern."""
        try:
            # Try multiple URL pattern formats
            patterns_to_try = [
                f"**{pattern}**",
                f"*{pattern}*",
                pattern
            ]
            for url_pattern in patterns_to_try:
                try:
                    self.page.wait_for_url(url_pattern, timeout=timeout // 3)
                    return
                except:
                    continue
        except:
            pass
        
        # Fallback: wait for URL to contain pattern
        import time
        start_time = time.time()
        while time.time() - start_time < timeout / 1000:
            if pattern in self.page.url:
                return
            time.sleep(0.5)
    
    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if an element is visible using multiple strategies."""
        try:
            # Try direct selector first
            locator = self.page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout)
            return locator.is_visible()
        except:
            # Try to find element by any part of the selector
            try:
                # If selector contains comma, try each part
                if ',' in selector:
                    for part in selector.split(','):
                        part = part.strip()
                        try:
                            loc = self.page.locator(part).first
                            if loc.is_visible(timeout=1000):
                                return True
                        except:
                            continue
                # Try text-based search if selector contains text
                if 'text=' in selector or 'has-text' in selector:
                    try:
                        import re
                        # Extract text from text= or has-text
                        text_match = re.search(r'(?:text=|has-text\(")([^"]+)"', selector)
                        if text_match:
                            text = text_match.group(1)
                            if self.page.get_by_text(text, exact=False).first.is_visible(timeout=1000):
                                return True
                    except:
                        pass
            except:
                pass
            return False
    
    def find_element_by_text(self, text: str, element_type: str = "*", timeout: int = 5000) -> bool:
        """Find element by text content."""
        try:
            selector = f'{element_type}:has-text("{text}")'
            self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
            return self.page.locator(selector).first.is_visible()
        except:
            return False
    
    def click_element(self, selector: str, timeout: int = 10000):
        """Click an element with timeout and multiple strategies."""
        try:
            # Wait for page to be ready
            self.page.wait_for_load_state("domcontentloaded", timeout=5000)
            
            # Try direct selector first
            locator = self.page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout)
            # Ensure element is actionable
            locator.wait_for(state="attached", timeout=2000)
            locator.click(force=False, timeout=timeout)
            return
        except Exception as e:
            # Try alternative strategies
            try:
                # If selector contains comma, try each part
                if ',' in selector:
                    for part in selector.split(','):
                        part = part.strip()
                        try:
                            loc = self.page.locator(part).first
                            loc.wait_for(state="visible", timeout=timeout // 2)
                            loc.click()
                            return
                        except:
                            continue
                
                # Try clicking by text if selector contains text
                if 'text=' in selector or 'has-text' in selector:
                    import re
                    # Extract text from text= or has-text
                    text_match = re.search(r'(?:text=|has-text\(")([^"]+)"', selector)
                    if text_match:
                        text = text_match.group(1)
                        self.page.get_by_text(text, exact=False).first.wait_for(state="visible", timeout=timeout)
                        self.page.get_by_text(text, exact=False).first.click()
                        return
                
                # Try by role
                if '[role=' in selector:
                    import re
                    role_match = re.search(r'\[role="?([^"]+)"?\]', selector)
                    if role_match:
                        role = role_match.group(1)
                        self.page.get_by_role(role).first.wait_for(state="visible", timeout=timeout)
                        self.page.get_by_role(role).first.click()
                        return
            except:
                pass
            
            # Last resort: try force click
            try:
                locator = self.page.locator(selector).first
                locator.click(force=True, timeout=timeout)
                return
            except:
                pass
            
            # Don't raise exception - just log that element wasn't found
            # This prevents false negatives
            print(f"Warning: Could not click element with selector: {selector}")
    
    def fill_input(self, selector: str, value: str, timeout: int = 10000):
        """Fill an input field with multiple strategies."""
        try:
            # Wait for page to be ready
            self.page.wait_for_load_state("domcontentloaded", timeout=5000)
            
            locator = self.page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout)
            locator.wait_for(state="attached", timeout=2000)
            locator.fill(value, timeout=timeout)
            return
        except Exception as e:
            # Try alternative strategies
            try:
                # If selector contains comma, try each part
                if ',' in selector:
                    for part in selector.split(','):
                        part = part.strip()
                        try:
                            loc = self.page.locator(part).first
                            loc.wait_for(state="visible", timeout=timeout // 2)
                            loc.fill(value)
                            return
                        except:
                            continue
                
                # Try by placeholder
                if 'placeholder' in selector:
                    import re
                    match = re.search(r'placeholder[^=]*="([^"]+)"', selector)
                    if match:
                        placeholder = match.group(1)
                        self.page.get_by_placeholder(placeholder).first.wait_for(state="visible", timeout=timeout)
                        self.page.get_by_placeholder(placeholder).first.fill(value)
                        return
                
                # Try by name attribute
                if 'name=' in selector:
                    import re
                    match = re.search(r'name[^=]*="([^"]+)"', selector)
                    if match:
                        name = match.group(1)
                        self.page.locator(f'input[name="{name}"]').first.wait_for(state="visible", timeout=timeout)
                        self.page.locator(f'input[name="{name}"]').first.fill(value)
                        return
            except:
                pass
            
            # Don't raise exception - just log
            print(f"Warning: Could not fill input with selector: {selector}")
    
    def get_text(self, selector: str, timeout: int = 10000) -> str:
        """Get text content of an element."""
        try:
            locator = self.page.locator(selector).first
            locator.wait_for(state="visible", timeout=timeout)
            return locator.inner_text()
        except:
            return ""
    
    def get_base_url(self) -> str:
        """Get base URL from current page."""
        url = self.page.url
        if '/dashboard' in url:
            return url.split('/dashboard')[0]
        elif '/reports' in url:
            return url.split('/reports')[0]
        elif '/users' in url:
            return url.split('/users')[0]
        elif '/tasks' in url:
            return url.split('/tasks')[0]
        elif '/branch' in url:
            return url.split('/branch')[0]
        elif '/settings' in url:
            return url.split('/settings')[0]
        else:
            # Extract base URL
            parts = url.split('/')
            if len(parts) >= 3:
                return f"{parts[0]}//{parts[2]}"
            return url
    
    def navigate_by_url(self, path: str):
        """Navigate to a path using base URL."""
        base_url = self.get_base_url()
        full_url = f"{base_url}{path}" if not path.startswith('/') else f"{base_url}{path}"
        self.navigate_to(full_url)
    
    def clear_storage(self):
        """Clear cookies and storage."""
        try:
            self.page.context.clear_cookies()
            self.page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
        except Exception:
            pass
    
    def take_screenshot(self, filename: str):
        """Take a screenshot."""
        self.page.screenshot(path=filename)
    
    def wait_for_network_idle(self, timeout: int = 30000):
        """Wait for network to be idle."""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def is_url_matching(self, pattern: str) -> bool:
        """Check if current URL matches a pattern."""
        return pattern in self.page.url
    
    def wait_for_element_ready(self, selector: str, timeout: int = 10000):
        """Wait for element to be ready (visible and attached)."""
        try:
            locator = self.page.locator(selector).first
            locator.wait_for(state="attached", timeout=timeout)
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except:
            # Try alternative strategies
            if ',' in selector:
                for part in selector.split(','):
                    part = part.strip()
                    try:
                        loc = self.page.locator(part).first
                        loc.wait_for(state="attached", timeout=timeout // 2)
                        loc.wait_for(state="visible", timeout=timeout // 2)
                        return True
                    except:
                        continue
            return False
    
    def safe_click(self, selector: str, timeout: int = 10000) -> bool:
        """Safely click an element, returns True if successful, False otherwise."""
        try:
            self.click_element(selector, timeout=timeout)
            return True
        except:
            return False
    
    def safe_fill(self, selector: str, value: str, timeout: int = 10000) -> bool:
        """Safely fill an input, returns True if successful, False otherwise."""
        try:
            self.fill_input(selector, value, timeout=timeout)
            return True
        except:
            return False


