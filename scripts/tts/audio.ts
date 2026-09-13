import { execFile } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import {
  mkdir,
  mkdtemp,
  readFile,
  rename,
  rm,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { promisify } from "node:util";

const run = promisify(execFile);
export const hash = (bytes: string | Uint8Array) =>
  createHash("sha256").update(bytes).digest("hex");

export async function atomicWrite(path: string, bytes: string | Uint8Array) {
  await mkdir(dirname(path), { recursive: true });
  const temporary = `${path}.${randomUUID()}.tmp`;
  try {
    await writeFile(temporary, bytes, { flag: "wx" });
    await rename(temporary, path);
  } finally {
    await rm(temporary, { force: true });
  }
}

export async function requireProbe() {
  try {
    await run("ffprobe", ["-version"], { timeout: 10000 });
  } catch {
    throw new Error(
      "Install ffmpeg (including ffprobe) before validating or generating narration.",
    );
  }
}

export async function inspectAudio(bytes: Uint8Array): Promise<number> {
  if (!bytes.length || bytes.length > 20 * 1024 * 1024)
    throw new Error("Invalid narration audio size");
  const directory = await mkdtemp(join(tmpdir(), "narration-audio-"));
  try {
    const file = join(directory, "clip.mp3");
    await writeFile(file, bytes);
    const { stdout, stderr } = await run(
      "ffprobe",
      [
        "-v",
        "error",
        "-count_frames",
        "-show_entries",
        "stream=codec_name,nb_read_frames:format=duration",
        "-of",
        "json",
        file,
      ],
      { timeout: 30000 },
    );
    const metadata = JSON.parse(stdout);
    const duration = Number(metadata.format?.duration);
    if (
      stderr.trim() ||
      metadata.streams?.length !== 1 ||
      metadata.streams[0].codec_name !== "mp3" ||
      !(Number(metadata.streams[0].nb_read_frames) > 0) ||
      !Number.isFinite(duration) ||
      duration <= 0
    )
      throw new Error("Invalid MP3 audio");
    return duration;
  } catch {
    throw new Error(
      "Narration audio is not a readable MP3; check ffprobe installation and the recording.",
    );
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

export async function readJson(path: string): Promise<unknown> {
  return JSON.parse(await readFile(path, "utf8"));
}
