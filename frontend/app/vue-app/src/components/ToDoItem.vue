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
    <YouTube v-show="isMenuOpen" />
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
  background-color: white;
  border: 4px solid hsla(160, 100%, 37%, 1);
  border-radius: 4px;
  color: hsla(160, 100%, 37%, 1);
  font-weight: bold;
  cursor: pointer;
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
  border: none;
  cursor: pointer;
}
</style>
