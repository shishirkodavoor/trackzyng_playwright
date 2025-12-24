import sys
import os
import pytest
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Create screenshots directory
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Create reports directory
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

@pytest.fixture(scope="function")
def page():
    """Playwright page fixture."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page_obj = context.new_page()
        try:
            yield page_obj
        finally:
            # Best-effort close; swallow exceptions to avoid teardown errors in test reporting
            try:
                context.close()
            except Exception:
                pass
            try:
                browser.close()
            except Exception:
                pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failure."""
    outcome = yield
    rep = outcome.get_result()
    
    # Take screenshot on failure
    if rep.when == "call" and rep.failed:
        # Get page fixture if available
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.name.replace(" ", "_").replace("::", "_")
                screenshot_path = SCREENSHOTS_DIR / f"{test_name}_{timestamp}.png"
                page.screenshot(path=str(screenshot_path))
                print(f"\nScreenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
    
    return rep
