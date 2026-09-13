# MVP data and asset provenance

## Statistics

1. [Home Office summary tables, year ending June 2026](https://assets.publishing.service.gov.uk/media/6a8c11c3a8f84a582b84281a/illegal-entry-routes-to-the-uk-summary-jun-2026-tables.ods), published 27 August 2026, IER_02a. Used for 2018–2025 annual counts. Open Government Licence v3.0 except where otherwise stated.
2. [Home Office daily time series, 4 September 2026](https://assets.publishing.service.gov.uk/media/6a9a9e583b22fb169dc1921b/04_September_2026_Small_boats_-_time_series.ods), SB_01. Sum of 246 daily records, 1 January–3 September 2026: 16,513 people and 244 boats. Provisional; see the [publication and definitions](https://www.gov.uk/government/publications/migrants-detected-crossing-the-english-channel-in-small-boats). Open Government Licence v3.0 except where otherwise stated.

Both raw workbooks are retained under `research/raw/`, with SHA-256 hashes in its manifest. The provisional record's metadata is in `research/mvp-2026-snapshot.json`; the initial research registry is retained separately.

## Geography

- Natural Earth 1:50m Admin 0 Countries, obtained 11 September 2026 from the [Natural Earth vector repository](https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_50m_admin_0_countries.geojson). [Public-domain terms](https://www.naturalearthdata.com/about/terms-of-use/).
- `public/data/land.geojson` retains UK, France, Belgium, Netherlands, Germany, Ireland and Luxembourg polygons; unused properties are removed. Only the regional camera extent is shown. This is a generalised base layer, not a navigational chart.
- City and region labels in `ChannelMap.tsx` are approximate cartographic reference annotations, not measured event locations. Scenario endpoints are deliberately illustrative and never classified as observations.

## Fonts and icons

- DM Sans and Manrope variable fonts from the [Google Fonts source repository](https://github.com/google/fonts), hosted locally. SIL Open Font Licence texts are in `public/fonts/`.
- Lucide icons, ISC licence; dependency licences are retained in installed packages.
- MapLibre GL JS uses BSD-3-Clause; Three.js and React use MIT licences. See installed dependency licences and the pinned `yarn.lock`.

No external tile service is used. Source links open the original publisher; rendering the page itself does not require external network services.
