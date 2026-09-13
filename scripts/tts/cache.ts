import { readdir, readFile, rm, stat } from "node:fs/promises";
import { join } from "node:path";
import { atomicWrite, hash, inspectAudio, readJson } from "./audio";
import type { SpeechRequest } from "./openai";

export const keyFor = (request: SpeechRequest) =>
  hash(
    JSON.stringify([
      request.model,
      request.voice,
      request.instructions,
      request.response_format,
      request.input,
    ]),
  );
export interface CachedClip {
  bytes: Uint8Array;
  audioHash: string;
  duration: number;
}

export async function get(
  directory: string,
  request: SpeechRequest,
): Promise<CachedClip | null> {
  try {
    const entry = (await readJson(
      join(directory, `${keyFor(request)}.json`),
    )) as {
      request: SpeechRequest;
      audioHash: string;
      duration: number;
    };
    if (
      keyFor(entry.request) !== keyFor(request) ||
      !/^[a-f0-9]{64}$/.test(entry.audioHash)
    )
      return null;
    const bytes = await readFile(join(directory, `${entry.audioHash}.mp3`));
    if (hash(bytes) !== entry.audioHash) return null;
    const duration = await inspectAudio(bytes);
    if (
      Math.abs(duration - entry.duration) > 0.01 ||
      !Number.isFinite(entry.duration)
    )
      return null;
    return { bytes, audioHash: entry.audioHash, duration };
  } catch {
    return null;
  }
}

export async function put(
  directory: string,
  request: SpeechRequest,
  clip: CachedClip,
) {
  await atomicWrite(join(directory, `${clip.audioHash}.mp3`), clip.bytes);
  await atomicWrite(
    join(directory, `${keyFor(request)}.json`),
    JSON.stringify(
      {
        request,
        audioHash: clip.audioHash,
        duration: clip.duration,
        created: new Date().toISOString(),
        bytes: clip.bytes.length,
      },
      null,
      2,
    ) + "\n",
  );
}

/** Run without concurrent builds. Retains all audio referenced by surviving entries. */
export async function prune(
  directory: string,
  active: Set<string>,
  keepDays: number,
  now = Date.now(),
) {
  if (!Number.isFinite(keepDays) || keepDays < 0)
    throw new Error("keep-days must be non-negative");
  let names: string[];
  try {
    names = await readdir(directory);
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return 0;
    throw error;
  }
  const cutoff = now - keepDays * 86400000;
  const retained = new Set<string>();
  let removed = 0;
  for (const name of names.filter((item) =>
    /^[a-f0-9]{64}\.json$/.test(item),
  )) {
    const path = join(directory, name);
    if (!active.has(name.slice(0, -5)) && (await stat(path)).mtimeMs < cutoff) {
      await rm(path);
      removed++;
    } else {
      const entry = (await readJson(path)) as { audioHash: string };
      if (!/^[a-f0-9]{64}$/.test(entry.audioHash))
        throw new Error("Invalid retained cache entry; audio pruning stopped");
      retained.add(entry.audioHash);
    }
  }
  for (const name of names.filter((item) => /^[a-f0-9]{64}\.mp3$/.test(item))) {
    const path = join(directory, name);
    if (
      !retained.has(name.slice(0, -4)) &&
      (await stat(path)).mtimeMs < cutoff
    ) {
      await rm(path);
      removed++;
    }
  }
  return removed;
}
