<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";
import { useLoadingStore } from "./loading";
import { validateInput } from "./validation";

import LoadingView from "./Loading.vue";

const router = useRouter();
const authStore = useAuthStore();
const loadingStore = useLoadingStore();

const username = ref("");
const password = ref("");

const error = ref(null);

const login = async () => {
  const valRes = validateInput(username.value, null, password.value);
  if (valRes) {
    error.value = valRes;
    alert("入力内容を確認してください");
    return;
  }

  try {
    await requestAPI.post(
      "/token/",
      {
        username: username.value,
        password: password.value,
      },
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        withCredentials: true,
      }
    );
    authStore.login();
    router.push("/");
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("ログインに失敗しました");
  }
};
</script>

<template>
  <div class="container" v-if="!loadingStore.isLoading">
    <h1 class="title">ログイン</h1>
    <form class="multiple-input-form" @submit.prevent="login">
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div class="labeled-text-input">
        <label for="username">ユーザー名</label>
        <input
          id="username"
          class="text-input"
          type="text"
          v-model="username"
          placeholder="ユーザー名を入力してください"
          required
        />
      </div>
      <div class="labeled-text-input">
        <label for="password">パスワード</label>
        <input
          id="password"
          class="text-input"
          type="password"
          v-model="password"
          placeholder="パスワードを入力してください"
          required
        />
      </div>
      <div style="margin-top: 3rem" class="flex-center-container">
        <button class="primary-button login-button" type="submit">
          ログイン
        </button>
        <button
          class="primary-button login-button"
          @click="router.push('/signup')"
        >
          新規登録
        </button>
      </div>
    </form>
  </div>
  <LoadingView v-else />
</template>

<style scoped>
.login-button {
  margin: 0 1rem;
}
</style>
