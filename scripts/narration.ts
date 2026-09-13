import { readFile } from "node:fs/promises";
import { parseEnv } from "node:util";
import { resolve } from "node:path";
import { narrationTranscript } from "../src/story/narration";
import { atomicWrite, requireProbe } from "./tts/audio";
import {
  buildNarration,
  checkManifest,
  requests,
  type CacheMode,
} from "./tts/build";
import { keyFor, prune } from "./tts/cache";
import { generateSpeech } from "./tts/openai";

async function main() {
  const [command, ...args] = process.argv.slice(2);
  const cacheDirectory = resolve(process.env.TTS_CACHE_DIR || ".cache/tts");
  const outputDirectory = resolve("public/audio/narration");
  if (command === "transcript" && !args.length) {
    await atomicWrite(
      "docs/narration/narration-transcript.md",
      narrationTranscript(),
    );
    console.log("Updated narration transcript.");
    return;
  }
  if (command === "prune") {
    if (
      args.some((arg) => !/^--keep-days=\d+(\.\d+)?$/.test(arg)) ||
      args.length > 1
    )
      throw new Error("Usage: narration:cache:prune [--keep-days=30]");
    const keepDays = Number(args[0]?.split("=")[1] ?? 30);
    console.log(
      `Removed ${await prune(cacheDirectory, new Set(requests().map(keyFor)), keepDays)} unused cache files.`,
    );
    return;
  }
  if (command === "check" && !args.length) {
    await requireProbe();
    await checkManifest(outputDirectory);
    console.log(
      "Narration manifest, figures, hashes and audio durations match.",
    );
    return;
  }
  if (
    command !== "build" ||
    args.length > 1 ||
    args.some((arg) => !/^--cache=(use|refresh|only|off)$/.test(arg))
  )
    throw new Error("Usage: narration:build [--cache=use|refresh|only|off]");
  await requireProbe();
  const mode = (args[0]?.split("=")[1] ?? "use") as CacheMode;
  // Read credentials only on a genuine cache miss, and never through Vite's client env loader.
  const generate = async (request: Parameters<typeof generateSpeech>[0]) => {
    let key = process.env.OPENAI_API_KEY;
    if (key === undefined) {
      try {
        key = parseEnv(await readFile(".env.local", "utf8")).OPENAI_API_KEY;
      } catch (error) {
        if ((error as NodeJS.ErrnoException).code !== "ENOENT")
          throw new Error("Unable to read .env.local");
      }
    }
    return generateSpeech(request, key ?? "");
  };
  const result = await buildNarration({
    cacheDirectory,
    outputDirectory,
    mode,
    generate,
  });
  console.log(
    `${result.manifest.clips.length} steps · ${result.hits} cache hits · ${result.generated} generated. Cost is not measured by this command.`,
  );
}

main().catch((error: unknown) => {
  console.error(
    error instanceof Error ? error.message : "Narration command failed",
  );
  process.exitCode = 1;
});
