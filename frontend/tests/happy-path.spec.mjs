import { test, expect } from '@playwright/test';

test('happy path: login and create issue', async ({ context, page }) => {
  await context.clearCookies();

  await page.goto('/');
  await page.screenshot({ path: 'debug-1-login-page.png', fullPage: true });

  await page.getByPlaceholder('Username').fill('rolika.agarwal@pangeatech.net');

  await page.getByPlaceholder('Password').fill('Rolika1234');

  await page.getByRole('button', { name: 'Login' }).click();

  await expect(page.getByText('Dashboard', { exact: true })).toBeVisible();


  await page.screenshot({ path: 'debug-2-after-login.png', fullPage: true });

  await page.getByRole('button', { name: 'Create Issue' }).click();

  await page.getByPlaceholder('Title').fill('Test Issue');
  await page.getByPlaceholder('Description').fill('This is a test issue');

  await page.getByRole('button', { name: 'Save' }).click();

  await expect(page.getByText('Test Issue').first()).toBeVisible();


  await page.screenshot({ path: 'debug-3-after-issue.png', fullPage: true });

});
