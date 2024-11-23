<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";
import { validateInput } from "./validation";
import { useLoadingStore } from "./loading";

import LoadingView from "./Loading.vue";

const router = useRouter();
const authStore = useAuthStore();
const loadingStore = useLoadingStore();

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
    if (e.response.data.detail === "Incorrect username or password") {
      error.value = "ユーザー名またはパスワードが間違っています";
    } else {
      error.value = e.response.data.detail;
    }
    alert("ログインに失敗しました");
  }
};

const signup = async () => {
  const valRes = validateInput(username.value, email.value, password.value);
  if (valRes) {
    error.value = valRes;
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
    if (e.response.data.detail === "Username already registered") {
      error.value = "ユーザー名は既に使用されています";
    } else if (e.response.data.detail === "Email already registered") {
      error.value = "メールアドレスは既に使用されています";
    } else {
      error.value = e.response.data.detail;
    }
    alert("登録に失敗しました");
  }
};
</script>

<template>
  <div class="container" v-if="!loadingStore.isLoading">
    <h1 class="title">新規登録</h1>
    <form class="multiple-input-form" @submit.prevent="signup">
      <div v-if="error" class="error-message">{{ error }}</div>
      <div class="labeled-text-input">
        <label for="username">ユーザー名</label>
        <input
          class="text-input"
          type="text"
          v-model="username"
          placeholder="ユーザー名を入力してください"
          required
        />
      </div>
      <div class="labeled-text-input">
        <label for="email">メールアドレス</label>
        <input
          class="text-input"
          type="email"
          v-model="email"
          placeholder="example@xxxx.com"
          required
        />
      </div>
      <div class="labeled-text-input">
        <label for="password">パスワード</label>
        <input
          class="text-input"
          type="password"
          v-model="password"
          placeholder="パスワードを入力してください"
          required
        />
      </div>
      <button id="signup-button" class="primary-button" type="submit">
        新規登録
      </button>
    </form>
  </div>
  <LoadingView v-else />
</template>

<style scoped>
#signup-button {
  margin: 3rem auto 0 auto;
}
</style>
