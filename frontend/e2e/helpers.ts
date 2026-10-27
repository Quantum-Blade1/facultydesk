import { Page, expect } from "@playwright/test";

export async function loginAs(page: Page, email: string, pass: string): Promise<void> {
  await page.context().clearCookies();
  await page.goto("/login");
  await page.fill('input[type="email"]', email);
  await page.fill('input[type="password"]', pass);
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/\/today/);
}
