import type { PresetId } from "../scenarios/model";
export interface PlaybackFrame {
  sceneIndex: number;
  year: number;
  preset?: PresetId;
  /** The final step: the evidence summary and closing question. */
  closing?: true;
}
export const playbackFrames: PlaybackFrame[] = [
  { sceneIndex: 0, year: 2025 },
  ...Array.from({ length: 9 }, (_, index) => ({
    sceneIndex: 1,
    year: 2018 + index,
  })),
  { sceneIndex: 2, year: 2025 },
  { sceneIndex: 3, year: 2025, preset: "low" },
  { sceneIndex: 3, year: 2025, preset: "continuation" },
  { sceneIndex: 3, year: 2025, preset: "expansion" },
  { sceneIndex: 3, year: 2025, closing: true },
];
