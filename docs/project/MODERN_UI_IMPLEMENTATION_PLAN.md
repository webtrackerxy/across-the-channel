# Modern storytelling UI — implementation plan

Migration update: the old explorer has been retired and its remaining features moved into the story. See [Explorer retirement](EXPLORER_RETIREMENT.md) for the five removed files, preserved features and passing validation. Earlier phase notes below describe the development sequence before that migration.

Status: core implementation complete locally. Focused story checks pass; the full browser regression run encountered loading and narration timing failures and was interrupted. Physical-device, screen-reader and reader-comprehension reviews remain pending.

Working branch: `feat/scroll-story-ux`, based on local `internal_main`. This plan turns the [UX feedback proposal](UX_IMPROVEMENT_PLAN.md) and the user's modern-style direction into six delivery phases.

## Intended experience

Create a modern editorial story with bold typography, generous space, cinematic data graphics and purposeful animation. Guide first-time readers through a clear argument while retaining the current interface as an optional explorer for returning users.

The new story uses a longer, naturally scrolling page. The previous single-screen layout remains available in the explorer. Chapter anchors and an “Explore the data” entry point provide direct access without reading the whole story.

Opening headline:

> What does counting boats miss?

The comparison chapter, explicitly labelled **2022 versus 2025**, highlights:

- **39.5% fewer arriving boats**
- **9.4% fewer people arriving**
- **49.7% more people per boat**

These values must be calculated from the existing data before rounding. The central message is that boat counts alone give an incomplete picture of recorded arrivals. Occupancy does not establish vessel capacity, safety, or the cause of route changes.

## Visual direction

- Deep navy, warm white and vivid teal; amber reserved for hypothetical scenarios. Extend existing semantic theme tokens and verify contrast in both themes.
- A continuous Channel map with concise editorial headlines and figures integrated into supporting overlays. Use responsive typography that preserves user font scaling.
- Open, predominantly borderless compositions. Use borders and surfaces where they help identify controls or separate evidence.
- Keep one map visible from the opening, reframing it as the story moves from Dover–Calais to the wider Channel and Portsmouth.
- A compact header with chapter access, reading progress and discoverable display preferences. Keep primary reading content visually dominant.
- Short scroll-triggered transitions and restrained depth. No wheel interception, forced scrolling or continuous decorative motion.
- Mobile-specific layouts with inline graphics and natural reading order. A sticky visual must never consume the available reading area on a short screen.
- Reduced-motion mode presents equally clear static compositions. Narration remains optional and user-initiated.

## Phase 1 — Foundation and opening

### Work

1. Audit the existing design tokens, typography, preferences, story state and explorer layout.
2. Separate the current explorer shell from the new story entry point while reusing its data, charts and map components. Choose one navigation mechanism and preserve browser back/forward behaviour.
3. Define the editorial type scale, semantic colours, spacing, graphic styles and motion defaults. Document them in the existing design system.
4. Build the map-led opening and supporting 2022–2025 comparison: strong headline, integrated evidence, year labels and a clear invitation to scroll.
5. Add direct access to the explorer, sources and display preferences.

### Acceptance

- The opening communicates the central question without requiring a tab selection.
- Desktop and mobile compositions feel deliberate; no horizontal overflow at supported font sizes.
- Both themes, visible keyboard focus and reduced-motion behaviour work.
- The existing explorer remains usable.

**First reviewable milestone:** the opening and comparison, fully styled and responsive, establishes the visual direction before the full story is built.

## Phase 2 — Scroll-driven narrative

### Work

Implement these sections in normal document flow:

| Section | Main message | Primary visual |
| --- | --- | --- |
| The Channel | What does counting boats miss? | Wide Channel map |
| A different scale | 2018 averaged about seven people per boat | Small filled boat, people and boat totals |
| More people per boat | 2025 averaged about 62 people per boat | Small and large filled boats alongside Dover–Calais |
| Beyond boat counts | Boats fell much faster than arrivals in 2022–2025 | Comparison bars and occupancy increase |
| Farther west | A reported Portsmouth case adds geographic context | Both connections, provisional totals and separate dates |
| The bigger question | Read people, boats and occupancy together | Wide map and exploration invitation |

Use one fixed map behind short sections. On mobile, leave geographic space above each readable text surface and place evidence after its explanation. Keep the complete annual series in the explorer rather than adding nine mandatory stops.

Create a declarative section model that maps section IDs to copy, evidence, visual state and eventual narration. Use section visibility to update visual state and reading progress without controlling scroll position. Preserve a meaningful static reading order if visual enhancements fail.

### Acceptance

- Each section has one clear focal point and explanatory purpose.
- Chapter anchors, direct links and browser history remain predictable.
- Readers can reach the explorer without completing the story.
- No essential explanation is hidden behind a mobile notes toggle.

## Phase 3 — Animated data graphics

### Work

1. Use brief evidence-entry and comparison-bar transitions; keep numeric values stable and readable.
2. Build differently sized, densely filled boat illustrations for 2018 and 2025. Use equal-coordinate-size dots and exact rounded occupancy counts. Clearly label hull size as illustrative, not measured dimensions or rated capacity.
3. Present the longer-term comparison in reading order and make the full annual chart available in the explorer.
4. Define re-entry behaviour: reverse scrolling restores the appropriate visual state without repeatedly replaying long animations.
5. Keep final values accessible and avoid announcing every intermediate counter value to screen readers.

### Acceptance

- Animation makes a specific comparison easier to understand.
- Exact values, denominators and dates remain available throughout.
- Reduced-motion mode removes nonessential movement without hiding information.
- Scrolling remains smooth on representative mobile devices. The subsequently approved Dover route loop has a visible pause control and stops for reduced motion and hidden tabs.

## Phase 4 — Geographic chapter

### Work

1. Introduce the map immediately, using restrained camera transitions to connect each chapter to its geography.
2. Reuse one map instance where practical rather than creating a WebGL canvas for every section.
3. For 2026, show both indicative Calais–Dover context and the reported Utah Beach–Portsmouth endpoint connection.
4. Keep the provisional totals' 3 September cutoff distinct from the later 6 September case.
5. Keep the reading map non-interactive so scrolling remains predictable; link to the selected year in the fully controlled explorer and provide route explanations in HTML.

### Acceptance

- A drawn line is explicitly identified as indicative context or reported endpoints, never a recorded vessel track.
- No animated boat suggests an observed voyage, direction, speed or repeated traffic unsupported by the evidence.
- The single reported case is not presented as proof of a widespread route shift.
- Full-map interaction and map-failure behaviour work on desktop and mobile.

## Phase 5 — Narration and optional exploration

### Work

1. Define explicit reading and listening modes so scrolling and the playback clock do not compete.
2. Map six compatible existing recordings to the new sequence. Display their full transcript alongside abridged editorial copy. Bespoke recording revisions remain a future editorial pass; no regeneration is required for this implementation.
3. Provide an inline transcript and AI-generated voice disclosure using the existing accessible controls and preferences.
4. During listening, manual section navigation pauses audio and selects the new section. Resuming begins the appropriate recording; it must not continue a stale clip.
5. Preserve pause/resume, restart, failure recovery, cached audio and compatible-manifest checks.
6. Keep the current map/chart explorer, complete data table, sources and hypothetical scenarios available after the guided takeaway and through a shortcut.

### Acceptance

- Audio never starts solely because a reader scrolls or loads the page.
- Narration text matches the active section, including dates and evidence qualifications.
- Keyboard users can operate transport and transcript controls.
- Scenarios are clearly optional and hypothetical, not the factual conclusion.

## Phase 6 — Polish and validation

### Work

1. Refine visual rhythm, transitions, touch controls and loading/error states.
2. Test light/dark themes, keyboard reading order, contrast, enlarged text, narrow reflow and reduced motion.
3. Check desktop browsers and mobile Safari/Chrome. Distinguish browser emulation from testing on actual devices in the validation record.
4. Test navigation between story and explorer, narration interruption, cached playback, direct links and map failure.
5. Run the existing data, narration, unit, build and browser checks; update tests meaningfully for the new navigation model.
6. Update architecture, design-system, accessibility and narration documentation to match the final implementation.
7. Conduct a short comprehension test with a mix of desktop and mobile readers, including original reviewers where possible.

### Acceptance

- Readers can explain why the change in boat counts differs from the change in people arriving.
- Readers can distinguish annual evidence, the Portsmouth endpoint report and hypothetical scenarios.
- Suggested prototype target: four of five readers explain the central comparison without prompting. This is a design decision aid, not statistical proof.
- Required automated checks pass; manual verification and any remaining limitations are documented. Automated checks alone do not establish complete WCAG conformance.

## Delivery and release

- Complete each phase as a reviewable local increment on `feat/scroll-story-ux`.
- Keep source calculations and evidence qualifications intact while changing presentation.
- Preserve the explorer during migration; do not remove its capabilities merely to simplify the new story.
- Record significant design decisions and validation after each phase.
- Integrate completed work into local `internal_main`, then follow [the current release workflow](../release-workflow.md) through local `release_to_main` to published `main`.
- Do not push development branches. This plan does not authorize a deployment or release.

## Current status

Mobile narration now reveals the active text progressively from audio time updates: after a short opening hold, the page (or the Portsmouth panel's internal scroll area) moves until the remaining copy clears the timeline. Manual scrolling pauses narration, and reduced-motion mode disables this continuous reveal. Mobile panel backgrounds are translucent in both themes, with text shadows for separation from the map.

### Optional scenario chapter

Added “What happens next?” after the factual takeaway, with arriving-boat and occupancy sliders, a modelled total and a filled occupancy illustration. Defaults reuse the existing continuation assumptions: 670 × 62 = 41,540. A wider-connections checkbox switches the map from Calais–Dover to the four existing hypothetical connections, including Utah Beach–Portsmouth, Dieppe–Brighton and Dunkirk–Dover.

Scenario lines, boat symbols and evidence use amber and explicit hypothetical labels. Boat assumptions select a small illustrative symbol count per connection; zero boats hides symbols. Occupancy adjusts symbol/illustration size. No totals are allocated to routes. When the factual takeaway finishes playing, listening stops and the page scrolls to “What happens next?”. Narration is disabled in this adjustable section to avoid stale narrated assumptions. Manual pause does not trigger that transition. The full explorer remains available.

### Route movement amendment

Implemented the approved illustrative boat animation in the editorial map. Four staggered boat symbols move Calais → Dover from the first evidence chapter onward. The 2026 chapters add one Utah Beach → Portsmouth symbol, which completes once and remains at the endpoint; only an explicit replay restarts it. Counts, speeds and durations are display choices, not traffic measurements. The visible motion panel states this qualification.

Pause/play is independent of narration and preserves position. Reduced motion presents static symbols; hidden tabs suspend the shared animation loop without accumulating elapsed time. The opening has no moving boats. Markers follow shared connection coordinates and rotate with the projected direction. The existing explorer is unchanged.

From 2025 onward, chapters apply three successive user-requested 50% speed increases: 3.375× Dover animation speed (about 5.33 seconds per illustrative traversal instead of 18). Earlier years retain baseline pacing; Portsmouth remains a 24-second, single illustrative journey. The visible label distinguishes animation speed from measured vessel speed.

Route implementation validation: direction, looping, one-way completion and year-specific pacing have unit coverage. The initial route build passed; desktop/mobile browser checks timed out before markers appeared, so visual interaction verification remains incomplete.

Implemented locally on `feat/scroll-story-ux`:

- Phases 1–4: new story entry, responsive editorial foundation, six sections, section-driven map, filled boat illustrations, comparison evidence and Portsmouth context.
- Phase 5: six existing recordings mapped to sections, optional listening with interruption, full inline transcripts and links to the preserved explorer. No new recordings or API calls.
- Phase 6: desktop/mobile screenshot review and six new browser checks pass, including both themes with axe, map failure, enlarged text and listening interruption. Data, narration, formatting, 41 unit tests and the production build pass. The full browser run encountered loading/narration timing failures and was interrupted; it is not a passing full regression result.
- Follow-up: compact desktop headings and spacing keep the Portsmouth evidence, cutoff note and source link above the fixed timeline. A focused browser regression passes at 1806×870 and 1366×768, with screenshot review.

The approved preview amendments supersede the earlier figure-led opening: the map is the persistent visual stage and both illustrated boats are densely filled. Source records, cutoff dates and route qualifications remain unchanged.

Not yet performed: physical-device/Safari testing, comprehensive assistive-technology review, bespoke narration voice review and the proposed reader-comprehension study. No release, merge or push is included in this implementation.
