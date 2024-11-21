<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";
import { validateInput } from "./validation";

const router = useRouter();
const authStore = useAuthStore();

const currentPassword = ref("");
const newPassword = ref("");

const error = ref(null);

const updatePassword = async () => {
  const valRes = validateInput(null, null, newPassword.value);
  if (!valRes) {
    error.value = valRes;
    alert("入力内容を確認してください");
  }

  try {
    await requestAPI.put(
      "/users/me/password/",
      {
        current_password: currentPassword.value,
        new_password: newPassword.value,
      },
      {
        withCredentials: true,
      }
    );
    router.push("/mypage");
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("パスワードの変更に失敗しました");
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
  }
};
</script>

<template>
  <div class="container">
    <h1 class="title">パスワード変更</h1>
    <div v-if="error" class="error-message">{{ error }}</div>
    <form id="multiple-input-form" @submit.prevent="updatePassword">
      <div class="labeled-text-input">
        <label for="current-password" id="password-label"
          >現在のパスワード</label
        >
        <input
          type="password"
          id="current-password"
          class="text-input"
          required
        />
      </div>
      <div class="labeled-text-input">
        <label for="new-password" id="password-label">新しいパスワード</label>
        <input type="password" id="new-password" class="text-input" required />
      </div>
      <button id="password-update-button" class="update-button" type="submit">
        パスワードを変更
      </button>
    </form>
  </div>
</template>

<style scoped>
#password-label {
  font-size: 0.9rem;
}

#password-update-button {
  margin: 3rem auto 0 auto;
}
</style>
