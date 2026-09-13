# Narration plan

Drafted: 11 September 2026. Updated: 12 September 2026. Phases 1–2 complete; Phase 3 recordings generated and technically validated, with listening review pending. See [the implementation plan](narration-implementation-plan.md) for the current decisions, corrections and progress; the proposal below is retained as the original design.

Add spoken narration, generated with OpenAI TTS, to the "Play story" autoplay so that each of the 14 playback steps (`src/story/playback.ts`) has a matching voice clip.

The user explicitly authorized narration Phase 1 on 12 September 2026. This permits script and transcript work alongside the broader research review; it does not mark research claims as approved.

## Decisions

| Topic | Decision | Reason |
| --- | --- | --- |
| Engine | OpenAI `gpt-4o-mini-tts`, voice `sage`, mp3 | Same voice on every device; `instructions` controls the tone |
| When audio is generated | At build time, never in the browser | The app is static with no backend; calling the API from the browser would expose `OPENAI_API_KEY` |
| Delivery | Hashed mp3s in `public/audio/narration/`, committed | Deploys and CI never need the key |
| Cache | Two levels: a generation cache on the developer's machine and Cache Storage in the browser | Unchanged or previously generated text never calls the API again; repeat visits don't re-download clips |
| Default | Narration off; the setting is remembered | The page never plays sound unexpectedly (WCAG 1.4.2) |
| Disclosure | Show an "AI-generated voice" note next to the toggle | Required by OpenAI's usage policies |

Narrator instructions: "Calm, measured British English documentary narrator. Neutral, respectful tone."

## 1. Narration script: `src/story/narration.ts`

A pure function, `narrationFor(frame: PlaybackFrame): string`, builds the text for each step from `scenes` and `data/model`. The build script and the app both use it, so the spoken figures always match what's on screen.

- **Chapter-opening steps (0, 1, 10, 11):** read the scene title and body, with `\n` turned into a sentence break.
- **Year steps (2018–2026):** keep them short, around 4 seconds, so the Pace setting still matters. Example: "2019. 1,843 boats carried … people, an average of 11.1 per boat." For 2026, add "January to 3 September, provisional."
- **Comparison step:** the percentage falls in boats and in people, using `changePercent`.
- **Scenario steps (low / continuation / expansion):** the preset label, description and modelled arrivals, always with "a hypothetical scenario, not a forecast."
- **Words that read badly aloud:** "people / boat" becomes "people per boat"; numbers use `formatNumber`.

## 2. Generation: `yarn narration:build`

Files:

- `scripts/build-narration.ts`: handles the cache modes, writes the manifest and removes unused clips. Runs with `vite-node`, which comes with vitest, so no new dependency is needed.
- `scripts/tts/openai.ts`: `POST https://api.openai.com/v1/audio/speech` with `model`, `voice`, `input`, `instructions` and `response_format: "mp3"`. Retries up to 3 times, with increasing waits, on 429 and 5xx errors.
- `scripts/tts/cache.ts`: `keyFor`, `get`, `put` (writes to a temporary file, then renames), `prune`.

The key is read from `OPENAI_API_KEY` in the environment or `.env.local`. Add `.env.local` to `.gitignore`. The key is never bundled into the app.

For each step:

1. `key = sha256(model | voice | instructions | format | text)`.
2. If the clip is in the cache, copy it to `public/audio/narration/NN-<key8>.mp3`. No API call.
3. If it isn't, call OpenAI, write the result to the cache safely, then copy it to `public/`.
4. Write `public/audio/narration/manifest.json` (`{ frame, text, key, file }[]`) and delete clips in `public/` that are no longer used.

Print a summary at the end, for example: `14 steps · 12 cache hits · 2 generated · ~$0.01`.

## 3. Generation cache on the developer's machine

- Location: `.cache/tts/`, or `TTS_CACHE_DIR` if set. Add it to `.gitignore`.
- Each clip is stored as `<key>.mp3` plus `<key>.json` (text, model, voice, instructions, created, bytes).
- An empty or unreadable cached file counts as missing and is regenerated.
- Switching voices, changing instructions or undoing a wording change reuses clips generated earlier at no cost.

Modes (`--cache=<mode>`):

| Mode | Reads cache | Calls API | Use |
| --- | --- | --- | --- |
| `use` (default) | yes | only for missing clips | normal runs |
| `refresh` | no | yes, and overwrites the cache | re-record everything |
| `only` | yes | never; fails and lists missing clips | CI, or no API key |
| `off` | no | yes, but saves nothing to the cache | one-off tests |

Other commands:

- `yarn narration:check`: fails if `manifest.json` doesn't match the current `narrationFor` output. It needs no key. Add it to `yarn check`.
- `yarn narration:cache:prune [--keep-days 30]`: deletes cached clips that the current settings don't use.

## 4. Playback: `src/story/useNarration.ts`

- Loads `manifest.json`, plays the current step's clip in a single audio element and preloads the next step's clip.
- **Moving to the next step:** replace the fixed timer in `App.tsx`. Move on only when the Pace time has passed (`dwellDone`) *and* the clip has ended (`speechDone`). On the last step, stop after the clip ends. A fallback timeout (pace plus 20 s) covers the `ended` event never firing.
- **Pause:** every existing `setPlaying(false)` path pauses the audio through one effect. Resuming on the same step carries on from where it stopped. Restart rewinds to step 0.
- **Browser autoplay rules:** the first `play()` call happens inside the Play click handler.
- **If a clip is missing or can't play:** it counts as finished and playback continues silently.
- **Toggling narration mid-play:** turning it off pauses the audio and counts the clip as finished. Turning it on starts with the next step.

## 5. Playback cache in the browser: `src/story/audioCache.ts`

- Clip filenames include the hash, so a given file never changes. Each clip is downloaded once, stored in Cache Storage (`narration-v1`) and played from a blob URL afterwards. Once played, it also works offline.
- `manifest.json` is always fetched fresh when online. Stored clips it no longer lists are deleted.
- If Cache Storage isn't available (private browsing, blocked storage), the clip plays straight from its URL.

## 6. Controls and accessibility

- A **Narration** toggle (lucide `Volume2` / `VolumeX`, `aria-pressed`) in the Autoplay controls group. It's saved through `design/preferences.ts` and hidden if the manifest can't load.
- "AI-generated voice" note next to the toggle.
- **Caption line:** while narration is on, the playback bar shows the text for the current step, so the audio has a text equivalent.
- **Screen readers:** while narration is on, the hidden `role="status"` region (`App.tsx`) says only "Narration playing" / "Autoplay paused", so there aren't two voices at once.
- Styles in `styles.css`, using the existing design tokens.

## 7. Tests

Vitest:

- `narration.test.ts`: all 14 steps produce text; figures match `data/model`; scenario steps include "not a forecast"; 2026 says provisional.
- The committed manifest matches the current text (same check as `narration:check`).
- Cache, with a temporary folder and a fake API call:
  - a first run generates each clip once and a second run makes zero calls;
  - `refresh` regenerates;
  - `only` fails when clips are missing;
  - a damaged cache file gets regenerated;
  - `prune` removes only unused entries.

Playwright (`tests/story.spec.ts`), with clips served through `page.route` and a stubbed `HTMLMediaElement.play`:

- the story waits for `ended` before moving on;
- Pause pauses the audio and resuming continues;
- a missing clip doesn't stop playback;
- the toggle's state survives a reload;
- after a reload, playing again doesn't fetch the clips a second time.

The existing autoplay test isn't affected, because narration is off by default.

## 8. Docs

- `docs/project/ACCESSIBILITY.md`: audio control, captions, avoiding two voices with screen readers, AI-voice disclosure.
- `docs/project/ARCHITECTURE.md` / `README.md`: the new modules; when and how to run `narration:build`; the cache modes.
- `docs/project/AI_USAGE.md`: OpenAI TTS is used to generate the narration audio.
- `implementation-plan.md`: add a status line linking to this plan.

## Order of work

1. `narration.ts` and its tests.
2. `scripts/tts/*`, `build-narration.ts`, the cache tests and package scripts.
3. Generate the clips (needs `OPENAI_API_KEY`) and commit the manifest and mp3s.
4. `useNarration.ts`, `audioCache.ts` and the `App.tsx` changes.
5. Toggle, caption, disclosure and styles.
6. Playwright tests, docs, then `yarn check`.

Estimated API cost: well under $0.10 for all 14 clips; re-runs cost nothing unless the text changes.
