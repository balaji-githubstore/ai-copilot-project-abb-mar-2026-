"""
Locators for {Page Name} page using stable selector strategies.
Priority: ID > CSS Selector > XPath (only when absolutely necessary).
"""

from selenium.webdriver.common.by import By


class {PageName}Locators:
    """Locators for {page description} with priority on stability."""
    
    # Primary elements (ID selectors - most preferred)
    {FIELD1}_INPUT = (By.ID, "{field1_id}")
    {FIELD2}_INPUT = (By.ID, "{field2_id}")  
    {SUBMIT}_BUTTON = (By.ID, "{submit_button_id}")
    
    # Interactive elements (CSS selectors when ID not available)
    {ELEMENT}_LINK = (By.CSS_SELECTOR, "a[href*='{link_identifier}']")
    {ELEMENT}_BUTTON = (By.CSS_SELECTOR, "button[data-testid='{test_id}']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='error-message'], .error-text")
    
    # Dynamic content (CSS with fallback options)
    {CONTENT}_CONTAINER = (By.CSS_SELECTOR, ".{content}-container, [data-component='{content}']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-message, [role='alert'].success")
    
    # Form validation messages
    {FIELD1}_ERROR = (By.CSS_SELECTOR, "[data-field='{field1}'] .error-message")
    {FIELD2}_ERROR = (By.CSS_SELECTOR, "[data-field='{field2}'] .error-message")
    
    # Navigation and menu elements
    MAIN_MENU = (By.CSS_SELECTOR, "nav[role='navigation'], .main-navigation")
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb, [aria-label='breadcrumb']")
    
    # XPath selectors (use sparingly - only when structure is critical)
    # Use when: need to find elements by text content or complex relationships
    {DYNAMIC_ELEMENT} = (By.XPATH, "//div[@role='{role}'][contains(@class, '{class}')]")
    TEXT_CONTAINING_ELEMENT = (By.XPATH, "//span[contains(text(), '{expected_text}')]")
    
    # Multi-option selectors (for element that might have different implementations)
    SUBMIT_OPTIONS = [
        (By.ID, "{primary_submit_id}"),
        (By.CSS_SELECTOR, "input[type='submit'][value*='Submit']"),
        (By.XPATH, "//button[contains(text(), 'Submit')]")  # Last resort
    ]
    
    # Helper method for trying multiple locator strategies
    @classmethod
    def get_flexible_locator(cls, driver, locator_list):
        """Try multiple locator strategies until one works."""
        for locator in locator_list:
            try:
                elements = driver.find_elements(*locator)
                if elements:
                    return locator
            except Exception:
                continue
        return None