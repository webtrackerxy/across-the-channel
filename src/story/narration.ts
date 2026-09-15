import { byYear, changePercent, formatNumber, occupancy } from "../data/model";
import { modelArrivals, presets } from "../scenarios/model";
import { playbackFrames, type PlaybackFrame } from "./playback";
import { scenes } from "./scenes";
import { portsmouthCase } from "../map/portsmouth";
import { conclusion } from "./conclusion";

const spokenText = (text: string) =>
  text
    .replace(/people\s*\/\s*boat/gi, "people per boat")
    .replace(/\s+/g, " ")
    .trim();

const spokenDate = (date: string) =>
  new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    timeZone: "UTC",
  }).format(new Date(`${date}T00:00:00Z`));

/** Text for the fixed story steps; manual scenario edits are not narrated. */
export function narrationFor(frame: PlaybackFrame): string {
  const scene = scenes[frame.sceneIndex];
  if (!scene) throw new Error(`Unknown scene ${frame.sceneIndex}`);
  const opening = spokenText(`${scene.title} ${scene.body}`);
  if (frame.closing) {
    const summary = conclusion();
    return `What we know. ${summary.known} Open questions. ${summary.openQuestions} ${summary.invitation} ${summary.question}`;
  }

  switch (scene.id) {
    case "context":
      return opening;
    case "occupancy": {
      const record = byYear(frame.year);
      const period = record.partial
        ? ` From ${spokenDate(record.periodStart)} to ${spokenDate(record.periodEnd)}${record.provisional ? ", provisional" : ""}. These totals are not comparable with full years.`
        : record.provisional
          ? " Provisional."
          : "";
      const route =
        record.year === 2026
          ? ` The map shows the indicative Calais to Dover connection and a reported Utah Beach to Portsmouth connection. The separate ${spokenDate(portsmouthCase.date)} case falls after these totals' reporting cutoff. About ${portsmouthCase.peopleAboard} people were aboard, according to the French maritime prefecture, and the BBC reported the crossing to Portsmouth took about ${portsmouthCase.reportedHours} hours. The boat's size was not reported. The Portsmouth line links reported endpoints, not a recorded vessel track.`
          : "";
      const figures = `${record.year}. ${formatNumber(record.people)} people arrived on ${formatNumber(record.boats)} boats, averaging ${occupancy(record).toFixed(1)} people per boat.${period}${route}`;
      const firstYear = playbackFrames.find(
        (item) => item.sceneIndex === frame.sceneIndex,
      )?.year;
      return frame.year === firstYear ? `${opening} ${figures}` : figures;
    }
    case "comparison": {
      const before = byYear(2022);
      const after = byYear(2025);
      const change = (value: number) =>
        `${value < 0 ? "fell" : "rose"} by ${Math.abs(value).toFixed(1)} percent`;
      return `${opening} From ${before.year} to ${after.year}, arriving boats ${change(changePercent(before.boats, after.boats))}, while people arriving ${change(changePercent(before.people, after.people))}. Average people per boat ${change(changePercent(occupancy(before), occupancy(after)))}. Occupancy does not establish vessel capacity or the routes travelled.`;
    }
    case "scenarios": {
      if (!frame.preset || !Object.hasOwn(presets, frame.preset))
        throw new Error("Narration requires a known scenario preset");
      const preset = presets[frame.preset];
      const text = `${preset.label}: a hypothetical scenario, not a forecast. ${preset.description} Assuming ${formatNumber(preset.boats)} arriving boats and ${formatNumber(preset.occupancy)} people per boat gives ${formatNumber(modelArrivals(preset))} modelled arrivals. The map shows hypothetical connections, not recorded vessel tracks.`;
      return frame.preset === "low" ? `${opening} ${text}` : text;
    }
  }
}

export function narrationTranscript(): string {
  return (
    [
      "# Narration transcript",
      "Generated from the current application data and story presets. This is the text used for narration recordings. Regenerate the transcript and affected audio after data or wording changes.",
      ...playbackFrames.map((frame, index) => {
        const label = frame.closing
          ? "Conclusion"
          : frame.preset
            ? presets[frame.preset].label
            : String(frame.year);
        return `## Step ${index + 1} — ${scenes[frame.sceneIndex].label} (${label})\n\n${narrationFor(frame)}`;
      }),
    ].join("\n\n") + "\n"
  );
}
