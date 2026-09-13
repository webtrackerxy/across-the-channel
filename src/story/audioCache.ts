import { narrationFor } from "./narration";
import { playbackFrames } from "./playback";

export interface AudioClip {
  frame: number;
  text: string;
  key: string;
  audioHash: string;
  file: string;
  duration: number;
}
export interface AudioManifest {
  version: 1;
  clips: AudioClip[];
}
const base = `${import.meta.env.BASE_URL}audio/narration/`;
const manifestUrl = `${base}manifest.json`;
const cacheName = "channel-narration-v1";
export const clipUrl = (clip: AudioClip) => `${base}${clip.file}`;

export function validManifest(value: unknown): value is AudioManifest {
  const manifest = value as AudioManifest | null;
  return (
    manifest?.version === 1 &&
    Array.isArray(manifest.clips) &&
    manifest.clips.length === playbackFrames.length &&
    manifest.clips.every(
      (clip, index) =>
        clip &&
        clip.frame === index &&
        clip.text === narrationFor(playbackFrames[index]) &&
        /^[a-f0-9]{64}$/.test(clip.audioHash) &&
        clip.file === `${clip.audioHash}.mp3` &&
        Number.isFinite(clip.duration) &&
        clip.duration > 0 &&
        clip.duration < 600,
    )
  );
}

async function openCache() {
  try {
    return await caches.open(cacheName);
  } catch {
    return undefined;
  }
}

export async function loadAudioManifest(): Promise<AudioManifest | null> {
  const cache = await openCache();
  try {
    const response = await fetch(manifestUrl, {
      cache: "no-cache",
      signal: AbortSignal.timeout(8000),
    });
    if (!response.ok) throw new Error("Manifest unavailable");
    const value: unknown = await response.clone().json();
    if (!validManifest(value)) throw new Error("Stale manifest");
    try {
      await cache?.put(manifestUrl, response);
    } catch {
      /* Storage is optional. */
    }
    return value;
  } catch {
    try {
      const value: unknown = await (await cache?.match(manifestUrl))?.json();
      return validManifest(value) ? value : null;
    } catch {
      return null;
    }
  }
}

/** Keeps immutable recordings for other open app versions; never prunes on load. */
export class AudioSources {
  private urls = new Map<string, string>();
  private pending = new Map<string, Promise<void>>();
  private disposed = false;
  source(clip: AudioClip) {
    return this.urls.get(clip.file) ?? clipUrl(clip);
  }
  prepare(clip: AudioClip): Promise<void> {
    if (this.disposed || this.urls.has(clip.file)) return Promise.resolve();
    const existing = this.pending.get(clip.file);
    if (existing) return existing;
    const task = this.load(clip).finally(() => this.pending.delete(clip.file));
    this.pending.set(clip.file, task);
    return task;
  }
  private async load(clip: AudioClip) {
    try {
      const cache = await openCache();
      const url = clipUrl(clip);
      let response = await cache?.match(url);
      if (!response) {
        response = await fetch(url, { signal: AbortSignal.timeout(15000) });
        if (!response.ok) return;
      }
      const bytes = await response.clone().arrayBuffer();
      if (!bytes.byteLength) return;
      const digest = await crypto.subtle.digest("SHA-256", bytes);
      const hash = Array.from(new Uint8Array(digest), (value) =>
        value.toString(16).padStart(2, "0"),
      ).join("");
      if (hash !== clip.audioHash) {
        await cache?.delete(url);
        return;
      }
      try {
        await cache?.put(url, response);
      } catch {
        /* Direct playback still works. */
      }
      if (!this.disposed)
        this.urls.set(
          clip.file,
          URL.createObjectURL(new Blob([bytes], { type: "audio/mpeg" })),
        );
    } catch {
      /* Keep the direct URL fallback. */
    }
  }
  dispose() {
    this.disposed = true;
    for (const url of this.urls.values()) URL.revokeObjectURL(url);
    this.urls.clear();
  }
}
