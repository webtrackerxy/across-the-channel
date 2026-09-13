# Explorer retirement

The application now has one story interface. Removed exactly five retired implementation files:

- `src/App.tsx`
- `src/map/ChannelMap.tsx`
- `src/map/scenarioLayer.ts`
- `src/components/ScenarioControls.tsx`
- `src/story/useNarration.ts`

The new `DataTable.tsx` preserves the complete table, source links and CSV export. `StoryMap.tsx` supports a modal interactive map with year selection, pan, zoom, reset and fullscreen; historical year selection preserves the 2026 route distinction. Chart, sources and design-foundations dialogs remain available inside the story. The menu also links to the narration recording review page.

Old `?view=explore&year=…` URLs are normalized to the story; valid years open in the interactive map. All old explorer links were replaced by local dialogs. Scenario controls and amber connections remain in the optional scenario section. Three.js and its type dependency, bundle configuration and retired CSS layout selectors were removed. Existing explorer tests were adapted to the surviving features, not retained as dead tests.

The shared chart, dialogs, data, preferences, foundations, route coordinates and narration corpus remain. In particular, `scenes.ts` and `playback.ts` still participate in narration generation and compatibility validation; their apparent old-UI naming is not a reason to delete them.

Mobile amendments retain transparent bordered panels, smooth narration-driven reveal, and access to all enlarged-text content above the measured timeline height. Both development and preview servers listen on the local network (`0.0.0.0`); Vite prints the phone-accessible Network URL.

No release, push or new narration generation is included in this migration. Physical-device/Safari and comprehensive assistive-technology review remain separate from automated Chromium checks.

Validation: `yarn run check` passes data reconciliation, narration-manifest validation, formatting, all 44 unit tests, TypeScript/production build and 25 browser checks. One desktop-specific layout test is intentionally skipped in the mobile project. The local-network server returned HTTP 200 at the advertised LAN address. A final CTA hover-colour adjustment also passed formatting and whitespace checks.
