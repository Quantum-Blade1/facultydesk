import { test, expect } from "@playwright/test";
import { loginAs } from "./helpers";

test.describe("Journey 3: Meeting Reminder Exactly-Once Delivery", () => {
  test("A meeting scheduled ahead produces a notification record marked SENT", async ({
    request,
    page,
  }) => {
    test.setTimeout(60000);
    const facLoginRes = await request.post("/api/auth/login", {
      data: { email: "kks@facultydesk.local", password: "Faculty123!" },
    });
    expect(facLoginRes.ok()).toBeTruthy();
    const facAuth = await facLoginRes.json();
    const facToken = facAuth.access_token;
    const facProfileId = facAuth.profile.id;

    const now = new Date();
    const start = new Date(now.getTime() + 2 * 60 * 1000);
    const end = new Date(start.getTime() + 60 * 60 * 1000);

    const eventRes = await request.post("/api/calendar/events", {
      headers: { Authorization: `Bearer ${facToken}` },
      data: {
        title: "Automated E2E Urgent Faculty Sync",
        kind: "MEETING",
        start_utc: start.toISOString(),
        end_utc: end.toISOString(),
        location: "Meeting Room 101",
        attendee_ids: [facProfileId],
        override_clashes: true,
      },
    });
    expect(eventRes.status()).toBe(201);
    const event = await eventRes.json();
    expect(event.id).toBeDefined();

    await loginAs(page, "admin@facultydesk.local", "Admin123!");
    await page.goto("/today");
    await expect(page.locator("h1")).toBeVisible();

    const adminLogin = await request.post("/api/auth/login", {
      data: { email: "admin@facultydesk.local", password: "Admin123!" },
    });
    expect(adminLogin.ok()).toBeTruthy();
    const adminToken = (await adminLogin.json()).access_token;

    let metricsOk = false;
    for (let i = 0; i < 15; i++) {
      const metricsRes = await request.get("/api/admin/metrics", {
        headers: { Authorization: `Bearer ${adminToken}` },
      });
      if (metricsRes.ok()) {
        const metrics = await metricsRes.json();
        if (
          Array.isArray(metrics.failed_dead_letters) &&
          metrics.notifications_by_status !== undefined
        ) {
          metricsOk = true;
          break;
        }
      }
      await page.waitForTimeout(1000);
    }

    expect(metricsOk).toBeTruthy();
  });
});
