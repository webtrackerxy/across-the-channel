import type { Footprint } from "../scenarios/model";
// Reference connections only. These are not recorded departures, landings or tracks.
export const connections: Record<Footprint, [number, number][][]> = {
  strait: [
    [
      [1.86, 50.95],
      [1.32, 51.13],
    ],
  ],
  wider: [
    // Utah Beach → Portsmouth
    [
      [-1.174703, 49.415666],
      [-1.06776, 50.822113],
    ],
    // Dieppe → Brighton
    [
      [1.08, 49.92],
      [-0.14, 50.82],
    ],
    // Calais → Dover
    [
      [1.86, 50.95],
      [1.32, 51.13],
    ],
    // Dunkirk → Dover
    [
      [2.38, 51.04],
      [1.32, 51.13],
    ],
  ],
};

export const scenarioRouteLabels: Record<Footprint, string[]> = {
  strait: ["Calais → Dover"],
  wider: [
    "Utah Beach → Portsmouth",
    "Dieppe → Brighton",
    "Calais → Dover",
    "Dunkirk → Dover",
  ],
};
export function routeFeatures(footprint: Footprint) {
  return {
    type: "FeatureCollection" as const,
    features: connections[footprint].map((coordinates) => ({
      type: "Feature" as const,
      properties: {},
      geometry: { type: "LineString" as const, coordinates },
    })),
  };
}
export function endpointFeatures(footprint: Footprint) {
  return {
    type: "FeatureCollection" as const,
    features: connections[footprint].flatMap((points) =>
      points.map((coordinates) => ({
        type: "Feature" as const,
        properties: {},
        geometry: { type: "Point" as const, coordinates },
      })),
    ),
  };
}
