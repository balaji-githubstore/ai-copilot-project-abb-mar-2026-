// spec: specs/facebook-login-testplan.md
// seed: seed.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Invalid Login Scenarios', () => {
  test('Login with Invalid Email Format', async ({ page }) => {
    // 1. Navigate to Facebook homepage
    await page.goto('https://facebook.com');
    
    // Verify login form is visible
    await expect(page.getByRole('textbox', { name: 'Email address or mobile number' })).toBeVisible();

    // 2. Enter an invalid email format (e.g., 'invalidemail', 'test@', '@domain.com')
    await page.getByRole('textbox', { name: 'Email address or mobile number' }).fill('invalidemail');
    
    // Verify invalid email is entered in the field
    await expect(page.getByRole('textbox', { name: 'Email address or mobile number' })).toHaveValue('invalidemail');

    // 3. Enter any password
    await page.getByRole('textbox', { name: 'Password' }).fill('testpassword123');
    
    // Verify password is entered
    await expect(page.getByRole('textbox', { name: 'Password' })).toHaveValue('testpassword123');

    // 4. Click 'Log In'
    await page.getByRole('button', { name: 'Log in' }).click();

    // Verify login fails - error message appears indicating invalid email format
    await expect(page.getByText('The email address or mobile number you entered isn\'t connected to an account.')).toBeVisible();
    
    // Verify user remains on login page
    await expect(page.getByRole('button', { name: 'Log in' })).toBeVisible();
    
    // Verify form fields retain entered values
    await expect(page.getByRole('textbox', { name: 'Password' })).toHaveValue('testpassword123');
  });
});