"""
Login page object following Page Object Model pattern.
Encapsulates Facebook login page interactions and validations.
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage
from locators.login_locators import LoginLocators

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Facebook login page object with comprehensive login functionality."""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginLocators()
        self.url = "https://www.facebook.com/login"
    
    def navigate_to_login(self):
        """Navigate to Facebook login page."""
        logger.info(f"Navigating to login page: {self.url}")
        self.driver.get(self.url)
        self.wait_for_page_load()
        self._handle_cookie_banner()
        return self
    
    def wait_for_page_load(self, timeout=10):
        """Wait for login page to fully load."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.locators.LOGIN_FORM)
            )
            logger.info("Login page loaded successfully")
        except TimeoutException:
            logger.warning("Login page load timeout - continuing anyway")
    
    def _handle_cookie_banner(self):
        """Handle cookie acceptance banner if present."""
        try:
            if self.is_element_visible(self.locators.COOKIE_BANNER, timeout=3):
                self.click_element(self.locators.COOKIE_ACCEPT)
                logger.info("Cookie banner accepted")
        except:
            logger.debug("No cookie banner found or already handled")
    
    def enter_email(self, email):
        """
        Enter email address in the login form.
        
        Args:
            email: Email address to enter
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Entering email: {email}")
        self.send_keys(self.locators.EMAIL_INPUT, email)
        return self
    
    def enter_password(self, password):
        """
        Enter password in the login form.
        
        Args:
            password: Password to enter (will be masked in logs)
            
        Returns:
            Self for method chaining  
        """
        logger.info("Entering password")
        self.send_keys(self.locators.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self):
        """Click the login button."""
        logger.info("Clicking login button")
        self.click_element(self.locators.LOGIN_BUTTON)
        return self
    
    def perform_login(self, email, password):
        """
        Perform complete login sequence.
        
        Args:
            email: Email address
            password: Password
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Performing login for email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def perform_login_with_enter(self, email, password):
        """
        Perform login using Enter key instead of clicking login button.
        
        Args:
            email: Email address
            password: Password
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Performing login with Enter key for email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        
        # Press Enter key in password field
        password_field = self.find_element(self.locators.PASSWORD_INPUT)
        password_field.send_keys(Keys.RETURN)
        logger.info("Pressed Enter to submit login")
        return self
    
    def is_login_page_displayed(self):
        """Check if we're on the login page."""
        try:
            return self.is_element_visible(self.locators.LOGIN_FORM, timeout=5)
        except:
            return False
    
    def is_error_message_displayed(self, timeout=10):
        """
        Check if any error message is displayed after login attempt.
        
        Args:
            timeout: Time to wait for error message
            
        Returns:
            bool: True if error message is visible
        """
        error_locators = [
            self.locators.ERROR_MESSAGE,
            self.locators.GENERIC_ERROR,
            self.locators.LOGIN_ERROR_BOX,
            self.locators.ERROR_CONTAINER,
            self.locators.VALIDATION_ERROR
        ]
        
        for locator in error_locators:
            if self.is_element_visible(locator, timeout=timeout):
                logger.info(f"Error message found with locator: {locator}")
                return True
        
        logger.info("No error message found")
        return False
    
    def get_error_message(self):
        """
        Get the error message text displayed on the page.
        
        Returns:
            str: Error message text or empty string if not found
        """
        error_locators = [
            self.locators.ERROR_MESSAGE,
            self.locators.GENERIC_ERROR, 
            self.locators.LOGIN_ERROR_BOX,
            self.locators.ERROR_CONTAINER,
            self.locators.VALIDATION_ERROR
        ]
        
        for locator in error_locators:
            try:
                if self.is_element_visible(locator, timeout=3):
                    error_text = self.get_text(locator)
                    logger.info(f"Found error message: {error_text}")
                    return error_text
            except:
                continue
        
        logger.warning("No error message text found")
        return ""
    
    def clear_login_fields(self):
        """Clear both email and password fields."""
        logger.info("Clearing login fields")
        try:
            email_field = self.find_element(self.locators.EMAIL_INPUT)
            email_field.clear()
            
            password_field = self.find_element(self.locators.PASSWORD_INPUT)  
            password_field.clear()
            
            logger.info("Login fields cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear login fields: {str(e)}")
        
        return self
    
    def is_forgot_password_link_visible(self):
        """Check if forgot password link is visible."""
        return self.is_element_visible(self.locators.FORGOT_PASSWORD_LINK)
    
    def click_forgot_password_link(self):
        """Click the forgot password link."""
        logger.info("Clicking forgot password link")
        self.click_element(self.locators.FORGOT_PASSWORD_LINK)
        return self
    
    def wait_for_login_result(self, timeout=15):
        """
        Wait for login attempt to complete (either success or error).
        
        Args:
            timeout: Maximum time to wait
            
        Returns:
            str: 'success', 'error', or 'timeout'
        """
        try:
            # Wait for either error message or URL change (successful login)
            WebDriverWait(self.driver, timeout).until(
                lambda driver: (
                    self.is_error_message_displayed(timeout=1) or
                    driver.current_url != self.url
                )
            )
            
            if self.is_error_message_displayed(timeout=1):
                logger.info("Login failed - error message displayed")
                return 'error'
            elif self.driver.current_url != self.url:
                logger.info("Login appears successful - URL changed")
                return 'success'
            else:
                logger.warning("Login result unclear")
                return 'timeout'
                
        except TimeoutException:
            logger.warning("Timeout waiting for login result")
            return 'timeout'
    
    def get_current_url(self):
        """Get current page URL for validation."""
        return self.driver.current_url