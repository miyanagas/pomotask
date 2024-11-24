import axios from "axios";
import { useAuthStore } from "@/auth";
import { useLoadingStore } from "./loading";

const requestAPI = axios.create({
  baseURL: "https://todo-app-xsm9.onrender.com/api/v1",
  // baseURL: "http://localhost:8000/api/v1",
});

requestAPI.interceptors.request.use(
  (config) => {
    const loadingStore = useLoadingStore();
    loadingStore.startRequest();

    return config;
  },
  (error) => {
    const loadingStore = useLoadingStore();
    loadingStore.finishRequest();
    console.error("Error loading request:", error);

    return Promise.reject(error);
  }
);

requestAPI.interceptors.response.use(
  (response) => {
    const authStore = useAuthStore();
    useLoadingStore().finishRequest();

    authStore.login();

    return response;
  },
  async (error) => {
    const authStore = useAuthStore();
    const loadingStore = useLoadingStore();

    if (error.response.status === 401) {
      try {
        await axios.post(
          "https://todo-app-xsm9.onrender.com/api/v1/refresh/",
          //"http://localhost:8000/api/v1/refresh/",
          {},
          {
            withCredentials: true,
          }
        );

        return requestAPI.request(error.config);
      } catch (refreshError) {
        console.error("Error refreshing token:", refreshError);
        console.error("Error details:", refreshError.response.data.detail);
        loadingStore.finishRequest();

        authStore.logout();

        if (
          refreshError.response.data.detail ===
            "Could not validate credentials" ||
          refreshError.response.data.detail === "Refresh token is missing" ||
          refreshError.response.data.detail === "Invalid refresh token"
        ) {
          refreshError.response.data.detail = "認証情報が正しくありません";
        }

        return Promise.reject(refreshError);
      }
    }
    loadingStore.finishRequest();

    console.error("Error loading response:", error);
    console.error("Error details:", error.response.data.detail);

    if (
      error.response.data.detail === "Could not validate credentials" ||
      error.response.data.detail === "Access token is missing" ||
      error.response.data.detail === "User not found"
    ) {
      error.response.data.detail = "認証情報が正しくありません";
    }

    return Promise.reject(error);
  }
);

export default requestAPI;
