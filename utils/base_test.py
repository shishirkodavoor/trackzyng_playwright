import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page():
    """Playwright page fixture."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page_obj = context.new_page()
        yield page_obj
        context.close()
        browser.close()
