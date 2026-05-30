import { test, expect } from '@playwright/test';

test('index page loads', async ({ page }) => {
  await page.goto('http://127.0.0.1:8000/');
  await expect(page.locator('body')).toContainText('Narde');
});

test('health endpoint responds', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/health');
  expect(response?.status()).toBe(200);
  const json = await response?.json();
  expect(json).toEqual({ status: 'ok' });
});
