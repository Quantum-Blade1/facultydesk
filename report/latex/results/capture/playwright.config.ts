import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: ".",
  workers: 1,
  timeout: 90000,
  reporter: [["list"]],
  use: { baseURL: "http://localhost:3000", headless: true, viewport: { width: 1366, height: 860 } },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"], viewport: { width: 1366, height: 860 } } }],
});
