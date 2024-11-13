<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import requestAPI from "./requestAPI";

const router = useRouter();

onMounted(async () => {
  try {
    const token = localStorage.getItem("token");
    const response = await requestAPI.get("/users/me/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    username.value = response.data.username;
    email.value = response.data.email;
  } catch (e) {
    alert("ユーザー情報の取得に失敗しました");
    console.error(e);
  }
});

const username = ref("");
const email = ref("");

const logout = () => {
  localStorage.removeItem("token");
  router.push("/login");
};
</script>

<template>
  <div class="container">
    <h1 id="page-title">マイページ</h1>
    <div id="user-info">
      <p>ユーザー名</p>
      <div class="info-group">
        <p>{{ username }}</p>
        <button @click="router.push('/edit')">編集</button>
      </div>
      <p>メールアドレス</p>
      <div class="info-group">
        <p>{{ email }}</p>
        <button @click="router.push('/edit')">編集</button>
      </div>
      <p>パスワード</p>
      <div class="info-group">
        <p>********</p>
        <button @click="router.push('/edit')">編集</button>
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

.info-group p {
  width: 80%;
  font-size: 14px;
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
