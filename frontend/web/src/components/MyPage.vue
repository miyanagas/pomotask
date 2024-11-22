<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";
import { useAuthStore } from "@/auth";
import { validateInput } from "./validation";

const router = useRouter();
const authStore = useAuthStore();

const error = ref(null);

// ユーザー情報を取得
onMounted(async () => {
  try {
    const response = await requestAPI.get("/users/me/", {
      withCredentials: true,
    });
    username.value = response.data.username;
    email.value = response.data.email;
    newUsername.value = username.value;
    newEmail.value = email.value;
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("ユーザー情報の取得に失敗しました");
  }
});

const username = ref("");
const email = ref("");
const newUsername = ref("");
const newEmail = ref("");

const isEditingUsername = ref(false);
const isEditingEmail = ref(false);

const toggleIsEditingUsername = () => {
  isEditingUsername.value = !isEditingUsername.value;
};

const toggleIsEditingEmail = () => {
  isEditingEmail.value = !isEditingEmail.value;
};

const updateUsername = async () => {
  if (!newUsername.value) return;
  if (newUsername.value === username.value) {
    toggleIsEditingUsername();
    return;
  }

  const valRes = validateInput(newUsername.value, null, null);
  if (valRes) {
    error.value = valRes;
    alert("入力内容を確認してください");
    return;
  }

  try {
    const response = await requestAPI.patch(
      "/users/me/",
      {
        username: username.value,
      },
      {
        withCredentials: true,
      }
    );

    username.value = response.data.username;
    newUsername.value = username.value;
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("ユーザー名の更新に失敗しました");
  }
  toggleIsEditingUsername();
};

const updateEmail = async () => {
  if (!newEmail.value) return;
  if (newEmail.value === email.value) {
    toggleIsEditingEmail();
    return;
  }

  const valRes = validateInput(null, newEmail.value, null);
  if (valRes) {
    error.value = valRes;
    alert("入力内容を確認してください");
    return;
  }

  try {
    const response = await requestAPI.patch(
      "/users/me/",
      {
        email: email.value,
      },
      {
        withCredentials: true,
      }
    );

    email.value = response.data.email;
    newEmail.value = email.value;
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("メールアドレスの更新に失敗しました");
  }
  toggleIsEditingEmail();
};

const logout = async () => {
  try {
    await requestAPI.delete("/logout/", {
      withCredentials: true,
    });
    authStore.logout();
    router.push("/login");
  } catch (e) {
    console.error(e);
    alert("ログアウトに失敗しました");
    authStore.checkLoginStatus();
  }
};

const deleteUser = async () => {
  if (!confirm("アカウントを削除しますか？")) return;
  try {
    await requestAPI.delete("/users/me/", {
      withCredentials: true,
    });
    authStore.logout();
    router.push("/login");
  } catch (e) {
    console.error(e);
    alert("アカウントの削除に失敗しました");
    authStore.checkLoginStatus();
  }
};
</script>

<template>
  <div class="container">
    <h1 id="mypage-title" class="title">マイページ</h1>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div id="user-info">
      <span class="user-info-label">ユーザー名</span>
      <form class="user-info-editor" @submit.prevent="updateUsername">
        <input
          class="text-input"
          type="text"
          v-model="newUsername"
          v-bind:readonly="!isEditingUsername"
          required
        />
        <button
          v-if="!isEditingUsername"
          class="edit-button"
          @click="toggleIsEditingUsername"
        >
          編集
        </button>
        <button v-else class="update-button" type="submit">保存</button>
      </form>
      <span class="user-info-label">メールアドレス</span>
      <form class="user-info-editor" @submit.prevent="updateEmail">
        <input
          class="text-input"
          type="email"
          v-model="newEmail"
          v-bind:readonly="!isEditingEmail"
          required
        />
        <button
          v-if="!isEditingEmail"
          class="edit-button"
          @click="toggleIsEditingEmail"
        >
          編集
        </button>
        <button v-else class="update-button" type="submit">保存</button>
      </form>
      <span class="user-info-label">パスワード</span>
      <div class="user-info-editor">
        <input class="text-input" type="password" readonly value="********" />
        <button class="edit-button" @click="router.push('/edit_password')">
          編集
        </button>
      </div>
    </div>
    <div style="display: flex; margin-top: 3rem">
      <button
        style="margin-right: auto"
        class="danger-button"
        @click="deleteUser"
      >
        アカウントを削除
      </button>
      <button style="margin-left: auto" class="primary-button" @click="logout">
        ログアウト
      </button>
    </div>
  </div>
</template>

<style scoped>
#mypage-title {
  margin: 0 auto 0 0;
  color: var(--color-primary);
}

#user-info {
  margin: 3rem 0;
  display: flex;
  flex-direction: column;
}

.user-info-label {
  padding: 0.5rem;
  font-size: 18px;
}

.user-info-editor {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-info-editor input {
  width: 80%;
  font-size: 16px;
}

input[readonly]:focus {
  outline: none;
}

.user-info-editor button {
  margin-left: auto;
}
</style>
