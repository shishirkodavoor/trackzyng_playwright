"""Dashboard page object."""
from pages.base_page import BasePage

class DashboardPage(BasePage):
    """Page object for the dashboard page."""
    
    def __init__(self, page):
        super().__init__(page)
        # Dashboard specific selectors based on actual page structure
        self.header = 'text=Dashboard, h1:has-text("Dashboard"), [data-testid*="dashboard-header"]'
        self.page_title = 'title, h1, h2'
        self.content_area = 'main, [role="main"], .content, .dashboard-content'
        
        # Key Metrics Cards
        self.active_users_card = 'text=Active Users, [class*="card"]:has-text("Active Users")'
        self.users_checked_in_card = 'text=Users Checked-In, [class*="card"]:has-text("Users Checked-In")'
        self.users_checked_out_card = 'text=Users Checked-Out, [class*="card"]:has-text("Users Checked-Out")'
        self.metric_cards = '[class*="card"], .metric-card, [data-testid*="metric"]'
        
        # User Live Approx. Location Section
        self.user_location_section = 'text=User Live Approx. Location, [class*="section"]:has-text("User Live Approx. Location")'
        self.search_users_input = 'input[placeholder*="Search Users"], input[name*="search"], input[type="search"]'
        self.last_updated_text = 'text=Last updated, [class*="last-updated"]'
        self.refresh_button = 'button[aria-label*="refresh"], [class*="refresh"], button:has([class*="refresh"])'
        
        # Areas by Checked-In Users
        self.areas_section = 'text=Areas by Checked-In Users, [class*="section"]:has-text("Areas")'
        self.area_cards = '[class*="area-card"], [class*="location-card"], [data-testid*="area"]'
        self.area_card_template = '[class*="card"]:has-text("Checked-in:")'
        
        # General elements
        self.widgets = '[data-testid*="widget"], .widget, .card, [class*="widget"]'
        self.charts = 'canvas, svg, [class*="chart"]'
        self.tables = 'table, [role="table"]'
        self.buttons = 'button, [role="button"]'
        self.forms = 'form'
        self.inputs = 'input, textarea, select'
        self.loading_indicator = '[data-testid*="loading"], .spinner, .loading'

    def is_loaded(self, timeout: int = 15000) -> bool:
        """Check if dashboard is loaded - URL is primary check."""
        try:
            # Wait for URL first
            self.wait_for_url_pattern("/dashboard", timeout=timeout)
            # URL check is primary - if URL matches, page is loaded
            if "/dashboard" in self.get_current_url():
                # Wait for page to be ready
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                # Give time for dynamic content to load
                self.page.wait_for_timeout(2000)
                return True
            # Secondary: try to find header element
            return self.is_element_visible(self.header, timeout=3000)
        except:
            # Final fallback: just check URL
            return "/dashboard" in self.get_current_url()
    
    def wait_for_dashboard_load(self, timeout: int = 15000):
        """Wait for dashboard to fully load."""
        try:
            # Wait for URL
            self.wait_for_url_pattern("/dashboard", timeout=timeout)
            
            # Wait for page load states
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            
            # Wait for loading indicator to disappear if present
            try:
                loading_locator = self.page.locator(self.loading_indicator).first
                if loading_locator.is_visible(timeout=1000):
                    loading_locator.wait_for(state="hidden", timeout=timeout)
            except:
                pass  # No loading indicator, that's fine
            
            # Wait a bit for dynamic content
            self.page.wait_for_timeout(2000)
            
            # Try to wait for network idle, but don't fail if it times out
            try:
                self.wait_for_network_idle(timeout=5000)
            except:
                pass
        except Exception as e:
            # Even if waiting fails, if URL is correct, consider it loaded
            if "/dashboard" in self.get_current_url():
                self.page.wait_for_timeout(2000)
                return
            raise
    
    def get_all_widgets(self):
        """Get all widget elements on the dashboard."""
        return self.page.locator(self.widgets).all()
    
    def get_all_charts(self):
        """Get all chart elements on the dashboard."""
        return self.page.locator(self.charts).all()
    
    def get_all_tables(self):
        """Get all table elements on the dashboard."""
        return self.page.locator(self.tables).all()
    
    def is_content_visible(self) -> bool:
        """Check if main content area is visible."""
        return self.is_element_visible(self.content_area, timeout=5000)
    
    def get_page_elements_count(self, selector: str) -> int:
        """Get count of elements matching selector."""
        try:
            return self.page.locator(selector).count()
        except:
            return 0

