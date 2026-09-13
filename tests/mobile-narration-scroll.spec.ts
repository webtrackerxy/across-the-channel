import { test, expect } from "@playwright/test";

test("manual scrolling keeps narration playing and changes the narrated chapter", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 794 });
  await page.emulateMedia({ reducedMotion: "no-preference" });
  await page.addInitScript(() => {
    HTMLMediaElement.prototype.play = function () {
      const state = window as unknown as { playCalls?: number };
      state.playCalls = (state.playCalls ?? 0) + 1;
      Object.defineProperty(this, "paused", {
        configurable: true,
        get: () => false,
      });
      Object.defineProperty(this, "duration", {
        configurable: true,
        get: () => 60,
      });
      (window as unknown as { testAudio: HTMLMediaElement }).testAudio = this;
      return Promise.resolve();
    };
  });
  await page.goto("/");
  const listen = page.getByRole("button", { name: "Listen to the story" });
  await expect(listen).toBeEnabled({ timeout: 20000 });
  await listen.click();
  // The page must track the audio clock even between sparse timeupdate events.
  await page.evaluate(() => {
    const audio = (window as unknown as { testAudio: HTMLMediaElement })
      .testAudio;
    const started = performance.now();
    Object.defineProperty(audio, "currentTime", {
      configurable: true,
      get: () => 15 + (performance.now() - started) / 1000,
    });
  });
  await expect.poll(() => page.evaluate(() => scrollY)).toBeGreaterThan(5);
  await page.evaluate(() => {
    const audio = (window as unknown as { testAudio: HTMLMediaElement })
      .testAudio;
    Object.defineProperty(audio, "currentTime", {
      configurable: true,
      get: () => 54,
    });
    audio.dispatchEvent(new Event("timeupdate"));
  });
  await expect.poll(() => page.evaluate(() => scrollY)).toBeGreaterThan(30);
  const cta = page.getByRole("button", { name: "Scroll to discover" });
  await expect
    .poll(async () => {
      const box = await cta.boundingBox();
      const footer = await page.locator(".editorial-timeline").boundingBox();
      return !!box && !!footer && box.y + box.height < footer.y;
    })
    .toBe(true);
  await page.evaluate(() => window.dispatchEvent(new WheelEvent("wheel")));
  await expect(
    page.getByRole("button", { name: "Pause narration" }),
  ).toBeVisible();
  await page.locator("#small-boat").evaluate((section) =>
    section.scrollIntoView({
      behavior: "instant",
      block: "start",
    }),
  );
  await expect(page.locator("#small-boat")).toHaveAttribute(
    "data-active",
    "true",
  );
  await expect
    .poll(() =>
      page.evaluate(
        () => (window as unknown as { playCalls?: number }).playCalls ?? 0,
      ),
    )
    .toBeGreaterThanOrEqual(2);
  await expect(
    page.getByRole("button", { name: "Pause narration" }),
  ).toBeVisible();
  await page.screenshot({ path: "test-results/mobile-narration-scroll.png" });
});
