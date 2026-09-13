import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("fast manual scrolling settles on one chapter transition", async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: "no-preference" });
  await page.goto("/#channel");
  await page
    .getByRole("heading", { name: "What does counting boats miss?" })
    .waitFor();

  await page.evaluate(() => {
    const state = window as Window & { activeChapterChanges?: number };
    state.activeChapterChanges = 0;
    new MutationObserver((changes) => {
      state.activeChapterChanges! += changes.length;
    }).observe(document.querySelector(".editorial-story")!, {
      attributes: true,
      attributeFilter: ["data-active"],
      subtree: true,
    });
  });

  // Jump through the chapters inside the page, one frame apart. Driving each
  // jump from the test adds a round trip that can exceed the page's 120 ms
  // settle delay when the machine is busy, which is not fast scrolling.
  await page.evaluate(async () => {
    for (const id of [
      "small-boat",
      "fuller-picture",
      "comparison",
      "farther-west",
    ]) {
      document.body.dispatchEvent(new WheelEvent("wheel", { bubbles: true }));
      document
        .getElementById(id)!
        .scrollIntoView({ behavior: "instant", block: "start" });
      await new Promise(requestAnimationFrame);
    }
  });

  await expect(page.locator(".editorial-timeline")).toContainText("2026");
  await expect(page.locator("#farther-west")).toHaveAttribute(
    "data-active",
    "true",
  );
  expect(
    await page.evaluate(
      () =>
        (window as Window & { activeChapterChanges?: number })
          .activeChapterChanges,
    ),
  ).toBeLessThanOrEqual(2);
});

test("Portsmouth evidence clears the fixed timeline on laptop screens", async ({
  page,
}, info) => {
  test.skip(info.project.name !== "desktop", "Desktop viewport layout");
  await page.emulateMedia({ reducedMotion: "reduce" });
  for (const viewport of [
    { width: 1806, height: 870 },
    { width: 1366, height: 768 },
  ]) {
    await page.setViewportSize(viewport);
    await page.goto("/#farther-west");
    const sources = page.getByRole("button", {
      name: "Sources and reporting dates",
    });
    await expect(sources).toBeVisible({ timeout: 20000 });
    await sources.evaluate((node) =>
      node.scrollIntoView({ behavior: "instant", block: "center" }),
    );
    await expect
      .poll(async () => {
        const footer = await page.locator(".editorial-timeline").boundingBox();
        const link = await sources.boundingBox();
        return !!footer && !!link && link.y + link.height < footer.y;
      })
      .toBe(true);
    await page.screenshot({
      path: `test-results/editorial-portsmouth-${viewport.width}.png`,
    });
  }
});

test("map-led story follows navigation and opens the interactive map", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "What does counting boats miss?" }),
  ).toBeVisible({ timeout: 20000 });
  await expect(page.getByTestId("story-map")).toHaveAttribute(
    "data-ready",
    "true",
    { timeout: 20000 },
  );
  await page.screenshot({
    path: `test-results/editorial-opening-${test.info().project.name}.png`,
  });
  await page
    .getByRole("button", { name: "Go to More people per boat" })
    .click();
  await expect(page.getByTestId("story-map")).toHaveAttribute(
    "data-section",
    "2",
  );
  await expect(page.locator("#fuller-picture")).toBeInViewport();
  await expect
    .poll(() =>
      page
        .locator("#fuller-picture")
        .evaluate((node) => Math.abs(node.getBoundingClientRect().top)),
    )
    .toBeLessThan(2);
  await expect(page.locator("#fuller-picture svg circle")).toHaveCount(69);
  await page.screenshot({
    path: `test-results/editorial-occupancy-${test.info().project.name}.png`,
  });
  await page.getByRole("button", { name: "Go to Farther west" }).click();
  await expect(page.getByTestId("story-map")).toHaveAttribute(
    "data-section",
    "4",
  );
  await expect(page.locator("#farther-west")).toContainText("16,513");
  await expect(page.locator("#farther-west")).toContainText(
    "outside these totals",
  );
  await page
    .getByRole("button", { name: "Explore this map interactively" })
    .click();
  await expect(page.getByLabel("Map year", { exact: true })).toHaveValue(
    "2026",
  );
  await expect(page.getByTestId("interactive-map")).toHaveAttribute(
    "data-ready",
    "true",
    { timeout: 20000 },
  );
  await page
    .getByRole("button", { name: "Close Interactive map", exact: true })
    .click();
  await expect(page.getByTestId("story-map")).toBeAttached();
});

test("story is readable with reduced motion, both themes and map failure", async ({
  page,
}) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.route("**/data/land.geojson", (route) => route.abort());
  await page.goto("/#comparison");
  await expect(page.locator(".editorial")).toHaveClass(/editorial-reduced/);
  await expect(page.locator("#comparison")).toBeInViewport();
  await expect(page.locator("#comparison")).toContainText("+49.7%");
  for (const theme of ["dark", "light"]) {
    if (theme === "light") {
      await page.getByLabel("Story menu").click();
      await page.getByRole("button", { name: "Light appearance" }).click();
      await page.getByLabel("Story menu").click();
    }
    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
      .analyze();
    expect(results.violations).toEqual([]);
  }
  await page.getByLabel("Story menu").click();
  await page.getByLabel("Story text size").selectOption("5");
  await page.getByLabel("Story menu").click();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth + 1,
    ),
  ).toBe(true);
});

test("manual story navigation pauses listening and keeps transcripts available", async ({
  page,
}) => {
  await page.goto("/");
  const listen = page.getByRole("button", { name: "Listen to the story" });
  await expect(listen).toBeEnabled();
  await listen.click();
  await expect(
    page.getByRole("button", { name: "Pause narration" }),
  ).toBeVisible();
  if (test.info().project.name !== "mobile") {
    await page.getByRole("button", { name: "Transcript", exact: true }).click();
    await expect(page.locator(".editorial-audio-note p")).toContainText(
      "boat count",
    );
  }
  await page.getByRole("button", { name: "Go to Farther west" }).click();
  await expect(listen).toBeVisible();
  if (test.info().project.name !== "mobile")
    await expect(page.locator(".editorial-audio-note p")).toContainText(
      "Portsmouth",
    );
  await expect(page.getByTestId("story-map")).toHaveAttribute(
    "data-section",
    "4",
  );
});
