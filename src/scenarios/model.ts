export type Footprint = "strait" | "wider";
export type PresetId = "low" | "continuation" | "expansion";
export interface Scenario {
  boats: number;
  occupancy: number;
  footprint: Footprint;
}
export const presets: Record<
  PresetId,
  Scenario & { label: string; description: string }
> = {
  low: {
    label: "Low",
    boats: 400,
    occupancy: 45,
    footprint: "strait",
    description: "Fewer arriving boats, lower occupancy.",
  },
  continuation: {
    label: "Continuation",
    boats: 670,
    occupancy: 62,
    footprint: "strait",
    description: "Rounded assumptions near the 2025 totals.",
  },
  expansion: {
    label: "Expansion",
    boats: 800,
    occupancy: 80,
    footprint: "wider",
    description:
      "More arriving boats, higher occupancy, wider illustrative geography.",
  },
};
export function modelArrivals(scenario: Scenario): number {
  if (
    !Number.isInteger(scenario.boats) ||
    scenario.boats < 0 ||
    scenario.boats > 1500 ||
    !Number.isFinite(scenario.occupancy) ||
    scenario.occupancy < 1 ||
    scenario.occupancy > 150
  ) {
    throw new Error("Scenario assumptions are outside the supported range.");
  }
  return scenario.boats * scenario.occupancy;
}
