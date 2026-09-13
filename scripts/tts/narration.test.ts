import { execFile } from "node:child_process";
import {
  mkdtemp,
  readFile,
  readdir,
  rm,
  utimes,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import { afterAll, beforeAll, describe, expect, it, vi } from "vitest";
import { hash, inspectAudio } from "./audio";
import { buildNarration, checkManifest, type CacheMode } from "./build";
import { keyFor, prune } from "./cache";
import { generateSpeech, speechSettings } from "./openai";

let root: string;
let first: Uint8Array;
let second: Uint8Array;
const script = ["First test clip.", "Second test clip."].map((input) => ({
  ...speechSettings,
  input,
}));
beforeAll(async () => {
  root = await mkdtemp(join(tmpdir(), "narration-tests-"));
  for (const frequency of [440, 660]) {
    await promisify(execFile)("ffmpeg", [
      "-v",
      "error",
      "-f",
      "lavfi",
      "-i",
      `sine=frequency=${frequency}:duration=0.25`,
      "-c:a",
      "libmp3lame",
      join(root, `${frequency}.mp3`),
    ]);
  }
  first = await readFile(join(root, "440.mp3"));
  second = await readFile(join(root, "660.mp3"));
});
afterAll(async () => {
  if (root) await rm(root, { recursive: true, force: true });
});

async function setup() {
  const directory = await mkdtemp(join(root, "case-"));
  const options = {
    cacheDirectory: join(directory, "cache"),
    outputDirectory: join(directory, "public"),
    script,
    mode: "use" as CacheMode,
    generate: vi.fn(async () => first),
  };
  return options;
}

describe("Generation and publication", () => {
  it("validates MP3 duration and rejects non-audio payloads", async () => {
    expect(await inspectAudio(first)).toBeGreaterThan(0.2);
    await expect(inspectAudio(Buffer.from("not audio"))).rejects.toThrow();
  });
  it("generates once, reuses valid cache without API calls and checks the manifest", async () => {
    const options = await setup();
    expect((await buildNarration(options)).generated).toBe(2);
    options.generate.mockClear();
    expect((await buildNarration(options)).hits).toBe(2);
    expect(options.generate).not.toHaveBeenCalled();
    await checkManifest(options.outputDirectory, script);
    await expect(
      checkManifest(options.outputDirectory, [
        { ...script[0], input: "Changed" },
        script[1],
      ]),
    ).rejects.toThrow("mismatch");
  });
  it("refresh changes public URLs and retains older published clips", async () => {
    const options = await setup();
    const old = await buildNarration(options);
    options.generate.mockResolvedValue(second);
    const fresh = await buildNarration({ ...options, mode: "refresh" });
    expect(fresh.generated).toBe(2);
    expect(fresh.manifest.clips[0].file).not.toBe(old.manifest.clips[0].file);
    expect(await readdir(options.outputDirectory)).toContain(
      old.manifest.clips[0].file,
    );
    expect(fresh.manifest.clips[0].audioHash).toBe(hash(second));
  });
  it("cache-only lists all missing steps without generating or publishing", async () => {
    const options = await setup();
    await expect(buildNarration({ ...options, mode: "only" })).rejects.toThrow(
      "steps: 1, 2",
    );
    expect(options.generate).not.toHaveBeenCalled();
    await expect(readdir(options.outputDirectory)).rejects.toMatchObject({
      code: "ENOENT",
    });
  });
  it("regenerates corrupt cache entries and rejects corrupt published audio", async () => {
    const options = await setup();
    const result = await buildNarration(options);
    await writeFile(
      join(options.cacheDirectory, `${hash(first)}.mp3`),
      "corrupt",
    );
    expect((await buildNarration(options)).generated).toBe(2);
    await writeFile(
      join(options.outputDirectory, result.manifest.clips[0].file),
      "corrupt",
    );
    await expect(
      checkManifest(options.outputDirectory, script),
    ).rejects.toThrow("mismatch");
  });
  it("preserves the release on a partial generation failure", async () => {
    const options = await setup();
    await buildNarration(options);
    const path = join(options.outputDirectory, "manifest.json");
    const before = await readFile(path, "utf8");
    options.generate
      .mockResolvedValueOnce(second)
      .mockRejectedValueOnce(new Error("upstream failed"));
    await expect(
      buildNarration({ ...options, mode: "refresh" }),
    ).rejects.toThrow("upstream failed");
    expect(await readFile(path, "utf8")).toBe(before);
    await checkManifest(options.outputDirectory, script);
  });
  it("off mode publishes without creating a generation cache", async () => {
    const options = await setup();
    await buildNarration({ ...options, mode: "off" });
    await expect(readdir(options.cacheDirectory)).rejects.toMatchObject({
      code: "ENOENT",
    });
    await checkManifest(options.outputDirectory, script);
  });
  it("prunes only old unused entries and preserves shared active audio", async () => {
    const options = await setup();
    await buildNarration(options);
    const old = new Date(Date.now() - 40 * 86400000);
    for (const name of await readdir(options.cacheDirectory))
      await utimes(join(options.cacheDirectory, name), old, old);
    expect(
      await prune(options.cacheDirectory, new Set([keyFor(script[0])]), 30),
    ).toBe(1);
    expect(await readdir(options.cacheDirectory)).toContain(
      `${hash(first)}.mp3`,
    );
    expect(await prune(options.cacheDirectory, new Set(), 30)).toBe(2);
    await buildNarration(options);
    expect(await prune(options.cacheDirectory, new Set(), 30)).toBe(0);
  });
});

describe("Speech API client", () => {
  it("sends the selected settings and retries rate limits using Retry-After", async () => {
    const fetcher = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(
        new Response(null, { status: 429, headers: { "Retry-After": "2" } }),
      )
      .mockResolvedValueOnce(
        new Response(Buffer.from(first), {
          headers: { "Content-Type": "audio/mpeg" },
        }),
      );
    const sleep = vi.fn(async () => {});
    await generateSpeech(script[0], "test-only", fetcher, sleep);
    expect(sleep).toHaveBeenCalledWith(2000);
    expect(JSON.parse(fetcher.mock.calls[0][1]!.body as string)).toEqual(
      script[0],
    );
    expect(fetcher.mock.calls[0][0]).toBe(
      "https://api.openai.com/v1/audio/speech",
    );
  });
  it("bounds retries and does not retry authentication errors or expose response bodies", async () => {
    const fetcher = vi
      .fn<typeof fetch>()
      .mockImplementation(async () => new Response("private", { status: 503 }));
    await expect(
      generateSpeech(script[0], "test-only", fetcher, async () => {}),
    ).rejects.toThrow("HTTP 503");
    expect(fetcher).toHaveBeenCalledTimes(4);
    fetcher
      .mockClear()
      .mockResolvedValue(new Response("private", { status: 401 }));
    await expect(
      generateSpeech(script[0], "test-only", fetcher),
    ).rejects.toThrow("HTTP 401");
    expect(fetcher).toHaveBeenCalledTimes(1);
  });
  it("rejects missing credentials, excessive waits and non-audio responses", async () => {
    const fetcher = vi.fn<typeof fetch>();
    await expect(generateSpeech(script[0], "", fetcher)).rejects.toThrow(
      "OPENAI_API_KEY",
    );
    expect(fetcher).not.toHaveBeenCalled();
    fetcher.mockResolvedValueOnce(
      new Response(null, { status: 429, headers: { "Retry-After": "120" } }),
    );
    await expect(
      generateSpeech(script[0], "test-only", fetcher),
    ).rejects.toThrow("rerun later");
    fetcher.mockResolvedValueOnce(
      new Response("{}", { headers: { "Content-Type": "application/json" } }),
    );
    await expect(
      generateSpeech(script[0], "test-only", fetcher),
    ).rejects.toThrow("content type");
  });
});
