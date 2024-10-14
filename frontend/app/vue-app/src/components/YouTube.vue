<script setup>
import { ref } from "vue";

const youtubeUrl = ref("");

const getYouTubeId = (url) => {
  const regExp =
    /^(https:\/\/www\.youtube\.com\/watch\?v=|https:\/\/youtu\.be\/)([a-zA-Z0-9-_]+)(\?|$)/;
  const match = url.match(regExp);
  return match ? match[2] : null;
};

const roadYouTube = () => {
  const youtubeId = getYouTubeId(youtubeUrl.value);
  youtubeUrl.value = "";
  if (youtubeId) {
    const iframe = document.querySelector("iframe");
    iframe.width = "640";
    iframe.height = "360";
    iframe.src = `https://www.youtube.com/embed/${youtubeId}`;
  } else {
    alert("無効なURLです");
  }
};
</script>

<template>
  <div class="video-container">
    <div class="video-input-form">
      <input type="text" v-model="youtubeUrl" placeholder="YouTube URL" />
      <button @click="roadYouTube()">ロード</button>
    </div>
    <iframe
      width="0"
      height="0"
      src=""
      title="YouTube video player"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      referrerpolicy="strict-origin-when-cross-origin"
      allowfullscreen
    ></iframe>
  </div>
</template>

<style>
.video-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 1rem auto;
  width: 55%;
}

.video-input-form {
  display: flex;
  justify-content: center;
  width: 50%;
  margin: 0rem auto 1rem auto;
}

.video-input-form input {
  width: 60%;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin: 0 0.5rem 0 0;
  font-size: 14px;
}

.video-input-form button {
  padding: 0.5rem 1rem;
  margin: 0 0 0 0.5rem;
  border: 1px solid var(--color-background);
  border-radius: 4px;
  background-color: var(--color-red);
  color: var(--color-text-white);
  font-size: 14px;
  font-weight: bold;
}

.video-input-form button:hover {
  background-color: var(--color-red-hover);
}
</style>
