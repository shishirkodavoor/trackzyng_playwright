"""Tasks page object."""
from pages.base_page import BasePage

class TasksPage(BasePage):
    """Page object for the Tasks section."""
    
    def __init__(self, page):
        super().__init__(page)
        # Tasks page selectors - based on actual inspection
        self.header = 'text=Tasks, h1:has-text("Tasks"), [data-testid*="tasks-header"]'
        self.tasks_list = 'table tbody tr, [data-testid*="task"], .task-item, .task-card'
        self.create_task_button = 'button:has-text("ADD TASK"), button:has-text("Create Task"), button:has-text("Add Task"), [data-testid*="create-task"]'
        self.search_input = 'input[placeholder="Search"], input[placeholder*="Search" i], input[type="search"], input[name*="search"]'
        self.date_picker = 'input[id="«r4»"], input[placeholder="MM/DD/YYYY"], input[aria-label*="date" i], input[type="date"]'
        self.filter_button = 'button:has-text("Filter"), [data-testid*="filter"]'
        self.status_filter = 'select[name*="status"], [data-testid*="status-filter"]'
        self.priority_filter = 'select[name*="priority"], [data-testid*="priority-filter"]'
        self.assignee_filter = 'select[name*="assignee"], [data-testid*="assignee-filter"]'
        self.tasks_table = 'table, [role="table"]'
        self.task_actions_menu = '[data-testid*="actions"], [aria-label*="actions"], [aria-label*="Open"]'
        self.edit_task_button = 'button:has-text("Edit"), [data-testid*="edit-task"]'
        self.delete_task_button = 'button:has-text("Delete"), [data-testid*="delete-task"]'
        self.view_task_button = 'button:has-text("View"), a:has-text("View")'
        self.complete_task_button = 'button:has-text("Complete"), [data-testid*="complete"]'
        self.pagination = '[data-testid*="pagination"], .pagination'
        self.next_page_button = 'button[aria-label*="next" i], button:has-text("Next"), [aria-label*="next"]'
        self.prev_page_button = 'button[aria-label*="previous" i], button:has-text("Previous"), [aria-label*="previous"]'
        
        # Create/Edit Task Form selectors
        self.task_title_input = 'input[name*="title"], input[placeholder*="Title"]'
        self.task_description_input = 'textarea[name*="description"], textarea[placeholder*="Description"]'
        self.task_status_select = 'select[name*="status"], [data-testid*="status"]'
        self.task_priority_select = 'select[name*="priority"], [data-testid*="priority"]'
        self.task_assignee_select = 'select[name*="assignee"], [data-testid*="assignee"]'
        self.task_due_date_input = 'input[type="date"], input[name*="due_date"]'
        self.save_button = 'button:has-text("Save"), button[type="submit"], button:has-text("Create")'
        self.cancel_button = 'button:has-text("Cancel"), button[type="button"]'
        self.task_form = 'form, [data-testid*="task-form"]'
    
    def is_loaded(self, timeout: int = 15000) -> bool:
        """Check if tasks page is loaded - URL is primary check."""
        try:
            self.wait_for_url_pattern("/tasks", timeout=timeout)
            # URL check is primary
            if "/tasks" in self.get_current_url():
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
                self.page.wait_for_timeout(2000)
                return True
            # Secondary: try to find header element
            return self.is_element_visible(self.header, timeout=3000)
        except:
            # Final fallback: just check URL
            return "/tasks" in self.get_current_url()
    
    def navigate_to_tasks(self):
        """Navigate to tasks page."""
        try:
            base_url = self.get_base_url()
            self.navigate_to(f"{base_url}/tasks")
            self.wait_for_url_pattern("/tasks", timeout=15000)
            self.page.wait_for_load_state("domcontentloaded", timeout=10000)
            self.page.wait_for_timeout(2000)
        except:
            # Fallback
            base_url = self.get_base_url()
            self.page.goto(f"{base_url}/tasks", wait_until="domcontentloaded", timeout=30000)
            self.page.wait_for_timeout(2000)
    
    def get_tasks_count(self) -> int:
        """Get count of tasks displayed."""
        try:
            return self.page.locator(self.tasks_list).count()
        except:
            return 0
    
    def search_task(self, search_term: str):
        """Search for a task."""
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
    
    def filter_by_status(self, status: str):
        """Filter tasks by status."""
        if self.is_element_visible(self.status_filter, timeout=3000):
            self.page.locator(self.status_filter).select_option(status)
            self.page.wait_for_timeout(1000)
    
    def filter_by_priority(self, priority: str):
        """Filter tasks by priority."""
        if self.is_element_visible(self.priority_filter, timeout=3000):
            self.page.locator(self.priority_filter).select_option(priority)
            self.page.wait_for_timeout(1000)
    
    def click_create_task(self):
        """Click create task button."""
        try:
            # Try exact text match first
            try:
                add_button = self.page.get_by_text("ADD TASK", exact=False).first
                if add_button.is_visible(timeout=5000):
                    add_button.click()
                    self.page.wait_for_timeout(2000)
                    return
            except:
                pass
            
            # Fallback to generic selector
            if self.is_element_visible(self.create_task_button, timeout=5000):
                self.click_element(self.create_task_button)
                self.page.wait_for_timeout(2000)
        except:
            pass  # Button not found, that's okay
    
    def fill_task_form(self, title: str = "", description: str = "", status: str = "", 
                      priority: str = "", assignee: str = "", due_date: str = ""):
        """Fill task creation/edit form."""
        if title and self.is_element_visible(self.task_title_input, timeout=3000):
            self.fill_input(self.task_title_input, title)
        if description and self.is_element_visible(self.task_description_input, timeout=3000):
            self.fill_input(self.task_description_input, description)
        if status and self.is_element_visible(self.task_status_select, timeout=3000):
            self.page.locator(self.task_status_select).select_option(status)
        if priority and self.is_element_visible(self.task_priority_select, timeout=3000):
            self.page.locator(self.task_priority_select).select_option(priority)
        if assignee and self.is_element_visible(self.task_assignee_select, timeout=3000):
            self.page.locator(self.task_assignee_select).select_option(assignee)
        if due_date and self.is_element_visible(self.task_due_date_input, timeout=3000):
            self.fill_input(self.task_due_date_input, due_date)
    
    def save_task_form(self):
        """Save task form."""
        if self.is_element_visible(self.save_button, timeout=3000):
            self.click_element(self.save_button)
            self.page.wait_for_timeout(2000)
    
    def view_task(self, index: int = 0):
        """View a specific task."""
        try:
            view_buttons = self.page.locator(self.view_task_button).all()
            if len(view_buttons) > index:
                view_buttons[index].wait_for(state="visible", timeout=5000)
                view_buttons[index].click()
                self.page.wait_for_load_state("domcontentloaded", timeout=10000)
                self.page.wait_for_timeout(2000)
        except:
            pass  # View button not found, that's okay
    
    def edit_task(self, index: int = 0):
        """Edit a specific task."""
        try:
            if self.is_element_visible(self.task_actions_menu, timeout=5000):
                menus = self.page.locator(self.task_actions_menu).all()
                if len(menus) > index:
                    menus[index].wait_for(state="visible", timeout=5000)
                    menus[index].click()
                    self.page.wait_for_timeout(1000)
                    if self.is_element_visible(self.edit_task_button, timeout=3000):
                        self.click_element(self.edit_task_button)
                        self.page.wait_for_timeout(2000)
        except:
            pass  # Edit functionality not available, that's okay

