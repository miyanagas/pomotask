<script setup>
import { ref } from "vue";
import YouTube from "./YouTube.vue";
import Timer from "./ToDoTimer.vue";

const isMenuOpen = ref(false);
</script>

<template>
  <div class="container">
    <div class="todo-header">
      <button class="back-button" @click="$router.push('/')">戻る</button>
    </div>
    <div id="todo-title-headline">
      <img
        alt="App logo"
        class="logo"
        src="@/assets/todo-logo2.svg"
        width="35"
        height="35"
      />
      <h1 id="todo-title">{{ $route.params.title }}</h1>
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
    <Transition>
      <YouTube v-show="isMenuOpen" />
    </Transition>
    <Timer />
  </div>
</template>

<style scoped>
.todo-header {
  display: flex;
  padding: 1rem;
  justify-content: flex-start;
}

.back-button {
  padding: 0.5rem 1rem;
  font-size: 16px;
  margin: 0 0% 0 0;
  background-color: var(--color-primary-text);
  border: 4px solid var(--color-primary);
  border-radius: 4px;
  color: var(--color-primary);
  font-weight: bold;
  cursor: pointer;
}

.back-button:hover {
  background-color: var(--color-primary);
  color: var(--color-primary-text);
}

#todo-title-headline {
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

#todo-title {
  margin: 0 1rem;
  font-weight: bold;
}

#todo-title-headline button {
  margin: 0 0 0 auto;
  padding: 0.5rem;
  background-color: #f1f1f1;
  border-radius: 100%;
  border: none;
  cursor: pointer;
}

#todo-title-headline button:hover {
  background-color: #e1e1e1;
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
