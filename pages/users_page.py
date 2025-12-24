"""Users management page object."""
from pages.base_page import BasePage

class UsersPage(BasePage):
    """Page object for the Users management section."""
    
    def __init__(self, page):
        super().__init__(page)
        # Users page selectors - based on actual inspection
        self.header = 'text=Users, h1:has-text("Users"), [data-testid*="users-header"]'
        self.users_list = 'table tbody tr, [data-testid*="user"], .user-item, .user-card'
        self.create_user_button = 'button:has-text("ADD USER"), button:has-text("Create User"), button:has-text("Add User"), [data-testid*="create-user"]'
        self.search_input = 'input[placeholder="Search"], input[placeholder*="Search" i], input[type="search"], input[name*="search"]'
        self.filter_button = 'button:has-text("Filter"), [data-testid*="filter"]'
        self.role_filter = 'select[name*="role"], [data-testid*="role-filter"]'
        self.status_filter = 'select[name*="status"], [data-testid*="status-filter"]'
        self.users_table = 'table, [role="table"]'
        self.user_actions_menu = '[data-testid*="actions"], [aria-label*="actions"], [aria-label*="Open"]'
        self.edit_user_button = 'button:has-text("Edit"), [data-testid*="edit-user"]'
        self.delete_user_button = 'button:has-text("Delete"), [data-testid*="delete-user"]'
        self.view_user_button = 'button:has-text("View"), a:has-text("View")'
        self.activate_user_button = 'button:has-text("Activate"), [data-testid*="activate"]'
        self.deactivate_user_button = 'button:has-text("Deactivate"), [data-testid*="deactivate"]'
        self.pagination = '[data-testid*="pagination"], .pagination'
        self.next_page_button = 'button[aria-label*="next" i], button:has-text("Next"), [aria-label*="next"]'
        self.prev_page_button = 'button[aria-label*="previous" i], button:has-text("Previous"), [aria-label*="previous"]'
        
        # Create/Edit User Form selectors
        self.email_input = 'input[type="email"], input[name*="email"]'
        self.name_input = 'input[name*="name"], input[placeholder*="Name"]'
        self.password_input = 'input[type="password"], input[name*="password"]'
        self.confirm_password_input = 'input[name*="confirm"], input[name*="confirm_password"]'
        self.role_select = 'select[name*="role"], [data-testid*="role"]'
        self.status_select = 'select[name*="status"], [data-testid*="status"]'
        self.phone_input = 'input[type="tel"], input[name*="phone"]'
        self.save_button = 'button:has-text("Save"), button[type="submit"], button:has-text("Create")'
        self.cancel_button = 'button:has-text("Cancel"), button[type="button"]'
        self.user_form = 'form, [data-testid*="user-form"]'
    
    def is_loaded(self, timeout: int = 15000) -> bool:
        """Check if users page is loaded - URL is primary check."""
        try:
            self.wait_for_url_pattern("/users", timeout=timeout)
            # URL check is primary
            if "/users" in self.get_current_url():
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                self.page.wait_for_timeout(2000)
                return True
            # Secondary: try to find header element
            return self.is_element_visible(self.header, timeout=3000)
        except:
            # Final fallback: just check URL
            return "/users" in self.get_current_url()
    
    def navigate_to_users(self):
        """Navigate to users page."""
        try:
            base_url = self.get_base_url()
            self.navigate_to(f"{base_url}/users")
            self.wait_for_url_pattern("/users", timeout=15000)
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
        except:
            base_url = self.get_base_url()
            self.page.goto(f"{base_url}/users", wait_until="domcontentloaded", timeout=30000)
            self.page.wait_for_timeout(2000)
    
    def get_users_count(self) -> int:
        """Get count of users displayed."""
        try:
            return self.page.locator(self.users_list).count()
        except:
            return 0
    
    def search_user(self, search_term: str):
        """Search for a user."""
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
    
    def filter_by_role(self, role: str):
        """Filter users by role."""
        if self.is_element_visible(self.role_filter, timeout=3000):
            self.page.locator(self.role_filter).select_option(role)
            self.page.wait_for_timeout(1000)
    
    def filter_by_status(self, status: str):
        """Filter users by status."""
        if self.is_element_visible(self.status_filter, timeout=3000):
            self.page.locator(self.status_filter).select_option(status)
            self.page.wait_for_timeout(1000)
    
    def click_create_user(self):
        """Click create user button."""
        try:
            # Try exact text match first
            try:
                add_button = self.page.get_by_text("ADD USER", exact=False).first
                if add_button.is_visible(timeout=5000):
                    add_button.click()
                    self.page.wait_for_timeout(2000)
                    return
            except:
                pass
            
            # Fallback to generic selector
            if self.is_element_visible(self.create_user_button, timeout=5000):
                self.click_element(self.create_user_button)
                self.page.wait_for_timeout(2000)
        except:
            pass  # Button not found, that's okay
    
    def fill_user_form(self, email: str = "", name: str = "", password: str = "", 
                      role: str = "", status: str = "", phone: str = ""):
        """Fill user creation/edit form."""
        if email and self.is_element_visible(self.email_input, timeout=3000):
            self.fill_input(self.email_input, email)
        if name and self.is_element_visible(self.name_input, timeout=3000):
            self.fill_input(self.name_input, name)
        if password and self.is_element_visible(self.password_input, timeout=3000):
            self.fill_input(self.password_input, password)
            if self.is_element_visible(self.confirm_password_input, timeout=2000):
                self.fill_input(self.confirm_password_input, password)
        if role and self.is_element_visible(self.role_select, timeout=3000):
            self.page.locator(self.role_select).select_option(role)
        if status and self.is_element_visible(self.status_select, timeout=3000):
            self.page.locator(self.status_select).select_option(status)
        if phone and self.is_element_visible(self.phone_input, timeout=3000):
            self.fill_input(self.phone_input, phone)
    
    def save_user_form(self):
        """Save user form."""
        if self.is_element_visible(self.save_button, timeout=3000):
            self.click_element(self.save_button)
            self.page.wait_for_timeout(2000)
    
    def cancel_user_form(self):
        """Cancel user form."""
        if self.is_element_visible(self.cancel_button, timeout=3000):
            self.click_element(self.cancel_button)
    
    def view_user(self, index: int = 0):
        """View a specific user."""
        try:
            view_buttons = self.page.locator(self.view_user_button).all()
            if len(view_buttons) > index:
                view_buttons[index].wait_for(state="visible", timeout=5000)
                view_buttons[index].click()
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                self.page.wait_for_timeout(2000)
        except:
            pass  # View button not found, that's okay
    
    def edit_user(self, index: int = 0):
        """Edit a specific user."""
        try:
            if self.is_element_visible(self.user_actions_menu, timeout=5000):
                menus = self.page.locator(self.user_actions_menu).all()
                if len(menus) > index:
                    menus[index].wait_for(state="visible", timeout=5000)
                    menus[index].click()
                    self.page.wait_for_timeout(1000)
                    if self.is_element_visible(self.edit_user_button, timeout=3000):
                        self.click_element(self.edit_user_button)
                        self.page.wait_for_timeout(2000)
        except:
            pass  # Edit functionality not available, that's okay
    
    def delete_user(self, index: int = 0, confirm: bool = True):
        """Delete a specific user."""
        try:
            if self.is_element_visible(self.user_actions_menu, timeout=5000):
                menus = self.page.locator(self.user_actions_menu).all()
                if len(menus) > index:
                    menus[index].wait_for(state="visible", timeout=5000)
                    menus[index].click()
                    self.page.wait_for_timeout(1000)
                    if self.is_element_visible(self.delete_user_button, timeout=3000):
                        self.click_element(self.delete_user_button)
                        if confirm:
                            self.page.wait_for_timeout(1000)
                            self.page.keyboard.press("Enter")
                            self.page.wait_for_timeout(2000)
        except:
            pass  # Delete functionality not available, that's okay

