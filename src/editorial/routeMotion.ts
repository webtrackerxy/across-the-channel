/** Display pacing only: neither boat frequency nor journey duration is measured. */
export const DOVER_BOATS = 4;
export const DOVER_DURATION = 18000;
export const PORTSMOUTH_DURATION = 24000;

/** User-selected visual emphasis, not measured vessel speed. */
export function doverSpeed(year: number) {
  return year >= 2025 ? 3.375 : 1;
}

export function routeProgress(elapsed: number, index: number, west: boolean) {
  return west
    ? Math.min(1, elapsed / PORTSMOUTH_DURATION)
    : (elapsed / DOVER_DURATION + index / DOVER_BOATS) % 1;
}

export function routePosition(
  points: [number, number][],
  progress: number,
): [number, number] {
  const [start, end] = points;
  return [
    start[0] + (end[0] - start[0]) * progress,
    start[1] + (end[1] - start[1]) * progress,
  ];
}
