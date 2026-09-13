# Channel design system

Version 1.0. Open **Design foundations** (story menu) for the live foundation and component preview. It responds to the active theme and text size.

## Foundations

`src/design/foundations.css` owns semantic colours, typography, spacing, radii and control-size tokens. Dark and light palettes share token names. Interface surfaces, chart bars, map land/water, labels and scenario lines respond to the chosen palette. Highlighted route lines use a contrasting halo, dashed stroke and endpoint markers; the Dover–Calais connection is explicitly indicative and scenario connections are hypothetical.

- DM Sans: body, controls and tabular figures. Manrope: headings and key figures. Fonts are hosted locally.
- Base type scale: 12, 14, 16, 20 and 28 px; rem units scale with user preferences. Dense mobile chart labels use a smaller secondary scale.
- Spacing: 4 px base with 4, 8, 12, 16, 24 and 32 px steps.
- Corner radii: approximately 5 and 10 px.
- Primary controls: at least 44 px at the default text size. Compact chart links retain at least 24 px targets.
- Semantic colour roles: background, panel, surface, primary/muted text, accent, scenario, boundaries and focus. Historical and hypothetical content also have explicit text labels.

The preview includes colour swatches, type specimens, spacing samples, action buttons, selected/disabled states, evidence labels and a sample input. New components should consume these foundation tokens and preserve native HTML control semantics.

## Preferences and layout

The story menu provides light/dark appearance, persistent 100–200% text sizing, reduced motion, motion pause/replay, full data and CSV, design foundations and the narration recording review link. Storage failures leave session controls usable. Browser zoom remains independent.

The map-led page scrolls through six factual sections and one optional scenario. Desktop evidence sits to the left of the map; mobile panels are translucent. Portsmouth details use an internally scrollable panel when needed so the timeline cannot hide the remaining content. Mobile narration gently reveals the text, unless reduced motion is selected.

The bottom timeline provides chapter shortcuts and a chart popup. Chart year selection updates its figures; its interactive-map button opens that year in a native dialog. The map dialog provides pan, zoom, reset and fullscreen. Wider hypothetical connections remain amber and labelled. The data table supports horizontal scrolling and CSV export.

## Listening

Listen starts or resumes the current section; Pause preserves audio position. Manual navigation/scrolling, hidden tabs and opening data/map dialogs pause playback. Six existing recordings accompany the factual sections. Completion scrolls to the optional scenario and stops audio. Scenario inputs are not narrated. Motion controls are independent of narration, and reduced motion disables continuous camera/boat/text movement.

## Phone layout

Phones keep compact header controls and a dot-based chapter timeline with an accessible chart button. Theme, text sizing and motion controls remain available in the menu. The floating AI-voice/transcript box is hidden on mobile at the user's request; the menu links to the full recording/transcript review page. Interactive-map pan, zoom and fullscreen controls remain available on phones.

# Editorial story extension

The scroll story scopes its presentation in `src/editorial/editorial.css`: navy sea, warm-white text and mint accents, with a corresponding light palette. Serif display headings distinguish narrative copy from the existing sans-serif evidence and controls. Shared theme and text-size preferences apply to both experiences.

One fixed map provides geographic continuity while six sections scroll naturally. Desktop text occupies the left portion; mobile places a readable surface below the map opening. A compact header and chapter timeline provide shortcuts. Camera transitions last 1.4 seconds and stop in reduced-motion mode. The approved route amendment adds a pausable four-boat Dover flow and one Portsmouth journey with explicit replay; reduced motion shows static boats. Display pacing and symbol counts are illustrative, with a visible qualification beside the motion controls.

Boat hulls scale with illustrated occupancy and contain an exact rounded number of equal-coordinate-size dots. They do not depict measured vessel dimensions or rated capacity. Numeric evidence remains data-derived and available without animation. The design foundations preview is available in the story menu.
