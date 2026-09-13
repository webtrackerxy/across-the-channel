import { useState, useId } from "react";
import { ArrowUpRight } from "lucide-react";
import {
  records,
  metricValue,
  metricLabels,
  formatNumber,
  type Metric,
} from "../data/model";

interface Props {
  selectedYear: number;
  onYearChange: (year: number) => void;
  onSource: () => void;
  selectionHint?: string;
}
export function HistoryChart({
  selectedYear,
  onYearChange,
  onSource,
  selectionHint = "Select a year to update the story.",
}: Props) {
  const titleId = useId();
  const [metric, setMetric] = useState<Metric>("occupancy");
  const max = Math.max(...records.map((record) => metricValue(record, metric)));
  return (
    <section className="history-panel" aria-labelledby={titleId}>
      <div className="history-heading">
        <div>
          <h2 id={titleId}>Year by year</h2>
        </div>
        <div className="metric-tabs" aria-label="Chart metric">
          {(["people", "boats", "occupancy"] as Metric[]).map((item) => (
            <button
              key={item}
              aria-pressed={metric === item}
              onClick={() => setMetric(item)}
            >
              {item === "people"
                ? "People"
                : item === "boats"
                  ? "Boats"
                  : "People / boat"}
            </button>
          ))}
        </div>
      </div>
      <div
        className="bar-chart"
        role="group"
        aria-label={`${metricLabels[metric]} by year. ${selectionHint}`}
      >
        <div className="chart-grid" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
        {records.map((record) => {
          const value = metricValue(record, metric);
          return (
            <button
              className={`bar-column ${record.year === selectedYear ? "selected" : ""} ${record.partial ? "partial" : ""}`}
              key={record.year}
              onClick={() => onYearChange(record.year)}
              aria-pressed={record.year === selectedYear}
              aria-label={`${record.year}${record.partial ? " January to 3 September, provisional" : ""}: ${metric === "occupancy" ? value.toFixed(2) : formatNumber(value)} ${metricLabels[metric].toLowerCase()}`}
            >
              <span className="bar-track">
                <span
                  className="bar"
                  style={{ height: `${(value / max) * 100}%` }}
                >
                  <span className="bar-value">
                    {metric === "occupancy"
                      ? value.toFixed(1)
                      : value >= 10000
                        ? `${(value / 1000).toFixed(1)}k`
                        : formatNumber(value)}
                  </span>
                </span>
              </span>
              <span className="bar-year">
                {record.year}
                {record.partial && <small> YTD*</small>}
              </span>
            </button>
          );
        })}
      </div>
      <div className="chart-footnote">
        <span>
          <span className="legend-dot" /> Zero baseline · calculated occupancy{" "}
          <span className="partial-key">▧ 2026 is a partial year</span>
        </span>
        <button className="text-link" onClick={onSource}>
          Source & calculation <ArrowUpRight size={14} />
        </button>
      </div>
      <p className="chart-caveat">
        * 2026 covers 1 January–3 September and is provisional. Totals are not
        comparable with full years. Occupancy ≠ rated capacity.
      </p>
    </section>
  );
}
