# Narration implementation plan

Date: 12 September 2026. Phases 1–4 authorized by the user. This is the execution plan for [the narration proposal](narration-plan.md); it supersedes conflicting details in that draft. The broader research review remains pending.

## Phase 1 — Script and review transcript

Create a pure `narrationFor(frame)` function for the 14 existing playback steps. Read chapter introductions once at steps 1, 2, 11 and 12 (one-based), followed by the applicable annual figures, comparison or preset. Use existing application data and scene copy rather than a second numeric dataset.

Annual narration includes people, boats and calculated occupancy to one decimal place. Correct 2019 to 1,843 people, 164 boats and 11.2 people per boat. Derive partial-year dates and provisional labels from the data; explain that partial totals cannot be compared with full years. Calculate comparison percentages before rounding. Every scenario identifies its assumptions, modelled result and hypothetical status; map connections are not vessel tracks.

Deliver `src/story/narration.ts`, unit tests and [the generated review transcript](narration-transcript.md). Test transcript synchronization so factual edits cannot silently leave the document stale. Do not promise four-second recordings: figures and caveats need natural speaking time. This phase does not generate audio or change playback.

Acceptance: all 14 steps covered; exact annual units and calculations tested; chapter introductions occur once; provisional and scenario qualifications retained; transcript matches the function output.

## Phase 2 — Generation tooling

Create an explicit `narration:build` command, separate from application builds. Use the proposed `gpt-4o-mini-tts`, `sage`, MP3 and calm British documentary instructions. Verify the current API contract before implementing the client. Load the key only in the local generation process, from the environment or `.env.local`; never expose it to browser code or logs. Declare any CLI runner as a direct dependency.

Implement `use`, `refresh`, `only` and `off` cache modes. Hash a structured serialization of the request settings for generation-cache identity; hash the actual audio bytes for public filenames. A refreshed recording therefore receives a new URL when its bytes change. Reuse is free only when a valid matching cache entry exists.

Validate responses and cached audio, use bounded retries respecting Retry-After, and write cache entries atomically. Stage all clips before atomically replacing the manifest; generation failure must preserve the previous release. Record frame, text, request key, audio hash, filename and duration. Defer obsolete-file removal until successful publication and account for older open clients. Prune only unused cache entries older than the retention period. Ignore `.cache/tts/`.

Acceptance: fake API tests cover cache hits, refresh, corruption, missing entries in cache-only mode, partial failure and safe pruning. Extend Vitest discovery if tests live under `scripts/`. Normal builds and CI need no key. Add a key-free manifest consistency check once audio exists.

## Phase 3 — Recordings

Generate the 14 clips from the reviewed transcript. Listen for figures, pronunciation, tone and truncation; record actual durations. Treat cost as an estimate until measured, including cache misses and retries. Prepare audio and manifest as versioned static assets; generation does not itself commit repository changes.

Acceptance: every frame has a valid matching clip, intelligible narration and measured duration; the manifest check passes.

## Phase 4 — Playback and browser cache

Coordinate dwell time and speech completion. Preserve pause/resume position and remaining dwell time; restart at frame zero. Resolve the selected UI frame before playing, cancel obsolete async work after navigation, and prevent stale audio or captions. Keep the initial play call inside the user gesture, without awaiting cache/network work first. Handle rejected play promises.

Use duration-aware playback recovery with a separate bounded loading/stall timeout; paused time must not consume the timeout. Missing or failed audio permits silent progression. Turning narration off completes the audio gate; turning it on applies at the next step. Test the final frame with narration both on and off.

Cache a validated manifest as well as clips, check compatibility with the current script, and fall back to the last compatible manifest offline. Retain assets needed by active versions. Cache eviction or unsupported storage must fall back gracefully to direct URLs. Revoke unused blob URLs. Cached narration can work in an already loaded app offline; this does not promise offline page loading.

Acceptance: integration tests cover timing, rapid navigation, pause/resume, restart, visibility changes, errors, offline fallback and stale manifests. Include real browser playback coverage beyond a mocked `play()` call.

## Phase 5 — Controls and accessibility

Add a remembered Narration toggle, initially off, with an AI-generated voice disclosure. Provide an expandable text transcript without enlarging the fixed playback bar beyond the available viewport. Preserve keyboard access, focus visibility, font scaling, light/dark themes and responsive layout. Entering full-map mode pauses narration, matching existing interaction behaviour.

Review all live regions, including scenario results, to reduce competing speech without claiming to control a screen reader. Do not make the full transcript an automatic live announcement. Keep status and failure feedback understandable.

Acceptance: desktop/mobile, large text, keyboard and accessibility checks pass; transcript and controls fit the intended layouts.

## Phase 6 — Validation and handover

Run script, generation and playback tests; retain existing autoplay regression coverage. Update README, docs/project/ARCHITECTURE.md, docs/project/ACCESSIBILITY.md and docs/project/AI_USAGE.md to describe the implemented behaviour. Run `yarn run check` (the explicit project script).

Completion: all steps have matching audio, users can control playback, refreshed audio invalidates old caches, and deployment requires no API access.

## Progress

- Phase 1: complete. Script and generated transcript cover all 14 steps. Eight narration tests verify figures, chapter openings, qualifications, invalid inputs and transcript synchronization. `yarn run check` passed: data validation, formatting, 16 unit tests, production build and 20 desktop/mobile browser tests. The existing large-bundle advisory remains. No API calls or audio generation were performed.
- Phase 2: complete. Added explicit CLI commands, a direct vite-node dependency, local credentials loading, request-keyed cache modes, MP3 hash/duration validation with ffprobe, bounded HTTP retries, atomic manifest publication and conservative pruning. Older public audio is retained for existing clients. Eleven new tooling tests use fake API responses and local tones. `yarn run check` passed: data validation, formatting, 27 unit tests, production build and 20 desktop/mobile browser tests. Transcript regeneration and cache-only missing-clip handling were exercised without API calls. FFmpeg is now a documented tooling/test prerequisite. The strict manifest check stays separate from the main check until recordings exist in Phase 3.
- Phase 3: all 14 recordings generated and technically validated (247.20 seconds, 3,955,200 bytes). Full decoding, hashes, durations and requested-text consistency pass; a cache-only rebuild used 14 hits and zero API calls. The main check now validates the delivered manifest. A [recording review report](narration-recording-review.md) and `/audio/narration/review.html` provide durations, audio controls and transcripts. Data validation, narration validation, formatting, 27 unit tests and the production build passed. All 22 browser tests passed, including real recording playback on desktop/mobile; browser checks ran outside the sandbox after its local-server restriction. All audio assets and the review page are present in the static build. Listening review of spoken fidelity, pronunciation and tone remains pending, so the phase's listening acceptance criterion is not yet met. No API cost measurement or repository commit was made.
- Phase 4: complete. The story now waits for narration and dwell completion, resumes audio position and remaining dwell after pauses, cancels stale navigation, handles final-step completion and falls back silently after rejected or stalled audio. Initial play is called synchronously from the click. Manifest compatibility and SHA-256 audio checks protect cached playback; cached current/next clips are prepared before a returning user's first play. Blob URLs are disposed on unmount and older immutable recordings are retained. A minimal remembered Narration toggle, disclosure and transcript link make this integration usable; inline transcript and broader live-region refinement remain Phase 5. Data/manifest validation, formatting, 38 unit tests and the production build passed. All 28 browser cases passed across the full run and the targeted rerun of the two updated comparison assertions. The user's amendments also show total arrivals in the occupancy panel, highlight the 49.7% occupancy increase and increase the gap between the route legend and map scale. The comparison was reviewed in a desktop screenshot; the final spacing-only CSS edit passed formatting/diff checks. No new API calls were made.
- Phases 5–6: not started.
- 12 September amendment: Step 10 now narrates both the indicative Calais–Dover connection and the reported Utah Beach–Portsmouth endpoints, keeping the 6 September case outside the 3 September totals. Regenerated one recording and reused 13; the replacement is 34.248 seconds. Transcript/manifest validation, 38 unit tests, full MP3 decoding and production build passed. Listening review remains pending.
