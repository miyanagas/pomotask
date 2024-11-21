<script setup>
import { ref } from "vue";
import { useVideoStore } from "./video";

const videoStore = useVideoStore();

const youtubeUrl = ref("");
const youtubeId = ref(videoStore.video_id);
const youtubeSrc = ref(`https://www.youtube.com/embed/${youtubeId.value}`);

const extractYoutubeId = (url) => {
  const regExp =
    /^(https:\/\/www\.youtube\.com\/watch\?v=|https:\/\/youtu\.be\/)([a-zA-Z0-9-_]+)(\?|$)/;
  const match = url.match(regExp);
  return match ? match[2] : null;
};

const embedYoutube = () => {
  if (youtubeUrl.value == "") return;

  youtubeId.value = extractYoutubeId(youtubeUrl.value);
  youtubeUrl.value = "";
  if (youtubeId.value) {
    youtubeSrc.value = `https://www.youtube.com/embed/${youtubeId.value}`;
  } else {
    alert("正しいYouTubeのURLを入力してください");
  }
};

const updateVideoId = () => {
  if (youtubeId.value == "") return;
  videoStore.setVideoId(youtubeId.value);
  alert("お気に入りの動画に設定しました");
};
</script>

<template>
  <div style="padding: 0 1rem">
    <form class="single-input-form" @submit.prevent="embedYoutube">
      <input
        style="font-size: 14px"
        class="text-input"
        type="text"
        v-model="youtubeUrl"
        required
        placeholder="YouTube URL"
      />
      <button
        style="margin-left: 2rem"
        class="youtube-button video-button"
        type="submit"
      >
        ロード
      </button>
      <button
        style="margin-left: 1rem"
        class="primary-button video-button"
        id="reset"
        @click="updateVideoId()"
      >
        お気に入り
      </button>
    </form>
    <iframe
      v-if="!youtubeId.value"
      v-bind:src="youtubeSrc"
      width="640"
      height="360"
      title="YouTube video player"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      referrerpolicy="strict-origin-when-cross-origin"
      allowfullscreen
    ></iframe>
  </div>
</template>

<style>
iframe {
  display: block;
  margin: 0 auto;
}

.video-button {
  font-size: 14px;
}

.youtube-button {
  background-color: red;
  color: var(--color-text-white);
}

@media (hover: hover) {
  .youtube-button:hover {
    background-color: var(--color-red-hover);
  }
}
</style>
