export default class Timer {
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
