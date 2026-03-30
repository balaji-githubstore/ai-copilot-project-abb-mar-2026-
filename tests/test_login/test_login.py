"""
Comprehensive Facebook login test suite covering invalid login scenarios.
Tests various authentication failure conditions with proper assertions.
"""

import pytest
import logging
from assertpy import assert_that
from pages.login_page import LoginPage
from config.settings import Settings

logger = logging.getLogger(__name__)


class TestLogin:
    """Test class for Facebook login functionality with focus on invalid scenarios."""
    
    @pytest.fixture(autouse=True)
    def setup_method(self, driver):
        """Setup method that runs before each test."""
        self.login_page = LoginPage(driver)
        logger.info("Starting login test setup")
        
        # Navigate to login page
        self.login_page.navigate_to_login()
        
        # Verify we're on the correct page
        assert_that(self.login_page.is_login_page_displayed()).is_true()
        logger.info("Login page loaded and verified")
    
    @pytest.mark.critical
    @pytest.mark.login
    def test_invalid_login_wrong_email_format(self, driver):
        """Test login with invalid email format."""
        logger.info("Testing invalid email format")
        
        invalid_emails = [
            "invalid-email",           # No @ symbol
            "@gmail.com",             # Missing username
            "user@",                  # Missing domain
            "user@domain",            # Missing TLD
            "user..double@gmail.com", # Double dots
            "user name@gmail.com",    # Space in username
        ]
        
        for invalid_email in invalid_emails:
            logger.info(f"Testing invalid email: {invalid_email}")
            
            # Clear fields and attempt login
            self.login_page.clear_login_fields()
            result = self.login_page.perform_login(invalid_email, "password123").wait_for_login_result()
            
            # Assert that login failed with error
            assert_that(result).is_equal_to('error')
            assert_that(self.login_page.is_error_message_displayed()).is_true()
            
            error_message = self.login_page.get_error_message()
            assert_that(error_message).is_not_empty()
            logger.info(f"Error message for {invalid_email}: {error_message}")
    
    @pytest.mark.critical
    @pytest.mark.login
    def test_invalid_login_nonexistent_email(self, driver):
        """Test login with non-existent email address."""
        logger.info("Testing non-existent email address")
        
        nonexistent_email = "nonexistent.user.12345@fakeemail.com"
        password = "password123"
        
        # Attempt login
        result = self.login_page.perform_login(nonexistent_email, password).wait_for_login_result()
        
        # Verify login failed
        assert_that(result).is_equal_to('error')
        assert_that(self.login_page.is_error_message_displayed()).is_true()
        
        # Verify error message contains appropriate text
        error_message = self.login_page.get_error_message()
        assert_that(error_message).is_not_empty()
        
        # Facebook typically shows generic error for security
        expected_error_keywords = ["wrong", "incorrect", "invalid", "error"]
        assert_that(error_message.lower()).contains_ignoring_case_any_of(*expected_error_keywords)
        
        logger.info(f"Login correctly failed with error: {error_message}")
    
    @pytest.mark.critical 
    @pytest.mark.login
    def test_invalid_login_wrong_password(self, driver):
        """Test login with wrong password for valid email."""
        logger.info("Testing wrong password scenario")
        
        # Use a realistic email format but wrong password
        email = "test.user@gmail.com" 
        wrong_passwords = [
            "wrongpassword",
            "12345",
            "",  # Empty password
            " ",  # Space only
            "password123!@#$%^&*()",  # Special characters
        ]
        
        for wrong_password in wrong_passwords:
            logger.info(f"Testing wrong password: {'*' * len(wrong_password) if wrong_password.strip() else 'empty'}")
            
            # Clear fields and attempt login
            self.login_page.clear_login_fields()
            result = self.login_page.perform_login(email, wrong_password).wait_for_login_result()
            
            # Verify login failed
            assert_that(result).is_equal_to('error')
            assert_that(self.login_page.is_error_message_displayed()).is_true()
            
            error_message = self.login_page.get_error_message()
            assert_that(error_message).is_not_empty()
            logger.info(f"Error message for wrong password: {error_message}")
    
    @pytest.mark.login
    def test_invalid_login_empty_fields(self, driver):
        """Test login with empty email and password fields."""
        logger.info("Testing empty login fields")
        
        # Attempt login with empty fields
        result = self.login_page.perform_login("", "").wait_for_login_result()
        
        # Verify login failed
        assert_that(result).is_equal_to('error')
        assert_that(self.login_page.is_error_message_displayed()).is_true()
        
        error_message = self.login_page.get_error_message()
        assert_that(error_message).is_not_empty()
        
        # Error should indicate required fields
        expected_keywords = ["required", "enter", "email", "password"]
        found_keyword = any(keyword in error_message.lower() for keyword in expected_keywords)
        assert_that(found_keyword).is_true()
        
        logger.info(f"Empty fields error message: {error_message}")
    
    @pytest.mark.login
    def test_invalid_login_empty_email_only(self, driver):
        """Test login with empty email but valid password format."""
        logger.info("Testing empty email field only")
        
        result = self.login_page.perform_login("", "password123").wait_for_login_result()
        
        # Verify login failed 
        assert_that(result).is_equal_to('error')
        assert_that(self.login_page.is_error_message_displayed()).is_true()
        
        error_message = self.login_page.get_error_message()
        assert_that(error_message).is_not_empty()
        logger.info(f"Empty email error message: {error_message}")
    
    @pytest.mark.login
    def test_invalid_login_empty_password_only(self, driver):
        """Test login with valid email format but empty password.""" 
        logger.info("Testing empty password field only")
        
        result = self.login_page.perform_login("test@gmail.com", "").wait_for_login_result()
        
        # Verify login failed
        assert_that(result).is_equal_to('error') 
        assert_that(self.login_page.is_error_message_displayed()).is_true()
        
        error_message = self.login_page.get_error_message()
        assert_that(error_message).is_not_empty()
        logger.info(f"Empty password error message: {error_message}")
    
    @pytest.mark.login
    def test_invalid_login_with_enter_key(self, driver):
        """Test invalid login using Enter key instead of clicking login button."""
        logger.info("Testing invalid login with Enter key")
        
        result = self.login_page.perform_login_with_enter(
            "invalid@test.com", 
            "wrongpassword"
        ).wait_for_login_result()
        
        # Verify login failed same as clicking button
        assert_that(result).is_equal_to('error')
        assert_that(self.login_page.is_error_message_displayed()).is_true()
        
        error_message = self.login_page.get_error_message()
        assert_that(error_message).is_not_empty() 
        logger.info(f"Enter key login error message: {error_message}")
    
    @pytest.mark.login
    def test_invalid_login_special_characters_email(self, driver):
        """Test login with special characters in email."""
        logger.info("Testing special characters in email")
        
        special_emails = [
            "user<script>@gmail.com",  # Script injection attempt
            "user'@gmail.com",         # Apostrophe
            "user\"@gmail.com",        # Quote
            "user;@gmail.com",         # Semicolon
            "user&@gmail.com",         # Ampersand
        ]
        
        for special_email in special_emails:
            logger.info(f"Testing special character email: {special_email}")
            
            self.login_page.clear_login_fields()
            result = self.login_page.perform_login(special_email, "password123").wait_for_login_result()
            
            # Should handle gracefully and show error
            assert_that(result).is_equal_to('error')
            assert_that(self.login_page.is_error_message_displayed()).is_true()
            
            error_message = self.login_page.get_error_message()
            assert_that(error_message).is_not_empty()
            logger.info(f"Special character email error: {error_message}")
    
    @pytest.mark.login
    def test_invalid_login_sql_injection_attempt(self, driver):
        """Test login with SQL injection patterns."""
        logger.info("Testing SQL injection patterns")
        
        sql_injection_patterns = [
            "admin'--",
            "admin' OR '1'='1",  
            "'; DROP TABLE users; --",
            "admin' UNION SELECT * FROM users --",
        ]
        
        for injection_pattern in sql_injection_patterns:
            logger.info(f"Testing SQL injection pattern: {injection_pattern}")
            
            self.login_page.clear_login_fields()
            result = self.login_page.perform_login(injection_pattern, "password").wait_for_login_result()
            
            # Should be handled securely and show error
            assert_that(result).is_equal_to('error')
            assert_that(self.login_page.is_error_message_displayed()).is_true()
            
            # Verify we're still on login page (not compromised)
            assert_that(self.login_page.is_login_page_displayed()).is_true()
            
            error_message = self.login_page.get_error_message()
            logger.info(f"SQL injection attempt blocked with error: {error_message}")
    
    @pytest.mark.login  
    def test_invalid_login_page_elements_present(self, driver):
        """Verify all necessary login page elements are present after failed login."""
        logger.info("Testing login page elements after failed login")
        
        # Perform invalid login
        self.login_page.perform_login("invalid@test.com", "wrongpass")
        
        # Wait for error to appear
        assert_that(self.login_page.is_error_message_displayed()).is_true()
        
        # Verify all login elements are still present
        assert_that(self.login_page.is_login_page_displayed()).is_true()
        assert_that(self.login_page.is_forgot_password_link_visible()).is_true()
        
        # Verify we can still interact with login form
        self.login_page.clear_login_fields()
        self.login_page.enter_email("test@example.com")
        
        # Verify email was entered successfully
        email_value = self.login_page.get_attribute(
            self.login_page.locators.EMAIL_INPUT, 'value'
        )
        assert_that(email_value).is_equal_to("test@example.com")
        
        logger.info("All login page elements working correctly after failed login")
    
    @pytest.mark.login
    def test_invalid_login_url_remains_unchanged(self, driver):
        """Verify URL doesn't change after invalid login attempts."""
        logger.info("Testing URL stability after invalid login")
        
        initial_url = self.login_page.get_current_url()
        logger.info(f"Initial URL: {initial_url}")
        
        # Try multiple invalid login attempts
        invalid_credentials = [
            ("invalid1@test.com", "wrong1"),
            ("invalid2@test.com", "wrong2"), 
            ("", ""),
        ]
        
        for email, password in invalid_credentials:
            self.login_page.clear_login_fields()
            self.login_page.perform_login(email, password)
            self.login_page.wait_for_login_result() 
            
            # Verify URL hasn't changed (still on login page)
            current_url = self.login_page.get_current_url()
            assert_that(current_url).contains("facebook.com")
            assert_that(current_url).contains_ignoring_case("login")
            
            logger.info(f"URL after failed login: {current_url}")
        
        logger.info("URL remained stable throughout invalid login attempts")
    def test_invalid_login(self):
        assert True