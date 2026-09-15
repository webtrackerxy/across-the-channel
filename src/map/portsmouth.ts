// Representative points from the research gazetteer (Utah-Beach hamlet, Eastney suburb), not landing coordinates.
// User requested this reported case; the independent research review remains pending.
export const portsmouthCase = {
  date: "2026-09-06",
  /** French maritime prefecture notice (claim VES-PREMAR-2026-09-SEINE). */
  peopleAboard: 140,
  /** BBC News, 7 September 2026 (claim VES-UTAH-PORTSMOUTH-2026). */
  reportedHours: 10,
  coordinates: [
    [-1.174703, 49.415666],
    [-1.047632, 50.787241],
  ] as [number, number][],
  sources: [
    {
      title: "BBC News · Eastney Landing, about 10 hours, 7 September 2026",
      url: "https://www.bbc.co.uk/news/articles/crl60z17lyko",
    },
    {
      title: "ICI / AFP · reported Utah Beach departure, 7 September 2026",
      url: "https://www.ici.fr/normandie/manche-50/les-140-migrants-partis-de-la-manche-sont-arrives-en-angleterre-ou-une-manifestation-a-eclate-8847927",
    },
    {
      title:
        "French maritime prefecture · assistance west of the Bay of Seine, 6 September 2026",
      url: "https://www.premar-manche.gouv.fr/communiques-presse/operation-d-assistance-d-une-embarcation-de-migrants-a-l-ouest-de-la-baie-de-seine",
    },
    {
      title: "ITV Meridian · RNLI landing at Eastney Marina, 9 September 2026",
      url: "https://www.itv.com/news/meridian/2026-09-09/southampton-and-portsmouth-ports-declined-request-to-land-migrants-in-rnli-boat",
    },
  ],
};
export function portsmouthFeatures(endpoints = false) {
  const coordinates = portsmouthCase.coordinates;
  return endpoints
    ? {
        type: "FeatureCollection" as const,
        features: coordinates.map((point) => ({
          type: "Feature" as const,
          properties: {},
          geometry: { type: "Point" as const, coordinates: point },
        })),
      }
    : {
        type: "FeatureCollection" as const,
        features: [
          {
            type: "Feature" as const,
            properties: {},
            geometry: { type: "LineString" as const, coordinates },
          },
        ],
      };
}
