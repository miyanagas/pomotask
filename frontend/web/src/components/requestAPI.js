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
        await axios.get("https://todo-app-xsm9.onrender.com/api/v1/refresh/", {
          // await axios.get("http://localhost:8000/api/v1/refresh/", {
          withCredentials: true,
        });

        return requestAPI.request(error.config);
      } catch (refreshError) {
        console.error("Error refreshing token:", refreshError);
        loadingStore.finishRequest();

        authStore.logout();

        return Promise.reject(refreshError);
      }
    }
    loadingStore.finishRequest();

    return Promise.reject(error);
  }
);

export default requestAPI;
