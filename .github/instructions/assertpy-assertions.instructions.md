---
description: "Use when writing test assertions, validating test outcomes, or checking expected vs actual values. Enforces assertpy library for all test assertions instead of standard Python assert statements."
name: "Assertpy Test Assertions"
applyTo: "**/*test*.py"
---

# Assertpy Assertion Guidelines

Use only assertpy assertions in test files. Never use standard Python `assert` statements or built-in pytest assertions.

## Required Import

Always include at assertpy import at the top of test files:

```python
from assertpy import assert_that
```

## Standard Replacements

**❌ Don't use standard assertions:**
```python
# Standard Python assertions
assert user.is_active == True
assert len(items) > 0
assert result is not None
assert "error" in response_text

# Pytest built-in assertions  
assert result == expected
```

**✅ Use assertpy instead:**
```python
# Boolean checks
assert_that(user.is_active).is_true()
assert_that(user.is_archived).is_false()

# Numeric comparisons
assert_that(len(items)).is_greater_than(0)
assert_that(score).is_between(0, 100)
assert_that(total).is_equal_to(expected_total)

# Null/None checks
assert_that(result).is_not_none()
assert_that(empty_var).is_none()

# String assertions
assert_that(response_text).contains("success")
assert_that(email).matches(r'^[^@]+@[^@]+\.[^@]+$')
assert_that(username).starts_with("user_")

# Collection assertions
assert_that(user_list).is_not_empty()
assert_that(items).has_length(5)
assert_that(names).contains("John")
```

## Advanced Patterns

```python
# Exception assertions
assert_that(lambda: divide_by_zero()).raises(ZeroDivisionError)

# Object property assertions
assert_that(user).has_name("John").has_age(25)

# Complex collection assertions
assert_that(users).extracting('name').contains('Alice', 'Bob')
assert_that(numbers).is_sorted()

# Custom error messages
assert_that(total, "Payment total calculation").is_equal_to(expected)
```

## Why Assertpy?

- **Readability**: Natural language assertions that read like English
- **Rich API**: Extensive built-in assertion methods for all data types
- **Better errors**: Clear, descriptive failure messages with context
- **Fluent interface**: Chainable assertions for complex validations
- **Extensibility**: Easy to create custom assertion methods

## Installation

Ensure assertpy is in your requirements.txt:
```
assertpy>=1.1
```