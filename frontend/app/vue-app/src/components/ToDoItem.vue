<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";

import YouTube from "./YouTube.vue";
import Timer from "./ToDoTimer.vue";

const authStore = useAuthStore();

const routeId = useRoute().params.id;
const error = ref(null);

const isMenuOpen = ref(false);
const title = ref("");
const timeToComplete = ref(null);

// タスク情報を取得
onMounted(async () => {
  try {
    const response = await requestAPI.get(`/todo-list/${routeId}`, {
      withCredentials: true,
    });

    if (!response.data) return;
    title.value = response.data.title;
    timeToComplete.value = response.data.time_to_complete;
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("タスク情報の取得に失敗しました");
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
  }
});
</script>

<template>
  <div class="container">
    <div v-if="error" class="error-message">{{ error }}</div>
    <div id="title">
      <img
        alt="App logo"
        class="logo"
        src="@/assets/todo-logo2.svg"
        width="35"
        height="35"
      />
      <h1 style="margin-left: 1rem; font-weight: bold">{{ title }}</h1>
      <button id="toggle-button" @click="isMenuOpen = !isMenuOpen">
        <img
          v-if="!isMenuOpen"
          src="@/assets/arrow-down.svg"
          width="25"
          height="25"
        />
        <img v-else src="@/assets/arrow-up.svg" width="25" height="25" />
      </button>
    </div>
    <Transition>
      <YouTube v-show="isMenuOpen" />
    </Transition>
    <Timer :timeToComplete="timeToComplete" v-if="timeToComplete != null" />
  </div>
</template>

<style scoped>
#title {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 0.5rem 1.5rem;
  background-color: var(--color-gray);
  border-radius: 8px;
}

.logo {
  margin: 0 0 0 1rem;
}

#toggle-button {
  margin: 0 0 0 auto;
  padding: 0.5rem;
  background-color: var(--color-gray);
  border-radius: 100%;
}

@media (hover: hover) {
  #toggle-button:hover {
    background-color: var(--color-gray-hover);
  }
}

.v-enter-active {
  animation: fall-in 0.5s;
}

.v-leave-active {
  animation: fall-in 0.5s reverse;
}

@keyframes fall-in {
  0% {
    opacity: 0;
    transform: translateY(-5px);
  }
  100% {
    opacity: 1;
    transform: translateY(5px);
  }
}
</style>
