<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from "vue";
import alarm from "@/assets/sound-alarm.mp3";
import requestAPI from "./requestAPI";
import { useRoute } from "vue-router";
import YouTube from "./YouTube.vue";

const defaultTaskTime = 25;
const defaultBreakTime = 5;
const seconds = 60;

const taskTime = ref(defaultTaskTime);
const breakTime = ref(defaultBreakTime);

let timeType = {
  task: taskTime.value * seconds,
  break: breakTime.value * seconds,
};

let isTimerRunning;
let currentTimer;
let totalPassedTime;
const timerWorker = new Worker(new URL("./timerWorker.js", import.meta.url));
const circumference = 2 * Math.PI * 45;
const remainingTime = ref(0);
const isMenuOpen = ref(false);
const routeId = useRoute().params.id;

const error = ref(null);

onMounted(async () => {
  await fetchToDoItem();
  currentTimer = timeType.task;
  remainingTime.value = currentTimer;
  timerWorker.postMessage({ command: "set", time: remainingTime.value });
});

onBeforeUnmount(async () => {
  timerWorker.postMessage({ command: "stop" });
  totalPassedTime += currentTimer - remainingTime.value;
  await updateToDoItem();
});

timerWorker.addEventListener("message", (e) => {
  remainingTime.value = e.data.time;
  isTimerRunning = e.data.isRunning;
  if (remainingTime.value <= 0) timerEnded();
});

const progressOffset = computed(() => {
  return circumference - (remainingTime.value / currentTimer) * circumference;
});

const formattedTime = computed(() => {
  if (!remainingTime.value) return "00:00";
  const minutes = String(Math.floor(remainingTime.value / 60)).padStart(2, "0");
  const seconds = String(remainingTime.value % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
});

const formattedTotalTime = computed(() => {
  const minutes = String(
    Math.floor((currentTimer - remainingTime.value + totalPassedTime) / 60)
  ).padStart(2, "0");
  const seconds = String(
    (currentTimer - remainingTime.value + totalPassedTime) % 60
  ).padStart(2, "0");
  return `${minutes}:${seconds}`;
});

const fetchToDoItem = async () => {
  try {
    const response = await requestAPI.get("/todolist/items", {
      params: {
        id: routeId,
      },
    });
    if (!response.data) return;
    totalPassedTime = response.data.time_to_complete;
  } catch (e) {
    error.value = e;
    console.log(e);
    alert("エラーが発生しました");
  }
};

const updateToDoItem = async () => {
  try {
    await requestAPI.post(`/todolist/items/${routeId}`, {
      time_to_complete: totalPassedTime,
    });
  } catch (e) {
    error.value = e;
    alert("エラーが発生しました");
  }
};

const timerEnded = () => {
  // alert("Time's up!");
  const audio = new Audio(alarm);
  audio.play();
  currentTimer =
    currentTimer === timeType.task ? timeType.break : timeType.task;
  setTimeout(async () => {
    totalPassedTime += currentTimer;
    await updateToDoItem();
    remainingTime.value = currentTimer;
    timerWorker.postMessage({ command: "set", time: remainingTime.value });
    timerWorker.postMessage({ command: "start" });
  }, 1000);
};

// Timer control functions
const play = () => {
  if (isTimerRunning) {
    timerWorker.postMessage({ command: "stop" });
    document.getElementById("timer-play-button").textContent = "再開";
  } else {
    timerWorker.postMessage({ command: "start" });
    document.getElementById("timer-play-button").textContent = "一時停止";
  }
};

const stop = async () => {
  timerWorker.postMessage({ command: "stop" });
  document.getElementById("timer-play-button").textContent = "スタート";
  totalPassedTime += currentTimer - remainingTime.value;
  await updateToDoItem();
  remainingTime.value = currentTimer;
  timerWorker.postMessage({ command: "set", time: remainingTime.value });
};

const customizeTimer = () => {
  timerWorker.postMessage({ command: "stop" });
  document.getElementById("timer-play-button").textContent = "スタート";
  timeType.task = taskTime.value * seconds;
  timeType.break = breakTime.value * seconds;
  currentTimer = timeType.task;
  remainingTime.value = currentTimer;
  timerWorker.postMessage({ command: "set", time: remainingTime.value });
};
</script>

<template>
  <div class="container">
    <div class="todo-header">
      <button class="back-button" @click="$router.push('/')">戻る</button>
    </div>
    <div class="todo-title-headline">
      <img
        alt="App logo"
        class="logo"
        src="@/assets/todo-logo2.svg"
        width="35"
        height="35"
      />
      <h1 class="todo-title">{{ $route.params.title }}</h1>
      <button @click="isMenuOpen = !isMenuOpen">
        <img
          v-if="!isMenuOpen"
          id="toggle-button"
          src="@/assets/arrow-down.svg"
          width="25"
          height="25"
        />
        <img
          v-else
          id="toggle-button"
          src="@/assets/arrow-up.svg"
          width="25"
          height="25"
        />
      </button>
    </div>
    <YouTube v-show="isMenuOpen" />
    <div class="timer-customize">
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
      <button @click="customizeTimer()">設定</button>
    </div>
    <div class="todo-timer">
      <div class="timer-screen">
        <div class="progress-circle">
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
      <div class="timer-button">
        <button id="timer-play-button" @click="play()">スタート</button>
        <button @click="stop()">リセット</button>
      </div>
    </div>
  </div>
</template>

<style>
.todo-header {
  display: flex;
  padding: 1rem;
  justify-content: flex-start;
}

.back-button {
  padding: 0.5rem 1rem;
  font-size: 16px;
  margin: 0 0% 0 0;
  background-color: white;
  border: 4px solid hsla(160, 100%, 37%, 1);
  border-radius: 4px;
  color: hsla(160, 100%, 37%, 1);
  font-weight: bold;
  cursor: pointer;
}

.todo-title-headline {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  width: 55%;
  margin: 0 auto;
  padding: 0.5rem 1.5rem;
  background-color: #f1f1f1;
  /* border: 3px solid #ccc; */
  border-radius: 8px;
}

.logo {
  margin: 0 0 0 1rem;
}

.todo-title {
  margin: 0 1rem;
  font-weight: bold;
}

.todo-title-headline button {
  margin: 0 0 0 auto;
  padding: 0.5rem;
  background-color: #f1f1f1;
  border: none;
  cursor: pointer;
}

.todo-timer {
  width: 55%;
  margin: 0.5rem auto;
  padding: 1rem;
}

.timer-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  border: 2px solid #ccc;
  border-radius: 4px;
}

.timer-screen span {
  font-size: 128px;
  font-family: "Lucida Console", monospace;
  margin: 8px 8px 8px 64px;
  padding: 8px;
}

.timer-customize {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 1rem auto 0.5rem auto;
  width: 55%;
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
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.timer-customize button {
  padding: 0.5rem 1rem;
  margin: 0 0 0 0.5rem;
  border: 1px solid lightseagreen;
  border-radius: 4px;
  background-color: lightseagreen;
  color: white;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
}

.progress-circle {
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
  stroke: #e6e6e6;
  stroke-width: 10;
}

.progress-bar {
  fill: none;
  stroke: lightseagreen;
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
  border: 1px solid #ccc;
  border-radius: 4px;
}

.timer-button {
  display: flex;
  justify-content: center;
}

.timer-button button {
  width: 130px;
  font-size: 24px;
  padding: 0.5rem 1rem;
  margin: 1.5rem;
  border: 1px solid hsla(160, 100%, 37%, 1);
  border-radius: 4px;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  cursor: pointer;
}
</style>
