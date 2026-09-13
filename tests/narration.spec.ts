import { test, expect } from "@playwright/test";
test("recordings load and real audio plays only on request", async ({
  page,
}) => {
  await page.goto("/audio/narration/review.html");
  await expect(page.getByRole("status")).toContainText("15 recordings");
  await expect(page.locator("audio")).toHaveCount(15);
  expect(
    await page
      .locator("audio")
      .evaluateAll((elements) =>
        elements.every((element) => (element as HTMLAudioElement).paused),
      ),
  ).toBe(true);
  const durations = await page.locator("audio").evaluateAll(async (elements) =>
    Promise.all(
      elements.map(
        (element) =>
          new Promise<number>((resolve, reject) => {
            const audio = element as HTMLAudioElement;
            audio.addEventListener(
              "loadedmetadata",
              () => resolve(audio.duration),
              { once: true },
            );
            audio.addEventListener(
              "error",
              () => reject(new Error("Audio decode failed")),
              { once: true },
            );
            audio.preload = "metadata";
            audio.load();
          }),
      ),
    ),
  );
  expect(
    durations.every((duration) => Number.isFinite(duration) && duration > 0),
  ).toBe(true);
  // A real user gesture and browser decoder, not a stub of HTMLMediaElement.play.
  await page.evaluate(() => {
    const button = document.createElement("button");
    button.textContent = "Test play recording";
    button.onclick = () => void document.querySelector("audio")!.play();
    document.body.append(button);
  });
  await page.getByRole("button", { name: "Test play recording" }).click();
  await expect
    .poll(() =>
      page
        .locator("audio")
        .first()
        .evaluate((element) => (element as HTMLAudioElement).currentTime),
    )
    .toBeGreaterThan(0.1);
  await page
    .locator("audio")
    .first()
    .evaluate((element) => (element as HTMLAudioElement).pause());
  expect(
    await page
      .locator("audio")
      .first()
      .evaluate((element) => (element as HTMLAudioElement).paused),
  ).toBe(true);
});
