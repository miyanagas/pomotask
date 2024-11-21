<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";

const router = useRouter();
const authStore = useAuthStore();

const currentPassword = ref("");
const newPassword = ref("");

const error = ref(null);

const updatePassword = async () => {
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
    <h1 id="page-title">パスワード変更</h1>
    <div v-if="error">{{ error }}</div>
    <form id="edit-password-form" @submit.prevent="updatePassword">
      <div class="form-group">
        <label for="current-password">現在のパスワード</label>
        <input type="password" id="current-password" />
      </div>
      <div class="form-group">
        <label for="new-password">新しいパスワード</label>
        <input type="password" id="new-password" />
      </div>
      <button id="update-password-button" type="submit">
        パスワードを変更
      </button>
    </form>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#page-title {
  margin-bottom: 1.2rem;
}

#edit-password-form {
  padding: 20px;
  width: 400px;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
}

#update-password-button {
  background-color: var(--color-primary);
  color: var(--color-white);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 1rem;
}

#update-password-button:hover {
  background-color: var(--color-primary-hover);
}
</style>
