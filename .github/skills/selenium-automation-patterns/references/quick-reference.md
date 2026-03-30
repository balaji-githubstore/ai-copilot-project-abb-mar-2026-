# Selenium Automation Quick Reference

## Essential Wait Patterns

```python
# Wait for element to be visible
element = self.wait_for_element_visible(locator, timeout=10)

# Wait for element to be clickable
element = self.wait_for_element_clickable(locator, timeout=10)

# Wait for text to be present 
self.wait.until(EC.text_to_be_present_in_element(locator, "text"))

# Wait for URL to change
self.wait.until(EC.url_contains("success"))

# Wait for element to disappear
self.wait.until(EC.invisibility_of_element_located(locator))
```

## Locator Priority Order

1. **ID** - `(By.ID, "element-id")` ✅ Most stable
2. **CSS** - `(By.CSS_SELECTOR, "[data-testid='element']")` ✅ Good performance
3. **XPath** - `(By.XPATH, "//div[@role='button']")` ⚠️ Use sparingly

## Page Object Method Patterns

```python
# Input method
def enter_field(self, value):
    element = self.wait_for_element_clickable(self.locators.FIELD_INPUT)
    element.clear()
    element.send_keys(value)
    return self  # Enable chaining

# Click method  
def click_button(self):
    element = self.wait_for_element_clickable(self.locators.BUTTON)
    element.click()
    return self  # or return next page object

# Verification method
def is_element_displayed(self):
    return self.is_element_present(self.locators.ELEMENT, timeout=5)
```

## Common ExpectedConditions

- `presence_of_element_located(locator)` - Element exists in DOM
- `visibility_of_element_located(locator)` - Element visible and has height/width
- `element_to_be_clickable(locator)` - Element visible and enabled
- `text_to_be_present_in_element(locator, text)` - Text appears in element
- `url_contains(text)` - URL contains specified text
- `staleness_of(element)` - Element is no longer attached to DOM

## Error Handling Template

```python
try:
    element = self.wait_for_element_clickable(locator, timeout=10)
    element.click()
except TimeoutException:
    self.logger.error(f"Element not clickable: {locator}")
    raise
except StaleElementReferenceException:
    self.logger.warning("Stale element, retrying...")
    # Retry logic here
    raise
```

## Test Structure Template

```python
def test_scenario(self, driver):
    # Arrange
    test_data = "value"
    
    # Act
    result = (self.page
                .perform_action(test_data)
                .wait_for_result())
    
    # Assert
    assert_that(result).is_equal_to("expected")
```