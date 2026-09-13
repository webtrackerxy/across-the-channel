import {
  lazy,
  Suspense,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
} from "react";
import {
  ArrowDown,
  ChartColumn,
  Github,
  ArrowRight,
  ArrowUpRight,
  Maximize2,
  Headphones,
  Menu,
  Moon,
  Pause,
  Sun,
  Waves,
} from "lucide-react";
import {
  byYear,
  changePercent,
  formatNumber,
  occupancy,
  records,
} from "../data/model";
import {
  initialTextIndex,
  initialTheme,
  savePreference,
  textSizes,
} from "../design/preferences";
import { EvidenceDialog } from "../components/EvidenceDialog";
import { BoatIllustration } from "./BoatIllustration";
import { storySections } from "./sections";
import { useStoryListening } from "./useStoryListening";
import "./editorial.css";
import { presets, type Scenario } from "../scenarios/model";
import { StoryScenario } from "./StoryScenario";
import { HistoryChart } from "../components/HistoryChart";
import { Dialog } from "../components/Dialog";
import { DataTable } from "../components/DataTable";
import { Foundations } from "../design/Foundations";
const requestedYear = Number(new URLSearchParams(location.search).get("year"));
const initialYear = records.some((record) => record.year === requestedYear)
  ? requestedYear
  : 2025;

const StoryMap = lazy(() => import("./StoryMap"));
const first = byYear(2018),
  before = byYear(2022),
  recent = byYear(2025),
  latest = byYear(2026);
const drop = (a: number, b: number) => Math.abs(changePercent(a, b)).toFixed(1);

export default function StoryPage() {
  const [active, setActive] = useState(0);
  const activeRef = useRef(0);
  const [theme, setTheme] = useState(initialTheme);
  const [textIndex, setTextIndex] = useState(initialTextIndex);
  const [reduce, setReduce] = useState(
    () => matchMedia("(prefers-reduced-motion: reduce)").matches,
  );
  const [sourceOpen, setSourceOpen] = useState(false);
  const [chartOpen, setChartOpen] = useState(false);
  const [chartYear, setChartYear] = useState(initialYear);
  const [mapYear, setMapYear] = useState(initialYear);
  const [mapScenario, setMapScenario] = useState(false);
  const [mapOpen, setMapOpen] = useState(
    records.some((record) => record.year === requestedYear),
  );
  const [dataOpen, setDataOpen] = useState(false);
  const [designOpen, setDesignOpen] = useState(false);
  const [sourceYear, setSourceYear] = useState(initialYear);
  const [transcriptOpen, setTranscriptOpen] = useState(false);
  const [motionPaused, setMotionPaused] = useState(false);
  const [routeReplay, setRouteReplay] = useState(0);
  const [scenario, setScenario] = useState<Scenario>({
    ...presets.continuation,
  });
  const automaticScroll = useRef(false);
  const manualScroll = useRef(false);
  const chapterTransitionUntil = useRef(0);
  const narrationScroll = useRef<{
    element: HTMLElement | null;
    top: number;
  } | null>(null);
  const scrollTimer = useRef<ReturnType<typeof setTimeout> | undefined>(
    undefined,
  );
  const listening = useStoryListening(
    (index) => navigate(index, true),
    (progress) => {
      if (
        innerWidth >= 760 ||
        reduce ||
        manualScroll.current ||
        performance.now() < chapterTransitionUntil.current
      )
        return;
      const section = document.getElementById(
        storySections[activeRef.current].id,
      );
      const panel = section?.querySelector<HTMLElement>(".editorial-copy");
      const timeline = document.querySelector<HTMLElement>(
        ".editorial-timeline",
      );
      if (!section || !panel || !timeline) return;
      // Leave the opening still briefly, then reveal the full copy before speech ends.
      const fraction = Math.min(1, Math.max(0, (progress - 0.12) / 0.75));
      const reveal = fraction * fraction * (3 - 2 * fraction);
      automaticScroll.current = true;
      clearTimeout(scrollTimer.current);
      if (panel.scrollHeight > panel.clientHeight + 1) {
        narrationScroll.current = {
          element: panel,
          top: (panel.scrollHeight - panel.clientHeight) * reveal,
        };
      } else {
        const start = scrollY + section.getBoundingClientRect().top;
        const end =
          scrollY +
          panel.getBoundingClientRect().bottom -
          timeline.getBoundingClientRect().top +
          16;
        narrationScroll.current = {
          element: null,
          top: start + Math.max(0, end - start) * reveal,
        };
      }
    },
  );
  const listeningRef = useRef(listening);
  listeningRef.current = listening;
  useEffect(() => {
    const timeline = document.querySelector<HTMLElement>(".editorial-timeline");
    const root = document.querySelector<HTMLElement>(".editorial");
    const header = document.querySelector<HTMLElement>(".editorial-header");
    if (!timeline || !root) return;
    const update = () => {
      const section = document.getElementById(
        storySections[activeRef.current].id,
      );
      const before = section?.getBoundingClientRect().top;
      root.style.setProperty(
        "--timeline-height",
        `${timeline.getBoundingClientRect().height}px`,
      );
      if (header)
        root.style.setProperty(
          "--header-height",
          `${header.getBoundingClientRect().height}px`,
        );
      if (section && before !== undefined) {
        const shift = section.getBoundingClientRect().top - before;
        if (Math.abs(shift) > 0.5)
          window.scrollBy({ top: shift, behavior: "instant" });
      }
    };
    const observer = new ResizeObserver(update);
    observer.observe(timeline);
    if (header) observer.observe(header);
    update();
    return () => observer.disconnect();
  }, []);
  useEffect(() => {
    if (!listening.playing || reduce) return;
    let frame = 0;
    let previous = performance.now();
    let position: number | null = null;
    const tick = (now: number) => {
      const delta = Math.min(now - previous, 64);
      previous = now;
      listeningRef.current.sampleProgress();
      const target = narrationScroll.current;
      if (target && innerWidth < 760 && !document.hidden) {
        const current =
          position ?? (target.element ? target.element.scrollTop : scrollY);
        const distance = target.top - current;
        const top =
          Math.abs(distance) < 0.75
            ? target.top
            : current + distance * (1 - Math.exp(-delta / 180));
        position = top;
        if (target.element)
          target.element.scrollTo({ top, behavior: "instant" });
        else window.scrollTo({ top, behavior: "instant" });
      } else position = null;
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(frame);
      narrationScroll.current = null;
    };
  }, [listening.playing, reduce]);
  function navigate(index: number, automatic = false) {
    narrationScroll.current = null;
    manualScroll.current = false;
    chapterTransitionUntil.current = performance.now() + (reduce ? 0 : 1200);
    if (!automatic) listening.cancel();
    automaticScroll.current = true;
    clearTimeout(scrollTimer.current);
    activeRef.current = index;
    setActive(index);
    document.getElementById(storySections[index].id)?.scrollIntoView({
      behavior: reduce ? "instant" : "smooth",
      block: "start",
    });
    history.replaceState(null, "", `#${storySections[index].id}`);
    scrollTimer.current = setTimeout(
      () => {
        automaticScroll.current = false;
      },
      reduce ? 0 : 1200,
    );
  }
  useLayoutEffect(() => {
    document.documentElement.dataset.theme = theme;
    savePreference("theme", theme);
  }, [theme]);
  useLayoutEffect(() => {
    document.documentElement.style.fontSize = `${textSizes[textIndex]}%`;
    document.documentElement.dataset.largeText = String(
      textSizes[textIndex] >= 150,
    );
    savePreference("text-size", String(textSizes[textIndex]));
  }, [textIndex]);
  useEffect(() => {
    const media = matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReduce(media.matches);
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);
  useEffect(() => {
    let settleTimer: ReturnType<typeof setTimeout> | undefined;
    const scan = () => {
      if (automaticScroll.current) return;
      let next = 0,
        distance = Infinity;
      storySections.forEach((section, index) => {
        const box = document
          .getElementById(section.id)!
          .getBoundingClientRect();
        const value = Math.abs(box.top + box.height / 2 - innerHeight / 2);
        if (value < distance) {
          next = index;
          distance = value;
        }
      });
      if (next !== activeRef.current) {
        const wasPlaying = listeningRef.current.playing;
        activeRef.current = next;
        setActive(next);
        history.replaceState(null, "", `#${storySections[next].id}`);
        if (wasPlaying) {
          if (next < storySections.length - 1) {
            manualScroll.current = false;
            listeningRef.current.play(next);
          } else {
            listeningRef.current.cancel();
          }
        }
      }
    };
    const scroll = () => {
      clearTimeout(settleTimer);
      // Momentum scrolling can cross several chapters in a few frames. Waiting
      // briefly avoids restarting the map camera and reveal animation for every
      // chapter passed on the way to the reader's actual destination.
      settleTimer = setTimeout(scan, 120);
    };
    const interrupt = () => {
      clearTimeout(settleTimer);
      automaticScroll.current = false;
      manualScroll.current = true;
      narrationScroll.current = null;
      clearTimeout(scrollTimer.current);
    };
    const keyboard = (event: KeyboardEvent) => {
      if (
        (event.target as HTMLElement).closest(
          "button, a, input, select, summary",
        )
      )
        return;
      if (
        [
          "ArrowDown",
          "ArrowUp",
          "PageDown",
          "PageUp",
          "Home",
          "End",
          " ",
        ].includes(event.key)
      )
        interrupt();
    };
    const pointer = (event: PointerEvent) => {
      if (
        (event.target as HTMLElement).closest(
          "button, a, input, select, summary",
        )
      )
        return;
      interrupt();
    };
    const visibility = () => {
      if (document.hidden) listeningRef.current.pause();
    };
    const hash = () => {
      const index = storySections.findIndex(
        (section) => `#${section.id}` === location.hash,
      );
      if (index >= 0) {
        listeningRef.current.cancel();
        activeRef.current = index;
        setActive(index);
        document
          .getElementById(storySections[index].id)
          ?.scrollIntoView({ behavior: "instant" });
      }
    };
    hash();
    window.addEventListener("scroll", scroll, { passive: true });
    window.addEventListener("wheel", interrupt, { passive: true });
    window.addEventListener("touchmove", interrupt, { passive: true });
    window.addEventListener("pointerdown", pointer, { passive: true });
    window.addEventListener("keydown", keyboard);
    window.addEventListener("hashchange", hash);
    document.addEventListener("visibilitychange", visibility);
    return () => {
      clearTimeout(settleTimer);
      clearTimeout(scrollTimer.current);
      window.removeEventListener("scroll", scroll);
      window.removeEventListener("wheel", interrupt);
      window.removeEventListener("touchmove", interrupt);
      window.removeEventListener("pointerdown", pointer);
      window.removeEventListener("keydown", keyboard);
      window.removeEventListener("hashchange", hash);
      document.removeEventListener("visibilitychange", visibility);
    };
  }, []);
  const openSources = () => {
    listening.pause();
    setSourceYear(storySections[active].year);
    setSourceOpen(true);
  };
  const showChart = () => {
    listening.pause();
    setChartYear(storySections[active].year);
    setChartOpen(true);
  };
  const showMap = (year: number, hypothetical = false) => {
    listening.pause();
    setMapScenario(hypothetical);
    setMapYear(year);
    setMapOpen(true);
  };
  const showData = () => {
    listening.pause();
    setDataOpen(true);
  };
  return (
    <div
      className={`editorial ${reduce ? "editorial-reduced" : ""} ${active === 6 ? "editorial-scenario" : ""}`}
    >
      <button
        className="editorial-expand"
        onClick={() => showMap(storySections[active].year, active === 6)}
        aria-label="Explore this map interactively"
      >
        <Maximize2 size={19} />
      </button>
      <a className="skip-link" href="#channel">
        Skip to the story
      </a>
      <Suspense fallback={<div className="editorial-map" />}>
        <StoryMap
          section={active}
          reduced={reduce}
          theme={theme}
          motionPaused={motionPaused}
          replay={routeReplay}
          scenario={active === 6 ? scenario : undefined}
        />
      </Suspense>
      <div className="editorial-shade" aria-hidden="true" />
      <header className="editorial-header">
        <div className="editorial-identity">
          <a
            className="editorial-brand"
            href="#channel"
            onClick={(event) => {
              event.preventDefault();
              navigate(0);
            }}
          >
            <Waves aria-hidden="true" />
            <span>ACROSS THE CHANNEL</span>
          </a>
          <a
            className="editorial-github"
            href="https://github.com/webtrackerxy/across-the-channel"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="View Across the Channel on GitHub (opens in a new tab)"
          >
            <Github size={14} aria-hidden="true" /> GitHub
          </a>
        </div>
        <div className="editorial-header-progress" aria-hidden="true">
          <span
            style={{ width: `${((active + 1) / storySections.length) * 100}%` }}
          />
        </div>
        <div className="editorial-header-notice">
          <p>AI-generated content — verify against the cited sources</p>
          <p>Tip: Press the headphones icon to hear the whole story.</p>
        </div>
        <div className="editorial-actions">
          <button
            className="editorial-listen"
            disabled={!listening.available || active === 6}
            title={
              active === 6
                ? "Read and adjust this optional scenario; narration covers the factual story."
                : undefined
            }
            onPointerEnter={() => listening.prepare(active)}
            onFocus={() => listening.prepare(active)}
            onClick={() =>
              listening.playing ? listening.pause() : listening.play(active)
            }
            aria-label={
              listening.playing ? "Pause narration" : "Listen to the story"
            }
          >
            {listening.playing ? <Pause size={17} /> : <Headphones size={17} />}
            <span>{listening.playing ? "Pause" : "Listen"}</span>
          </button>
          <button className="editorial-explore-top" onClick={showChart}>
            Explore data <ArrowUpRight size={15} />
          </button>
          <details className="editorial-menu">
            <summary aria-label="Story menu">
              <Menu size={22} />
            </summary>
            <div className="editorial-menu-panel">
              <p>YOUR READING EXPERIENCE</p>
              <button
                onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              >
                {theme === "dark" ? <Sun size={17} /> : <Moon size={17} />}{" "}
                {theme === "dark" ? "Light" : "Dark"} appearance
              </button>
              <label>
                Text size{" "}
                <select
                  aria-label="Story text size"
                  value={textIndex}
                  onChange={(event) => setTextIndex(Number(event.target.value))}
                >
                  {textSizes.map((size, index) => (
                    <option key={size} value={index}>
                      {size}%
                    </option>
                  ))}
                </select>
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={reduce}
                  onChange={(event) => setReduce(event.target.checked)}
                />{" "}
                Reduce motion
              </label>
              {active > 0 && (
                <aside
                  className="editorial-motion-menu"
                  aria-label="Illustrative route animation"
                >
                  <p>
                    {active === 6
                      ? "Hypothetical connections—not predicted routes or recorded journeys."
                      : "Illustrative movement—not recorded journeys or boat frequency."}
                  </p>
                  {active !== 6 && storySections[active].year >= 2025 && (
                    <p>
                      2025 onward: Dover animation at 3.375× speed · not
                      measured boat speed.
                    </p>
                  )}
                  {reduce ? (
                    <span>Reduced motion · static boats</span>
                  ) : (
                    <>
                      <button onClick={() => setMotionPaused(!motionPaused)}>
                        {motionPaused ? "Play motion" : "Pause motion"}
                      </button>
                      {active >= 4 && active < 6 && (
                        <button
                          onClick={() => {
                            setRouteReplay((value) => value + 1);
                            setMotionPaused(false);
                          }}
                        >
                          Replay Portsmouth journey
                        </button>
                      )}
                    </>
                  )}
                </aside>
              )}
              <button onClick={openSources}>Sources and method</button>
              <a
                href={`${import.meta.env.BASE_URL}audio/narration/review.html`}
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => listening.pause()}
              >
                Narration recording review{" "}
                <ArrowUpRight size={15} aria-hidden="true" />
                <span className="sr-only"> (opens in a new tab)</span>
              </a>
              <button onClick={showChart}>Year-by-year chart</button>
              <button onClick={showData}>Full data table & CSV</button>
              <button
                onClick={() => {
                  listening.pause();
                  setDesignOpen(true);
                }}
              >
                Design foundations
              </button>
              <nav aria-label="Story chapters">
                {storySections.map((section, index) => (
                  <a
                    key={section.id}
                    href={`#${section.id}`}
                    onClick={(event) => {
                      event.preventDefault();
                      event.currentTarget.closest("details")!.open = false;
                      navigate(index);
                    }}
                  >
                    {String(index + 1).padStart(2, "0")} · {section.label}
                  </a>
                ))}
              </nav>
            </div>
          </details>
        </div>
      </header>
      <main
        className="editorial-story"
        aria-label="Across the Channel: a guided story"
      >
        {storySections.map((section, index) => (
          <section
            key={section.id}
            id={section.id}
            className={`editorial-section section-${section.id}`}
            data-active={active === index}
            aria-labelledby={`${section.id}-title`}
          >
            <div className="editorial-copy">
              <p className="editorial-kicker">
                <span>{String(index + 1).padStart(2, "0")}</span>{" "}
                {index === 0
                  ? "A STORY IN PEOPLE, NOT JUST BOATS"
                  : section.label.toUpperCase()}
              </p>
              {index === 0 && (
                <>
                  <h1 id={`${section.id}-title`}>
                    What does
                    <br />
                    counting boats
                    <br />
                    <em>miss?</em>
                  </h1>
                  <p className="editorial-deck">
                    Across a narrow sea,
                    <br />
                    the numbers tell a bigger story.
                  </p>
                  <p className="editorial-intro-note">
                    Recorded UK arrivals. Changing occupancy.
                    <br />
                    And the questions the evidence leaves open.
                  </p>
                  <button
                    className="editorial-scroll"
                    onClick={() => navigate(1)}
                  >
                    Scroll to discover <ArrowDown size={19} />
                  </button>
                </>
              )}
              {index === 1 && (
                <>
                  <h2 id={`${section.id}-title`}>
                    One boat.
                    <br />
                    <em>A different scale.</em>
                  </h2>
                  <p className="editorial-deck">
                    Start in 2018. On average, an arriving boat carried about
                    seven people.
                  </p>
                  <div className="editorial-evidence">
                    <BoatIllustration people={occupancy(first)} year={2018} />
                    <div className="editorial-small-stats">
                      <div>
                        <strong>{formatNumber(first.people)}</strong>
                        <span>people arriving</span>
                      </div>
                      <div>
                        <strong>{formatNumber(first.boats)}</strong>
                        <span>boats</span>
                      </div>
                    </div>
                  </div>
                  <p className="editorial-caption">
                    Illustration scaled by average occupancy.
                    <br />
                    Not measured boat size or capacity.
                  </p>
                </>
              )}
              {index === 2 && (
                <>
                  <h2 id={`${section.id}-title`}>
                    Now look
                    <br />
                    <em>inside the numbers.</em>
                  </h2>
                  <p className="editorial-deck">
                    By 2025, the average was almost nine times higher. About 62
                    people per arriving boat.
                  </p>
                  <div className="editorial-evidence">
                    <p className="editorial-card-label">
                      AVERAGE PEOPLE PER BOAT
                    </p>
                    <div className="editorial-boats">
                      <BoatIllustration people={occupancy(first)} year={2018} />
                      <BoatIllustration
                        people={occupancy(recent)}
                        year={2025}
                      />
                    </div>
                    <p className="editorial-caption">
                      Illustration scaled by occupancy, not measured vessel
                      dimensions.
                    </p>
                    <div className="editorial-small-stats">
                      <div>
                        <strong>{formatNumber(recent.people)}</strong>
                        <span>people arriving in 2025</span>
                      </div>
                      <div>
                        <strong>{formatNumber(recent.boats)}</strong>
                        <span>boats</span>
                      </div>
                    </div>
                  </div>
                </>
              )}
              {index === 3 && (
                <>
                  <h2 id={`${section.id}-title`}>
                    Fewer boats.
                    <br />
                    <em>Almost as many people.</em>
                  </h2>
                  <p className="editorial-deck">
                    Between 2022 and 2025, boat numbers fell much faster than
                    the number of people arriving.
                  </p>
                  <div className="editorial-evidence editorial-comparison">
                    <div className="editorial-year-key">
                      <span>2022</span>
                      <span>2025</span>
                    </div>
                    {[
                      {
                        label: "Arriving boats",
                        a: before.boats,
                        b: recent.boats,
                      },
                      {
                        label: "People arriving",
                        a: before.people,
                        b: recent.people,
                      },
                    ].map((metric) => (
                      <div className="editorial-metric" key={metric.label}>
                        <div>
                          <span>{metric.label}</span>
                          <strong>−{drop(metric.a, metric.b)}%</strong>
                        </div>
                        <div className="editorial-bar">
                          <span style={{ width: "100%" }}>
                            {formatNumber(metric.a)}
                          </span>
                        </div>
                        <div className="editorial-bar current">
                          <span
                            style={{ width: `${(metric.b / metric.a) * 100}%` }}
                          >
                            {formatNumber(metric.b)}
                          </span>
                        </div>
                      </div>
                    ))}
                    <p className="editorial-increase">
                      <strong>
                        +
                        {changePercent(
                          occupancy(before),
                          occupancy(recent),
                        ).toFixed(1)}
                        %
                      </strong>
                      <span>
                        people per boat
                        <br />
                        <b>
                          {occupancy(before).toFixed(1)} →{" "}
                          {occupancy(recent).toFixed(1)}
                        </b>
                      </span>
                    </p>
                  </div>
                  <button
                    className="editorial-source-link"
                    onClick={openSources}
                  >
                    Check the comparison <ArrowUpRight size={16} />
                  </button>
                </>
              )}
              {index === 4 && (
                <>
                  <h2 id={`${section.id}-title`}>
                    Farther
                    <br />
                    <em>west.</em>
                  </h2>
                  <p className="editorial-deck">
                    A reported connection from Utah Beach to Portsmouth adds a
                    different geographic question.
                  </p>
                  <div className="editorial-case">
                    <span className="editorial-route-dot" />
                    <div>
                      <strong>Utah Beach → Portsmouth</strong>
                      <span>Reported endpoints · 6 Sep 2026</span>
                    </div>
                  </div>
                  <p className="editorial-caption">
                    The map links reported endpoints, not a recorded vessel
                    track. This case alone does not establish a wider route
                    shift.
                  </p>
                  <div className="editorial-evidence">
                    <p className="editorial-card-label">
                      2026 YEAR TO DATE · 1 JAN–3 SEP · PROVISIONAL
                    </p>
                    <div className="editorial-small-stats">
                      <div>
                        <strong>{formatNumber(latest.people)}</strong>
                        <span>people</span>
                      </div>
                      <div>
                        <strong>{latest.boats}</strong>
                        <span>boats</span>
                      </div>
                      <div>
                        <strong>{occupancy(latest).toFixed(1)}</strong>
                        <span>people / boat</span>
                      </div>
                    </div>
                    <p className="editorial-caption">
                      The 6 September case is outside these totals. Partial-year
                      totals are not comparable with full years.
                    </p>
                  </div>
                  <button
                    className="editorial-source-link"
                    onClick={openSources}
                  >
                    Sources and reporting dates <ArrowUpRight size={16} />
                  </button>
                </>
              )}
              {index === 5 && (
                <>
                  <h2 id={`${section.id}-title`}>
                    People. Boats.
                    <br />
                    <em>Perspective.</em>
                  </h2>
                  <p className="editorial-deck">
                    Count the boats. Count the people.
                    <br />
                    Read the two together.
                  </p>
                  <p className="editorial-body">
                    The change in occupancy is clear. Its causes—and what it
                    means for future journeys—need more than a boat count to
                    explain.
                  </p>
                  <p className="editorial-body">
                    Explore the annual figures, check the sources, or change the
                    assumptions in clearly labelled hypothetical scenarios.
                  </p>
                  <button className="editorial-cta" onClick={showChart}>
                    Explore the data <ArrowRight size={19} />
                  </button>
                  <button
                    className="editorial-source-link"
                    onClick={() => navigate(6)}
                  >
                    Try an optional scenario <ArrowRight size={19} />
                  </button>
                  <button
                    className="editorial-source-link"
                    onClick={openSources}
                  >
                    Read the evidence <ArrowUpRight size={16} />
                  </button>
                  <p className="editorial-caption">
                    Recorded arrivals include rescue and interception. Occupancy
                    is not rated capacity. Scenarios are not forecasts.
                  </p>
                </>
              )}
              {index === 6 && (
                <StoryScenario
                  value={scenario}
                  onChange={(value) => {
                    listening.cancel();
                    setScenario(value);
                  }}
                />
              )}
            </div>
          </section>
        ))}
      </main>
      <footer className="editorial-timeline">
        <span className="editorial-current-year">
          {active === 6 ? "What if?" : storySections[active].year}
        </span>
        <nav aria-label="Story progress">
          {storySections.map((section, index) => (
            <button
              key={section.id}
              aria-label={`Go to ${section.label}`}
              aria-current={active === index ? "step" : undefined}
              onClick={() => navigate(index)}
            >
              <span className="timeline-dot" />
              <span className="timeline-text">{section.label}</span>
            </button>
          ))}
        </nav>
        <button
          className="editorial-chart-toggle"
          aria-label="Open year-by-year chart"
          aria-haspopup="dialog"
          onClick={() => {
            listening.pause();
            setChartYear(storySections[active].year);
            setChartOpen(true);
          }}
        >
          <ChartColumn size={22} aria-hidden="true" />
          <span>Chart</span>
        </button>
        <span className="editorial-step-count">
          {String(active + 1).padStart(2, "0")} /{" "}
          {String(storySections.length).padStart(2, "0")}
        </span>
      </footer>
      {active !== 6 && (listening.playing || transcriptOpen) && (
        <aside className="editorial-audio-note">
          <span>AI-generated voice</span>
          <button
            aria-expanded={transcriptOpen}
            onClick={() => setTranscriptOpen(!transcriptOpen)}
          >
            Transcript
          </button>
          {transcriptOpen && <p>{listening.clips[active]?.text}</p>}
        </aside>
      )}
      <span className="sr-only" role="status">
        {listening.error
          ? "Audio unavailable. Continue reading or explore the transcript."
          : listening.playing
            ? "Narration playing. Scrolling pauses narration."
            : "Narration paused"}
      </span>
      <Dialog
        open={chartOpen}
        title="Year-by-year chart"
        onClose={() => setChartOpen(false)}
      >
        <div className="editorial-chart-popup">
          <HistoryChart
            selectedYear={chartYear}
            onYearChange={setChartYear}
            onSource={() => {
              setSourceYear(chartYear);
              setSourceOpen(true);
            }}
            selectionHint="Select a year to inspect its figures."
          />
          <p className="editorial-chart-summary" aria-live="polite">
            {chartYear}
            {chartYear === 2026 ? " YTD (provisional)" : ""}:{" "}
            {formatNumber(byYear(chartYear).people)} people ·{" "}
            {formatNumber(byYear(chartYear).boats)} boats ·{" "}
            {occupancy(byYear(chartYear)).toFixed(1)} people / boat
          </p>
          <button className="text-link" onClick={() => showMap(chartYear)}>
            Explore {chartYear} on the interactive map{" "}
            <ArrowUpRight size={15} />
          </button>
          <button className="text-link" onClick={showData}>
            Full data table & CSV
          </button>
        </div>
      </Dialog>
      <Dialog
        open={mapOpen}
        title="Interactive map"
        onClose={() => setMapOpen(false)}
      >
        <div className="editorial-map-dialog">
          <label>
            Selected year{" "}
            <select
              aria-label="Map year"
              value={mapYear}
              onChange={(event) => {
                const year = Number(event.target.value);
                setMapYear(year);
                setMapScenario(false);
                const url = new URL(location.href);
                url.searchParams.set("year", String(year));
                history.replaceState(null, "", url);
              }}
            >
              {records.map((r) => (
                <option key={r.year} value={r.year}>
                  {r.year}
                  {r.partial ? " YTD" : ""}
                </option>
              ))}
            </select>
          </label>
          <p>
            {formatNumber(byYear(mapYear).people)} people ·{" "}
            {formatNumber(byYear(mapYear).boats)} boats ·{" "}
            {occupancy(byYear(mapYear)).toFixed(1)} people / boat
          </p>
          {mapOpen && (
            <Suspense fallback={<p>Loading map…</p>}>
              <StoryMap
                interactive
                section={mapScenario ? 6 : mapYear === 2026 ? 4 : 2}
                reduced={reduce}
                theme={theme}
                motionPaused
                replay={0}
                scenario={mapScenario ? scenario : undefined}
              />
            </Suspense>
          )}
          <p className="chart-caveat">
            {mapScenario
              ? "Hypothetical connections—not predicted routes or recorded journeys."
              : mapYear === 2026
                ? "Calais–Dover is indicative context; Utah Beach–Portsmouth links reported endpoints for 6 September, after the 3 September provisional totals cutoff. Neither line is a recorded vessel track."
                : "Calais–Dover is an indicative connection, not a recorded vessel track."}
          </p>
          <button
            onClick={() => {
              setSourceYear(mapYear);
              setSourceOpen(true);
            }}
          >
            Source for {mapYear}
          </button>
        </div>
      </Dialog>
      <Dialog
        open={dataOpen}
        title="Crossings data"
        onClose={() => setDataOpen(false)}
      >
        <DataTable
          onSource={(year) => {
            setSourceYear(year);
            setSourceOpen(true);
          }}
        />
      </Dialog>
      <Dialog
        open={designOpen}
        title="Design foundations"
        onClose={() => setDesignOpen(false)}
      >
        <Foundations />
      </Dialog>
      <EvidenceDialog
        open={sourceOpen}
        record={byYear(sourceYear)}
        onClose={() => setSourceOpen(false)}
      />
    </div>
  );
}
