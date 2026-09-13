import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("optional story scenario updates totals and hypothetical connections", async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/#scenarios");
  const section = page.locator("#scenarios");
  await expect(section.locator("output")).toHaveText("41,540", {
    timeout: 20000,
  });
  await expect(page.locator(".editorial")).toHaveClass(/editorial-scenario/);
  await expect(
    page.getByRole("button", { name: "Listen to the story" }),
  ).toBeDisabled();
  await page
    .getByRole("slider", { name: /Assumed arriving boats/ })
    .press("End");
  await page
    .getByRole("slider", { name: /Average people per boat/ })
    .press("End");
  await expect(section.locator("output")).toHaveText("225,000");
  await expect(section.locator("svg circle")).toHaveCount(150);
  await page.getByLabel("Explore wider connections", { exact: true }).check();
  await expect(page.getByTestId("story-map")).toHaveAttribute(
    "data-route-count",
    "4",
  );
  await page
    .getByRole("slider", { name: /Assumed arriving boats/ })
    .press("Home");
  await expect(section.locator("output")).toHaveText("0");
  await expect(
    page.locator('.editorial-route-boat[data-route="scenario"]'),
  ).toHaveCount(0);
  await page.getByLabel("Explore wider connections", { exact: true }).uncheck();
  await expect(page.getByTestId("story-map")).toHaveAttribute(
    "data-route-count",
    "1",
  );
  expect(
    (
      await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
        .analyze()
    ).violations,
  ).toEqual([]);
});
