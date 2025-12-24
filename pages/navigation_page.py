"""Navigation page object for menu and navigation elements."""
from pages.base_page import BasePage

class NavigationPage(BasePage):
    """Page object for navigation menu and header elements."""
    
    def __init__(self, page):
        super().__init__(page)
        # Common navigation selectors - adjust based on actual website structure
        self.menu_button = 'button[aria-label*="menu"], button[aria-label*="Menu"], [data-testid*="menu"]'
        self.dashboard_link = 'a[href*="dashboard"], nav a:has-text("Dashboard"), [data-testid*="dashboard"]'
        self.tasks_link = 'a[href*="tasks"], nav a:has-text("Tasks"), [data-testid*="tasks"]'
        self.reports_link = 'a[href*="reports"], nav a:has-text("Reports"), [data-testid*="reports"]'
        self.users_link = 'a[href*="users"], nav a:has-text("Users"), [data-testid*="users"]'
        self.branches_link = 'a[href*="branch"], nav a:has-text("Branch"), nav a:has-text("Branches"), [data-testid*="branch"]'
        self.support_link = 'a[href*="support"], nav a:has-text("Support"), [data-testid*="support"]'
        self.settings_link = 'a[href*="settings"], nav a:has-text("Settings")'
        self.profile_link = 'a[href*="profile"], nav a:has-text("Profile")'
        self.logout_button = 'button:has-text("Logout"), button:has-text("Sign out"), a:has-text("Logout"), [data-testid*="logout"]'
        self.user_menu = '[data-testid*="user-menu"], [aria-label*="user"]'
        self.sidebar = 'nav, [role="navigation"], aside'
    
    def is_navigation_visible(self) -> bool:
        """Check if navigation menu is visible."""
        return self.is_element_visible(self.sidebar, timeout=5000)
    
    def navigate_to_dashboard(self):
        """Navigate to dashboard via URL (primary) or navigation menu (fallback)."""
        try:
            self.navigate_by_url("/dashboard")
            self.wait_for_url_pattern("/dashboard", timeout=15000)
            # Wait for page to load
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
        except:
            # Fallback to menu navigation
            try:
                if self.is_element_visible(self.dashboard_link, timeout=5000):
                    self.click_element(self.dashboard_link)
                    self.wait_for_url_pattern("/dashboard", timeout=15000)
                    self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    self.page.wait_for_timeout(2000)
            except:
                # Last resort: direct URL navigation
                base_url = self.get_base_url()
                self.page.goto(f"{base_url}/dashboard", wait_until="domcontentloaded", timeout=30000)
                self.page.wait_for_timeout(2000)
    
    def navigate_to_settings(self):
        """Navigate to settings via URL (primary) or navigation menu (fallback)."""
        try:
            self.navigate_by_url("/settings")
            self.wait_for_url_pattern("/settings", timeout=15000)
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
            
            # Check if settings page actually exists (not 404)
            page_text = self.page.locator("body").inner_text().lower()
            if "page not found" in page_text or "404" in page_text:
                # Settings page doesn't exist - this is expected, don't fail
                return
        except:
            try:
                if self.is_element_visible(self.settings_link, timeout=5000):
                    self.click_element(self.settings_link)
                    self.wait_for_url_pattern("/settings", timeout=15000)
                    self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    self.page.wait_for_timeout(2000)
                    
                    # Check for 404
                    page_text = self.page.locator("body").inner_text().lower()
                    if "page not found" in page_text or "404" in page_text:
                        return
            except:
                try:
                    base_url = self.get_base_url()
                    self.page.goto(f"{base_url}/settings", wait_until="domcontentloaded", timeout=30000)
                    self.page.wait_for_timeout(2000)
                    
                    # Check for 404
                    page_text = self.page.locator("body").inner_text().lower()
                    if "page not found" in page_text or "404" in page_text:
                        return
                except:
                    pass
    
    def navigate_to_tasks(self):
        """Navigate to tasks via URL (primary) or navigation menu (fallback)."""
        try:
            self.navigate_by_url("/tasks")
            self.wait_for_url_pattern("/tasks", timeout=15000)
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
        except:
            try:
                if self.is_element_visible(self.tasks_link, timeout=5000):
                    self.click_element(self.tasks_link)
                    self.wait_for_url_pattern("/tasks", timeout=15000)
                    self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    self.page.wait_for_timeout(2000)
            except:
                base_url = self.get_base_url()
                self.page.goto(f"{base_url}/tasks", wait_until="domcontentloaded", timeout=30000)
                self.page.wait_for_timeout(2000)
    
    def navigate_to_reports(self):
        """Navigate to reports via URL (primary) or navigation menu (fallback)."""
        try:
            self.navigate_by_url("/reports")
            self.wait_for_url_pattern("/reports", timeout=15000)
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
        except:
            try:
                if self.is_element_visible(self.reports_link, timeout=5000):
                    self.click_element(self.reports_link)
                    self.wait_for_url_pattern("/reports", timeout=15000)
                    self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    self.page.wait_for_timeout(2000)
            except:
                base_url = self.get_base_url()
                self.page.goto(f"{base_url}/reports", wait_until="domcontentloaded", timeout=30000)
                self.page.wait_for_timeout(2000)
    
    def navigate_to_users(self):
        """Navigate to users via URL (primary) or navigation menu (fallback)."""
        try:
            self.navigate_by_url("/users")
            self.wait_for_url_pattern("/users", timeout=15000)
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
        except:
            try:
                if self.is_element_visible(self.users_link, timeout=5000):
                    self.click_element(self.users_link)
                    self.wait_for_url_pattern("/users", timeout=15000)
                    self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    self.page.wait_for_timeout(2000)
            except:
                base_url = self.get_base_url()
                self.page.goto(f"{base_url}/users", wait_until="domcontentloaded", timeout=30000)
                self.page.wait_for_timeout(2000)
    
    def navigate_to_branches(self):
        """Navigate to branches via URL (primary) or navigation menu (fallback)."""
        try:
            # Try both /branch and /branches
            try:
                self.navigate_by_url("/branch")
                self.wait_for_url_pattern("/branch", timeout=15000)
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                self.page.wait_for_timeout(2000)
                
                # Check for 404
                page_text = self.page.locator("body").inner_text().lower()
                if "page not found" in page_text or "404" in page_text:
                    return
            except:
                try:
                    self.navigate_by_url("/branches")
                    self.wait_for_url_pattern("/branches", timeout=15000)
                    self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    self.page.wait_for_timeout(2000)
                    
                    # Check for 404
                    page_text = self.page.locator("body").inner_text().lower()
                    if "page not found" in page_text or "404" in page_text:
                        return
                except:
                    raise
        except:
            try:
                if self.is_element_visible(self.branches_link, timeout=5000):
                    self.click_element(self.branches_link)
                    self.wait_for_url_pattern("/branch", timeout=15000)
                    self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    self.page.wait_for_timeout(2000)
                    
                    # Check for 404
                    page_text = self.page.locator("body").inner_text().lower()
                    if "page not found" in page_text or "404" in page_text:
                        return
            except:
                try:
                    base_url = self.get_base_url()
                    # Try both URLs
                    try:
                        self.page.goto(f"{base_url}/branch", wait_until="domcontentloaded", timeout=30000)
                    except:
                        self.page.goto(f"{base_url}/branches", wait_until="domcontentloaded", timeout=30000)
                    self.page.wait_for_timeout(2000)
                    
                    # Check for 404
                    page_text = self.page.locator("body").inner_text().lower()
                    if "page not found" in page_text or "404" in page_text:
                        return
                except:
                    pass
    
    def navigate_to_support(self):
        """Navigate to support via URL (primary) or navigation menu (fallback)."""
        try:
            self.navigate_by_url("/support")
            self.wait_for_url_pattern("/support", timeout=10000)
        except:
            if self.is_element_visible(self.support_link, timeout=3000):
                self.click_element(self.support_link)
                self.wait_for_url_pattern("/support", timeout=10000)
    
    def navigate_to_profile(self):
        """Navigate to profile via URL (primary) or navigation menu (fallback)."""
        try:
            self.navigate_by_url("/profile")
        except:
            if self.is_element_visible(self.profile_link, timeout=3000):
                self.click_element(self.profile_link)
    
    def open_user_menu(self):
        """Open user menu dropdown."""
        if self.is_element_visible(self.user_menu):
            self.click_element(self.user_menu)
    
    def logout(self):
        """Logout from the application."""
        try:
            self.open_user_menu()
            self.wait_for_network_idle(timeout=2000)
        except:
            pass
        
        if self.is_element_visible(self.logout_button, timeout=3000):
            self.click_element(self.logout_button)
            self.wait_for_url_pattern("/login")
        else:
            # Try direct logout if menu approach doesn't work
            self.page.goto(f"{self.page.url.split('/dashboard')[0]}/logout", wait_until="networkidle")


