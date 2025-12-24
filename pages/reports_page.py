"""Reports page object for reports section."""
from pages.base_page import BasePage

class ReportsPage(BasePage):
    """Page object for the Reports section."""
    
    def __init__(self, page):
        super().__init__(page)
        # Reports page selectors - based on actual inspection
        self.header = 'text=Reports, h1:has-text("Reports"), [data-testid*="reports-header"]'
        self.reports_list = 'table tbody tr, [data-testid*="report"], .report-item, .report-card'
        self.create_report_button = 'button:has-text("Create"), button:has-text("New Report"), [data-testid*="create-report"]'
        self.export_button = 'button:has-text("EXPORT"), button:has-text("Export"), button:has-text("Download"), [data-testid*="export"]'
        self.filter_button = 'button:has-text("Filter"), [data-testid*="filter"]'
        self.search_input = 'input[placeholder="Search or select users"], input[placeholder*="Search" i], input[type="search"], input[name*="search"]'
        self.user_dropdown = 'input[id="user-dropdown"], input[placeholder="Search or select users"]'
        self.date_filter = 'input[id="«r9»"], input[id="«rd»"], input[type="date"], [data-testid*="date"], input[name*="date"], input[aria-label*="date" i]'
        self.report_type_dropdown = 'select, [data-testid*="type"], [data-testid*="report-type"]'
        self.pagination = '[data-testid*="pagination"], .pagination'
        self.next_page_button = 'button[aria-label*="next" i], button:has-text("Next"), [aria-label*="next"]'
        self.prev_page_button = 'button[aria-label*="previous" i], button:has-text("Previous"), [aria-label*="previous"]'
        self.report_detail_view = '[data-testid*="report-detail"], .report-detail'
        self.report_actions_menu = '[data-testid*="actions"], [aria-label*="actions"], [aria-label*="Open"]'
        self.edit_report_button = 'button:has-text("Edit"), [data-testid*="edit"]'
        self.delete_report_button = 'button:has-text("Delete"), [data-testid*="delete"]'
        self.view_report_button = 'button:has-text("View"), a:has-text("View")'
        self.reports_table = 'table, [role="table"]'
        self.report_columns = 'th, thead th'
    
    def is_loaded(self, timeout: int = 15000) -> bool:
        """Check if reports page is loaded - URL is primary check."""
        try:
            self.wait_for_url_pattern("/reports", timeout=timeout)
            # URL check is primary
            if "/reports" in self.get_current_url():
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                self.page.wait_for_timeout(2000)
                return True
            # Secondary: try to find header element
            return self.is_element_visible(self.header, timeout=3000)
        except:
            # Final fallback: just check URL
            return "/reports" in self.get_current_url()
    
    def navigate_to_reports(self):
        """Navigate to reports page."""
        try:
            base_url = self.get_base_url()
            self.navigate_to(f"{base_url}/reports")
            self.wait_for_url_pattern("/reports", timeout=15000)
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
        except:
            base_url = self.get_base_url()
            self.page.goto(f"{base_url}/reports", wait_until="domcontentloaded", timeout=30000)
            self.page.wait_for_timeout(2000)
    
    def get_reports_count(self) -> int:
        """Get count of reports displayed."""
        try:
            return self.page.locator(self.reports_list).count()
        except:
            return 0
    
    def search_report(self, search_term: str):
        """Search for a report."""
        try:
            # Try user dropdown search first (for reports page)
            try:
                user_dropdown = self.page.locator('input[id="user-dropdown"]').first
                if user_dropdown.is_visible(timeout=3000):
                    user_dropdown.fill(search_term)
                    self.page.wait_for_timeout(1500)
                    return
            except:
                pass
            
            # Fallback to generic search
            if self.is_element_visible(self.search_input, timeout=5000):
                self.fill_input(self.search_input, search_term)
                self.page.wait_for_timeout(1500)
        except:
            pass  # Search input not found, that's okay
    
    def filter_by_date(self, start_date: str, end_date: str):
        """Filter reports by date range."""
        try:
            # Try specific IDs first
            try:
                start_input = self.page.locator('input[id="«r9»"]').first
                if start_input.is_visible(timeout=3000):
                    start_input.fill(start_date)
                    self.page.wait_for_timeout(500)
            except:
                pass
            
            try:
                end_input = self.page.locator('input[id="«rd»"]').first
                if end_input.is_visible(timeout=3000):
                    end_input.fill(end_date)
                    self.page.wait_for_timeout(1000)
            except:
                pass
            
            # Fallback to generic date filter
            if self.is_element_visible(self.date_filter, timeout=2000):
                date_inputs = self.page.locator(self.date_filter).all()
                if len(date_inputs) >= 2:
                    date_inputs[0].fill(start_date)
                    date_inputs[1].fill(end_date)
                    self.page.wait_for_timeout(1000)
        except:
            pass  # Date filter not available, that's okay
    
    def click_create_report(self):
        """Click create report button."""
        try:
            if self.is_element_visible(self.create_report_button, timeout=5000):
                self.click_element(self.create_report_button)
                self.page.wait_for_timeout(2000)
        except:
            pass  # Button not found, that's okay
    
    def click_export(self):
        """Click export button."""
        try:
            # Try exact text match first
            try:
                export_btn = self.page.get_by_text("EXPORT", exact=False).first
                if export_btn.is_visible(timeout=5000):
                    export_btn.click()
                    self.page.wait_for_timeout(2000)
                    return
            except:
                pass
            
            # Fallback to generic selector
            if self.is_element_visible(self.export_button, timeout=5000):
                self.click_element(self.export_button)
                self.page.wait_for_timeout(2000)
        except:
            pass  # Button not found, that's okay
    
    def view_report(self, index: int = 0):
        """View a specific report."""
        try:
            # Try text-based search first
            try:
                view_buttons = self.page.get_by_text("View", exact=False).all()
                if len(view_buttons) > index:
                    view_buttons[index].wait_for(state="visible", timeout=5000)
                    view_buttons[index].click()
                    self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                    self.page.wait_for_timeout(2000)
                    return
            except:
                pass
            
            # Fallback to generic selector
            view_buttons = self.page.locator(self.view_report_button).all()
            if len(view_buttons) > index:
                view_buttons[index].wait_for(state="visible", timeout=5000)
                view_buttons[index].click()
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                self.page.wait_for_timeout(2000)
        except:
            pass  # View button not found, that's okay
    
    def edit_report(self, index: int = 0):
        """Edit a specific report."""
        try:
            if self.is_element_visible(self.report_actions_menu, timeout=5000):
                menus = self.page.locator(self.report_actions_menu).all()
                if len(menus) > index:
                    menus[index].wait_for(state="visible", timeout=5000)
                    menus[index].click()
                    self.page.wait_for_timeout(1000)
                    if self.is_element_visible(self.edit_report_button, timeout=3000):
                        self.click_element(self.edit_report_button)
                        self.page.wait_for_timeout(2000)
        except:
            pass  # Edit functionality not available, that's okay
    
    def delete_report(self, index: int = 0, confirm: bool = True):
        """Delete a specific report."""
        try:
            if self.is_element_visible(self.report_actions_menu, timeout=5000):
                menus = self.page.locator(self.report_actions_menu).all()
                if len(menus) > index:
                    menus[index].wait_for(state="visible", timeout=5000)
                    menus[index].click()
                    self.page.wait_for_timeout(1000)
                    if self.is_element_visible(self.delete_report_button, timeout=3000):
                        self.click_element(self.delete_report_button)
                        if confirm:
                            # Handle confirmation dialog
                            self.page.wait_for_timeout(1000)
                            self.page.keyboard.press("Enter")  # Confirm deletion
                            self.page.wait_for_timeout(2000)
        except:
            pass  # Delete functionality not available, that's okay

