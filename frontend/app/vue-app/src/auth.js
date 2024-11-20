import { defineStore } from "pinia";
import requestAPI from "./components/requestAPI";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: false,
    initialized: false,
  }),
  actions: {
    async checkLoginStatus() {
      try {
        const response = await requestAPI.get("/status/", {
          withCredentials: true,
        });
        this.isAuthenticated = response.data.is_authenticated;
      } catch (error) {
        console.error("Error checking login status:", error);
        this.isAuthenticated = false;
      }
    },
    async initialize() {
      await this.checkLoginStatus();
      this.initialized = true;
    },
    login() {
      this.isAuthenticated = true;
    },
    logout() {
      this.isAuthenticated = false;
    },
  },
});
