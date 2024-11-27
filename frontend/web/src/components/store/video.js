import { defineStore } from "pinia";

export const useVideoStore = defineStore("video", {
  state: () => ({
    video_id: "",
  }),
  actions: {
    setVideoId(video_id) {
      this.video_id = video_id;
    },
  },
  persist: {
    key: "video",
    storage: localStorage,
  },
});
