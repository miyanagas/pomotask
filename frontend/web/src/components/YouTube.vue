<script setup>
import { ref } from "vue";
import { useVideoStore } from "./video";

const error = ref(null);

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
    error.value = "正しいYouTubeのURLを入力してください";
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
    <div class="single-input-form">
      <input
        style="font-size: 14px"
        class="text-input"
        type="text"
        v-model="youtubeUrl"
        placeholder="YouTube URL"
      />
      <button
        id="load-button"
        class="youtube-button video-button"
        @click="embedYoutube()"
      >
        ロード
      </button>
      <button
        id="favorite-button"
        class="primary-button video-button"
        @click="updateVideoId()"
      >
        お気に入り
      </button>
    </div>
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
  width: 640px;
  height: 360px;
}

@media screen and (max-width: 490px) {
  iframe {
    width: 320px;
    height: 180px;
  }
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

#load-button {
  margin-left: 2rem;
}

@media screen and (max-width: 490px) {
  #load-button {
    margin-left: 1rem;
  }
}

#favorite-button {
  margin-left: 1rem;
}

@media screen and (max-width: 490px) {
  #favorite-button {
    display: none;
  }
}
</style>
