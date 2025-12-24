"""Test helper utilities for common test operations."""
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.navigation_page import NavigationPage
from config.config import BASE_URL

def ensure_fresh_session(page):
    """Ensure a clean session before each test."""
    try:
        page.context.clear_cookies()
    except Exception:
        pass
    
    try:
        page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
    except Exception:
        pass

def login_user(page, username: str, password: str) -> DashboardPage:
    """Helper function to login a user and return dashboard page."""
    ensure_fresh_session(page)
    
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username, password)
    
    # Wait for dashboard URL
    try:
        page.wait_for_url("**/dashboard**", timeout=15000)
    except:
        # Fallback: wait for URL to contain dashboard
        import time
        start_time = time.time()
        while time.time() - start_time < 15:
            if "/dashboard" in page.url:
                break
            time.sleep(0.5)
    
    dashboard = DashboardPage(page)
    dashboard.wait_for_dashboard_load()
    
    return dashboard

def logout_user(page):
    """Helper function to logout a user."""
    try:
        nav = NavigationPage(page)
        nav.logout()
        page.wait_for_url("**/login**", timeout=10000)
    except:
        # If logout fails, just ensure we're not on dashboard
        page.wait_for_timeout(2000)
        pass

def wait_for_page_ready(page, timeout: int = 30000):
    """Wait for page to be fully ready."""
    page.wait_for_load_state("networkidle", timeout=timeout)
    page.wait_for_load_state("domcontentloaded", timeout=timeout)


