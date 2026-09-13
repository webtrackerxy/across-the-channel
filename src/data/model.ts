import raw from "./crossings.json";

export interface CrossingRecord {
  year: number;
  people: number;
  boats: number;
  periodStart: string;
  periodEnd: string;
  partial: boolean;
  provisional: boolean;
  sourceId: string;
  claimId: string;
}

export const records: CrossingRecord[] = raw.records;
export const sources = raw.sources;
export const metadata = {
  updatedAt: raw.updatedAt,
  reviewStatus: raw.reviewStatus,
};
export const formatNumber = (value: number) =>
  new Intl.NumberFormat("en-GB").format(value);
export function occupancy(
  record: Pick<CrossingRecord, "people" | "boats">,
): number {
  if (
    !Number.isFinite(record.people) ||
    record.people < 0 ||
    !Number.isFinite(record.boats) ||
    record.boats <= 0
  ) {
    throw new Error(
      "Occupancy requires a non-negative people count and a positive boat count.",
    );
  }
  return record.people / record.boats;
}
export function changePercent(before: number, after: number): number {
  if (
    !Number.isFinite(before) ||
    before <= 0 ||
    !Number.isFinite(after) ||
    after < 0
  )
    throw new Error("Invalid comparison");
  return (after / before - 1) * 100;
}
export const byYear = (year: number): CrossingRecord => {
  const record = records.find((item) => item.year === year);
  if (!record) throw new Error(`Unknown year ${year}`);
  return record;
};
export type Metric = "people" | "boats" | "occupancy";
export const metricValue = (record: CrossingRecord, metric: Metric) =>
  metric === "occupancy" ? occupancy(record) : record[metric];
export const metricLabels: Record<Metric, string> = {
  people: "People arriving",
  boats: "Boats arriving",
  occupancy: "People per boat",
};
const shortDate = (date: string) =>
  new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "short",
    timeZone: "UTC",
  }).format(new Date(`${date}T00:00:00Z`));
export const periodLabel = (record: CrossingRecord) =>
  record.partial
    ? `${shortDate(record.periodStart)}–${shortDate(record.periodEnd)} ${record.year}${record.provisional ? " · provisional" : ""}`
    : `Full year ${record.year}`;
