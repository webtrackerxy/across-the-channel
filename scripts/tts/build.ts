import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { playbackFrames } from "../../src/story/playback";
import { narrationFor } from "../../src/story/narration";
import { atomicWrite, hash, inspectAudio, readJson } from "./audio";
import { get, keyFor, put } from "./cache";
import { speechSettings, type SpeechRequest } from "./openai";

export type CacheMode = "use" | "refresh" | "only" | "off";
export const requests = () =>
  playbackFrames.map((frame) => ({
    ...speechSettings,
    input: narrationFor(frame),
  }));
export interface ManifestEntry {
  frame: number;
  text: string;
  key: string;
  audioHash: string;
  file: string;
  duration: number;
}
export interface Manifest {
  version: 1;
  clips: ManifestEntry[];
}

export async function buildNarration(options: {
  cacheDirectory: string;
  outputDirectory: string;
  mode: CacheMode;
  generate: (request: SpeechRequest) => Promise<Uint8Array>;
  script?: SpeechRequest[];
}) {
  const script = options.script ?? requests();
  if (!["use", "refresh", "only", "off"].includes(options.mode))
    throw new Error("Invalid cache mode");
  const cached = await Promise.all(
    script.map((request) =>
      options.mode === "use" || options.mode === "only"
        ? get(options.cacheDirectory, request)
        : null,
    ),
  );
  if (options.mode === "only") {
    const missing = cached.flatMap((clip, index) => (clip ? [] : [index + 1]));
    if (missing.length)
      throw new Error(
        `Missing valid cached clips for steps: ${missing.join(", ")}`,
      );
  }
  const clips: ManifestEntry[] = [];
  // Staging in memory keeps the published release intact until all clips validate.
  const audio = new Map<string, Uint8Array>();
  let generated = 0;
  for (const [index, request] of script.entries()) {
    let clip = cached[index];
    if (!clip) {
      const bytes = await options.generate(request);
      clip = {
        bytes,
        audioHash: hash(bytes),
        duration: await inspectAudio(bytes),
      };
      generated++;
      if (options.mode !== "off")
        await put(options.cacheDirectory, request, clip);
    }
    const file = `${clip.audioHash}.mp3`;
    audio.set(file, clip.bytes);
    clips.push({
      frame: index,
      text: request.input,
      key: keyFor(request),
      audioHash: clip.audioHash,
      file,
      duration: clip.duration,
    });
  }
  for (const [file, bytes] of audio)
    await atomicWrite(join(options.outputDirectory, file), bytes);
  const manifest: Manifest = { version: 1, clips };
  await atomicWrite(
    join(options.outputDirectory, "manifest.json"),
    JSON.stringify(manifest, null, 2) + "\n",
  );
  // Keep older public clips for open tabs and older manifests; no automatic public pruning.
  return { manifest, generated, hits: script.length - generated };
}

export async function checkManifest(directory: string, script = requests()) {
  const manifest = (await readJson(
    join(directory, "manifest.json"),
  )) as Manifest;
  if (
    manifest?.version !== 1 ||
    !Array.isArray(manifest.clips) ||
    manifest.clips.length !== script.length
  )
    throw new Error("Narration manifest has an invalid version or step count");
  for (const [index, request] of script.entries()) {
    const entry = manifest.clips[index];
    if (
      !entry ||
      entry.frame !== index ||
      entry.text !== request.input ||
      entry.key !== keyFor(request) ||
      !/^[a-f0-9]{64}$/.test(entry.audioHash) ||
      entry.file !== `${entry.audioHash}.mp3` ||
      !Number.isFinite(entry.duration) ||
      entry.duration <= 0
    )
      throw new Error(`Narration manifest mismatch at step ${index + 1}`);
    const bytes = await readFile(join(directory, entry.file));
    if (
      hash(bytes) !== entry.audioHash ||
      Math.abs((await inspectAudio(bytes)) - entry.duration) > 0.01
    )
      throw new Error(`Narration audio mismatch at step ${index + 1}`);
  }
  return manifest;
}
