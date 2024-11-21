<script setup>
import { ref, onMounted, computed } from "vue";
import alarm from "@/assets/sound-alarm.mp3";
import requestAPI from "./requestAPI";
import { useRoute, useRouter, onBeforeRouteLeave } from "vue-router";
import { useAuthStore } from "@/auth";
import { timeFormat } from "./time";

const props = defineProps({
  timeToComplete: {
    type: Number,
    required: true,
  },
});

const routeId = useRoute().params.id;
const router = useRouter();
const authStore = useAuthStore();

const defaultTaskTime = 25;
const defaultBreakTime = 5;
const taskTime = ref(defaultTaskTime);
const breakTime = ref(defaultBreakTime);
const seconds = 60;
const circumference = 2 * Math.PI * 45;

const timeToComplete = ref(props.timeToComplete);

let timeType = {
  task: taskTime.value * seconds,
  break: breakTime.value * seconds,
};
let isTimerRunning;
let currentTimer;

const timerWorker = ref(
  new Worker(new URL("./timerWorker.js", import.meta.url))
);
const remainingTime = ref(0);
const error = ref(null);

const progressOffset = computed(() => {
  return circumference - (remainingTime.value / currentTimer) * circumference;
});

const formattedTime = computed(() => {
  return timeFormat(remainingTime.value);
});

const formattedTotalTime = computed(() => {
  return timeFormat(currentTimer - remainingTime.value + timeToComplete.value);
});

onMounted(() => {
  setTimer(timeType.task);
});

onBeforeRouteLeave((to, from, next) => {
  timerWorker.value.postMessage({ command: "stop" });
  next();
});

timerWorker.value.addEventListener("message", (e) => {
  remainingTime.value = e.data.time;
  isTimerRunning = e.data.isRunning;
  if (remainingTime.value <= 0) timerEnded();
});

const updateTodo = async (completed = false) => {
  try {
    const response = await requestAPI.patch(
      `/todo-list/${routeId}`,
      {
        completed: completed,
        time_to_complete:
          currentTimer - remainingTime.value + timeToComplete.value,
      },
      {
        withCredentials: true,
      }
    );

    if (completed) {
      router.push("/");
    } else {
      timeToComplete.value = response.data.time_to_complete;
    }
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("Todoの更新に失敗しました");
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
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
    await updateTodo();
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

const reset = () => {
  timerWorker.value.postMessage({ command: "stop" });
  document.getElementById("timer-play-button").textContent = "スタート";
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
      <button id="complete-todo" @click="updateTodo(true)">完了</button>
    </div>
    <div id="timer-buttons">
      <button id="timer-play-button" @click="play()">スタート</button>
      <button @click="reset()">リセット</button>
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

#complete-todo {
  padding: 0.5rem 1rem;
  margin-left: 0.5rem;
  border-radius: 4px;
  background-color: var(--color-primary);
  color: var(--color-text-white);
  font-size: 18px;
  font-weight: bold;
}
</style>
