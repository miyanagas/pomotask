<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";

const router = useRouter();

const username = ref("");
const password = ref("");

const error = ref(null);

const login = async () => {
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
      }
    );
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
      <div v-if="error">{{ error }}</div>
      <div class="form-group">
        <label for="username">ユーザー名</label>
        <input
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
          class="login-input"
          type="password"
          v-model="password"
          placeholder="パスワードを入力してください"
          required
        />
      </div>
      <div class="login-buttons">
        <button class="login-button" type="submit">ログイン</button>
        <button class="login-button" @click="this.$router.push('/signup')">
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

.login-button {
  padding: 0.5rem 1rem;
  margin: 0.5rem 1rem;
  border-radius: 4px;
  background-color: var(--color-primary);
  color: var(--color-text-white);
}

@media (hover: hover) {
  .login-button:hover {
    background-color: var(--color-primary-hover);
  }

  .signup-button:hover {
    background-color: var(--color-secondary-hover);
  }
}
</style>
