import { useEffect, useRef, useState } from "react";
import {
  AudioSources,
  loadAudioManifest,
  type AudioClip,
} from "../story/audioCache";
import { NarrationPlayer } from "../story/narrationPlayer";
import { storySections } from "./sections";

export function useStoryListening(
  onAdvance: (section: number) => void,
  onProgress?: (progress: number) => void,
) {
  const [playing, setPlaying] = useState(false);
  const [available, setAvailable] = useState(false);
  const [error, setError] = useState(false);
  const [clips, setClips] = useState<AudioClip[]>([]);
  const player = useRef<NarrationPlayer | null>(null);
  const source = useRef<AudioSources | null>(null);
  const sampleProgress = useRef(() => {});
  const callback = useRef(onAdvance);
  callback.current = onAdvance;
  const progressCallback = useRef(onProgress);
  progressCallback.current = onProgress;
  useEffect(() => {
    let active = true;
    const audio = new Audio();
    const reportProgress = () => {
      if (
        !audio.paused &&
        Number.isFinite(audio.duration) &&
        audio.duration > 0
      )
        progressCallback.current?.(
          Math.min(1, audio.currentTime / audio.duration),
        );
    };
    sampleProgress.current = reportProgress;
    audio.dataset.editorialNarration = "true";
    const cache = new AudioSources();
    source.current = cache;
    const engine = new NarrationPlayer(
      audio,
      (clip) => cache.source(clip),
      storySections.length - 1,
      (index) => callback.current(index),
      () => {
        setPlaying(false);
        callback.current(storySections.length - 1);
      },
      () => setError(true),
    );
    engine.setEnabled(true);
    engine.setPace(0);
    player.current = engine;
    void loadAudioManifest().then((manifest) => {
      if (!active || !manifest) return;
      const selected = storySections.map(
        (section) => manifest.clips[section.audioFrame],
      );
      engine.setClips(selected);
      setClips(selected);
      setAvailable(true);
    });
    return () => {
      active = false;
      sampleProgress.current = () => {};
      engine.cancel();
      cache.dispose();
      player.current = null;
    };
  }, []);
  return {
    playing,
    available,
    error,
    clips,
    sampleProgress: () => sampleProgress.current(),
    prepare: (index: number) => {
      for (const clip of clips.slice(index, index + 2))
        void source.current?.prepare(clip);
    },
    play: (index: number) => {
      player.current?.start(index);
      setPlaying(true);
      setError(false);
    },
    pause: () => {
      player.current?.pause();
      setPlaying(false);
    },
    cancel: () => {
      player.current?.cancel();
      setPlaying(false);
      setError(false);
    },
  };
}
