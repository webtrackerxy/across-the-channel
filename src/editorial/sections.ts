export const storySections = [
  { id: "channel", label: "The Channel", year: 2018, audioFrame: 0 },
  { id: "small-boat", label: "A different scale", year: 2018, audioFrame: 1 },
  {
    id: "fuller-picture",
    label: "More people per boat",
    year: 2025,
    audioFrame: 8,
  },
  { id: "comparison", label: "Beyond boat counts", year: 2025, audioFrame: 10 },
  { id: "farther-west", label: "Farther west", year: 2026, audioFrame: 9 },
  {
    id: "perspective",
    label: "The bigger question",
    year: 2026,
    audioFrame: 14,
  },
  { id: "scenarios", label: "What happens next?", year: 2026, audioFrame: 11 },
] as const;

/** Compact, equally spaced occupants; the hull is an illustration, not a measurement. */
export function boatGeometry(people: number) {
  const count = Math.max(1, Math.round(people));
  const rows = Math.max(2, Math.round(Math.sqrt(count / 2.4)));
  const columns = Math.ceil(count / rows);
  const height = rows * 13 + 18;
  const width = columns * 13 + 44;
  const dots = Array.from({ length: count }, (_, index) => ({
    x: 32 + (index % columns) * 13,
    y: (height - (rows - 1) * 13) / 2 + Math.floor(index / columns) * 13,
  }));
  return { width, height, dots };
}
