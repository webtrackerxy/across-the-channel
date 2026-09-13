import { describe, expect, it } from "vitest";
import { boatGeometry, storySections } from "./sections";
import { playbackFrames } from "../story/playback";
import { byYear, occupancy } from "../data/model";

describe("Map-led story", () => {
  it("illustrates rounded occupancy with exactly one mark per person", () => {
    for (const year of [2018, 2025, 2026]) {
      const people = Math.round(occupancy(byYear(year)));
      const boat = boatGeometry(people);
      expect(boat.dots).toHaveLength(people);
      expect(new Set(boat.dots.map((dot) => `${dot.x},${dot.y}`)).size).toBe(
        people,
      );
      expect(
        boat.dots.every(
          (dot) =>
            dot.x > 4 &&
            dot.x < boat.width - 4 &&
            dot.y > 4 &&
            dot.y < boat.height - 4,
        ),
      ).toBe(true);
    }
    const small = boatGeometry(7),
      large = boatGeometry(62);
    expect(large.width).toBeGreaterThan(small.width);
    expect(large.height).toBeGreaterThan(small.height);
  });
  it("maps sections to existing recordings and reporting years", () => {
    expect(new Set(storySections.map((section) => section.id)).size).toBe(
      storySections.length,
    );
    for (const section of storySections) {
      expect(playbackFrames[section.audioFrame]).toBeDefined();
      expect(byYear(section.year)).toBeDefined();
    }
    expect(playbackFrames[storySections[4].audioFrame].year).toBe(2026);
    expect(playbackFrames[storySections[5].audioFrame].closing).toBe(true);
  });
});
