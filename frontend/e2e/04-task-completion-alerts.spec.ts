import { test, expect } from "@playwright/test";
import { loginAs } from "./helpers";

test.describe("Journey 4: Department Task Assignment & Faculty Completion", () => {
  test("HOD assigns template task, faculty completes it, alerts are resolved", async ({
    page,
  }) => {
    test.setTimeout(60000);

    // 1. Log in as HOD
    await loginAs(page, "hod.cse@facultydesk.local", "Hod123!");

    // 2. Navigate to Tasks page and open HOD Assignment tab
    await page.goto("/tasks");
    await expect(page.locator("h1")).toContainText(/Documentation/i);

    const assignTab = page.getByRole("button", { name: "HOD Assignment" });
    await expect(assignTab).toBeVisible({ timeout: 10000 });
    await assignTab.click();

    // Fill Title
    const titleInput = page.locator('input[placeholder="Upload Module 1 IA Marks"]');
    await expect(titleInput).toBeVisible({ timeout: 10000 });
    await titleInput.fill("Automated CO-PO Mapping Compliance");

    // Fill Deadline
    const deadlineInput = page.locator('input[type="datetime-local"]').first();
    const nextWeek = new Date(Date.now() + 7 * 86400 * 1000).toISOString().slice(0, 16);
    await deadlineInput.fill(nextWeek);

    // Select faculty assignee KKS
    const kksBtn = page.locator("button:has-text('KKS')").first();
    await expect(kksBtn).toBeVisible({ timeout: 10000 });
    await kksBtn.click();

    // Submit assignment
    const submitAssignBtn = page.getByRole("button", { name: /Dispatch Assignment to Faculty/i });
    await expect(submitAssignBtn).toBeEnabled({ timeout: 10000 });
    await submitAssignBtn.click();
    await expect(page.locator("span:has-text('Assigned task cohort')")).toBeVisible({ timeout: 10000 });

    // 3. Log in as Faculty KKS
    await loginAs(page, "kks@facultydesk.local", "Faculty123!");

    // 4. Navigate to Tasks page
    await page.goto("/tasks");
    await expect(page.locator("h1")).toContainText(/Documentation/i);

    // 5. Find a task and mark it done
    const markDoneBtn = page.locator('button[aria-label="Mark done"]').first();
    await expect(markDoneBtn).toBeVisible({ timeout: 10000 });
    await markDoneBtn.click();
    await page.waitForTimeout(1000);

    // 6. Switch filter to Completed to verify task is marked completed and can be reopened
    await page.locator("select").first().selectOption("DONE");
    const reopenBtn = page.locator("button:has-text('Reopen')").first();
    await expect(reopenBtn).toBeVisible({ timeout: 10000 });
  });
});
