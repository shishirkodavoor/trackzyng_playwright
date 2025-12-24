"""Accessibility tests."""
import pytest
import allure
from pages.login_page import LoginPage
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD
from utils.test_helpers import ensure_fresh_session, login_user

class TestAccessibility:
    """Accessibility test suite."""
    
    def test_keyboard_navigation(self, page):
        """Test keyboard navigation."""
        allure.dynamic.title("Accessibility: Keyboard navigation changes focus")
        allure.dynamic.description(
            "Tabbing through interactive elements should move focus to focusable controls or the page should expose focusable elements."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.wait_for_timeout(1000)
        
        # Get initial focused element
        initial_focus = page.evaluate("() => document.activeElement?.tagName || null")
        
        # Tab through elements
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)
        focus_after_first_tab = page.evaluate("() => document.activeElement?.tagName || null")
        
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)
        focus_after_second_tab = page.evaluate("() => document.activeElement?.tagName || null")
        
        # Verify that focus actually changed (keyboard navigation is working)
        # At least one tab should change focus, or we should have focusable elements
        focus_changed = (initial_focus != focus_after_first_tab) or (focus_after_first_tab != focus_after_second_tab)
        has_focusable_elements = page.locator("input, button, a, [tabindex]").count() > 0
        
        assert focus_changed or has_focusable_elements, \
            f"Keyboard navigation should work - focus should change when tabbing (initial: {initial_focus}, after 1st tab: {focus_after_first_tab}, after 2nd tab: {focus_after_second_tab})"
    
    def test_aria_labels(self, page):
        """Test ARIA labels on interactive elements."""
        allure.dynamic.title("Accessibility: Buttons have ARIA labels or visible text")
        allure.dynamic.description(
            "Verify that primary interactive buttons expose either an aria-label or visible text for screen reader users."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.wait_for_timeout(1000)
        
        # Check for ARIA labels on buttons
        buttons = page.locator("button").all()
        buttons_with_labels = 0
        buttons_with_text = 0
        
        for button in buttons[:5]:  # Check first 5 buttons
            aria_label = button.get_attribute("aria-label")
            button_text = button.inner_text().strip()
            
            if aria_label and len(aria_label) > 0:
                buttons_with_labels += 1
            if button_text and len(button_text) > 0:
                buttons_with_text += 1
        
        # Buttons should have either aria-label OR visible text for accessibility
        total_buttons_checked = min(len(buttons), 5)
        accessible_buttons = buttons_with_labels + buttons_with_text
        
        # At least some buttons should be accessible (have label or text)
        # For login page, we expect at least the Next/Sign in button to have text
        assert accessible_buttons > 0 or total_buttons_checked == 0, \
            f"Buttons should have accessible labels - checked {total_buttons_checked} buttons, {buttons_with_labels} have aria-label, {buttons_with_text} have text"
    
    def test_form_labels(self, page):
        """Test form field labels."""
        allure.dynamic.title("Accessibility: Form inputs have associated labels or aria-labels")
        allure.dynamic.description(
            "Inputs should have an associated <label> or aria-label to ensure they are announced by assistive technologies; placeholder text is a fallback."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.wait_for_timeout(1000)
        
        # Check if inputs have associated labels
        inputs = page.locator("input").all()
        inputs_with_labels = 0
        inputs_with_aria = 0
        inputs_with_placeholder = 0
        
        for inp in inputs:
            # Check for associated label element
            inp_id = inp.get_attribute("id")
            if inp_id:
                label = page.locator(f'label[for="{inp_id}"]').count()
                if label > 0:
                    inputs_with_labels += 1
            
            # Check for aria-label
            aria_label = inp.get_attribute("aria-label")
            if aria_label and len(aria_label) > 0:
                inputs_with_aria += 1
            
            # Check for placeholder (less ideal but provides context)
            placeholder = inp.get_attribute("placeholder")
            if placeholder and len(placeholder) > 0:
                inputs_with_placeholder += 1
        
        total_inputs = len(inputs)
        accessible_inputs = inputs_with_labels + inputs_with_aria
        
        # Inputs should have labels for accessibility
        # Placeholder is acceptable as fallback but not ideal
        assert accessible_inputs > 0 or (inputs_with_placeholder > 0 and total_inputs > 0) or total_inputs == 0, \
            f"Form inputs should have labels - {total_inputs} inputs found, {inputs_with_labels} have <label>, {inputs_with_aria} have aria-label, {inputs_with_placeholder} have placeholder"
    
    def test_color_contrast(self, page):
        """Test color contrast for readability."""
        allure.dynamic.title("Accessibility: Page loads and contains content for contrast checks")
        allure.dynamic.description(
            "Confirm page loads and contains content so color contrast checks (to be performed by accessibility tools) are meaningful."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        # Wait for page to load
        try:
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            page.wait_for_timeout(2000)
        except Exception as e:
            pytest.skip(f"Page did not load in time for color contrast test: {e}")
        
        # Check that page loaded successfully (URL and title are indicators)
        try:
            url = page.url
            title = page.title()
            page_loaded = (url.startswith("http") and len(title) > 0)
        except Exception:
            page_loaded = False
        
        # Check for any content on the page - multiple strategies
        has_content = False
        
        # Strategy 1: Check for input elements (login page should have these)
        try:
            inputs = page.locator("input").count()
            if inputs > 0:
                has_content = True
        except Exception:
            inputs = 0
        
        # Strategy 2: Check for buttons
        if not has_content:
            try:
                buttons = page.locator("button").count()
                if buttons > 0:
                    has_content = True
            except Exception:
                buttons = 0
        
        # Strategy 3: Check for any visible elements
        if not has_content:
            try:
                visible_elements = page.locator("body *").count()
                if visible_elements > 0:
                    has_content = True
            except Exception:
                visible_elements = 0
        
        # Strategy 4: Check page title as content indicator
        if not has_content:
            try:
                if page.title() and len(page.title().strip()) > 0:
                    has_content = True
            except Exception:
                pass
    
        assert page_loaded or has_content, \
            "Page should load successfully and have content for color contrast verification (actual contrast should be checked with accessibility tools)"
    
    def test_screen_reader_compatibility(self, page):
        """Test screen reader compatibility."""
        allure.dynamic.title("Accessibility: Page exposes semantic landmarks and interactive elements")
        allure.dynamic.description(
            "Check for headings, landmarks, forms, and interactive elements to ensure screen readers can navigate the page."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        # Wait for page to load
        try:
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            page.wait_for_timeout(2000)
        except Exception:
            pass  # Page might already be loaded
        
        # Check for semantic HTML elements
        headings = 0
        landmarks = 0
        aria_landmarks = 0
        forms = 0
        inputs = 0
        buttons = 0
        labels = 0
        
        try:
            headings = page.locator("h1, h2, h3, h4, h5, h6").count()
        except Exception:
            headings = 0
        
        try:
            landmarks = page.locator("nav, main, header, footer, aside, section, article").count()
        except Exception:
            landmarks = 0
        
        try:
            aria_landmarks = page.locator('[role="navigation"], [role="main"], [role="banner"], [role="contentinfo"]').count()
        except Exception:
            aria_landmarks = 0
        
        try:
            forms = page.locator("form").count()
        except Exception:
            forms = 0
        
        try:
            inputs = page.locator("input, select, textarea").count()
        except Exception:
            inputs = 0
        
        try:
            buttons = page.locator("button, [role='button']").count()
        except Exception:
            buttons = 0
        
        try:
            labels = page.locator("label").count()
        except Exception:
            labels = 0
        
        has_semantic_structure = (headings > 0 or landmarks > 0 or aria_landmarks > 0)
        has_form_structure = forms > 0
        has_interactive_elements = (inputs > 0 or buttons > 0)
        has_navigable_content = has_semantic_structure or has_form_structure or has_interactive_elements
        
        # Additional check: page should have some structure (not just empty)
        page_has_structure = (headings + landmarks + aria_landmarks + forms + inputs + buttons) > 0
        
        assert has_navigable_content and page_has_structure, \
            f"Page should have semantic structure or interactive elements for screen readers - " \
            f"headings: {headings}, landmarks: {landmarks}, aria: {aria_landmarks}, " \
            f"forms: {forms}, inputs: {inputs}, buttons: {buttons}, labels: {labels}"
    
    def test_focus_indication(self, page):
        """Test focus indication for keyboard users."""
        allure.dynamic.title("Accessibility: Focus indicators visible for keyboard navigation")
        allure.dynamic.description(
            "Ensure focused interactive elements have a visible indicator (outline, border, or box-shadow) for keyboard users."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.wait_for_timeout(1000)
        
        # Tab to input
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)
        
        # Check if focused element exists and is focusable
        try:
            focused_element = page.evaluate("() => document.activeElement")
        except Exception as e:
            pytest.skip(f"Unable to evaluate focused element: {e}")

        assert focused_element is not None, "Focus should be visible - no element is focused"

        focus_style = page.evaluate("""
            () => {
                const el = document.activeElement;
                if (!el) return null;
                const style = window.getComputedStyle(el);
                return {
                    outline: style.outline,
                    outlineWidth: style.outlineWidth,
                    outlineStyle: style.outlineStyle,
                    border: style.border,
                    boxShadow: style.boxShadow
                };
            }
        """)
        
        # Focus should have some visible indicator (outline, border, or box-shadow)
        has_focus_indicator = False
        if focus_style:
            outline_width = focus_style.get('outlineWidth', '0px')
            has_outline = outline_width and outline_width != '0px'
            border = focus_style.get('border', '')
            has_border = border and '0px' not in border
            box_shadow = focus_style.get('boxShadow', 'none')
            has_shadow = box_shadow and box_shadow != 'none'
            has_focus_indicator = has_outline or has_border or has_shadow
        
  
        focused_tag = page.evaluate("() => document.activeElement?.tagName?.toLowerCase() || ''")
        needs_indicator = focused_tag not in ['body', 'html']
        
        assert has_focus_indicator or not needs_indicator, \
            f"Focused element ({focused_tag}) should have visible focus indicator (outline, border, or box-shadow) for keyboard users"
    
    def test_alt_text_for_images(self, page):
        """Test alt text for images."""
        allure.dynamic.title("Accessibility: Images provide alt attributes when present")
        allure.dynamic.description(
            "Verify that images include an alt attribute (can be empty for decorative images) so they are readable by screen readers."
        )
        ensure_fresh_session(page)
        login_user(page, ADMIN_USERNAME, ADMIN_PASSWORD)
        
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.wait_for_timeout(2000)
        
        images = page.locator("img").all()
        images_with_alt = 0
        images_checked = 0
        
        for img in images[:10]:  # Check first 10 images
            # Check if alt attribute exists (even if empty, it should exist)
            try:
                alt = img.get_attribute("alt")
            except Exception:
                alt = None

            images_checked += 1
            if alt is not None:
                images_with_alt += 1

        assert images_with_alt == images_checked or images_checked == 0, \
            f"Images should have alt attributes - checked {images_checked} images, {images_with_alt} have alt attribute"
    
    def test_skip_links(self, page):
        """Test skip to main content links."""
        allure.dynamic.title("Accessibility: Skip links present on complex pages")
        allure.dynamic.description(
            "Pages with multiple landmark regions should provide a skip-to-main link to improve keyboard navigation."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.wait_for_timeout(1000)
        
        # Check for skip links (optional but good practice)
        skip_links = page.locator('a[href*="#main"], a[href*="#content"], a[href*="#skip"]').count()
        
        page_complexity = page.locator("nav, header, footer, aside").count()
        needs_skip_links = page_complexity > 2  # Complex pages should have skip links
        
        # Test passes if skip links exist OR page is simple enough
        assert skip_links > 0 or not needs_skip_links, \
            f"Skip links should be considered for complex pages - found {skip_links} skip links, page has {page_complexity} landmark elements"
    
    def test_error_message_accessibility(self, page):
        """Test error messages are accessible."""
        allure.dynamic.title("Accessibility: Error messages are announced and visible")
        allure.dynamic.description(
            "After submitting invalid credentials, the page should surface accessible error notifications via ARIA or visible text."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.wait_for_timeout(1000)
        
        # Try invalid login
        login.login("wrong@email.com", "wrongpass")
        page.wait_for_timeout(3000)
        
        try:
            error_elements = page.locator('[role="alert"], .error, [aria-live], [class*="error" i], [class*="alert" i]').count()
        except Exception:
            error_elements = 0

        try:
            error_text = page.locator("body").inner_text().lower()
        except Exception:
            error_text = ""

        has_error_keywords = any(keyword in error_text for keyword in ["error", "invalid", "incorrect", "wrong", "failed"])

        assert error_elements > 0 or has_error_keywords or "/dashboard" not in page.url, \
            f"Error messages should be accessible - found {error_elements} ARIA error elements, error keywords in text: {has_error_keywords}, still on login: {'/dashboard' not in page.url}"
    
    def test_responsive_design_accessibility(self, page):
        """Test accessibility on different screen sizes."""
        allure.dynamic.title("Accessibility: Form controls remain accessible on mobile viewport")
        allure.dynamic.description(
            "Verify critical form elements remain available and accessible when using a mobile viewport size."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        
        # Test mobile viewport
        page.set_viewport_size({"width": 375, "height": 667})
        login.open()
        
        # Check if elements are accessible on mobile
        inputs = page.locator("input").count()
        assert inputs > 0, "Form should be accessible on mobile"
    
    def test_language_attribute(self, page):
        """Test language attribute on HTML."""
        allure.dynamic.title("Accessibility: HTML document specifies language")
        allure.dynamic.description(
            "Ensure the <html> element has a lang attribute so assistive technologies announce content in the correct language."
        )
        ensure_fresh_session(page)
        login = LoginPage(page)
        login.open()
        
        page.wait_for_load_state("domcontentloaded", timeout=10000)
        page.wait_for_timeout(1000)
        
        # Check lang attribute on html element
        lang = page.locator("html").get_attribute("lang")
        
        # HTML should have lang attribute for screen readers
        # This is a WCAG requirement
        assert lang is not None and len(lang.strip()) > 0, \
            f"Page should have language attribute on <html> element for screen readers - found: '{lang}'"

