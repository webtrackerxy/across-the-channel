import { useEffect, useRef } from "react";
import { X, ExternalLink, BookOpen } from "lucide-react";
import {
  sources,
  occupancy,
  formatNumber,
  periodLabel,
  type CrossingRecord,
} from "../data/model";

export function EvidenceDialog({
  open,
  record,
  onClose,
}: {
  open: boolean;
  record: CrossingRecord;
  onClose: () => void;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const dialog = ref.current;
    if (open && !dialog?.open) dialog?.showModal();
    if (!open && dialog?.open) dialog.close();
  }, [open]);
  const source = sources.find((item) => item.id === record.sourceId)!;
  return (
    <dialog
      className="evidence-dialog"
      ref={ref}
      onCancel={onClose}
      onClose={onClose}
      onClick={(event) => {
        if (event.target === ref.current) onClose();
      }}
      aria-labelledby="evidence-title"
    >
      <div className="dialog-inner">
        <header>
          <span className="eyebrow">
            <BookOpen size={15} /> BEHIND THE NUMBERS
          </span>
          <button
            className="icon-button"
            aria-label="Close sources"
            onClick={onClose}
          >
            <X size={21} />
          </button>
        </header>
        <h2 id="evidence-title">Evidence, made visible.</h2>
        <p>
          Every number has an origin. Estimates stay separate from observations.
        </p>
        <div className="evidence-calculation">
          <span>{periodLabel(record)}</span>
          <strong>
            {formatNumber(record.people)} ÷ {formatNumber(record.boats)} ={" "}
            {occupancy(record).toFixed(2)}
          </strong>
          <p>People arriving ÷ boats arriving = average people per boat</p>
        </div>
        <span className="evidence-pill">
          {record.provisional ? "PROVISIONAL COUNTS" : "OFFICIAL ANNUAL COUNTS"}{" "}
          · DERIVED AVERAGE
        </span>
        <h3>Source for {record.year}</h3>
        <a
          className="source-title"
          href={source.url}
          target="_blank"
          rel="noreferrer"
        >
          {source.title}
          <ExternalLink size={16} />
        </a>
        <p className="source-meta">
          {source.publisher} · Published {source.publishedAt}
          <br />
          {source.table}
        </p>
        <p>{source.note}</p>
        <h3>What the data can tell us</h3>
        <p>
          These are detected arrivals, including people rescued or intercepted
          at sea and brought to the UK. They exclude undetected arrivals and
          people returned to France by French authorities. Occupancy describes
          an average, not every boat or a certified vessel capacity.
        </p>
        <h3>Research status</h3>
        <p>
          Source-checked for this MVP on 11 September 2026. Independent research
          review remains pending. Vessel size, engine range and longer-route
          causation are not established by these counts.
        </p>
        <h3>Map & scenarios</h3>
        <p>
          Map labels are approximate reference locations. Historical tracks are
          not reconstructed. Dashed 3D arcs are hypothetical connections; their
          height and placement are illustrative, not distance or range
          measurements.
        </p>
        <a
          className="text-link"
          href="https://www.naturalearthdata.com/about/terms-of-use/"
          target="_blank"
          rel="noreferrer"
        >
          Natural Earth · public-domain base geography{" "}
          <ExternalLink size={14} />
        </a>
        <details>
          <summary>All statistical sources</summary>
          {sources.map((item) => (
            <p key={item.id}>
              <a href={item.url} target="_blank" rel="noreferrer">
                {item.title}
              </a>
              <br />
              <small>
                Published {item.publishedAt} · {item.table}
              </small>
            </p>
          ))}
        </details>
      </div>
    </dialog>
  );
}
