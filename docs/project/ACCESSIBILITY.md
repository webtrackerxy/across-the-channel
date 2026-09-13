# Accessibility verification

The implementation targets [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/).

## Implemented

- Editorial route movement has a visible pause/play control independent of narration, stops in hidden tabs and becomes static in reduced-motion mode. The Portsmouth illustration runs once with explicit replay. Boat icons are decorative; the HTML qualification explains that movement is not recorded journeys or boat frequency.

- The new scroll story uses normal document flow, labelled chapter navigation and no map gesture capture. Its decorative map is hidden from assistive technology; evidence and route qualifications are HTML text, with a button opening the interactive map dialog.
- Story listening is explicitly user-started, provides a full inline transcript and pauses for manual scrolling or navigation. An opened transcript remains available after pausing. Story controls include theme, 100–200% text size and reduced motion.

- Light/dark semantic palettes with readable text, explicit control boundaries and visible keyboard focus.
- Native buttons, labelled ranges/checkboxes/selects, chapter state, chart selection state, headings and a skip link.
- Native modal dialogs with Escape dismissal, contained keyboard focus and return to the opening control. The data dialog can open a source dialog and returns focus to the source link when it closes.
- A semantic data table and CSV alternative to the chart and WebGL map. Partial-year/provisional labels remain visible.
- Map pan buttons as a single-pointer alternative to dragging, zoom/reset controls and a geographic text description. Map failure leaves evidence and scenarios usable.
- 100–200% rem-based text controls with local persistence; narrow-screen reflow and scrollable data tables.
- User-initiated listening with pause/resume and discrete status announcements. No automatic playback on page load. Background tabs pause. Reduced-motion settings suppress camera transitions.
- Optional narration starts only on request. Desktop shows an AI-voice disclosure and inline transcript; the menu provides the full recording review page on all devices. Audio errors permit silent progression; opening a map or data dialog pauses narration.
- Forced-colour styles for chart bars and selected controls; meaning uses labels and selection indicators as well as colour.

## Reproducible checks

Run `yarn run check`. Playwright runs Chrome desktop and phone emulation with axe rules tagged `wcag2a`, `wcag2aa`, `wcag21aa` and `wcag22aa`.

Browser checks cover both themes, design foundations, scenario controls, source and data dialogs; keyboard slider adjustment and dialog focus restoration; 320 px reflow with 200% application text; persisted preferences; autoplay progression/pause/completion; map fallback; and map/chart bounds in a 1366×768 desktop and iPhone 13 viewport. Screenshots are written to `test-results/` for visual review.

## Scope

The editorial browser suite checks navigation, rendered occupancy dot counts, year selection in the interactive map dialog, reduced motion, map failure, both themes with axe, enlarged-text overflow and manual narration interruption. Desktop and iPhone-sized Chromium screenshots were reviewed. This is browser emulation, not physical-device or Safari validation. Reader comprehension testing remains pending.

Automated checks and browser review are evidence toward the AA target, not a complete conformance assessment. Physical mobile/Safari testing and a full screen-reader review (VoiceOver/NVDA), OS high-contrast review, and browser zoom/text-spacing review remain necessary before claiming audited WCAG 2.2 AA conformance. The map is supplemental: all numeric data and model inputs remain available in native HTML.

## Phone layout

The floating narration transcript box is hidden at the user's request; the menu provides access to the full recording review and transcripts. Display preferences remain in the menu. Chart, source and full-data dialogs work on desktop and mobile, including nested source-dialog focus restoration. The interactive map includes visible pan/zoom controls on phones, in addition to gestures. Chapter buttons have accessible names even when their visual labels are hidden.
