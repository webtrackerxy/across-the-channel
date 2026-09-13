export type Theme = "light" | "dark";
export const textSizes = [100, 112.5, 125, 150, 175, 200] as const;
export function readPreference(key: string): string | null {
  try {
    return localStorage.getItem(`channel-${key}`);
  } catch {
    return null;
  }
}
export function savePreference(key: string, value: string) {
  try {
    localStorage.setItem(`channel-${key}`, value);
  } catch {
    /* Session controls still work when storage is unavailable. */
  }
}
/** A saved choice wins; otherwise the story opens in dark mode, whatever the system setting. */
export function initialTheme(): Theme {
  const saved = readPreference("theme");
  return saved === "light" || saved === "dark" ? saved : "dark";
}
export function initialTextIndex() {
  const index = textSizes.findIndex(
    (size) => String(size) === readPreference("text-size"),
  );
  return index < 0 ? 0 : index;
}
