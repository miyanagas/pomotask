<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import requestAPI from "./requestAPI";
import { useLoadingStore } from "./loading";

import YouTube from "./YouTube.vue";
import Timer from "./ToDoTimer.vue";
import LoadingView from "./Loading.vue";

const routeId = useRoute().params.id;
const loadingStore = useLoadingStore();
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
    if (e.response.data.detail === "Todo not found") {
      error.value = "Todoが見つかりませんでした";
    } else {
      error.value = e.response.data.detail;
    }
    alert("Todo情報の取得に失敗しました");
  }
});
</script>

<template>
  <div class="container" v-if="!loadingStore.isLoading">
    <div v-if="error" class="error-message">{{ error }}</div>
    <div id="todo-titlebar">
      <img
        id="todo-logo"
        alt="App logo"
        class="icon"
        src="@/assets/todo-logo2.svg"
      />
      <h1 id="todo-title">
        {{ title }}
      </h1>
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
  <LoadingView v-else />
</template>

<style scoped>
#todo-titlebar {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 0.5rem 1.5rem;
  background-color: var(--color-gray);
  border-radius: 8px;
}

#todo-logo {
  margin-left: 1rem;
}

@media screen and (max-width: 490px) {
  #todo-logo {
    margin: 0;
  }
}

#todo-title {
  margin-left: 1rem;
  font-weight: bold;
}

@media screen and (max-width: 490px) {
  #todo-title {
    font-size: 1.5rem;
  }
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
