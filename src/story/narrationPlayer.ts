import type { AudioClip } from "./audioCache";

/** One clock for the story and one audio element; only active time consumes budgets. */
export class NarrationPlayer {
  private frame = -1;
  private running = false;
  private enabled = false;
  private speechDone = true;
  private finished = false;
  private elapsed = 0;
  private started = 0;
  private pace = 8000;
  private epoch = 0;
  private attempt = 0;
  private timer?: ReturnType<typeof setTimeout>;
  private stall?: ReturnType<typeof setTimeout>;
  private clips: AudioClip[] = [];
  constructor(
    private audio: HTMLAudioElement,
    private source: (clip: AudioClip) => string,
    private count: number,
    private onFrame: (frame: number) => void,
    private onStop: () => void,
    private onFailure: () => void,
  ) {}
  setClips(clips: AudioClip[]) {
    this.clips = clips;
  }
  setEnabled(enabled: boolean) {
    this.enabled = enabled;
    if (!enabled && !this.speechDone) {
      this.attempt++;
      this.audio.pause();
      this.speechDone = true;
      this.schedule();
    }
    // Enabling during a step intentionally takes effect at the next step.
  }
  setPace(milliseconds: number) {
    this.capture();
    this.pace = milliseconds;
    this.schedule();
  }
  start(frame: number) {
    if (frame !== this.frame || this.finished) this.select(frame);
    if (this.running) return;
    this.running = true;
    this.started = Date.now();
    if (!this.speechDone) this.play();
    this.schedule();
  }
  pause() {
    this.capture();
    this.running = false;
    this.attempt++;
    this.clearTimers();
    this.audio.pause();
  }
  cancel() {
    this.pause();
    this.epoch++;
    this.frame = -1;
    this.audio.removeAttribute("src");
    this.audio.load();
  }
  private select(frame: number) {
    this.pause();
    this.epoch++;
    this.frame = frame;
    this.finished = false;
    this.elapsed = 0;
    const clip = this.clips[frame];
    this.speechDone = !this.enabled || !clip;
    const epoch = this.epoch;
    this.audio.onended = () => {
      if (epoch !== this.epoch || !this.running) return;
      this.speechDone = true;
      this.schedule();
    };
    this.audio.onerror = () => {
      if (epoch === this.epoch && this.running) this.fail();
    };
    this.audio.ontimeupdate = () => {
      if (epoch === this.epoch) this.watchStall();
    };
    if (!this.speechDone) {
      this.audio.src = this.source(clip);
      this.audio.load();
    }
  }
  private play() {
    const epoch = this.epoch;
    const attempt = ++this.attempt;
    this.watchStall();
    // Called synchronously by start() from the user's click, never after a fetch.
    try {
      void this.audio.play().catch(() => {
        if (epoch === this.epoch && attempt === this.attempt && this.running)
          this.fail();
      });
    } catch {
      this.fail();
    }
  }
  private fail() {
    this.audio.pause();
    this.speechDone = true;
    this.onFailure();
    this.schedule();
  }
  private watchStall() {
    clearTimeout(this.stall);
    if (this.running && !this.speechDone)
      this.stall = setTimeout(() => this.fail(), 15000);
  }
  private capture() {
    if (this.running) {
      this.elapsed += Date.now() - this.started;
      this.started = Date.now();
    }
  }
  private clearTimers() {
    clearTimeout(this.timer);
    clearTimeout(this.stall);
  }
  private schedule() {
    clearTimeout(this.timer);
    if (!this.running) return;
    this.capture();
    if (this.speechDone) {
      clearTimeout(this.stall);
      this.timer = setTimeout(
        () => this.advance(),
        Math.max(0, this.pace - this.elapsed),
      );
    } else {
      const limit = (this.clips[this.frame]?.duration ?? 0) * 1000 + 20000;
      this.timer = setTimeout(
        () => this.fail(),
        Math.max(0, limit - this.elapsed),
      );
    }
  }
  private advance() {
    if (!this.running) return;
    if (this.frame === this.count - 1) {
      this.pause();
      this.finished = true;
      this.onStop();
    } else {
      const next = this.frame + 1;
      this.select(next);
      this.onFrame(next);
      this.start(next);
    }
  }
}
