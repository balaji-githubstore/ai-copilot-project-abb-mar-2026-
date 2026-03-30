---
name: selenium-automation-patterns
description: 'Write Selenium WebDriver code using explicit waits and page object model patterns. Use for creating robust automation scripts, implementing page objects, debugging flaky tests, and following Selenium best practices.'
argument-hint: 'Component to implement (e.g., "login page object" or "test method with explicit waits")'
---

# Selenium Automation Patterns

## When to Use
- Writing new Selenium WebDriver automation code
- Implementing page object model classes
- Fixing flaky tests with proper wait strategies
- Creating robust locator strategies
- Debugging element interaction issues
- Refactoring existing Selenium code to best practices

## Core Principles

### 1. Explicit Waits Only
- **NEVER use** `time.sleep()` or implicit waits
- **ALWAYS use** `WebDriverWait` with expected conditions
- **DEFAULT timeout**: 10 seconds for most operations
- **CUSTOM timeouts**: Use shorter waits (2-5s) for elements that should appear quickly

### 2. Page Object Model Structure
- **Page classes** inherit from `BasePage`
- **Locators** defined in separate locator classes
- **Methods** return page objects for chaining
- **Assertions** belong in test files, not page objects

### 3. Resilient Locator Strategy Priority
1. **ID** (highest priority - unique and stable)
2. **CSS selectors** (good performance and readability)  
3. **XPath** (use only when absolutely necessary)
4. **AVOID** text-based locators (fragile with internationalization)

## Step-by-Step Implementation

### Phase 1: Create Locator Class
```python
# locators/{page_name}_locators.py
from selenium.webdriver.common.by import By

class LoginLocators:
    # ID selectors (preferred)
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "pass")
    LOGIN_BUTTON = (By.ID, "loginbutton")
    
    # CSS selectors (when ID unavailable)
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-testid='royal_email_error']")
    FORGOT_PASSWORD = (By.CSS_SELECTOR, "a[href*='recover']")
    
    # XPath (last resort - when structure matters)
    DYNAMIC_ERROR = (By.XPATH, "//div[@role='alert'][contains(@class, 'error')]")
```

### Phase 2: Implement Base Page Class
```python
# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.short_wait = WebDriverWait(driver, 3)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def wait_for_element_visible(self, locator, timeout=10):
        \"\"\"Wait for element to be visible and return it.\"\"\"
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f"Element not visible: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=10):
        \"\"\"Wait for element to be clickable and return it.\"\"\"
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            raise
    
    def is_element_present(self, locator, timeout=3):
        \"\"\"Check if element is present without raising exception.\"\"\"
        try:
            self.short_wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
```

### Phase 3: Create Page Object Class
```python
# pages/{page_name}_page.py
from pages.base_page import BasePage
from locators.{page_name}_locators import {Page}Locators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class {Page}Page(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = {Page}Locators()
    
    # Navigation methods
    def navigate_to_{page}(self):
        \"\"\"Navigate to {page} page and verify loading.\"\"\"
        self.driver.get(self.base_url + "/{page}")
        self.wait_for_{page}_page_load()
        return self
    
    # Element interaction methods  
    def enter_{field}(self, value):
        \"\"\"Enter value into {field} field with explicit wait.\"\"\"
        element = self.wait_for_element_clickable(self.locators.{FIELD}_INPUT)
        element.clear()
        element.send_keys(value)
        return self
    
    def click_{element}(self):
        \"\"\"Click {element} with explicit wait for clickability.\"\"\"
        element = self.wait_for_element_clickable(self.locators.{ELEMENT}_BUTTON)
        element.click()
        return self
    
    # State verification methods
    def is_{page}_page_displayed(self):
        \"\"\"Verify {page} page is displayed by checking key elements.\"\"\"
        return (self.is_element_present(self.locators.{KEY_ELEMENT}) and
                self.wait_for_element_visible(self.locators.{ANOTHER_KEY_ELEMENT}))
    
    def get_{data}_message(self):
        \"\"\"Get {data} message text with explicit wait.\"\"\"
        element = self.wait_for_element_visible(self.locators.{DATA}_MESSAGE)
        return element.text
    
    # Complex workflow methods (chaining)
    def perform_{action}(self, param1, param2):
        \"\"\"Perform complete {action} workflow.\"\"\"
        return (self.enter_{field1}(param1)
                   .enter_{field2}(param2)  
                   .click_{submit_button}())
    
    # Wait for state changes
    def wait_for_{action}_result(self, timeout=10):
        \"\"\"Wait for {action} to complete and return result state.\"\"\"
        try:
            # Wait for success indicator
            self.wait.until(EC.url_contains("success"))
            return "success"
        except TimeoutException:
            # Check for error state
            if self.is_element_present(self.locators.ERROR_MESSAGE):
                return "error"
            return "timeout"
```

### Phase 4: Implement Test Methods
```python
# tests/test_{feature}/test_{feature}.py
import pytest
from assertpy import assert_that
from pages.{page}_page import {Page}Page

class Test{Feature}:
    @pytest.fixture(autouse=True)
    def setup_method(self, driver):
        \"\"\"Setup with explicit verification.\"\"\"
        self.{page}_page = {Page}Page(driver)
        self.{page}_page.navigate_to_{page}()
        
        # Explicit verification page loaded
        assert_that(self.{page}_page.is_{page}_page_displayed()).is_true()
    
    def test_{scenario}(self, driver):
        \"\"\"Test {scenario} with explicit waits and assertpy.\"\"\"
        # Arrange - set up test data
        test_data = "test_value"
        
        # Act - perform action with explicit waits
        result = (self.{page}_page
                    .perform_{action}(test_data)
                    .wait_for_{action}_result())
        
        # Assert - verify outcome with assertpy
        assert_that(result).is_equal_to("expected_result")
        assert_that(self.{page}_page.get_{verification}_data()).contains("expected_text")
```

## Wait Strategy Patterns

### Standard Waits
```python
# Wait for element to be visible
element = self.wait_for_element_visible(locator)

# Wait for element to be clickable  
element = self.wait_for_element_clickable(locator, timeout=5)

# Wait for text to be present
self.wait.until(EC.text_to_be_present_in_element(locator, "expected text"))

# Wait for URL change
self.wait.until(EC.url_contains("success"))
```

### Custom Wait Conditions
```python
def wait_for_ajax_complete(self, timeout=10):
    \"\"\"Wait for jQuery/AJAX to complete.\"\"\"
    wait = WebDriverWait(self.driver, timeout)
    wait.until(lambda driver: driver.execute_script("return jQuery.active == 0"))

def wait_for_element_count(self, locator, expected_count, timeout=10):
    \"\"\"Wait for specific number of elements matching locator.\"\"\"
    wait = WebDriverWait(self.driver, timeout)
    wait.until(lambda driver: len(driver.find_elements(*locator)) == expected_count)
```

## Error Handling Patterns

### Robust Element Interactions
```python
def safe_click(self, locator, timeout=10):
    \"\"\"Click element with retry logic for stale elements.\"\"\"
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            element.click()
            return True
        except StaleElementReferenceException:
            if attempt == max_attempts - 1:
                raise
            self.logger.warning(f"Stale element, retrying... (attempt {attempt + 1})")
        except TimeoutException:
            self.logger.error(f"Element not clickable after {timeout}s: {locator}")
            raise
    return False
```

## Quality Checklists

### Before Implementation
- [ ] Identified page elements and their most stable locators
- [ ] Defined page object methods that return self or other pages
- [ ] Planned explicit wait strategies for each interaction
- [ ] Separated test logic from page object logic

### After Implementation  
- [ ] All waits use `WebDriverWait` with `expected_conditions`
- [ ] No `time.sleep()` calls anywhere in code
- [ ] Page methods return page objects for chaining
- [ ] Test assertions use assertpy, not standard assert
- [ ] Error handling covers common Selenium exceptions
- [ ] Locators prioritize ID > CSS > XPath

### Testing Validation
- [ ] Tests pass consistently (no flaky failures)
- [ ] Page load times are reasonable (under 10s)
- [ ] Clear error messages when elements not found
- [ ] Tests work across different browsers
- [ ] Code follows PEP 8 style guidelines

## Common Anti-patterns to Avoid

### ❌ Bad Practices
```python
# DON'T: Use implicit waits or sleep
time.sleep(5)
driver.implicitly_wait(10)

# DON'T: Direct driver calls in tests  
driver.find_element(By.ID, "email").send_keys("test")

# DON'T: Assertions in page objects
def login(self, email, password):
    # ... perform login
    assert "Welcome" in self.driver.title  # NO!

# DON'T: Fragile XPath locators
(By.XPATH, "//div[3]/span[2]/a[1]")  # Breaks easily
```

### ✅ Best Practices  
```python
# DO: Use explicit waits
element = self.wait_for_element_clickable(locator, timeout=10)

# DO: Use page object methods in tests
self.login_page.perform_login(email, password)

# DO: Assertions in tests only
result = self.login_page.perform_login(email, password)
assert_that(result).is_equal_to("success")

# DO: Stable locators with meaning
(By.CSS_SELECTOR, "[data-testid='login-button']")
```

## Implementation Order

1. **Create locator class** with stable selectors
2. **Extend base page** with wait utilities  
3. **Implement page methods** with explicit waits
4. **Write test methods** using page objects
5. **Add error handling** for robustness
6. **Validate** with multiple test runs

This ensures each component builds on the previous one and maintains consistency across the automation framework.