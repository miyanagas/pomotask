import { defineStore } from "pinia";
import requestAPI from "./components/requestAPI";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    isAuthenticated: false,
  }),
  actions: {
    async checkLoginStatus() {
      try {
        const response = await requestAPI.get("/auth/status/", {
          withCredentials: true,
        });
        this.isAuthenticated = response.data.is_authenticated;
      } catch (error) {
        console.error("Error checking login status:", error);
        this.isAuthenticated = false;
      }
    },
  },
});
