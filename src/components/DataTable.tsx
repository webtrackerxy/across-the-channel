import { records, occupancy, formatNumber } from "../data/model";

export function downloadData() {
  const rows = [
    "year,period_start,period_end,people,boats,average_people_per_boat,provisional,source_id",
    ...records.map((r) =>
      [
        r.year,
        r.periodStart,
        r.periodEnd,
        r.people,
        r.boats,
        occupancy(r).toFixed(6),
        r.provisional,
        r.sourceId,
      ].join(","),
    ),
  ];
  const url = URL.createObjectURL(
    new Blob([rows.join("\n")], { type: "text/csv;charset=utf-8" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = "channel-crossings-2018-2026.csv";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
export function DataTable({ onSource }: { onSource: (year: number) => void }) {
  return (
    <>
      <button className="download-button" onClick={downloadData}>
        Download CSV
      </button>
      <div
        className="table-scroll"
        tabIndex={0}
        role="region"
        aria-label="Crossings data table, scroll horizontally on small screens"
      >
        <table>
          <caption>
            Recorded arrivals and calculated occupancy, 2018–2026
          </caption>
          <thead>
            <tr>
              <th scope="col">Period</th>
              <th scope="col">People arriving</th>
              <th scope="col">Boats</th>
              <th scope="col">People / boat</th>
              <th scope="col">Evidence</th>
            </tr>
          </thead>
          <tbody>
            {records.map((r) => (
              <tr key={r.year}>
                <th scope="row">
                  {r.year}
                  {r.partial && " Jan–3 Sep*"}
                </th>
                <td>{formatNumber(r.people)}</td>
                <td>{formatNumber(r.boats)}</td>
                <td>{occupancy(r).toFixed(2)}</td>
                <td>
                  <button
                    className="text-link"
                    aria-label={`View ${r.year} source`}
                    onClick={() => onSource(r.year)}
                  >
                    {r.provisional ? "Provisional" : "Home Office"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="chart-caveat">
        * 2026 covers 1 January–3 September, is provisional and is not
        comparable with full years. Averages are people ÷ boats, not rated
        capacity.
      </p>
    </>
  );
}
