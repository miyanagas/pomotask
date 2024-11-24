<script setup>
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
  <header>
    <router-link to="/" id="header-title" class="title">PomoTask</router-link>
    <img alt="App logo" class="icon" src="./assets/todo-logo.svg" />
    <router-link
      to="/mypage"
      class="title"
      id="mypage-link"
      v-if="route.meta.requiresAuth"
    >
      <img alt="My page" class="icon" src="./assets/user.svg" />
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

@media screen and (max-width: 490px) {
  #header-title {
    margin: 0;
  }
}

#mypage-link {
  margin: 0 2rem 0 auto;
  padding: 0;
}

@media screen and (max-width: 490px) {
  #mypage-link {
    margin-right: 1rem;
  }
}
</style>
