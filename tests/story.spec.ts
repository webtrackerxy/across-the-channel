import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFile } from "node:fs/promises";

test("old explorer URLs retain their year in the new interactive map", async ({
  page,
}) => {
  await page.goto("/?view=explore&year=2026");
  await expect(
    page.getByRole("dialog", { name: "Interactive map", exact: true }),
  ).toBeVisible();
  await expect(page).not.toHaveURL(/view=explore/);
  await expect(page.getByLabel("Map year", { exact: true })).toHaveValue(
    "2026",
  );
  const map = page.getByTestId("interactive-map");
  await expect(map).toHaveAttribute("data-ready", "true", { timeout: 20000 });
  await expect(map).toHaveAttribute("data-route-count", "2");
  await page.getByLabel("Map year", { exact: true }).selectOption("2020");
  await expect(map).toHaveAttribute("data-route-count", "1");
  await expect(page.locator(".editorial-map-dialog")).toContainText(
    "8,466 people",
  );
  await page.getByRole("button", { name: "Pan west", exact: true }).click();
  await page.getByRole("button", { name: "Reset map", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Zoom in", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Close Interactive map", exact: true })
    .click();
  await expect(page.getByTestId("story-map")).toBeVisible();
});

test("data table, CSV, sources and design foundations are available in the story", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByLabel("Story menu", { exact: true }).click();
  await expect(
    page.getByRole("link", { name: /Narration recording review/ }),
  ).toHaveAttribute("href", "/audio/narration/review.html");
  await expect(
    page.getByRole("link", { name: /Narration recording review/ }),
  ).toHaveAttribute("target", "_blank");
  await page
    .getByRole("button", { name: "Full data table & CSV", exact: true })
    .click();
  const dialog = page.getByRole("dialog", {
    name: "Crossings data",
    exact: true,
  });
  await expect(dialog.getByRole("row")).toHaveCount(10);
  const download = page.waitForEvent("download");
  await dialog
    .getByRole("button", { name: "Download CSV", exact: true })
    .click();
  const file = await download;
  expect(file.suggestedFilename()).toBe("channel-crossings-2018-2026.csv");
  expect(await readFile((await file.path())!, "utf8")).toContain(
    "2025,2025-01-01,2025-12-31,41472,672",
  );
  await dialog
    .getByRole("button", { name: "View 2025 source", exact: true })
    .click();
  await expect(page.locator(".evidence-calculation")).toContainText(
    "41,472 ÷ 672",
  );
  await page.keyboard.press("Escape");
  await expect(
    dialog.getByRole("button", { name: "View 2025 source", exact: true }),
  ).toBeFocused();
  await page.keyboard.press("Escape");
  await page
    .getByRole("button", { name: "Design foundations", exact: true })
    .click();
  await expect(
    page.getByRole("dialog", { name: "Design foundations", exact: true }),
  ).toBeVisible();
});

test("interactive map failure preserves figures and both themes remain accessible", async ({
  page,
}) => {
  await page.route("**/data/land.geojson", (route) => route.abort());
  await page.goto("/?view=explore&year=2025");
  await expect(page.locator(".editorial-map-dialog")).toContainText(
    "41,472 people",
  );
  for (const theme of ["dark", "light"]) {
    await page.evaluate((theme) => {
      document.documentElement.dataset.theme = theme;
    }, theme);
    expect(
      (
        await new AxeBuilder({ page })
          .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
          .analyze()
      ).violations,
    ).toEqual([]);
  }
});
