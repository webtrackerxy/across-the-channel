import { afterEach, describe, expect, it, vi } from "vitest";
import manifest from "../../public/audio/narration/manifest.json";
import { AudioSources, loadAudioManifest, validManifest } from "./audioCache";

afterEach(() => vi.unstubAllGlobals());
function cache() {
  const responses = new Map<string, Response>();
  const store = {
    match: vi.fn(async (url: string) => responses.get(url)?.clone()),
    put: vi.fn(async (url: string, response: Response) => {
      responses.set(url, response.clone());
    }),
    delete: vi.fn(async (url: string) => responses.delete(url)),
  };
  vi.stubGlobal("caches", { open: async () => store });
  return { responses, store };
}
describe("Compatible offline narration", () => {
  it("stores a valid manifest and reuses it offline without pruning older assets", async () => {
    const { store } = cache();
    const fetcher = vi
      .fn()
      .mockResolvedValueOnce(Response.json(manifest))
      .mockRejectedValue(new Error("offline"));
    vi.stubGlobal("fetch", fetcher);
    expect(await loadAudioManifest()).toEqual(manifest);
    expect(await loadAudioManifest()).toEqual(manifest);
    expect(store.delete).not.toHaveBeenCalled();
  });
  it("rejects stale script text and unsafe filenames", () => {
    expect(validManifest(manifest)).toBe(true);
    const stale = structuredClone(manifest);
    stale.clips[0].text = "out of date";
    expect(validManifest(stale)).toBe(false);
    stale.clips[0] = { ...manifest.clips[0], file: "../outside.mp3" };
    expect(validManifest(stale)).toBe(false);
  });
  it("works without Cache Storage and returns null if both sources fail", async () => {
    vi.stubGlobal("caches", {
      open: async () => {
        throw new Error("storage blocked");
      },
    });
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        .mockResolvedValueOnce(Response.json(manifest))
        .mockRejectedValue(new Error("offline")),
    );
    expect(await loadAudioManifest()).toEqual(manifest);
    expect(await loadAudioManifest()).toBeNull();
  });
  it("rejects corrupt cached audio and keeps a direct fallback", async () => {
    const { responses, store } = cache();
    const clip = manifest.clips[0];
    responses.set(`/audio/narration/${clip.file}`, new Response("bad bytes"));
    const sources = new AudioSources();
    await sources.prepare(clip);
    expect(store.delete).toHaveBeenCalled();
    expect(sources.source(clip)).toBe(`/audio/narration/${clip.file}`);
    sources.dispose();
  });
});
