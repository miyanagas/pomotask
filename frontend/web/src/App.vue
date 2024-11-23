<script setup>
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
  <header v-if="!route.meta.hideHeader">
    <router-link to="/" id="header-title" class="title">今日のToDo</router-link>
    <img
      alt="App logo"
      class="icon"
      src="./assets/todo-logo.svg"
      width="35"
      height="35"
    />
    <router-link to="/mypage" class="title" id="mypage-link"
      ><img
        alt="My page"
        class="icon"
        src="./assets/user.svg"
        width="35"
        height="35"
      />
    </router-link>
  </header>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
header {
  background-color: var(--color-primary);
  color: var(--color-text-white);
  padding: 1rem;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  flex-direction: row;
}

#header-title {
  margin: 0 0 0 1rem;
  color: var(--color-text-white);
}

#mypage-link {
  margin: 0 2rem 0 auto;
  padding: 0;
}
</style>
