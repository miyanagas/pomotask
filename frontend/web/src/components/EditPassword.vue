<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";
import { useLoadingStore } from "./store/loading";
import { validateInput } from "./validation";

import LoadingView from "./Loading.vue";

const router = useRouter();
const loadingStore = useLoadingStore();

const currentPassword = ref("");
const newPassword = ref("");

const error = ref(null);

const updatePassword = async () => {
  const valRes = validateInput(null, null, newPassword.value);
  if (!valRes) {
    error.value = valRes;
  }

  try {
    await requestAPI.patch(
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
    error.value = e.response.data.detail;
    alert("パスワードの変更に失敗しました");
  }
};
</script>

<template>
  <div class="container" v-if="!loadingStore.isLoading">
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
  <LoadingView v-else />
</template>

<style scoped>
#password-label {
  font-size: 0.9rem;
}

#password-update-button {
  margin: 3rem auto 0 auto;
}
</style>
