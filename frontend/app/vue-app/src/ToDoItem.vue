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
const remainingTime = ref(0);
const isTimerRunning = ref(false);

onMounted(() => {
  remainingTime.value = taskPlan[taskIndex];
  timer = new Timer(remainingTime.value, updateTime, timerEnded);
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
  alert("Time's up!");
  const nextTask = getNextTask();
  remainingTime.value = timeType[nextTask];
  timer.setTime(remainingTime.value);
  timer.start();
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
  remainingTime.value = 0;
  taskIndex = 0;
  timer.setTime(taskPlan[taskIndex]);
};

const getNextTask = () => {
  taskIndex++;
  if (taskIndex >= taskPlan.length) taskIndex = 0;
  return taskPlan[taskIndex];
};
</script>

<template>
  <div class="container">
    <button class="back-button" @click="$router.push('/')">Back</button>
    <h2 class="todo-title">{{ $route.params.title }}</h2>
    <div class="todo-timer">
      <div class="timer-screen">
        <p>{{ formattedTime }}</p>
      </div>
      <button class="timer-button" v-if="!isTimerRunning" @click="start()">
        Start
      </button>
      <button class="timer-button" v-else @click="pause()">Pause</button>
      <button class="timer-button" @click="stop()">Stop</button>
    </div>
  </div>
</template>
