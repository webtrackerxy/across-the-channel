# UX improvement proposal: a guided Channel crossings story

Execution plan: [Modern UI implementation plan](MODERN_UI_IMPLEMENTATION_PLAN.md), incorporating the user's modern editorial design direction and six delivery phases.

Status: original feedback proposal; the linked implementation plan records the subsequent approved map-led design and implementation. Local branch: `feat/scroll-story-ux`, created from `internal_main` at `a91eb91`. Follow the current internal release workflow: work branches stay local; only `main` is published through `release_to_main`.

## What the feedback tells us

The comments are a small qualitative sample, including desktop and mobile readers, not a usability study. They identify four useful problems:

| Feedback | Interpretation | Proposed response |
| --- | --- | --- |
| The facts need a clearer focus; readers do not know where to look | Several panels compete for attention before the central claim is established | Lead with a single question and reveal one comparison at a time |
| Figures should be larger | The main evidence lacks visual priority | Use large, labelled numbers with the year and denominator immediately beside them |
| Scroll through the storyline rather than using four tabs | The current interface asks readers to assemble the argument themselves | Make natural page scrolling the primary reading path; retain chapter links for shortcuts |
| Add counters, dashed-line animation and parallax; the design feels generic | Readers want stronger editorial direction and movement | Introduce a distinctive visual language and animate meaningful changes only |

The strongest recommendation is to improve narrative structure first. The comments do not establish a requirement for a 3D game. Treat the cited news graphics as references for editorial pacing, not as a request to copy a particular publication.

## Proposed central message

**Fewer boats can still carry nearly as many people.**

Opening question: **What does counting boats miss?**

Use the 2022–2025 comparison as the opening evidence: arriving boats fell 39.5%, people arriving fell 9.4%, and average people per boat rose 49.7%. Explain that these are recorded arrivals; occupancy is not rated vessel capacity. This answers the focus question without asserting that occupancy caused longer routes or establishing any policy conclusion.

## Reading sequence

1. **The surprise.** Show 1,110 boats in 2022 and 672 in 2025, then reveal that recorded arrivals fell from 45,774 to 41,472. The main visual here is a comparison chart, not a map.
2. **What boat counts miss.** Make the rise from 41.2 to 61.7 people per boat the dominant figure. Show all three changes together only after the individual measures are understood. Label each denominator clearly.
3. **The longer view.** Progress from 2018 through 2025 with a simple occupancy graphic and an annotated trend. Offer the complete annual chart and data table for exploration. Avoid forcing nine full-screen stops.
4. **Geography adds another question.** Introduce the map here. In the 2026 section, show both indicative Dover context and the reported Utah Beach–Portsmouth endpoints. Keep the 3 September statistical cutoff visible and distinguish the later 6 September case. State that the connection is not a recorded vessel track and does not establish a widespread route shift.
5. **The takeaway.** Restate why people, boats and occupancy must be read together. Put optional hypothetical scenarios behind an explicit “Explore assumptions” invitation, followed by sources and limitations. Scenarios should not serve as the factual conclusion.

## Layout and interaction

- **Desktop:** one sticky visual beside short paragraphs in the normal document flow. Each paragraph advances the highlighted evidence. Bring the map forward only in the geography section. Provide compact chapter anchors and a visible reading-progress indicator.
- **Mobile:** use an inline, single-column article with a visual directly after the sentence it explains. Limit sticky graphics on short screens; essential text must not be hidden behind a “Read chapter” toggle. Show the same narrative and caveats as desktop.
- **Numbers:** approximately 48–72 px hero figures on desktop and 36–48 px on mobile as starting design values, with responsive sizing and user font scaling. Keep labels legible, not oversized numerals beside tiny explanations. Use one dominant figure per scene.
- **Controls:** group display preferences in a compact, labelled control. Keep sources and data easy to reach; move design-foundation tooling away from the reader's primary path. Accessibility must be built into ordinary reading, not depend on discovering a toolbar.
- **Exploration:** retain the existing chart, map expansion and scenario controls as a secondary explorer after the guided story. Natural document scrolling becomes the default; the earlier single-screen requirement applies to the explorer rather than the whole article.

## Motion and narration

- Animate bars and transitions between the two comparison years once on entry. A short numeric interpolation can reinforce the change, but the stable final value and label must always be available. Do not announce every animated intermediate number to screen readers.
- Draw an endpoint connection once when introducing geography. Avoid continuously travelling boat markers or marching route dashes: they can imply an observed path, direction, speed or repeated traffic that the evidence does not establish.
- Try restrained depth or parallax only after the story works without it. Do not intercept the mouse wheel, force scroll snapping or lock readers into animated sequences.
- Respect reduced-motion preferences and retain a static reading experience. W3C documents [how to prevent nonessential motion with prefers-reduced-motion](https://www.w3.org/WAI/WCAG21/Techniques/css/C39); interaction-animation criterion 2.3.3 is AAA, an additional design safeguard rather than a new claim of AA compliance.
- Keep narration optional and user-initiated. Offer “Read by scrolling” and “Listen to the story” as clear modes. Manual scrolling during guided audio should pause it and select the new section; it must not fight the playback clock. Rewrite the narration for the new sequence before regenerating clips.

## Order of implementation

1. **Narrative prototype:** build the opening comparison and occupancy explanation as a static scrollable page. Reuse approved data and calculations. Test whether readers can state the central message before adding animation.
2. **Responsive story:** implement the complete reading sequence, large figures, chapter anchors and accessible static fallbacks. Keep the existing explorer available.
3. **Purposeful motion:** add section-triggered chart transitions and bounded map transitions. Reuse the current map instance; avoid a WebGL canvas for every section.
4. **Narration integration:** map the new sections to playback, transcript and pause behaviour; regenerate only changed recordings after text review.
5. **Validation:** test keyboard reading order, reduced motion, font scaling, mobile Safari/Chrome, desktop, map failure and cached narration. Review contrast and reflow; an automated accessibility pass does not establish complete conformance.

## How to judge improvement

Run a short test with a small mix of desktop and mobile readers, including the original reviewers where possible. Ask them to explain the main finding in their own words, identify the largest change, and distinguish the Portsmouth endpoint report from the annual totals and hypothetical scenarios. Observe where they hesitate or lose their place.

Suggested first-round target: at least four of five readers can explain the boats/people/occupancy distinction without prompting. Treat this as a prototype decision aid, not statistical proof. Prioritize comprehension and successful navigation over time on page or animation engagement.
