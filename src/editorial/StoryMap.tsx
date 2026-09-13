import { useEffect, useRef, useState } from "react";
import {
  Map,
  NavigationControl,
  FullscreenControl,
  Marker,
  type GeoJSONSource,
  type StyleSpecification,
} from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { portsmouthFeatures } from "../map/portsmouth";
import { routeFeatures, endpointFeatures } from "../map/routes";
import type { Theme } from "../design/preferences";
import { RouteBoats } from "./RouteBoats";
import type { Scenario } from "../scenarios/model";

const geography = `${import.meta.env.BASE_URL}data/land.geojson`;
const style: StyleSpecification = {
  version: 8,
  sources: {
    land: {
      type: "geojson",
      data: geography,
      attribution: "Natural Earth · reference geography",
    },
  },
  layers: [
    { id: "sea", type: "background", paint: { "background-color": "#0b2737" } },
    {
      id: "shelf",
      type: "line",
      source: "land",
      paint: {
        "line-color": "#5da799",
        "line-width": 45,
        "line-opacity": 0.08,
      },
    },
    {
      id: "shore",
      type: "line",
      source: "land",
      paint: {
        "line-color": "#93bcaa",
        "line-width": 18,
        "line-opacity": 0.12,
      },
    },
    {
      id: "land",
      type: "fill",
      source: "land",
      paint: { "fill-color": "#587b76" },
    },
    {
      id: "coast",
      type: "line",
      source: "land",
      paint: { "line-color": "#b0c7b4", "line-width": 1, "line-opacity": 0.6 },
    },
  ],
};
const places: {
  name: string;
  coordinates: [number, number];
  country?: boolean;
  west?: boolean;
}[] = [
  { name: "ENGLAND", coordinates: [-1.2, 51.3], country: true },
  { name: "FRANCE", coordinates: [0.65, 49.2], country: true },
  { name: "Dover", coordinates: [1.32, 51.13] },
  { name: "Calais", coordinates: [1.86, 50.95] },
  { name: "Dunkirk", coordinates: [2.38, 51.04] },
  { name: "Dieppe", coordinates: [1.08, 49.92], west: true },
  { name: "Brighton", coordinates: [-0.14, 50.82], west: true },
  { name: "Portsmouth", coordinates: [-1.06776, 50.822113], west: true },
  { name: "Utah Beach", coordinates: [-1.174703, 49.415666], west: true },
];

export default function StoryMap({
  section,
  reduced,
  theme,
  motionPaused,
  replay,
  scenario,
  interactive = false,
}: {
  section: number;
  reduced: boolean;
  theme: Theme;
  motionPaused: boolean;
  replay: number;
  scenario?: Scenario;
  interactive?: boolean;
}) {
  const container = useRef<HTMLDivElement>(null);
  const instance = useRef<Map | null>(null);
  const [ready, setReady] = useState(false);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    if (!container.current) return;
    let map: Map;
    let active = true;
    const markers: Marker[] = [];
    try {
      map = new Map({
        container: container.current,
        style,
        center: [0, 50.35],
        zoom: 6.5,
        pitch: 0,
        interactive,
        attributionControl: false,
        canvasContextAttributes: { antialias: true },
        pixelRatio: Math.min(devicePixelRatio, 2),
      });
      instance.current = map;
      if (interactive) {
        map.addControl(new NavigationControl(), "top-right");
        map.addControl(new FullscreenControl(), "top-right");
      }
      map.on("error", () => {
        if (active) setFailed(true);
      });
      map.on("load", () => {
        if (!active) return;
        map.addSource("connections", {
          type: "geojson",
          data: routeFeatures("strait"),
        });
        map.addSource("endpoints", {
          type: "geojson",
          data: endpointFeatures("strait"),
        });
        map.addLayer({
          id: "connections",
          type: "line",
          source: "connections",
          paint: {
            "line-color": "#a6efdc",
            "line-width": 2,
            "line-dasharray": [3, 3],
          },
        });
        map.addLayer({
          id: "endpoints",
          type: "circle",
          source: "endpoints",
          paint: {
            "circle-color": "#b7f8de",
            "circle-radius": 5,
            "circle-stroke-color": "#0b2737",
            "circle-stroke-width": 2,
          },
        });
        for (const place of places) {
          const element = document.createElement("span");
          element.textContent = place.name;
          element.className = `editorial-place ${place.country ? "country" : ""} ${place.west ? "west" : ""}`;
          markers.push(
            new Marker({
              element,
              anchor: place.country ? "center" : "left",
              offset: place.country ? [0, 0] : [10, 0],
            })
              .setLngLat(place.coordinates)
              .addTo(map),
          );
        }
        setReady(true);
      });
    } catch {
      setFailed(true);
      return;
    }
    const resize = new ResizeObserver(() => map.resize());
    resize.observe(container.current);
    return () => {
      active = false;
      resize.disconnect();
      markers.forEach((marker) => marker.remove());
      map.remove();
      instance.current = null;
    };
  }, [interactive]);
  useEffect(() => {
    const map = instance.current;
    if (!map || !ready) return;
    const west = scenario ? scenario.footprint === "wider" : section >= 4;
    const wide = section === 0 || west;
    const mobile = window.innerWidth < 760;
    const bounds: [[number, number], [number, number]] = wide
      ? [
          [-2.5, 49.1],
          [2.7, 51.65],
        ]
      : [
          [0.2, 50.35],
          [2.8, 51.7],
        ];
    const frame = () => {
      const height = container.current!.clientHeight;
      const width = container.current!.clientWidth;
      const narrow = window.innerWidth < 760;
      map.fitBounds(bounds, {
        padding: interactive
          ? { top: 55, bottom: 45, left: 45, right: 65 }
          : narrow
            ? { top: 100, bottom: height * 0.39, left: 35, right: 60 }
            : { top: 90, bottom: 110, left: width * 0.41, right: 85 },
        duration: reduced ? 0 : 1400,
        maxZoom: 8,
      });
    };
    frame();
    window.addEventListener("resize", frame);
    const routes = {
      type: "FeatureCollection" as const,
      features: [
        ...routeFeatures("strait").features,
        ...(west ? portsmouthFeatures().features : []),
      ],
    };
    const endpoints = {
      type: "FeatureCollection" as const,
      features: [
        ...endpointFeatures("strait").features,
        ...(west ? portsmouthFeatures(true).features : []),
      ],
    };
    (map.getSource("connections") as GeoJSONSource).setData(
      scenario ? routeFeatures(scenario.footprint) : routes,
    );
    (map.getSource("endpoints") as GeoJSONSource).setData(
      scenario ? endpointFeatures(scenario.footprint) : endpoints,
    );
    map.setPaintProperty("connections", "line-opacity", section === 0 ? 0 : 1);
    map.setPaintProperty(
      "land",
      "fill-color",
      theme === "dark" ? "#587b76" : "#adc6b1",
    );
    map.setPaintProperty(
      "sea",
      "background-color",
      theme === "dark" ? "#0b2737" : "#dce9e5",
    );
    map.setPaintProperty(
      "connections",
      "line-color",
      scenario
        ? theme === "dark"
          ? "#ffc98b"
          : "#88400b"
        : theme === "dark"
          ? "#b7f8de"
          : "#005b4c",
    );
    map.setPaintProperty(
      "endpoints",
      "circle-color",
      scenario ? (theme === "dark" ? "#ffc98b" : "#88400b") : "#b7f8de",
    );
    container.current?.classList.toggle("show-west", wide);
    container.current?.classList.toggle("mobile-map", mobile);
    return () => window.removeEventListener("resize", frame);
  }, [section, ready, reduced, theme, scenario?.footprint, interactive]);
  return (
    <div
      className={interactive ? "editorial-interactive-map" : "editorial-map"}
      aria-hidden={interactive ? undefined : true}
      role={interactive ? "region" : undefined}
      aria-label={interactive ? "Interactive Channel map" : undefined}
      data-testid={interactive ? "interactive-map" : "story-map"}
      data-ready={ready}
      data-section={section}
      data-route-count={
        scenario
          ? scenario.footprint === "wider"
            ? 4
            : 1
          : section >= 4
            ? 2
            : 1
      }
    >
      <div ref={container} className="editorial-map-canvas" />
      {interactive && ready && (
        <div className="editorial-map-tools">
          <button
            onClick={() =>
              instance.current?.panBy([0, -100], {
                duration: reduced ? 0 : 200,
              })
            }
            aria-label="Pan north"
          >
            ↑
          </button>
          <button
            onClick={() =>
              instance.current?.panBy([-100, 0], {
                duration: reduced ? 0 : 200,
              })
            }
            aria-label="Pan west"
          >
            ←
          </button>
          <button
            onClick={() =>
              instance.current?.panBy([100, 0], { duration: reduced ? 0 : 200 })
            }
            aria-label="Pan east"
          >
            →
          </button>
          <button
            onClick={() =>
              instance.current?.panBy([0, 100], { duration: reduced ? 0 : 200 })
            }
            aria-label="Pan south"
          >
            ↓
          </button>
          <button
            onClick={() =>
              instance.current?.fitBounds(
                section >= 4
                  ? [
                      [-2.5, 49.1],
                      [2.7, 51.65],
                    ]
                  : [
                      [0.2, 50.35],
                      [2.8, 51.7],
                    ],
                { padding: 60, duration: reduced ? 0 : 500 },
              )
            }
          >
            Reset map
          </button>
        </div>
      )}
      {ready && instance.current && !failed && (
        <RouteBoats
          map={instance.current}
          section={section}
          paused={motionPaused}
          reduced={reduced}
          replay={replay}
          scenario={scenario}
        />
      )}
      {failed && (
        <p className="editorial-map-error">
          Map unavailable. The story and its figures remain available below.
        </p>
      )}
      <span className="editorial-cartography">
        Natural Earth · reference geography
      </span>
    </div>
  );
}
