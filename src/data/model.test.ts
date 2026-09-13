import { describe, expect, it } from "vitest";
import { byYear, changePercent, occupancy, records, sources } from "./model";
import { modelArrivals, presets } from "../scenarios/model";

describe("Evidence and arithmetic", () => {
  it("reconciles the key historical comparison without using rounded averages", () => {
    const before = byYear(2022),
      after = byYear(2025);
    expect(occupancy(before)).toBeCloseTo(41.237838, 5);
    expect(occupancy(after)).toBeCloseTo(61.714286, 5);
    expect(changePercent(before.boats, after.boats)).toBeCloseTo(-39.459459, 5);
    expect(changePercent(before.people, after.people)).toBeCloseTo(
      -9.398348,
      5,
    );
    expect(changePercent(occupancy(before), occupancy(after))).toBeCloseTo(
      49.654514,
      5,
    );
  });
  it("preserves the 2026 cutoff and provisional classification", () => {
    expect(byYear(2026)).toMatchObject({
      people: 16513,
      boats: 244,
      partial: true,
      provisional: true,
      periodEnd: "2026-09-03",
    });
    expect(occupancy(byYear(2026))).toBeCloseTo(67.67623, 4);
    expect(records.filter((record) => record.partial)).toHaveLength(1);
  });
  it("every displayed record has resolvable provenance and a bounded period", () => {
    for (const record of records) {
      expect(
        sources.find((source) => source.id === record.sourceId)?.url,
      ).toMatch(/^https:\/\//);
      expect(record.claimId).not.toBe("");
      expect(record.periodEnd > record.periodStart).toBe(true);
      expect(
        Number.isInteger(record.people) && Number.isInteger(record.boats),
      ).toBe(true);
    }
  });
  it("rejects invalid denominators and missing years", () => {
    expect(() => occupancy({ people: 100, boats: 0 })).toThrow();
    expect(() => occupancy({ people: -1, boats: 10 })).toThrow();
    expect(() => occupancy({ people: NaN, boats: 10 })).toThrow();
    expect(() => byYear(2017)).toThrow();
  });
});

describe("Hypothetical scenario engine", () => {
  it("calculates transparent preset results", () => {
    expect(modelArrivals(presets.low)).toBe(18000);
    expect(modelArrivals(presets.continuation)).toBe(41540);
    expect(modelArrivals(presets.expansion)).toBe(64000);
  });
  it("changing geography alone cannot increase the numeric result", () => {
    expect(
      modelArrivals({ boats: 672, occupancy: 62, footprint: "wider" }),
    ).toBe(modelArrivals({ boats: 672, occupancy: 62, footprint: "strait" }));
  });
  it("handles zero boats and rejects impossible or non-finite inputs", () => {
    expect(
      modelArrivals({ boats: 0, occupancy: 62, footprint: "strait" }),
    ).toBe(0);
    for (const boats of [-1, 1600, 2.5, NaN])
      expect(() =>
        modelArrivals({ boats, occupancy: 62, footprint: "strait" }),
      ).toThrow();
    expect(() =>
      modelArrivals({ boats: 600, occupancy: Infinity, footprint: "strait" }),
    ).toThrow();
  });
});
