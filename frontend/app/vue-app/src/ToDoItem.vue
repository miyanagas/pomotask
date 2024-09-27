<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from "vue";
import Timer from "@/Timer";
import alarm from "@/assets/sound-alarm.mp3";

const defaultTaskTime = 25;
const defaultBreakTime = 5;
const seconds = 60;

const taskTime = ref(defaultTaskTime);
const breakTime = ref(defaultBreakTime);

let timeType = {
  task: taskTime.value * seconds,
  break: breakTime.value * seconds,
};

let timer;
let currentTimer;
const circumference = 2 * Math.PI * 45;
const remainingTime = ref(0);
const isTimerRunning = ref(false);
const isMenuOpen = ref(false);
const youtubeUrl = ref("");

onMounted(() => {
  currentTimer = timeType.task;
  remainingTime.value = currentTimer;
  timer = new Timer(remainingTime.value, updateTime, timerEnded);
});

onBeforeUnmount(() => {
  if (timer.getIsTimerRunning()) timer.reset();
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

const updateTime = () => {
  remainingTime.value = timer.getRemainingTime();
};

const timerEnded = () => {
  // alert("Time's up!");
  const audio = new Audio(alarm);
  audio.play();
  currentTimer =
    currentTimer === timeType.task ? timeType.break : timeType.task;
  setTimeout(() => {
    remainingTime.value = currentTimer;
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
  remainingTime.value = currentTimer;
  timer.setTime(remainingTime.value);
};

const getYouTubeId = (url) => {
  const regExp =
    /^(https:\/\/www\.youtube\.com\/watch\?v=|https:\/\/youtu\.be\/)([a-zA-Z0-9-_]+)(\?|$)/;
  const match = url.match(regExp);
  return match ? match[2] : null;
};

const roadYouTube = () => {
  const youtubeId = getYouTubeId(youtubeUrl.value);
  youtubeUrl.value = "";
  if (youtubeId) {
    const iframe = document.querySelector("iframe");
    iframe.width = "640";
    iframe.height = "360";
    iframe.src = `https://www.youtube.com/embed/${youtubeId}`;
  } else {
    alert("無効なURLです");
  }
};

const customizeTimer = () => {
  if (timer.getIsTimerRunning()) {
    timer.reset();
    isTimerRunning.value = false;
  }
  timeType.task = taskTime.value * seconds;
  timeType.break = breakTime.value * seconds;
  currentTimer = timeType.task;
  remainingTime.value = currentTimer;
  timer.setTime(remainingTime.value);
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
      <button v-if="!isMenuOpen" @click="isMenuOpen = !isMenuOpen">
        <img
          id="toggle-button"
          src="./assets/arrow-down.svg"
          width="25"
          height="25"
        />
      </button>
      <button v-else @click="isMenuOpen = !isMenuOpen">
        <img
          id="toggle-button"
          src="./assets/arrow-up.svg"
          width="25"
          height="25"
        />
      </button>
    </div>
    <div v-show="isMenuOpen" class="video-container">
      <div class="video-input-form">
        <input type="text" v-model="youtubeUrl" placeholder="YouTube URL" />
        <button @click="roadYouTube()">ロード</button>
      </div>
      <iframe
        width="0"
        height="0"
        src=""
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin"
        allowfullscreen
      ></iframe>
    </div>
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

.video-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 1rem auto;
  width: 55%;
}

.video-input-form {
  display: flex;
  justify-content: center;
  width: 50%;
  margin: 0rem auto 1rem auto;
}

.video-input-form input {
  width: 60%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin: 0 0.5rem 0 0;
  font-size: 14px;
}

.video-input-form button {
  padding: 0.5rem 1rem;
  margin: 0 0 0 0.5rem;
  border: 1px solid black;
  border-radius: 4px;
  background-color: red;
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
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
