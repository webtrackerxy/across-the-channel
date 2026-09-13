import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { NarrationPlayer } from "./narrationPlayer";
import type { AudioClip } from "./audioCache";

function setup(enabled = true) {
  const audio = {
    src: "",
    currentTime: 0,
    play: vi.fn(() => Promise.resolve()),
    pause: vi.fn(),
    load: vi.fn(),
    removeAttribute: vi.fn(),
    onended: null as null | (() => void),
    onerror: null as null | (() => void),
    ontimeupdate: null as null | (() => void),
  };
  const onFrame = vi.fn(),
    onStop = vi.fn(),
    onFailure = vi.fn();
  const player = new NarrationPlayer(
    audio as unknown as HTMLAudioElement,
    (clip) => clip.file,
    2,
    onFrame,
    onStop,
    onFailure,
  );
  player.setClips(
    [0, 1].map(
      (frame) => ({ frame, file: `${frame}.mp3`, duration: 12 }) as AudioClip,
    ),
  );
  player.setPace(4000);
  player.setEnabled(enabled);
  return { player, audio, onFrame, onStop, onFailure };
}
beforeEach(() => {
  vi.useFakeTimers();
});
afterEach(() => {
  vi.useRealTimers();
});

describe("Narrated story transport", () => {
  it("waits for both dwell and speech, then stops on the final step", () => {
    const { player, audio, onFrame, onStop } = setup();
    player.start(0);
    vi.advanceTimersByTime(4100);
    expect(onFrame).not.toHaveBeenCalled();
    audio.onended!();
    vi.advanceTimersByTime(1);
    expect(onFrame).toHaveBeenCalledWith(1);
    audio.onended!();
    vi.advanceTimersByTime(3998);
    expect(onStop).not.toHaveBeenCalled();
    vi.advanceTimersByTime(2);
    expect(onStop).toHaveBeenCalledOnce();
  });
  it("preserves remaining dwell and audio position across long pauses", () => {
    const { player, audio, onFrame } = setup();
    player.start(0);
    vi.advanceTimersByTime(2000);
    audio.currentTime = 2;
    player.pause();
    vi.advanceTimersByTime(60000);
    player.start(0);
    expect(audio.currentTime).toBe(2);
    expect(audio.load).toHaveBeenCalledOnce();
    audio.onended!();
    vi.advanceTimersByTime(1999);
    expect(onFrame).not.toHaveBeenCalled();
    vi.advanceTimersByTime(2);
    expect(onFrame).toHaveBeenCalledWith(1);
  });
  it("ignores late rejections after pause or manual navigation", async () => {
    const { player, audio, onFailure } = setup();
    let reject!: (error: Error) => void;
    audio.play.mockImplementationOnce(
      () =>
        new Promise((_, fail) => {
          reject = fail;
        }),
    );
    player.start(0);
    player.cancel();
    player.start(1);
    reject(new Error("old play interrupted"));
    await Promise.resolve();
    expect(onFailure).not.toHaveBeenCalled();
    expect(audio.src).toBe("1.mp3");
  });
  it("disabling narration releases the current gate; enabling waits for next step", () => {
    const { player, audio, onFrame } = setup();
    player.start(0);
    vi.advanceTimersByTime(4500);
    player.setEnabled(false);
    player.setEnabled(true);
    expect(audio.play).toHaveBeenCalledOnce();
    vi.advanceTimersByTime(1);
    expect(onFrame).toHaveBeenCalledWith(1);
    expect(audio.play).toHaveBeenCalledTimes(2);
  });
  it("recovers from missing/failed audio and stalled loading", async () => {
    const { player, audio, onFailure, onFrame } = setup();
    audio.play.mockRejectedValueOnce(new Error("blocked"));
    player.start(0);
    await Promise.resolve();
    vi.advanceTimersByTime(4000);
    expect(onFailure).toHaveBeenCalledOnce();
    expect(onFrame).toHaveBeenCalledWith(1);
    vi.advanceTimersByTime(15001);
    expect(onFailure).toHaveBeenCalledTimes(2);
  });
  it("uses duration plus grace if ended never arrives despite time updates", () => {
    const { player, audio, onFailure } = setup();
    player.start(0);
    for (let i = 0; i < 6; i++) {
      vi.advanceTimersByTime(5000);
      audio.ontimeupdate!();
    }
    expect(onFailure).not.toHaveBeenCalled();
    vi.advanceTimersByTime(2001);
    expect(onFailure).toHaveBeenCalledOnce();
  });
  it("silent playback completes and pace changes retain elapsed time", () => {
    const { player, audio, onFrame, onStop } = setup(false);
    player.start(0);
    vi.advanceTimersByTime(2000);
    player.setPace(8000);
    vi.advanceTimersByTime(6000);
    expect(onFrame).toHaveBeenCalledWith(1);
    vi.advanceTimersByTime(8000);
    expect(onStop).toHaveBeenCalledOnce();
    expect(audio.play).not.toHaveBeenCalled();
  });
});
