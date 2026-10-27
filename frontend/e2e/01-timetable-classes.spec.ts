import { test, expect } from "@playwright/test";
import path from "node:path";
import { loginAs } from "./helpers";

test.describe("Journey 1: Timetable Ingestion & Class Generation", () => {
  test("HOD uploads standard timetable, confirms, and faculty calendar displays classes", async ({
    page,
  }) => {
    test.setTimeout(60000);

    await loginAs(page, "hod.cse@facultydesk.local", "Hod123!");

    await page.goto("/timetables");
    await expect(page.locator("h1")).toContainText("Upload Department Timetable");
    await expect(page.locator("select option").first()).toBeAttached({ timeout: 15000 });

    const filePath = path.resolve(__dirname, "../../samples/timetables/standard_timetable.xlsx");
    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(filePath);

    const parseBtn = page.getByRole("button", { name: "Parse Timetable" });
    await expect(parseBtn).toBeEnabled({ timeout: 30000 });
    await parseBtn.click();

    const confirmBtn = page.getByRole("button", { name: "Confirm & Save Timetable" });
    await expect(confirmBtn).toBeVisible({ timeout: 20000 });
    await confirmBtn.click();

    await expect(page.locator("text=CONFIRMED").first()).toBeVisible({ timeout: 10000 });

    await loginAs(page, "kks@facultydesk.local", "Faculty123!");

    await page.goto("/calendar");
    await expect(page.locator("h1")).toContainText(/Academic (Calendar|Schedule)/);

    const eventCards = page.locator(".space-y-3 > div, h4");
    await expect(eventCards.first()).toBeVisible({ timeout: 15000 });
    expect(await eventCards.count()).toBeGreaterThanOrEqual(1);
  });
});
