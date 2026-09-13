# Narration recordings — technical review

Generated 12 September 2026 with `gpt-4o-mini-tts`, voice `sage`, MP3. All 14 clips were generated from the current [transcript](narration-transcript.md), with no cache hits during initial generation. API cost was not measured.

Open [the listening review page](http://127.0.0.1:5173/audio/narration/review.html) with the development server running. Each recording has native playback controls, its expected transcript and a download link. Playback requires user action and starting a second recording pauses the first.

## Measured durations

| Step | Content | Seconds |
| --- | --- | ---: |
| 1 | Context | 14.52 |
| 2 | Occupancy introduction and 2018 | 23.16 |
| 3 | 2019 | 11.21 |
| 4 | 2020 | 11.30 |
| 5 | 2021 | 11.35 |
| 6 | 2022 | 12.72 |
| 7 | 2023 | 11.52 |
| 8 | 2024 | 11.35 |
| 9 | 2025 | 11.11 |
| 10 | 2026 partial year, Portsmouth connection and details | 48.22 |
| 11 | Comparison | 30.96 |
| 12 | Scenario introduction and Low | 36.46 |
| 13 | Continuation | 23.30 |
| 14 | Expansion | 23.02 |
| 15 | Conclusion (open questions) | 41.71 |

Current total: 321.912 seconds (5 minutes 22 seconds), 5,150,592 audio bytes. Step 10 was first regenerated on 12 September to include the indicative Dover connection and reported Utah Beach–Portsmouth endpoints, separating the 6 September case from the 3 September statistical cutoff. Later that day three clips were generated after wording changes: step 10 (about 140 people aboard, a reported arrival about 24 hours after leaving, boat size not reported), step 12 (the reworded closing question) and the new concluding step 15. The other 12 clips were reused from the local cache. Step 15 was then regenerated once more with an open ending (what is known, then open questions), with 14 cache hits.

## Findings

- All 15 clips passed MP3 structure/duration validation. The original clips and the clips generated later on 12 September, including the final step 15, each decoded fully with FFmpeg without reported errors.
- Manifest request keys, text and audio hashes match the current application script.
- After the 15-step update, all 39 unit tests and 30 browser tests passed (2 phone-only skips); the browser loads metadata for every delivered clip and exercises real playback on desktop/mobile. The production build contains all 15 recordings and the review page. The update generated 3 clips and reused 12 from the cache.
- Numeric-heavy full-year steps take about 11–13 seconds; the expanded 2026 step takes 48.22 seconds and the conclusion 41.71 seconds. Playback waits for audio completion and uses duration-aware failure handling.
- Decoding and matching requested text do not establish what was actually spoken. Listening review of figures, pronunciation, tone and sentence endings is pending; no human or model listening approval is claimed.
- The recordings are static assets ready for version control, but this work does not commit or deploy them. Playback integration remains Phase 4.
