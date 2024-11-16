<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";

const router = useRouter();

const username = ref("");
const email = ref("");
const password = ref("");

const login = async (username, password) => {
  try {
    const response = await requestAPI.post(
      "/token/",
      {
        username: username,
        password: password,
      },
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );
    localStorage.setItem("token", response.data.access_token);
    router.push("/");
  } catch (e) {
    alert("ログインに失敗しました");
    console.error(e);
  }
};

const signup = async () => {
  try {
    await requestAPI.post("/users/signup/", {
      username: username.value,
      email: email.value,
      password: password.value,
    });
    await login(username.value, password.value);
  } catch (e) {
    alert("登録に失敗しました");
    console.error(e);
  }
};
</script>

<template>
  <div class="container">
    <h1 class="title">新規登録</h1>
    <form class="signup-form" @submit.prevent="signup">
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
      <button class="signup-button" type="submit">新規登録</button>
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

.signup-button {
  padding: 0.5rem 1rem;
  margin: 2rem;
  border-radius: 4px;
  background-color: var(--color-primary);
  color: var(--color-text-white);
}

@media (hover: hover) {
  .signup-button:hover {
    background-color: var(--color-primary-hover);
  }
}
</style>
