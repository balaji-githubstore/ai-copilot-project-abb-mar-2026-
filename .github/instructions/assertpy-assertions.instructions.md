---
description: Use assertpy for all test assertions
name: assertpy-assertions
applyTo: "**/*test*.py"
---

# Assertpy Assertion Guidelines

Always use the `assertpy` library for test assertions instead of standard Python `assert` statements.

## Required Import

```python
from assertpy import assert_that
```

## Basic Assertion Replacements

Replace standard Python assertions with assertpy equivalents:

| Standard Assert | Assertpy Equivalent |
|---|---|
| `assert user.is_active == True` | `assert_that(user.is_active).is_true()` |
| `assert user.is_active == False` | `assert_that(user.is_active).is_false()` |
| `assert len(items) > 0` | `assert_that(len(items)).is_greater_than(0)` |
| `assert result is not None` | `assert_that(result).is_not_none()` |
| `assert result is None` | `assert_that(result).is_none()` |
| `assert a == b` | `assert_that(a).is_equal_to(b)` |
| `assert a != b` | `assert_that(a).is_not_equal_to(b)` |

## Examples

### Boolean Checks
```python
# Before
assert user.is_active == True

# After
assert_that(user.is_active).is_true()
```

### Numeric Checks
```python
# Before
assert len(items) > 0

# After
assert_that(len(items)).is_greater_than(0)
```

### Null Checks
```python
# Before
assert result is not None

# After
assert_that(result).is_not_none()
```

### String Assertions
```python
assert_that(response).contains("Paris")
assert_that(response).starts_with("The capital")
assert_that(response).ends_with("France.")
```

### Collection Assertions
```python
assert_that(items).is_not_empty()
assert_that(items).contains("Paris")
assert_that(set(df.columns)).is_equal_to(expected_columns)
```

## Advanced Patterns

### Exception Assertions
```python
assert_that(lambda: risky_function()).raises(ValueError).when_called_with(bad_input)
```

### Object Property Assertions
```python
assert_that(user).has_name("Alice").has_age(30)
```

### Extracting from Collections
```python
assert_that(users).extracting("name").contains("Alice", "Bob")
```

### Custom Error Messages
```python
assert_that(result).described_as("API response should not be None").is_not_none()
assert_that(score).described_as("Score should be above threshold").is_greater_than(0.5)
```

## Installation

Add to `requirements.txt`:
```
assertpy>=1.1
```
