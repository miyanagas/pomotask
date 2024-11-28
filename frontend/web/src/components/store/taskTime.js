import { defineStore } from "pinia";

export const useTimeStore = defineStore("time", {
  state: () => ({
    time_diff: 0,
  }),
  actions: {
    initialize(time) {
      this.time_diff = time;
    },
    increment(time) {
      this.time_diff += time;
    },
  },
  persist: {
    key: "time",
    storage: sessionStorage,
  },
});
