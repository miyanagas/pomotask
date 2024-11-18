<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from "vue";
import alarm from "@/assets/sound-alarm.mp3";
import requestAPI from "./requestAPI";
import { useRoute } from "vue-router";

const defaultTaskTime = 25;
const defaultBreakTime = 5;
const taskTime = ref(defaultTaskTime);
const breakTime = ref(defaultBreakTime);
const seconds = 60;
const circumference = 2 * Math.PI * 45;
const routeId = useRoute().params.id;

let timeType = {
  task: taskTime.value * seconds,
  break: breakTime.value * seconds,
};
let isTimerRunning;
let currentTimer;
let totalPassedTime;

const timerWorker = ref(
  new Worker(new URL("./timerWorker.js", import.meta.url))
);
const remainingTime = ref(0);
const error = ref(null);

const progressOffset = computed(() => {
  return circumference - (remainingTime.value / currentTimer) * circumference;
});

const formattedTime = computed(() => {
  return convertToTime(remainingTime.value);
});

const formattedTotalTime = computed(() => {
  const hours = Math.floor(
    (currentTimer - remainingTime.value + totalPassedTime) / 60 / 60
  );
  if (hours === 0) {
    return convertToTime(currentTimer - remainingTime.value + totalPassedTime);
  }
  return `${hours}:${convertToTime(
    currentTimer - remainingTime.value + totalPassedTime
  )}`;
});

const convertToTime = (time) => {
  const minutes = String(Math.floor(time / 60) % 60).padStart(2, "0");
  const seconds = String(time % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
};

onMounted(async () => {
  try {
    const token = localStorage.getItem("access_token");
    const response = await requestAPI.get(`/todo-list/${routeId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (!response.data) return;
    totalPassedTime = response.data.time_to_complete;
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoの取得に失敗しました");
  }
  setTimer(timeType.task);
});

onBeforeUnmount(async () => {
  timerWorker.value.postMessage({ command: "stop" });
  await updateTimeToComplete(
    totalPassedTime + currentTimer - remainingTime.value
  );
});

timerWorker.value.addEventListener("message", (e) => {
  remainingTime.value = e.data.time;
  isTimerRunning = e.data.isRunning;
  if (remainingTime.value <= 0) timerEnded();
});

const updateTimeToComplete = async (timeToComplete) => {
  try {
    const token = localStorage.getItem("access_token");
    await requestAPI.put(
      `/todo-list/${routeId}`,
      {
        time_to_complete: timeToComplete,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoの更新に失敗しました");
  }
};

// Timer functions
const setTimer = (time) => {
  currentTimer = time;
  remainingTime.value = currentTimer;
  timerWorker.value.postMessage({ command: "set", time: remainingTime.value });
};

const timerEnded = () => {
  const audio = new Audio(alarm);
  audio.play();
  currentTimer =
    currentTimer === timeType.task ? timeType.break : timeType.task;
  setTimeout(async () => {
    totalPassedTime += currentTimer;
    await updateTimeToComplete(totalPassedTime);
    setTimer(currentTimer);
    timerWorker.value.postMessage({ command: "start" });
  }, 1000);
};

// Timer control button functions
const play = () => {
  if (isTimerRunning) {
    timerWorker.value.postMessage({ command: "stop" });
    document.getElementById("timer-play-button").textContent = "再開";
  } else {
    timerWorker.value.postMessage({ command: "start" });
    document.getElementById("timer-play-button").textContent = "一時停止";
  }
};

const stop = async () => {
  timerWorker.value.postMessage({ command: "stop" });
  document.getElementById("timer-play-button").textContent = "スタート";
  totalPassedTime += currentTimer - remainingTime.value;
  await updateTimeToComplete(totalPassedTime);
  setTimer(currentTimer);
};

const customize = () => {
  timerWorker.value.postMessage({ command: "stop" });
  document.getElementById("timer-play-button").textContent = "スタート";
  timeType.task = taskTime.value * seconds;
  timeType.break = breakTime.value * seconds;
  setTimer(timeType.task);
};
</script>

<template>
  <div class="todo-timer">
    <div id="timer-screen">
      <div id="timer-progress">
        <svg class="progress-svg" viewBox="0 0 100 100">
          <circle class="progress-background" cx="50" cy="50" r="45"></circle>
          <circle
            class="progress-bar"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="progressOffset"
            cx="50"
            cy="50"
            r="45"
          ></circle>
        </svg>
      </div>
      <span>{{ formattedTime }}</span>
    </div>
    <div id="total-time-display">
      <span>総時間</span>
      <span id="total-time">{{ formattedTotalTime }}</span>
    </div>
    <div id="timer-buttons">
      <button id="timer-play-button" @click="play()">スタート</button>
      <button @click="stop()">リセット</button>
    </div>
    <div id="timer-customize">
      <div class="time-selector">
        <label for="task-time">タスク時間</label>
        <select v-model="taskTime" id="task-time">
          <option value="5">5分</option>
          <option value="10">10分</option>
          <option value="15">15分</option>
          <option value="20">20分</option>
          <option value="25">25分</option>
          <option value="30">30分</option>
          <option value="35">35分</option>
          <option value="40">40分</option>
          <option value="45">45分</option>
          <option value="50">50分</option>
          <option value="55">55分</option>
          <option value="60">60分</option>
          <option value="65">65分</option>
          <option value="70">70分</option>
          <option value="75">75分</option>
          <option value="80">80分</option>
          <option value="85">85分</option>
          <option value="90">90分</option>
        </select>
      </div>
      <div class="time-selector">
        <label for="break-time">休憩時間</label>
        <select v-model="breakTime" id="break-time">
          <option value="5">5分</option>
          <option value="10">10分</option>
          <option value="15">15分</option>
          <option value="20">20分</option>
          <option value="25">25分</option>
          <option value="30">30分</option>
        </select>
      </div>
      <button @click="customize()">設定</button>
    </div>
  </div>
</template>

<style scoped>
.todo-timer {
  width: 55%;
  margin: 0.5rem auto;
  padding: 1rem;
}

#timer-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  border: 2px solid var(--color-border);
  border-radius: 4px;
}

#timer-screen span {
  font-size: 128px;
  font-family: "Lucida Console", monospace;
  margin: 8px 8px 8px 64px;
  padding: 8px;
}

#timer-progress {
  display: flex;
  align-items: center;
  margin: auto 0;
  width: 200px;
  height: 200px;
}

.progress-svg {
  transform: rotate(-90deg) scale(1, -1);
}

.progress-background {
  fill: none;
  stroke: var(--color-gray);
  stroke-width: 10;
}

.progress-bar {
  fill: none;
  stroke: var(--color-text-blue);
  stroke-width: 10;
  stroke-linecap: round;
  transition: stroke-dashoffset 1s linear;
}

#total-time-display {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin: 0.5em 1em;
  font-size: 1em;
}

#total-time {
  font-family: "Lucida Console", monospace;
  font-size: 1.5em;
  margin: 0 0 0 0.25em;
  padding: 0 0.5em;
  border: 1px solid var(--color-border);
  border-radius: 4px;
}

#timer-buttons {
  display: flex;
  justify-content: center;
}

#timer-buttons button {
  width: 130px;
  font-size: 24px;
  padding: 0.5rem 1rem;
  margin: 1.5rem;
  border-radius: 4px;
  background-color: var(--color-primary);
  color: var(--color-text-white);
}

@media (hover: hover) {
  #timer-buttons button:hover {
    background-color: var(--color-primary-hover);
  }
}

#timer-customize {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 3rem auto 5rem auto;
}

.time-selector {
  display: flex;
  align-items: center;
  margin: 0 0.5rem;
}

.time-selector label {
  font-size: 16px;
  margin: 0 0.5rem 0 0;
}

.time-selector select {
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 16px;
}

#timer-customize button {
  padding: 0.5rem 1rem;
  margin: 0 0 0 0.5rem;
  border-radius: 4px;
  background-color: var(--color-primary);
  color: var(--color-text-white);
  font-weight: bold;
}

@media (hover: hover) {
  #timer-customize button:hover {
    background-color: var(--color-primary-hover);
  }
}
</style>
