export const speechSettings = {
  model: "gpt-4o-mini-tts",
  voice: "sage",
  instructions:
    "Calm, measured British English documentary narrator. Neutral, respectful tone.",
  response_format: "mp3",
} as const;
export type SpeechRequest = {
  model: string;
  voice: string;
  instructions: string;
  response_format: "mp3";
  input: string;
};

export async function generateSpeech(
  request: SpeechRequest,
  apiKey: string,
  fetcher: typeof fetch = fetch,
  sleep = (ms: number) =>
    new Promise<void>((resolve) => setTimeout(resolve, ms)),
): Promise<Uint8Array> {
  if (!apiKey.trim())
    throw new Error("OPENAI_API_KEY is required for uncached narration.");
  if (!request.input.trim() || request.input.length > 4096)
    throw new Error("Speech input must contain 1–4096 characters.");
  for (let attempt = 0; attempt < 4; attempt++) {
    let response: Response;
    try {
      response = await fetcher("https://api.openai.com/v1/audio/speech", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${apiKey}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
        signal: AbortSignal.timeout(60000),
        redirect: "error",
      });
    } catch {
      // A connection failure may occur after billing; do not retry ambiguously.
      throw new Error(
        "Speech request failed or timed out; no automatic network retry was made.",
      );
    }
    if (response.ok) {
      const type = response.headers.get("content-type")?.split(";")[0];
      if (
        !["audio/mpeg", "audio/mp3", "application/octet-stream"].includes(
          type ?? "",
        )
      ) {
        await response.body?.cancel();
        throw new Error("Speech API returned an unexpected content type.");
      }
      try {
        const bytes = new Uint8Array(await response.arrayBuffer());
        if (!bytes.length || bytes.length > 20 * 1024 * 1024)
          throw new Error("Invalid size");
        return bytes;
      } catch {
        throw new Error(
          "Speech API returned empty, oversized or incomplete audio.",
        );
      }
    }
    await response.body?.cancel();
    if ((response.status !== 429 && response.status < 500) || attempt === 3)
      throw new Error(
        `Speech API failed (HTTP ${response.status}); response details omitted to protect credentials.`,
      );
    const retry = response.headers.get("retry-after");
    const delay =
      retry === null
        ? 1000 * 2 ** attempt
        : Number.isFinite(Number(retry))
          ? Number(retry) * 1000
          : Date.parse(retry) - Date.now();
    if (delay > 60000)
      throw new Error(
        "Speech API requested a wait longer than 60 seconds; rerun later.",
      );
    await sleep(
      Number.isFinite(delay) ? Math.max(0, delay) : 1000 * 2 ** attempt,
    );
  }
  throw new Error("Speech retry limit reached");
}
