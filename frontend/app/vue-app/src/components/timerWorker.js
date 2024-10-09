let intervalId = null;
let isRunning = false;
let remainingTime = 0;

self.addEventListener(
  "message",
  (e) => {
    let command = e.data.command;

    if (command === "set") {
      remainingTime = e.data.time;
      self.postMessage({ time: remainingTime, isRunning: isRunning });
    } else if (command === "start") {
      intervalId = setInterval(() => {
        remainingTime -= 1;
        if (remainingTime <= 0) {
          clearInterval(intervalId);
          isRunning = false;
        }
        self.postMessage({ time: remainingTime, isRunning: isRunning });
      }, 1000);
      isRunning = true;
    } else if (command === "stop") {
      clearInterval(intervalId);
      isRunning = false;
      self.postMessage({ time: remainingTime, isRunning: isRunning });
    }
  },
  false
);
