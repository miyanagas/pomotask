<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";
import { validateInput } from "./validation";

const router = useRouter();
const authStore = useAuthStore();

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
  <div class="container">
    <h1 class="title">ログイン</h1>
    <form class="login-form" @submit.prevent="login">
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div class="form-group">
        <label for="username">ユーザー名</label>
        <input
          id="username"
          class="login-input"
          type="text"
          v-model="username"
          placeholder="ユーザー名を入力してください"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">パスワード</label>
        <input
          id="password"
          class="login-input"
          type="password"
          v-model="password"
          placeholder="パスワードを入力してください"
          required
        />
      </div>
      <div class="login-buttons">
        <button
          style="margin: 0.5rem 1rem"
          class="primary-button"
          type="submit"
        >
          ログイン
        </button>
        <button
          style="margin: 0.5rem 1rem"
          class="primary-button"
          @click="router.push('/signup')"
        >
          新規登録
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 2rem;
  margin: 1rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin: 1rem;
}

.login-input {
  width: 400px;
  padding: 0.5rem;
  margin: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 16px;
}

.login-buttons {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 1rem;
  margin: 1rem;
}
</style>
