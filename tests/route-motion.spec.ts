import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("route boats follow chapters, pause, replay and respect reduced motion", async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: "no-preference" });
  await page.goto("/#fuller-picture");
  const dover = page.locator('.editorial-route-boat[data-route="dover"]');
  const west = page.locator('.editorial-route-boat[data-route="portsmouth"]');
  await expect(dover).toHaveCount(4, { timeout: 20000 });
  await expect(west).toHaveCount(0);
  await page.getByLabel("Story menu", { exact: true }).click();
  await page.getByRole("button", { name: "Pause motion", exact: true }).click();
  const position = await dover.first().getAttribute("data-progress");
  await page.waitForTimeout(200);
  await expect(dover.first()).toHaveAttribute("data-progress", position!);
  await page.getByRole("button", { name: "Play motion", exact: true }).click();
  await expect(dover.first()).not.toHaveAttribute("data-progress", position!);
  await page.getByLabel("Story menu", { exact: true }).click();
  await page.getByRole("button", { name: "Go to Farther west" }).click();
  await expect(west).toHaveCount(1);
  await expect
    .poll(async () => Number(await west.getAttribute("data-progress")))
    .toBeGreaterThan(0.02);
  await page.getByLabel("Story menu", { exact: true }).click();
  await page.getByRole("button", { name: "Pause motion", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Listen to the story" }),
  ).toBeVisible();
  const before = Number(await west.getAttribute("data-progress"));
  await page.getByRole("button", { name: "Replay Portsmouth journey" }).click();
  await expect
    .poll(async () => Number(await west.getAttribute("data-progress")))
    .toBeLessThan(before);
  await page.emulateMedia({ reducedMotion: "reduce" });
  await expect(west).toHaveAttribute("data-progress", "0.5000");
  await expect(page.getByText("Reduced motion · static boats")).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Pause motion", exact: true }),
  ).toHaveCount(0);
  await page.screenshot({
    path: `test-results/route-boats-${test.info().project.name}.png`,
  });
  const audit = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(audit.violations).toEqual([]);
  await page
    .getByRole("button", { name: "Go to The Channel", exact: true })
    .click();
  await expect(dover).toHaveCount(0);
  await expect(west).toHaveCount(0);
});
