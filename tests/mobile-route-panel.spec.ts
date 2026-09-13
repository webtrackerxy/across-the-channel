import { test, expect } from "@playwright/test";

test("mobile route details use the page scroll", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 794 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/#farther-west");
  const panel = page.locator("#farther-west .editorial-copy");
  await expect(panel).toBeVisible({ timeout: 20000 });
  expect(
    await panel.evaluate((node) => getComputedStyle(node).overflowY),
  ).not.toBe("auto");
  const sources = page.getByRole("button", {
    name: "Sources and reporting dates",
  });
  await sources.evaluate((node) =>
    node.scrollIntoView({ behavior: "instant", block: "center" }),
  );
  await expect(sources).toBeInViewport();
  await page.screenshot({ path: "test-results/mobile-route-details.png" });
});
