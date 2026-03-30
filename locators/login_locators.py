"""
Locators for Facebook login page elements.
Centralized selector management for maintainable test automation.
"""

from selenium.webdriver.common.by import By


class LoginLocators:
    """Locators for Facebook login page - centralized selector management."""
    
    # Login form elements
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "pass")
    LOGIN_BUTTON = (By.NAME, "login")
    
    # Error messages and validation
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div[role='alert']")
    GENERIC_ERROR = (By.CSS_SELECTOR, ".fsl.fwb.fcb")
    LOGIN_ERROR_BOX = (By.CSS_SELECTOR, "div._9ay7")
    
    # Alternative error selectors for different Facebook layouts
    ERROR_CONTAINER = (By.CSS_SELECTOR, "div[data-testid='royal_login_form'] div[role='alert']")
    VALIDATION_ERROR = (By.CSS_SELECTOR, "div._5f5d")
    
    # Page identification elements
    LOGIN_FORM = (By.CSS_SELECTOR, "form#loginform")
    FACEBOOK_LOGO = (By.CSS_SELECTOR, "img._8ilh")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgotten password?")
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "a[data-testid='open-registration-form-button']")
    
    # Loading and progress indicators
    LOADING_SPINNER = (By.CSS_SELECTOR, "div[role='progressbar']")
    
    # Cookie and privacy banners
    COOKIE_BANNER = (By.CSS_SELECTOR, "div[data-testid='cookie-policy-manage-dialog']")
    COOKIE_ACCEPT = (By.CSS_SELECTOR, "button[data-testid='cookie-policy-manage-dialog-accept-button']")
    
    @staticmethod
    def get_error_by_text(error_text: str):
        """Dynamic locator for error messages containing specific text."""
        return (By.XPATH, f"//div[contains(text(), '{error_text}')]")
    
    @staticmethod
    def get_input_validation_error(field_name: str):
        """Dynamic locator for field-specific validation errors."""
        return (By.XPATH, f"//input[@name='{field_name}']/following-sibling::div[@role='alert']")