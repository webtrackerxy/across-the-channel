import { useEffect, useRef } from "react";
import { Marker, type Map } from "maplibre-gl";
import { connections } from "../map/routes";
import { portsmouthCase } from "../map/portsmouth";
import {
  DOVER_BOATS,
  doverSpeed,
  routePosition,
  routeProgress,
} from "./routeMotion";
import { storySections } from "./sections";
import type { Scenario } from "../scenarios/model";

export function RouteBoats({
  map,
  section,
  paused,
  reduced,
  replay,
  scenario,
}: {
  map: Map;
  section: number;
  paused: boolean;
  reduced: boolean;
  replay: number;
  scenario?: Scenario;
}) {
  const elapsed = useRef({ dover: 0, west: 0 });
  const lastReplay = useRef(replay);
  useEffect(() => {
    if (replay !== lastReplay.current) {
      elapsed.current.west = 0;
      lastReplay.current = replay;
    }
    if (section === 0) return;
    const scenarioCount = scenario
      ? scenario.boats === 0
        ? 0
        : Math.min(4, Math.ceil(scenario.boats / 300))
      : 0;
    const specs = scenario
      ? connections[scenario.footprint].flatMap((points) =>
          Array.from({ length: scenarioCount }, (_, index) => ({
            points,
            index,
            west: false,
          })),
        )
      : Array.from(
          { length: DOVER_BOATS + (section >= 4 ? 1 : 0) },
          (_, index) => ({
            points:
              index === DOVER_BOATS
                ? portsmouthCase.coordinates
                : connections.strait[0],
            index,
            west: index === DOVER_BOATS,
          }),
        );
    const boats = specs.map(({ points, index, west }) => {
      const element = document.createElement("div");
      element.className = `editorial-route-boat${west ? " portsmouth-boat" : ""}`;
      element.dataset.route = west ? "portsmouth" : "dover";
      if (scenario) {
        element.dataset.route = "scenario";
        element.classList.add("scenario-boat");
        const size = 12 + Math.sqrt(scenario.occupancy) * 1.2;
        element.style.width = `${size}px`;
        element.style.height = `${size * 1.5}px`;
      }
      element.innerHTML =
        '<svg viewBox="0 0 20 30" aria-hidden="true"><path class="boat-wake" d="M5 25 3 29 M10 26v4 M15 25l2 4"/><path class="boat-hull" d="M10 2Q2 9 3 23Q10 26 17 23Q18 9 10 2Z"/><path class="boat-seat" d="M6 14h8M6 19h8"/></svg>';
      const marker = new Marker({ element, rotationAlignment: "viewport" })
        .setLngLat(points[0])
        .addTo(map);
      return { west, marker, points, element, index };
    });
    const draw = () => {
      for (const boat of boats) {
        const progress = reduced
          ? boat.west
            ? 0.5
            : (boat.index + 0.5) / (scenario ? scenarioCount : DOVER_BOATS)
          : scenario
            ? (elapsed.current.dover / 18000 + boat.index / scenarioCount) % 1
            : routeProgress(
                boat.west ? elapsed.current.west : elapsed.current.dover,
                boat.index,
                boat.west,
              );
        const start = map.project(boat.points[0]);
        const end = map.project(boat.points[1]);
        boat.marker
          .setLngLat(routePosition(boat.points, progress))
          .setRotation(
            (Math.atan2(end.y - start.y, end.x - start.x) * 180) / Math.PI + 90,
          );
        boat.element.dataset.progress = progress.toFixed(4);
        boat.element.classList.toggle("arrived", boat.west && progress === 1);
      }
    };
    let frame = 0;
    let previous = 0;
    const tick = (now: number) => {
      if (previous) {
        const delta = Math.min(now - previous, 100);
        elapsed.current.dover +=
          delta * (scenario ? 1 : doverSpeed(storySections[section].year));
        if (section >= 4) elapsed.current.west += delta;
      }
      previous = now;
      draw();
      frame = requestAnimationFrame(tick);
    };
    const visibility = () => {
      cancelAnimationFrame(frame);
      previous = 0;
      if (!document.hidden && !paused && !reduced)
        frame = requestAnimationFrame(tick);
    };
    draw();
    visibility();
    map.on("move", draw);
    document.addEventListener("visibilitychange", visibility);
    return () => {
      cancelAnimationFrame(frame);
      map.off("move", draw);
      document.removeEventListener("visibilitychange", visibility);
      boats.forEach(({ marker }) => marker.remove());
    };
  }, [map, section, paused, reduced, replay, scenario]);
  return null;
}
