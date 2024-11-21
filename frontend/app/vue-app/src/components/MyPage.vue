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
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
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
    const response = await requestAPI.put(
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
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
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
    const response = await requestAPI.put(
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
    if (e.response.status === 401) {
      authStore.checkLoginStatus();
    }
  }
  toggleIsEditingEmail();
};

const logout = async () => {
  try {
    await requestAPI.post("/logout/", {
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
    <h1 id="page-title">マイページ</h1>
    <div v-if="error" class="error-message">{{ error }}</div>
    <div id="user-info">
      <p>ユーザー名</p>
      <div class="info-group" v-if="!isEditingUsername">
        <p>{{ username }}</p>
        <button @click="toggleIsEditingUsername">編集</button>
      </div>
      <form class="info-group" v-else @submit.prevent="updateUsername">
        <input type="text" v-model="newUsername" required />
        <button type="submit">保存</button>
      </form>
      <p>メールアドレス</p>
      <div class="info-group" v-if="!isEditingEmail">
        <p>{{ email }}</p>
        <button @click="toggleIsEditingEmail">編集</button>
      </div>
      <form class="info-group" v-else @submit.prevent="updateEmail">
        <input type="email" v-model="newEmail" required />
        <button type="submit">保存</button>
      </form>
      <p>パスワード</p>
      <div class="info-group">
        <p>********</p>
        <button @click="router.push('/edit_password')">編集</button>
      </div>
    </div>
    <div id="buttons">
      <button @click="deleteUser" id="delete-button">アカウントを削除</button>
      <button @click="logout" id="logout-button">ログアウト</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  margin: 0 auto;
  max-width: 500px;
}

#page-title {
  color: var(--color-primary);
}

#user-info {
  margin: 3rem 0 5rem 0;
}

#user-info p {
  font-size: 18px;
}

.info-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.info-group p,
input {
  width: 80%;
  height: 36px;
  font-size: 18px;
  padding: 0.25rem 0.5rem;
  border: 1px solid var(--color-gray);
  border-radius: 4px;
  word-wrap: break-word;
}

.info-group button {
  display: block;
  margin: 0.5rem 0 0.5rem auto;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 16px;
}

#buttons {
  display: flex;
}

#delete-button {
  display: block;
  margin: 2rem auto 1rem 0;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: var(--color-red);
  color: var(--color-white);
}

#logout-button {
  display: block;
  margin: 2rem 0 1rem auto;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: var(--color-primary);
  color: var(--color-white);
}
</style>
