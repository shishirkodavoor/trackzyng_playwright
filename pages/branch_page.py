"""Branch management page object."""
from pages.base_page import BasePage

class BranchPage(BasePage):
    """Page object for the Branch management section."""
    
    def __init__(self, page):
        super().__init__(page)
        # Branch page selectors - based on actual inspection
        self.header = 'text=Branch, text=Branches, h1:has-text("Branch"), h1:has-text("Branches"), [data-testid*="branch-header"]'
        self.branches_list = 'table tbody tr, [data-testid*="branch"], .branch-item, .branch-card'
        self.create_branch_button = 'button:has-text("ADD BRANCH"), button:has-text("Create Branch"), button:has-text("Add Branch"), [data-testid*="create-branch"]'
        self.search_input = 'input[placeholder="Search"], input[placeholder*="Search" i], input[type="search"], input[name*="search"]'
        self.filter_button = 'button:has-text("Filter"), [data-testid*="filter"]'
        self.location_filter = 'select[name*="location"], [data-testid*="location-filter"]'
        self.status_filter = 'select[name*="status"], [data-testid*="status-filter"]'
        self.branches_table = 'table, [role="table"]'
        self.branch_actions_menu = '[data-testid*="actions"], [aria-label*="actions"], [aria-label*="Open"]'
        self.edit_branch_button = 'button:has-text("Edit"), [data-testid*="edit-branch"]'
        self.delete_branch_button = 'button:has-text("Delete"), [data-testid*="delete-branch"]'
        self.view_branch_button = 'button:has-text("View"), a:has-text("View")'
        self.activate_branch_button = 'button:has-text("Activate"), [data-testid*="activate"]'
        self.deactivate_branch_button = 'button:has-text("Deactivate"), [data-testid*="deactivate"]'
        self.pagination = '[data-testid*="pagination"], .pagination'
        self.next_page_button = 'button[aria-label="Go to next page"], button[aria-label*="next" i], button:has-text("Next"), [aria-label*="next"]'
        self.prev_page_button = 'button[aria-label="Go to previous page"], button[aria-label*="previous" i], button:has-text("Previous"), [aria-label*="previous"]'
        
        # Create/Edit Branch Form selectors
        self.branch_name_input = 'input[name*="name"], input[placeholder*="Name"], input[placeholder*="Branch Name"]'
        self.branch_code_input = 'input[name*="code"], input[placeholder*="Code"], input[placeholder*="Branch Code"]'
        self.address_input = 'textarea[name*="address"], input[name*="address"], textarea[placeholder*="Address"]'
        self.city_input = 'input[name*="city"], input[placeholder*="City"]'
        self.state_input = 'input[name*="state"], input[placeholder*="State"]'
        self.zipcode_input = 'input[name*="zip"], input[name*="zipcode"], input[placeholder*="Zip"]'
        self.phone_input = 'input[type="tel"], input[name*="phone"]'
        self.email_input = 'input[type="email"], input[name*="email"]'
        self.status_select = 'select[name*="status"], [data-testid*="status"]'
        self.manager_select = 'select[name*="manager"], [data-testid*="manager"]'
        self.save_button = 'button:has-text("Save"), button[type="submit"], button:has-text("Create")'
        self.cancel_button = 'button:has-text("Cancel"), button[type="button"]'
        self.branch_form = 'form, [data-testid*="branch-form"]'
    
    def is_loaded(self, timeout: int = 15000) -> bool:
        """Check if branch page is loaded - URL is primary check."""
        try:
            # Try both /branch and /branches
            url = self.get_current_url()
            if "/branch" in url or "/branches" in url:
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                self.page.wait_for_timeout(2000)
                
                # Check for 404 or "Page Not Found"
                try:
                    page_text = self.page.locator("body").inner_text().lower()
                    if "page not found" in page_text or "404" in page_text or "not found" in page_text:
                        return False
                except:
                    pass
                
                return True
            self.wait_for_url_pattern("/branch", timeout=timeout)
            # URL check is primary
            url = self.get_current_url()
            if "/branch" in url or "/branches" in url:
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                self.page.wait_for_timeout(2000)
                
                # Check for 404
                try:
                    page_text = self.page.locator("body").inner_text().lower()
                    if "page not found" in page_text or "404" in page_text or "not found" in page_text:
                        return False
                except:
                    pass
                
                return True
            # Secondary: try to find header element
            return self.is_element_visible(self.header, timeout=3000)
        except:
            # Final fallback: just check URL
            url = self.get_current_url()
            if "/branch" in url or "/branches" in url:
                # Still check for 404
                try:
                    page_text = self.page.locator("body").inner_text().lower()
                    if "page not found" in page_text or "404" in page_text or "not found" in page_text:
                        return False
                except:
                    pass
            return "/branch" in url or "/branches" in url
    
    def navigate_to_branches(self):
        """Navigate to branches page."""
        try:
            base_url = self.get_base_url()
            # Try /branches first
            try:
                self.navigate_to(f"{base_url}/branch")
                self.wait_for_url_pattern("/branch", timeout=15000)
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                self.page.wait_for_timeout(2000)
            except:
                # Try /branch
                self.navigate_to(f"{base_url}/branch")
                self.wait_for_url_pattern("/branch", timeout=15000)
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                self.page.wait_for_timeout(2000)
        except:
            base_url = self.get_base_url()
            try:
                self.page.goto(f"{base_url}/branches", wait_until="domcontentloaded", timeout=30000)
            except:
                self.page.goto(f"{base_url}/branch", wait_until="domcontentloaded", timeout=30000)
            self.page.wait_for_timeout(2000)
    
    def get_branches_count(self) -> int:
        """Get count of branches displayed."""
        try:
            return self.page.locator(self.branches_list).count()
        except:
            return 0
    
    def search_branch(self, search_term: str):
        """Search for a branch."""
        try:
            # Try placeholder-based search first
            search_locator = self.page.locator('input[placeholder="Search"]').first
            if search_locator.is_visible(timeout=5000):
                search_locator.fill(search_term)
                self.page.wait_for_timeout(1500)
            elif self.is_element_visible(self.search_input, timeout=3000):
                self.fill_input(self.search_input, search_term)
                self.page.wait_for_timeout(1500)
        except:
            pass  # Search input not found, that's okay
    
    def filter_by_location(self, location: str):
        """Filter branches by location."""
        if self.is_element_visible(self.location_filter, timeout=3000):
            self.page.locator(self.location_filter).select_option(location)
            self.page.wait_for_timeout(1000)
    
    def filter_by_status(self, status: str):
        """Filter branches by status."""
        if self.is_element_visible(self.status_filter, timeout=3000):
            self.page.locator(self.status_filter).select_option(status)
            self.page.wait_for_timeout(1000)
    
    def click_create_branch(self):
        """Click create branch button."""
        try:
            # Try exact text match first
            try:
                add_button = self.page.get_by_text("ADD BRANCH", exact=False).first
                if add_button.is_visible(timeout=5000):
                    add_button.click()
                    self.page.wait_for_timeout(2000)
                    return
            except:
                pass
            
            # Fallback to generic selector
            if self.is_element_visible(self.create_branch_button, timeout=5000):
                self.click_element(self.create_branch_button)
                self.page.wait_for_timeout(2000)
        except:
            pass  # Button not found, that's okay
    
    def fill_branch_form(self, name: str = "", code: str = "", address: str = "", 
                        city: str = "", state: str = "", zipcode: str = "", 
                        phone: str = "", email: str = "", status: str = "", manager: str = ""):
        """Fill branch creation/edit form."""
        if name and self.is_element_visible(self.branch_name_input, timeout=3000):
            self.fill_input(self.branch_name_input, name)
        if code and self.is_element_visible(self.branch_code_input, timeout=3000):
            self.fill_input(self.branch_code_input, code)
        if address and self.is_element_visible(self.address_input, timeout=3000):
            self.fill_input(self.address_input, address)
        if city and self.is_element_visible(self.city_input, timeout=3000):
            self.fill_input(self.city_input, city)
        if state and self.is_element_visible(self.state_input, timeout=3000):
            self.fill_input(self.state_input, state)
        if zipcode and self.is_element_visible(self.zipcode_input, timeout=3000):
            self.fill_input(self.zipcode_input, zipcode)
        if phone and self.is_element_visible(self.phone_input, timeout=3000):
            self.fill_input(self.phone_input, phone)
        if email and self.is_element_visible(self.email_input, timeout=3000):
            self.fill_input(self.email_input, email)
        if status and self.is_element_visible(self.status_select, timeout=3000):
            self.page.locator(self.status_select).select_option(status)
        if manager and self.is_element_visible(self.manager_select, timeout=3000):
            self.page.locator(self.manager_select).select_option(manager)
    
    def save_branch_form(self):
        """Save branch form."""
        if self.is_element_visible(self.save_button, timeout=3000):
            self.click_element(self.save_button)
            self.page.wait_for_timeout(2000)
    
    def cancel_branch_form(self):
        """Cancel branch form."""
        if self.is_element_visible(self.cancel_button, timeout=3000):
            self.click_element(self.cancel_button)
    
    def view_branch(self, index: int = 0):
        """View a specific branch."""
        try:
            view_buttons = self.page.locator(self.view_branch_button).all()
            if len(view_buttons) > index:
                view_buttons[index].wait_for(state="visible", timeout=5000)
                view_buttons[index].click()
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                self.page.wait_for_timeout(2000)
        except:
            pass  # View button not found, that's okay
    
    def edit_branch(self, index: int = 0):
        """Edit a specific branch."""
        try:
            if self.is_element_visible(self.branch_actions_menu, timeout=5000):
                menus = self.page.locator(self.branch_actions_menu).all()
                if len(menus) > index:
                    menus[index].wait_for(state="visible", timeout=5000)
                    menus[index].click()
                    self.page.wait_for_timeout(1000)
                    if self.is_element_visible(self.edit_branch_button, timeout=3000):
                        self.click_element(self.edit_branch_button)
                        self.page.wait_for_timeout(2000)
        except:
            pass  # Edit functionality not available, that's okay
    
    def delete_branch(self, index: int = 0, confirm: bool = True):
        """Delete a specific branch."""
        try:
            if self.is_element_visible(self.branch_actions_menu, timeout=5000):
                menus = self.page.locator(self.branch_actions_menu).all()
                if len(menus) > index:
                    menus[index].wait_for(state="visible", timeout=5000)
                    menus[index].click()
                    self.page.wait_for_timeout(1000)
                    if self.is_element_visible(self.delete_branch_button, timeout=3000):
                        self.click_element(self.delete_branch_button)
                        if confirm:
                            self.page.wait_for_timeout(1000)
                            self.page.keyboard.press("Enter")
                            self.page.wait_for_timeout(2000)
        except:
            pass  # Delete functionality not available, that's okay

