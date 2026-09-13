import { modelArrivals, type Scenario } from "../scenarios/model";
import { formatNumber } from "../data/model";
import { BoatIllustration } from "./BoatIllustration";

export function StoryScenario({
  value,
  onChange,
}: {
  value: Scenario;
  onChange: (value: Scenario) => void;
}) {
  return (
    <>
      <p className="editorial-scenario-badge">SCENARIO · NOT A FORECAST</p>
      <h2 id="scenarios-title">
        Change the inputs.
        <br />
        <em>Explore the possibilities.</em>
      </h2>
      <p className="editorial-body">
        An optional exploration. Start with rounded assumptions near 2025;
        change boats or occupancy to see how the total changes.
      </p>
      <div className="editorial-scenario-inputs">
        <label>
          Assumed arriving boats <strong>{formatNumber(value.boats)}</strong>
          <input
            type="range"
            min="0"
            max="1500"
            step="10"
            value={value.boats}
            onChange={(event) =>
              onChange({ ...value, boats: Number(event.target.value) })
            }
          />
        </label>
        <label>
          Average people per boat <strong>{value.occupancy}</strong>
          <input
            type="range"
            min="1"
            max="150"
            step="1"
            value={value.occupancy}
            onChange={(event) =>
              onChange({ ...value, occupancy: Number(event.target.value) })
            }
          />
        </label>
        <label className="editorial-scenario-wider">
          <input
            type="checkbox"
            checked={value.footprint === "wider"}
            onChange={(event) =>
              onChange({
                ...value,
                footprint: event.target.checked ? "wider" : "strait",
              })
            }
          />
          Explore wider connections
        </label>
      </div>
      <div className="editorial-scenario-result">
        <div>
          <span>MODELLED PEOPLE ARRIVING</span>
          <output aria-live="polite">
            {formatNumber(modelArrivals(value))}
          </output>
          <p>
            {formatNumber(value.boats)} boats × {value.occupancy} people per
            boat
          </p>
        </div>
        <BoatIllustration people={value.occupancy} year="Assumed" />
      </div>
      <p className="editorial-caption">
        Hypothetical connections—not predicted routes or recorded journeys.
        Symbols illustrate assumptions, not route-level totals. Boat size
        illustrates occupancy, not measured dimensions.
      </p>
    </>
  );
}
