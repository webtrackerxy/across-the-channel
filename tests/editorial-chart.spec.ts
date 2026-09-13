import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("timeline opens an accessible chart popup with selectable metrics and years", async ({
  page,
}) => {
  await page.goto("/");
  const opener = page.getByRole("button", { name: "Open year-by-year chart" });
  await expect(opener).toBeVisible({ timeout: 20000 });
  await opener.click();
  const dialog = page.getByRole("dialog", {
    name: "Year-by-year chart",
    exact: true,
  });
  await expect(dialog).toBeVisible();
  await dialog.getByRole("button", { name: "People", exact: true }).click();
  await dialog.getByRole("button", { name: /^2025:/ }).click();
  await expect(dialog.locator(".editorial-chart-summary")).toContainText(
    "41,472 people",
  );
  await dialog.getByRole("button", { name: "Boats", exact: true }).click();
  await expect(dialog.getByRole("button", { name: /^2025:/ })).toHaveAttribute(
    "aria-label",
    /672/,
  );
  expect(
    (
      await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
        .analyze()
    ).violations,
  ).toEqual([]);
  await page.screenshot({
    path: `test-results/editorial-chart-${test.info().project.name}.png`,
  });
  await dialog
    .getByRole("button", { name: "Close Year-by-year chart" })
    .click();
  await expect(dialog).not.toBeVisible();
  await expect(opener).toBeFocused();
});
