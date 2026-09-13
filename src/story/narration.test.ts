import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { byYear, formatNumber, occupancy } from "../data/model";
import { modelArrivals, presets } from "../scenarios/model";
import { narrationFor, narrationTranscript } from "./narration";
import { playbackFrames } from "./playback";
import { scenes } from "./scenes";

describe("Narration script", () => {
  it("covers all 15 steps with distinct, speech-friendly text", () => {
    const texts = playbackFrames.map(narrationFor);
    expect(texts).toHaveLength(15);
    expect(new Set(texts).size).toBe(15);
    for (const text of texts) {
      expect(text.length).toBeGreaterThan(20);
      expect(text).not.toMatch(/\n|people\s*\/\s*boat|undefined|NaN/);
    }
  });

  it("keeps every annual figure tied to the data and its correct unit", () => {
    for (const frame of playbackFrames.filter(
      (item) => item.sceneIndex === 1,
    )) {
      const record = byYear(frame.year);
      expect(narrationFor(frame)).toContain(
        `${formatNumber(record.people)} people arrived on ${formatNumber(record.boats)} boats, averaging ${occupancy(record).toFixed(1)} people per boat`,
      );
    }
    expect(narrationFor({ sceneIndex: 1, year: 2019 })).toBe(
      "2019. 1,843 people arrived on 164 boats, averaging 11.2 people per boat.",
    );
  });

  it("reads each chapter opening once, before its step-specific figures", () => {
    for (const index of [0, 1, 10, 11]) {
      const frame = playbackFrames[index];
      expect(narrationFor(frame)).toContain(scenes[frame.sceneIndex].body);
    }
    for (const index of [2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14]) {
      const frame = playbackFrames[index];
      expect(narrationFor(frame)).not.toContain(scenes[frame.sceneIndex].body);
    }
  });

  it("qualifies the partial year without extending its reporting cutoff", () => {
    const text = narrationFor({ sceneIndex: 1, year: 2026 });
    expect(text).toContain("From 1 January to 3 September, provisional.");
    expect(text).toContain("not comparable with full years");
    expect(text).toContain("Calais to Dover");
    expect(text).toContain("Utah Beach to Portsmouth");
    expect(text).toContain(
      "6 September case falls after these totals' reporting cutoff",
    );
    expect(text).toContain("reported endpoints, not a recorded vessel track");
    expect(text).toContain("About 140 people were aboard");
    expect(text).toContain("about 24 hours after leaving");
    expect(text).toContain("The boat's size was not reported.");
    expect(narrationFor({ sceneIndex: 1, year: 2025 })).not.toContain(
      "Portsmouth",
    );
    expect(narrationFor({ sceneIndex: 1, year: 2025 })).not.toContain(
      "provisional",
    );
  });

  it("uses unrounded data for comparison and limits the interpretation", () => {
    const text = narrationFor({ sceneIndex: 2, year: 2025 });
    expect(text).toContain("arriving boats fell by 39.5 percent");
    expect(text).toContain("people arriving fell by 9.4 percent");
    expect(text).toContain("Average people per boat rose by 49.7 percent");
    expect(text).toContain(
      "does not establish vessel capacity or the routes travelled",
    );
  });

  it("labels every preset as hypothetical and explains the arithmetic", () => {
    for (const frame of playbackFrames.filter((item) => item.preset)) {
      const preset = presets[frame.preset!];
      const text = narrationFor(frame);
      expect(text).toContain("a hypothetical scenario, not a forecast");
      expect(text).toContain(preset.description);
      expect(text).toContain(`${formatNumber(preset.boats)} arriving boats`);
      expect(text).toContain(
        `${formatNumber(preset.occupancy)} people per boat`,
      );
      expect(text).toContain(
        `${formatNumber(modelArrivals(preset))} modelled arrivals`,
      );
      expect(text).toContain("not recorded vessel tracks");
    }
  });

  it("ends with what is known, then leaves the explanations open", () => {
    const text = narrationFor(playbackFrames[playbackFrames.length - 1]);
    expect(text).toContain("about 7 in 2018 and about 62 in 2025");
    expect(text).toContain("Open questions.");
    expect(text).toContain("bigger boats, fuller boats, or both?");
    expect(text).toContain("too soon to say whether it is part of a pattern");
    expect(text).not.toMatch(/does not show|not established|proves?/);
    expect(text).toContain(
      "What if boat numbers, occupancy or launch areas changed?",
    );
    expect(text).not.toMatch(/continue to increase/);
  });

  it("rejects invalid inputs instead of producing misleading narration", () => {
    expect(() => narrationFor({ sceneIndex: 99, year: 2025 })).toThrow();
    expect(() => narrationFor({ sceneIndex: 1, year: 2017 })).toThrow();
    expect(() => narrationFor({ sceneIndex: 3, year: 2025 })).toThrow();
  });

  it("keeps the review transcript synchronized with the script", () => {
    expect(readFileSync("docs/narration/narration-transcript.md", "utf8")).toBe(
      narrationTranscript(),
    );
  });
});
