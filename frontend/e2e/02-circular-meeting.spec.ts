import { test, expect } from "@playwright/test";
import path from "node:path";
import { loginAs } from "./helpers";

test.describe("Journey 2: Circular OCR Review Queue & Meeting Confirmation", () => {
  test("Faculty uploads circular sample, HOD reviews & confirms, attendees see meeting on calendar", async ({
    page,
  }) => {
    test.setTimeout(60000);

    // 1. Log in as Faculty KKS
    await loginAs(page, "kks@facultydesk.local", "Faculty123!");

    // 2. Navigate to Circulars page
    await page.goto("/circulars");
    await expect(page.locator("h1")).toContainText("Meeting Circulars");

    // 3. Upload circular sample 01_clean_text.pdf
    const filePath = path.resolve(__dirname, "../../samples/circulars/01_clean_text.pdf");
    const fileInput = page.locator('input[type="file"][accept*="pdf"]').first();
    await fileInput.setInputFiles(filePath);
    await expect(page.getByText(/Circular uploaded/i)).toBeVisible({ timeout: 10000 });
    await page.waitForTimeout(2000);

    // 4. Log in as HOD to review queue
    await loginAs(page, "hod.cse@facultydesk.local", "Hod123!");

    await page.goto("/circulars");

    // 5. Locate a circular in review queue (wait for OCR extraction and auto-poll)
    const reviewBtn = page.getByRole("button", { name: /Review & Confirm|View Details/i }).first();
    await expect(reviewBtn).toBeVisible({ timeout: 25000 });
    await reviewBtn.click();

    // 6. Review modal opens; verify confirm button is present
    const confirmMeetingBtn = page.getByRole("button", { name: "Confirm & Schedule Meeting" });
    await expect(confirmMeetingBtn).toBeVisible();

    // Fill date and start time if not auto-filled
    const dateInput = page.locator('input[type="date"]').first();
    const dateVal = await dateInput.inputValue();
    const upcomingDate = new Date(Date.now() + 3 * 86400 * 1000).toISOString().slice(0, 10);
    await dateInput.fill(upcomingDate);

    const timeInput = page.locator('input[type="time"]').first();
    const timeVal = await timeInput.inputValue();
    if (!timeVal) {
      await timeInput.fill("14:30");
    }

    // Confirm meeting
    await confirmMeetingBtn.click();
    await page.waitForTimeout(1000);

    // 7. Log in as Faculty and verify meeting on Calendar
    await loginAs(page, "kks@facultydesk.local", "Faculty123!");

    await page.goto("/calendar");
    await expect(page.locator("h1")).toContainText(/Academic (Calendar|Schedule)/);
    const eventCards = page.locator(".space-y-3 > div, h4");
    await expect(eventCards.first()).toBeVisible({ timeout: 15000 });
    expect(await eventCards.count()).toBeGreaterThanOrEqual(1);
  });
});
