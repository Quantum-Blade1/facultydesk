import { test } from "@playwright/test";
import path from "node:path";
import { loginAs } from "../../../../frontend/e2e/helpers";

const out = (name: string): string => path.resolve(__dirname, "../../figures/screens", `${name}.png`);

test("capture faculty and HOD screens", async ({ page }) => {
  await loginAs(page, "kks@facultydesk.local", "Faculty123!");
  for (const route of ["today", "calendar", "tasks", "settings"]) {
    await page.goto(`/${route}`);
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(1500);
    await page.screenshot({ path: out(`faculty-${route}`) });
  }
  await loginAs(page, "hod.cse@facultydesk.local", "Hod123!");
  for (const route of ["timetables", "circulars", "tasks", "directory"]) {
    await page.goto(`/${route}`);
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(1500);
    await page.screenshot({ path: out(`hod-${route}`) });
  }
});
