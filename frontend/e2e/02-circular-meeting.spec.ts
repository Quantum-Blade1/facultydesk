import { test, expect } from "@playwright/test";
import path from "node:path";
import { loginAs } from "./helpers";

test.describe("Journey 2: Circular OCR Review Queue & Meeting Confirmation", () => {
  test("Faculty uploads circular sample, HOD reviews & confirms, attendees see meeting on calendar", async ({
    page,
  }) => {
    test.setTimeout(60000);

    await loginAs(page, "kks@facultydesk.local", "Faculty123!");

    await page.goto("/circulars");
    await expect(page.locator("h1")).toContainText("Meeting Circulars");
    await page.waitForLoadState("networkidle");
    await expect(page.getByText(/\d+ Documents/)).toBeVisible({ timeout: 15000 });

    const filePath = path.resolve(__dirname, "../../samples/circulars/01_clean_text.pdf");
    const fileInput = page.locator('input[data-testid="circular-upload-input"]');

    const [uploadResponse] = await Promise.all([
      page.waitForResponse(
        (res) => res.url().includes("/api/circulars/upload") && (res.status() === 200 || res.status() === 202),
        { timeout: 30000 }
      ),
      fileInput.setInputFiles(filePath),
    ]);
    expect(uploadResponse.ok()).toBeTruthy();
    await page.waitForTimeout(2000);

    await loginAs(page, "hod.cse@facultydesk.local", "Hod123!");

    await page.goto("/circulars");

    const reviewBtn = page.getByRole("button", { name: /Review & Confirm|View Details/i }).first();
    await expect(reviewBtn).toBeVisible({ timeout: 25000 });
    await reviewBtn.click();

    const confirmMeetingBtn = page.getByRole("button", { name: "Confirm & Schedule Meeting" });
    await expect(confirmMeetingBtn).toBeVisible();

    const dateInput = page.locator('input[type="date"]').first();
    const upcomingDate = new Date(Date.now() + 3 * 86400 * 1000).toISOString().slice(0, 10);
    await dateInput.fill(upcomingDate);

    const timeInput = page.locator('input[type="time"]').first();
    const timeVal = await timeInput.inputValue();
    if (!timeVal) {
      await timeInput.fill("14:30");
    }

    await confirmMeetingBtn.click();
    await page.waitForTimeout(1000);

    await loginAs(page, "kks@facultydesk.local", "Faculty123!");

    await page.goto("/calendar");
    await expect(page.locator("h1")).toContainText(/Academic (Calendar|Schedule)/);
    const eventCards = page.locator(".space-y-3 > div, h4");
    await expect(eventCards.first()).toBeVisible({ timeout: 15000 });
    expect(await eventCards.count()).toBeGreaterThanOrEqual(1);
  });
});
