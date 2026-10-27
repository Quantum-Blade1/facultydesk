import { test, expect } from "@playwright/test";
import path from "node:path";
import { loginAs } from "./helpers";

test.describe("Journey 1: Timetable Ingestion & Class Generation", () => {
  test("HOD uploads standard timetable, confirms, and faculty calendar displays classes", async ({
    page,
  }) => {
    test.setTimeout(60000);

    // 1. Log in as HOD
    await loginAs(page, "hod.cse@facultydesk.local", "Hod123!");

    // 2. Navigate to Timetables page
    await page.goto("/timetables");
    await expect(page.locator("h1")).toContainText("Upload Department Timetable");

    // 3. Upload standard_timetable.xlsx
    const filePath = path.resolve(__dirname, "../../samples/timetables/standard_timetable.xlsx");
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(filePath);

    // 4. Click Parse Timetable
    const parseBtn = page.getByRole("button", { name: "Parse Timetable" });
    await expect(parseBtn).toBeEnabled({ timeout: 10000 });
    await parseBtn.click();

    // 5. Wait for preview report and confirm button
    const confirmBtn = page.getByRole("button", { name: "Confirm & Save Timetable" });
    await expect(confirmBtn).toBeVisible({ timeout: 20000 });
    await confirmBtn.click();

    // Verify confirmation badge
    await expect(page.locator("text=CONFIRMED").first()).toBeVisible({ timeout: 10000 });

    // 6. Log in as Faculty KKS
    await loginAs(page, "kks@facultydesk.local", "Faculty123!");

    // 7. View Calendar
    await page.goto("/calendar");
    await expect(page.locator("h1")).toContainText(/Academic (Calendar|Schedule)/);

    // Check that schedule slots or events exist
    const eventCards = page.locator(".space-y-3 > div, h4");
    await expect(eventCards.first()).toBeVisible({ timeout: 15000 });
    expect(await eventCards.count()).toBeGreaterThanOrEqual(1);
  });
});
