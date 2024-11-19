<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";

const router = useRouter();

const error = ref(null);

onMounted(async () => {
  try {
    const response = await requestAPI.get("/users/me/");
    username.value = response.data.username;
    email.value = response.data.email;
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("ユーザー情報の取得に失敗しました");
  }
});

const username = ref("");
const email = ref("");

const isEditingUsername = ref(false);
const isEditingEmail = ref(false);

const toggleIsEditingUsername = () => {
  isEditingUsername.value = !isEditingUsername.value;
};

const toggleIsEditingEmail = () => {
  isEditingEmail.value = !isEditingEmail.value;
};

const updateUsername = async () => {
  try {
    await requestAPI.put("/users/me/", {
      username: username.value,
    });
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("ユーザー名の更新に失敗しました");
  }
  toggleIsEditingUsername();
};

const updateEmail = async () => {
  try {
    await requestAPI.put("/users/me/", {
      email: email.value,
    });
  } catch (e) {
    console.error(e);
    error.value = e.response.data.detail;
    alert("メールアドレスの更新に失敗しました");
  }
  toggleIsEditingEmail();
};

const logout = async () => {
  try {
    await requestAPI.post("/logout/");
  } catch (e) {
    console.error(e);
    alert("ログアウトに失敗しました");
  }
  router.push("/login");
};
</script>

<template>
  <div class="container">
    <h1 id="page-title">マイページ</h1>
    <div v-if="error">{{ error }}</div>
    <div id="user-info">
      <p>ユーザー名</p>
      <div class="info-group" v-if="!isEditingUsername">
        <p>{{ username }}</p>
        <button @click="toggleIsEditingUsername">編集</button>
      </div>
      <div class="info-group" v-else>
        <input type="text" v-model="username" />
        <button @click="updateUsername">保存</button>
      </div>
      <p>メールアドレス</p>
      <div class="info-group" v-if="!isEditingEmail">
        <p>{{ email }}</p>
        <button @click="toggleIsEditingEmail">編集</button>
      </div>
      <div class="info-group" v-else>
        <input type="email" v-model="email" />
        <button @click="updateEmail">保存</button>
      </div>
      <p>パスワード</p>
      <div class="info-group">
        <p>********</p>
        <button @click="router.push('/edit_password')">編集</button>
      </div>
    </div>
    <button id="logout-button" @click="logout">ログアウト</button>
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

#logout-button {
  display: block;
  margin: 2rem 0 2rem auto;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: var(--color-primary);
  color: var(--color-white);
}
</style>
