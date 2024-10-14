<script setup></script>

<template>
  <header>
    <router-link to="/" class="title">今日のToDo</router-link>
    <img
      alt="App logo"
      class="logo"
      src="./assets/todo-logo.svg"
      width="35"
      height="35"
    />
  </header>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
.logo {
  display: block;
}

header {
  background-color: var(--color-primary);
  color: var(--color-text-white);
  padding: 1rem;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-direction: row;
}

.title {
  margin: 0;
  padding: 0.5rem 1rem 0.5rem 2rem;
  color: var(--color-text-white);
  font-size: 32px;
}
</style>
