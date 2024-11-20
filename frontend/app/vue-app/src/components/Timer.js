class Timer {
  constructor(time, onTick, onEnd) {
    this.remainingTime = time;
    this.isTimerRunning = false;
    this.intervalId = null;
    this.onTick = onTick;
    this.onEnd = onEnd;
  }

  setTime(time) {
    this.remainingTime = time;
  }

  getRemainingTime() {
    return this.remainingTime;
  }

  getIsTimerRunning() {
    return this.isTimerRunning;
  }

  start() {
    this.isTimerRunning = true;
    this.intervalId = setInterval(() => {
      this.remainingTime -= 1;
      this.onTick();
      if (this.remainingTime <= 0) {
        this.stop();
      }
    }, 1000);
  }

  pause() {
    this.isTimerRunning = false;
    clearInterval(this.intervalId);
  }

  stop() {
    this.isTimerRunning = false;
    clearInterval(this.intervalId);
    this.remainingTime = 0;
    this.onEnd();
  }

  reset() {
    this.isTimerRunning = false;
    clearInterval(this.intervalId);
    this.remainingTime = 0;
  }
}

const timeFormat = (time) => {
  const hours = Math.floor(time / 60 / 60);
  const minutes = String(Math.floor(time / 60) % 60).padStart(2, "0");
  const seconds = String(time % 60).padStart(2, "0");
  if (hours === 0) {
    return `${minutes}:${seconds}`;
  }
  return `${hours}:${minutes}:${seconds}`;
};

export { Timer, timeFormat };
