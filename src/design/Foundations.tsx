import { useState } from "react";
const colors = [
  "bg",
  "panel",
  "surface",
  "text",
  "muted",
  "accent",
  "accent-surface",
  "scenario",
  "scenario-surface",
  "line",
  "focus",
] as const;
export function Foundations() {
  const [sample, setSample] = useState(false);
  return (
    <div className="foundation-guide">
      <p className="lead">Channel / Foundations v1.0</p>
      <p>
        A shared visual language for the story, the map and the evidence. This
        preview uses the same tokens as the application and responds to your
        theme and text settings.
      </p>
      <h3>01 · Semantic colour</h3>
      <div className="swatch-grid">
        {colors.map((token) => (
          <div key={token}>
            <span
              className="swatch"
              style={{ background: `var(--${token})` }}
            />
            <code>--{token}</code>
          </div>
        ))}
      </div>
      <h3>02 · Typography</h3>
      <p className="type-display">People behind every number.</p>
      <p className="type-body">
        DM Sans / body, controls and data. Manrope / headings and key figures.
      </p>
      <p className="eyebrow">LABEL / CONTEXT / PROVENANCE</p>
      <p>
        Body scale: 12, 14, 16, 20 and 28 px at 100%. All text scales with the
        100–200% size controls. Browser zoom remains available.
      </p>
      <h3>03 · Spacing & shape</h3>
      <div className="spacing-samples">
        {[1, 2, 3, 4, 6, 8].map((size) => (
          <div key={size}>
            <span style={{ width: `var(--space-${size})` }} />
            <code>{size * 4}px</code>
          </div>
        ))}
      </div>
      <p>4 px spacing unit · 5 / 10 px radii · 44 px primary controls.</p>
      <h3>04 · Elements & states</h3>
      <div className="component-samples">
        <button
          className="primary-button"
          onClick={() => setSample(!sample)}
          aria-pressed={sample}
        >
          {sample ? "Selected state" : "Primary action"}
        </button>
        <button className="outline-button" disabled>
          Disabled action
        </button>
        <span className="evidence-tag">Historical evidence</span>
        <span className="evidence-tag scenario-tag">
          Scenario · not a forecast
        </span>
      </div>
      <label className="sample-input">
        Example field
        <input placeholder="Source or claim ID" />
      </label>
      <p>
        Visible focus rings, labelled controls, native dialogs and status text.
        Meaning never relies on colour alone.
      </p>
      <h3>05 · Accessibility contract</h3>
      <p>
        Target: WCAG 2.2 AA. Normal text ≥ 4.5:1, large text ≥ 3:1; control
        boundaries and focus indicators ≥ 3:1. Autoplay starts only on request
        and can always be paused. Enlarged text and narrow windows reflow
        instead of clipping content.
      </p>
    </div>
  );
}
