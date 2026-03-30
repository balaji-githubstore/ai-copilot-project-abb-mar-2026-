"""
Base page class providing common WebDriver operations and logging.
Foundation for all page objects in the framework.
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

logger = logging.getLogger(__name__)


class BasePage:
    """Base page class for all page objects in the application."""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logger
        self.actions = ActionChains(driver)
    
    def find_element(self, locator, timeout=10):
        """
        Find element with explicit wait.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
            timeout: Time to wait in seconds
            
        Returns:
            WebElement: Found element
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.debug(f"Found element: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Timeout finding element: {locator}")
            raise
    
    def find_elements(self, locator, timeout=10):
        """
        Find multiple elements with explicit wait.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
            timeout: Time to wait in seconds
            
        Returns:
            List[WebElement]: List of found elements
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            self.logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.warning(f"No elements found: {locator}")
            return []
    
    def click_element(self, locator, timeout=10):
        """
        Click element with wait for clickability.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
            timeout: Time to wait in seconds
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except ElementClickInterceptedException:
            # Try JavaScript click as fallback
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"Clicked element using JavaScript: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click element {locator}: {str(e)}")
            raise
    
    def send_keys(self, locator, keys, clear_first=True):
        """
        Send keys to element after optional clearing.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
            keys: Text to send
            clear_first: Whether to clear field before typing
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(keys)
        self.logger.info(f"Sent keys to {locator}: {'*' * len(str(keys)) if 'password' in str(locator).lower() else keys}")
    
    def get_text(self, locator):
        """
        Get element text.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
            
        Returns:
            str: Element text content
        """
        element = self.find_element(locator)
        text = element.text
        self.logger.debug(f"Retrieved text from {locator}: {text}")
        return text
    
    def get_attribute(self, locator, attribute_name):
        """
        Get element attribute value.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
            attribute_name: Name of attribute to get
            
        Returns:
            str: Attribute value
        """
        element = self.find_element(locator)
        value = element.get_attribute(attribute_name)
        self.logger.debug(f"Retrieved {attribute_name} from {locator}: {value}")
        return value
    
    def is_element_visible(self, locator, timeout=10):
        """
        Check if element is visible.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
            timeout: Time to wait in seconds
            
        Returns:
            bool: True if element is visible
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        """
        Check if element is present in DOM (may not be visible).
        
        Args:
            locator: Tuple of (By.TYPE, selector)
            
        Returns:
            bool: True if element exists in DOM
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=10):
        """
        Wait for element to disappear from the page.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
            timeout: Time to wait in seconds
            
        Returns:
            bool: True if element disappeared
        """
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            self.logger.warning(f"Element still present after timeout: {locator}")
            return False
    
    def scroll_to_element(self, locator):
        """
        Scroll element into view.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"Scrolled to element: {locator}")
    
    def hover_over_element(self, locator):
        """
        Hover mouse over element.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
        """
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()
        self.logger.info(f"Hovered over element: {locator}")
    
    def switch_to_frame(self, locator):
        """
        Switch to iframe.
        
        Args:
            locator: Tuple of (By.TYPE, selector)
        """
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)
        self.logger.info(f"Switched to frame: {locator}")
    
    def switch_to_default_content(self):
        """Switch back from iframe to main content."""
        self.driver.switch_to.default_content()
        self.logger.info("Switched to default content")
    
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
        self.logger.info("Page refreshed")
    
    def get_page_title(self):
        """Get current page title."""
        title = self.driver.title
        self.logger.debug(f"Page title: {title}")
        return title
    
    def get_current_url(self):
        """Get current page URL."""
        url = self.driver.current_url
        self.logger.debug(f"Current URL: {url}")
        return url