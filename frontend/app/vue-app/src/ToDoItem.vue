<script setup>
import { ref, onMounted, computed } from "vue";
import Timer from "@/Timer";

const timeType = {
  task: 25 * 60,
  break: 5 * 60,
  longBreak: 15 * 60,
};

const taskPlan = [
  timeType.task,
  timeType.break,
  timeType.task,
  timeType.break,
  timeType.task,
  timeType.break,
  timeType.task,
  timeType.longBreak,
];

let timer;
let taskIndex = 0;
let currentTask = 0;
const circumference = 2 * Math.PI * 45;
const remainingTime = ref(0);
const isTimerRunning = ref(false);

onMounted(() => {
  currentTask = taskPlan[taskIndex];
  remainingTime.value = currentTask;
  timer = new Timer(remainingTime.value, updateTime, timerEnded);
});

const progressOffset = computed(() => {
  return circumference - (remainingTime.value / currentTask) * circumference;
});

const formattedTime = computed(() => {
  if (!remainingTime.value) return "00:00";
  const minutes = String(Math.floor(remainingTime.value / 60)).padStart(2, "0");
  const seconds = String(remainingTime.value % 60).padStart(2, "0");
  return `${minutes}:${seconds}`;
});

const updateTime = () => {
  remainingTime.value = timer.getRemainingTime();
};

const timerEnded = () => {
  // alert("Time's up!");
  currentTask = getNextTask();
  setTimeout(() => {
    remainingTime.value = currentTask;
    timer.setTime(remainingTime.value);
    timer.start();
  }, 1000);
};

const start = () => {
  isTimerRunning.value = true;
  timer.start();
};

const pause = () => {
  isTimerRunning.value = false;
  timer.pause();
};

const stop = () => {
  isTimerRunning.value = false;
  timer.reset();
  remainingTime.value = currentTask;
  timer.setTime(remainingTime.value);
};

const getNextTask = () => {
  taskIndex += 1;
  if (taskIndex >= taskPlan.length) taskIndex = 0;
  return taskPlan[taskIndex];
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
        src="./assets/todo-logo2.svg"
        width="35"
        height="35"
      />
      <h1 class="todo-title">{{ $route.params.title }}</h1>
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
      <div class="timer-button">
        <button v-if="!isTimerRunning" @click="start()">スタート</button>
        <button v-else @click="pause()">一時停止</button>
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
  transition: 0.3s;
}

.progress-circle {
  display: flex;
  align-items: center;
  margin: auto;
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

.timer-button {
  display: flex;
  justify-content: center;
  margin: 5% 0;
}

.timer-button button {
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
