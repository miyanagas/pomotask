import { defineStore } from "pinia";
import requestAPI from "./components/requestAPI";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: false,
    initialized: false,
  }),
  actions: {
    async initialize() {
      try {
        const response = await requestAPI.get("/status/", {
          withCredentials: true,
        });
        this.isAuthenticated = response.data.is_authenticated;
      } catch (error) {
        this.isAuthenticated = false;
      }
      this.initialized = true;
    },
    login() {
      this.isAuthenticated = true;
    },
    logout() {
      this.isAuthenticated = false;
    },
  },
  persist: {
    key: "auth",
    storage: sessionStorage,
  },
});
