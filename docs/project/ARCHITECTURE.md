# Story architecture

## Boundaries

- `src/editorial/Entry.tsx`: the single lazy story entry; normalizes old explorer URLs and preserves year parameters.
- `src/editorial/StoryPage.tsx`: seven sections, scroll/navigation state, theme/type preferences and chart, map, data, source and design dialogs.
- `src/editorial/StoryMap.tsx`: MapLibre renderer shared by the persistent background and the interactive map dialog. The latter adds pan/zoom/reset/fullscreen controls and year selection; it is mounted only while open.
- `src/editorial/RouteBoats.tsx`: one animation loop per mounted map, using shared coordinates and retained progress. Paused/reduced-motion maps do not run the loop. The interactive dialog shows static symbols.
- `src/editorial/sections.ts` and `BoatIllustration.tsx`: section/recording mappings and rounded-occupancy SVGs. Hull dimensions are illustrative.
- `src/editorial/StoryScenario.tsx` and `src/scenarios/model.ts`: input controls and shared deterministic calculations, separate from historical totals.
- `src/components/HistoryChart.tsx`, `DataTable.tsx`, `Dialog.tsx` and `EvidenceDialog.tsx`: shared accessible evidence views and CSV export.
- `src/design`: semantic foundations, preference persistence and the live design preview.
- `src/data`: generated records and pure arithmetic; `scripts/build_data.py` checks source inputs.
- `src/map/routes.ts` and `portsmouth.ts`: indicative/hypothetical geometry and qualified reported endpoints.
- `src/editorial/useStoryListening.ts`: owns the narration transport, maps six existing recordings, and reveals mobile copy. Manual input and dialogs pause playback; completion moves to the optional scenario without narrating its inputs.
- `src/story/narrationPlayer.ts` and `audioCache.ts`: tested timing, cancellation, failure recovery, manifest compatibility and validated audio caching.
- `src/story/scenes.ts`, `playback.ts`, `narration.ts` and `conclusion.ts`: retained to generate and validate the 15-recording corpus. Removing the old UI does not invalidate or regenerate recordings.
- `scripts/narration.ts` and `scripts/tts`: local-only generation and cache tooling; no browser API key or runtime speech API requests.

## Map lifecycle and delivery

The background map is non-interactive and supplemental; the dialog map provides gestures, keyboard navigation and single-pointer pan controls. Each map removes its markers, listeners, observers and WebGL instance on unmount. Pixel ratio is capped at two. Reduced motion disables camera transitions and moving boats; hidden tabs suspend route animation. Map failures leave HTML evidence and controls available.

Natural Earth geography and fonts are locally hosted. MapLibre is code-split and loaded asynchronously. The retired explorer's Three.js renderer and dependencies are removed. The browser has no backend, database or secrets. Story hashes and year query parameters support direct links; native modal dialogs retain focus behavior.

## Review status

The implementation follows the user's 11 September 2026 instruction to start an MVP despite unanswered research questions. That overrides the earlier research-before-development sequencing, but does not change the truth status of the evidence. The wider nine-scene plan remains a roadmap.
