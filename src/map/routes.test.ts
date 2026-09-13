import { describe, expect, it } from "vitest";
import { connections, scenarioRouteLabels } from "./routes";

describe("scenario routes", () => {
  it("uses the four named endpoint pairs for the expansion view", () => {
    expect(scenarioRouteLabels.wider).toEqual([
      "Utah Beach → Portsmouth",
      "Dieppe → Brighton",
      "Calais → Dover",
      "Dunkirk → Dover",
    ]);
    expect(connections.wider).toEqual([
      [
        [-1.174703, 49.415666],
        [-1.06776, 50.822113],
      ],
      [
        [1.08, 49.92],
        [-0.14, 50.82],
      ],
      [
        [1.86, 50.95],
        [1.32, 51.13],
      ],
      [
        [2.38, 51.04],
        [1.32, 51.13],
      ],
    ]);
  });
});
