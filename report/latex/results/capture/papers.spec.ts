import { test } from "@playwright/test";
import path from "node:path";

const pages: [string, string][] = [
  ["paper-ijet-59329", "https://online-journals.org/index.php/i-jet/article/view/59329"],
  ["paper-arxiv-2607.03901", "https://arxiv.org/abs/2607.03901"],
  ["paper-arxiv-2603.02789", "https://arxiv.org/abs/2603.02789"],
  ["paper-arxiv-2604.26462", "https://arxiv.org/abs/2604.26462"],
  ["paper-arxiv-2605.18818", "https://arxiv.org/abs/2605.18818"],
];

for (const [name, url] of pages) {
  test(`capture ${name}`, async ({ page }) => {
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: path.resolve(__dirname, "../../figures/papers", `${name}.png`) });
  });
}
