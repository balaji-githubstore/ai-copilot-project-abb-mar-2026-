"""
{Page Name} page object following Page Object Model pattern.
Contains all interactions and validations for {page description}.
"""

import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from pages.base_page import BasePage
from locators.{page_name}_locators import {PageName}Locators

logger = logging.getLogger(__name__)


class {PageName}Page(BasePage):
    """Page object for {page description} with comprehensive functionality."""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = {PageName}Locators()
    
    # Navigation methods
    def navigate_to_{page_name}(self):
        """Navigate to {page name} page and verify loading."""
        self.driver.get(f"{self.base_url}/{page_path}")
        self.wait_for_{page_name}_page_load()
        return self
    
    def wait_for_{page_name}_page_load(self):
        """Wait for {page name} page to fully load."""
        self.wait_for_element_visible(self.locators.{KEY_ELEMENT})
        return self
    
    # Element interaction methods
    def enter_{field_name}(self, value):
        """Enter value into {field name} field with explicit wait."""
        element = self.wait_for_element_clickable(self.locators.{FIELD_NAME}_INPUT)
        element.clear()
        element.send_keys(value)
        self.logger.info(f"Entered value into {field_name} field")
        return self
    
    def click_{element_name}(self):
        """Click {element name} with explicit wait for clickability."""
        element = self.wait_for_element_clickable(self.locators.{ELEMENT_NAME}_BUTTON)
        element.click()
        self.logger.info(f"Clicked {element_name}")
        return self
    
    def clear_{field}_fields(self):
        """Clear all {field} input fields."""
        for locator in [self.locators.FIELD1_INPUT, self.locators.FIELD2_INPUT]:
            try:
                element = self.wait_for_element_clickable(locator, timeout=5)
                element.clear()
            except TimeoutException:
                self.logger.warning(f"Could not clear field: {locator}")
        return self
    
    # State verification methods  
    def is_{page_name}_page_displayed(self):
        """Verify {page name} page is displayed by checking key elements."""
        return (self.is_element_present(self.locators.{KEY_ELEMENT}) and
                self.is_element_present(self.locators.{ANOTHER_KEY_ELEMENT}))
    
    def is_{element}_visible(self):
        """Check if {element} is visible on the page."""
        return self.is_element_present(self.locators.{ELEMENT}, timeout=5)
    
    def get_{data}_message(self):
        """Get {data} message text with explicit wait."""
        try:
            element = self.wait_for_element_visible(self.locators.{DATA}_MESSAGE)
            return element.text
        except TimeoutException:
            self.logger.warning("No {data} message found")
            return ""
    
    # Complex workflow methods
    def perform_{action}(self, param1, param2=None):
        """Perform complete {action} workflow with method chaining."""
        workflow = self.enter_{field1}(param1)
        
        if param2:
            workflow = workflow.enter_{field2}(param2)
            
        return workflow.click_{submit_button}()
    
    def perform_{action}_with_enter_key(self, param1, param2):
        """Perform {action} using Enter key instead of button click."""
        field = self.wait_for_element_clickable(self.locators.{FIELD2}_INPUT)
        return (self.enter_{field1}(param1)
                   .enter_{field2}(param2))
        # Send Enter to the last field
        field.send_keys(Keys.RETURN)
        return self
    
    # Wait for state changes
    def wait_for_{action}_result(self, timeout=10):
        """Wait for {action} to complete and determine result state."""
        try:
            # Wait for success indicator
            self.wait.until(EC.url_contains("success"), timeout=timeout)
            return "success"
        except TimeoutException:
            # Check for error state
            if self.is_element_present(self.locators.ERROR_MESSAGE):
                return "error"
            # Check if still on same page (no redirect)
            if self.is_{page_name}_page_displayed():
                return "no_change"
            return "timeout"
    
    def get_current_url(self):
        """Get current page URL for verification."""
        return self.driver.current_url
    
    def get_attribute(self, locator, attribute_name):
        """Get attribute value from element with explicit wait."""
        element = self.wait_for_element_visible(locator)
        return element.get_attribute(attribute_name)