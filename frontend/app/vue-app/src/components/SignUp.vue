<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";
import { validateInput } from "./validation";

const router = useRouter();
const authStore = useAuthStore();

const username = ref("");
const email = ref("");
const password = ref("");

const error = ref(null);

const login = async (username, password) => {
  try {
    await requestAPI.post(
      "/token/",
      {
        username: username,
        password: password,
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

const signup = async () => {
  const valRes = validateInput(username.value, email.value, password.value);
  if (valRes) {
    error.value = valRes;
    alert("入力内容を確認してください");
    return;
  }

  try {
    await requestAPI.post("/users/signup/", {
      username: username.value,
      email: email.value,
      password: password.value,
    });
    await login(username.value, password.value);
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("登録に失敗しました");
  }
};
</script>

<template>
  <div class="container">
    <h1 class="title">新規登録</h1>
    <form class="signup-form" @submit.prevent="signup">
      <div v-if="error" class="error-message">{{ error }}</div>
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
        <label for="email">メールアドレス</label>
        <input
          class="login-input"
          type="email"
          v-model="email"
          placeholder="example@xxxx.com"
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
      <button style="margin: 2rem" class="primary-button" type="submit">
        新規登録
      </button>
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
  margin-bottom: 1rem;
}

.signup-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.login-input {
  width: 400px;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin: 0.5rem;
  font-size: 16px;
}
</style>
