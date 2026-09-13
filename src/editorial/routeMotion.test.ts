import { describe, expect, it } from "vitest";
import { connections } from "../map/routes";
import { portsmouthCase } from "../map/portsmouth";
import {
  DOVER_DURATION,
  doverSpeed,
  PORTSMOUTH_DURATION,
  routePosition,
  routeProgress,
} from "./routeMotion";

describe("illustrative route movement", () => {
  it("applies three successive 50% display speed increases from 2025 onward", () => {
    expect(doverSpeed(2025)).toBe(1.5 ** 3);
    expect(doverSpeed(2018)).toBe(1);
    expect(doverSpeed(2024)).toBe(1);
    expect(doverSpeed(2026)).toBe(3.375);
    expect(
      routeProgress((DOVER_DURATION / 2 / 3.375) * doverSpeed(2025), 0, false),
    ).toBeCloseTo(0.5);
  });
  it("moves from the French endpoint to the English endpoint", () => {
    for (const points of [connections.strait[0], portsmouthCase.coordinates]) {
      expect(routePosition(points, 0)).toEqual(points[0]);
      expect(routePosition(points, 1)).toEqual(points[1]);
      expect(routePosition(points, 0.5)[1]).toBeGreaterThan(points[0][1]);
    }
  });
  it("staggers Dover boats and loops only the illustrative Dover flow", () => {
    expect(routeProgress(0, 1, false)).toBe(0.25);
    expect(routeProgress(DOVER_DURATION, 1, false)).toBe(0.25);
    expect(routeProgress(PORTSMOUTH_DURATION / 2, 0, true)).toBe(0.5);
    expect(routeProgress(PORTSMOUTH_DURATION * 3, 0, true)).toBe(1);
  });
});
