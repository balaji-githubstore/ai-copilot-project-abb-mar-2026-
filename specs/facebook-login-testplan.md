# Facebook Login Functionality Test Plan

## Application Overview

Comprehensive test plan for Facebook login functionality covering valid login scenarios, invalid login attempts, and error message validation. Tests are designed to verify proper authentication flows, input validation, security measures, and user experience across different login states.

## Test Scenarios

### 1. Valid Login Scenarios

**Seed:** `tests/seed.spec.ts`

#### 1.1. Successful Login with Valid Email and Password

**File:** `tests/valid-login/successful-login-email.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage (facebook.com)
    - expect: Page loads successfully
    - expect: Login form is visible
    - expect: Email and password input fields are present
  2. Enter a valid email address in the email/phone field
    - expect: Email is accepted in the input field
    - expect: No validation errors appear
  3. Enter the correct password for the account
    - expect: Password is masked with dots/asterisks
    - expect: Password field accepts the input
  4. Click the 'Log In' button
    - expect: User is successfully logged into their account
    - expect: User is redirected to Facebook feed/homepage
    - expect: User's name appears in the top navigation
    - expect: Login form is no longer visible

#### 1.2. Successful Login with Valid Phone Number and Password

**File:** `tests/valid-login/successful-login-phone.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage (facebook.com)
    - expect: Page loads successfully
    - expect: Login form is visible
  2. Enter a valid phone number in the email/phone field
    - expect: Phone number is accepted in the input field
    - expect: No validation errors appear
  3. Enter the correct password for the account
    - expect: Password is masked
    - expect: Password field accepts the input
  4. Click the 'Log In' button
    - expect: User is successfully logged into their account
    - expect: User is redirected to Facebook feed/homepage
    - expect: User's profile information is accessible

#### 1.3. Login with Remember Me Option

**File:** `tests/valid-login/login-remember-me.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is displayed
  2. Enter valid email and password
    - expect: Credentials are entered correctly
  3. Check the 'Keep me logged in' checkbox if available
    - expect: Checkbox is selected
  4. Click 'Log In'
    - expect: User is logged in successfully
    - expect: Session persistence is enabled for future visits

### 2. Invalid Login Scenarios

**Seed:** `tests/seed.spec.ts`

#### 2.1. Login with Invalid Email Format

**File:** `tests/invalid-login/invalid-email-format.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is visible
  2. Enter an invalid email format (e.g., 'invalidemail', 'test@', '@domain.com')
    - expect: Invalid email is entered in the field
  3. Enter any password
    - expect: Password is entered
  4. Click 'Log In'
    - expect: Login fails
    - expect: Error message appears indicating invalid email format
    - expect: User remains on login page
    - expect: Form fields retain entered values

#### 2.2. Login with Non-existent Email

**File:** `tests/invalid-login/nonexistent-email.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is displayed
  2. Enter a valid email format but non-existent account (e.g., 'nonexistent@example.com')
    - expect: Email is entered in correct format
  3. Enter any password
    - expect: Password is entered
  4. Click 'Log In'
    - expect: Login fails
    - expect: Error message appears: 'The email address or phone number you entered isn't connected to an account'
    - expect: User remains on login page

#### 2.3. Login with Correct Email but Wrong Password

**File:** `tests/invalid-login/wrong-password.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is visible
  2. Enter a valid/existing email address
    - expect: Valid email is entered
  3. Enter an incorrect password
    - expect: Wrong password is entered and masked
  4. Click 'Log In'
    - expect: Login fails
    - expect: Error message appears: 'The password you entered is incorrect'
    - expect: 'Forgotten password?' link is displayed
    - expect: User remains on login page

#### 2.4. Login with Both Invalid Email and Password

**File:** `tests/invalid-login/both-invalid.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is displayed
  2. Enter an invalid/non-existent email
    - expect: Invalid email is entered
  3. Enter an incorrect password
    - expect: Wrong password is entered
  4. Click 'Log In'
    - expect: Login fails
    - expect: Appropriate error message is displayed
    - expect: User remains on login page

### 3. Empty Field Validation

**Seed:** `tests/seed.spec.ts`

#### 3.1. Login with Empty Email Field

**File:** `tests/empty-fields/empty-email.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is visible
  2. Leave the email/phone field empty
    - expect: Email field remains empty
  3. Enter a valid password
    - expect: Password is entered
  4. Click 'Log In'
    - expect: Login fails
    - expect: Validation error appears for empty email field
    - expect: Error message indicates email/phone is required
    - expect: User remains on login page

#### 3.2. Login with Empty Password Field

**File:** `tests/empty-fields/empty-password.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is displayed
  2. Enter a valid email address
    - expect: Email is entered correctly
  3. Leave the password field empty
    - expect: Password field remains empty
  4. Click 'Log In'
    - expect: Login fails
    - expect: Validation error appears for empty password field
    - expect: Error message indicates password is required
    - expect: User remains on login page

#### 3.3. Login with Both Fields Empty

**File:** `tests/empty-fields/both-empty.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is visible
  2. Leave both email and password fields empty
    - expect: Both fields remain empty
  3. Click 'Log In'
    - expect: Login fails
    - expect: Validation errors appear for both fields
    - expect: Error messages indicate both email and password are required
    - expect: User remains on login page

#### 3.4. Login with Only Whitespace in Fields

**File:** `tests/empty-fields/whitespace-only.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is displayed
  2. Enter only spaces in the email field
    - expect: Whitespace is entered in email field
  3. Enter only spaces in the password field
    - expect: Whitespace is entered in password field
  4. Click 'Log In'
    - expect: Login fails
    - expect: Validation errors treat whitespace as empty
    - expect: Appropriate error messages are displayed
    - expect: User remains on login page

### 4. Security and Edge Cases

**Seed:** `tests/seed.spec.ts`

#### 4.1. SQL Injection Attempt in Login Fields

**File:** `tests/security/sql-injection.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is visible
  2. Enter SQL injection payload in email field (e.g., "' OR '1'='1")
    - expect: Input is entered in email field
  3. Enter SQL injection payload in password field
    - expect: Input is entered in password field
  4. Click 'Log In'
    - expect: Login fails safely
    - expect: No SQL injection occurs
    - expect: Appropriate error message is shown
    - expect: System remains secure

#### 4.2. XSS Attempt in Login Fields

**File:** `tests/security/xss-attempt.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is displayed
  2. Enter XSS payload in email field (e.g., "<script>alert('xss')</script>")
    - expect: XSS payload is entered
  3. Enter normal password
    - expect: Password is entered
  4. Click 'Log In'
    - expect: Login fails
    - expect: No script execution occurs
    - expect: XSS payload is properly sanitized
    - expect: No alert or malicious code runs

#### 4.3. Maximum Character Length Testing

**File:** `tests/edge-cases/max-length.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is available
  2. Enter extremely long string in email field (1000+ characters)
    - expect: Long string is entered or truncated appropriately
  3. Enter extremely long string in password field (1000+ characters)
    - expect: Long string is handled appropriately
  4. Click 'Log In'
    - expect: Login fails gracefully
    - expect: No system errors occur
    - expect: Appropriate validation message is shown

#### 4.4. Special Characters in Login Fields

**File:** `tests/edge-cases/special-characters.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is displayed
  2. Enter email with special characters (e.g., "user+test@domain.com")
    - expect: Special characters are accepted in email field
  3. Enter password with special characters and symbols
    - expect: Special characters are accepted in password field
  4. Click 'Log In'
    - expect: Login attempt is processed correctly
    - expect: Special characters are handled properly
    - expect: Appropriate response is given based on credential validity

### 5. User Interface and Experience Testing

**Seed:** `tests/seed.spec.ts`

#### 5.1. Login Form Visual Elements

**File:** `tests/ui-ux/form-elements.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Page loads completely
  2. Verify all login form elements are present and properly styled
    - expect: Email/Phone input field is visible and properly labeled
    - expect: Password input field is visible and properly labeled
    - expect: Log In button is visible and clickable
    - expect: Forgotten password link is present
    - expect: Create new account link/button is present
  3. Check form responsiveness on different screen sizes
    - expect: Form elements adapt to screen size
    - expect: All elements remain accessible and usable
  4. Verify accessibility features
    - expect: Form fields have proper ARIA labels
    - expect: Tab navigation works correctly
    - expect: Screen readers can identify all elements

#### 5.2. Password Field Behavior

**File:** `tests/ui-ux/password-behavior.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is visible
  2. Click in the password field and start typing
    - expect: Characters are masked with dots or asterisks
    - expect: Password field is properly focused
  3. Verify show/hide password functionality if available
    - expect: Show password toggle works correctly
    - expect: Password visibility can be toggled
    - expect: Eye icon or similar control functions properly
  4. Test copy/paste functionality in password field
    - expect: Password can be pasted but may be masked
    - expect: Copy functionality may be restricted for security

#### 5.3. Keyboard Navigation and Shortcuts

**File:** `tests/ui-ux/keyboard-navigation.spec.ts`

**Steps:**
  1. Navigate to Facebook homepage
    - expect: Login form is displayed
  2. Use Tab key to navigate through login form elements
    - expect: Tab order is logical: email field → password field → Log In button
    - expect: Focus indicators are clearly visible
    - expect: All interactive elements are reachable
  3. Fill in login credentials using keyboard only
    - expect: Both fields can be filled using keyboard
    - expect: Navigation between fields works smoothly
  4. Press Enter key in the email field
    - expect: Focus moves to password field or form submits if both fields are filled
  5. Press Enter key in the password field
    - expect: Form submits (login attempt is made)
