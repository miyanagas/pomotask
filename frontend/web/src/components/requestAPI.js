import axios from "axios";
import { createPinia, setActivePinia } from "pinia";
import { useAuthStore } from "@/auth";
import { useLoadingStore } from "./loading";

const requestAPI = axios.create({
  baseURL: "https://todo-app-xsm9.onrender.com/api/v1",
  // baseURL: "http://localhost:8000/api/v1",
});

const pinia = createPinia();
setActivePinia(pinia);

const authStore = useAuthStore();
const loadingStore = useLoadingStore();

requestAPI.interceptors.request.use((config) => {
  loadingStore.setLoading(true);
  return config;
});

requestAPI.interceptors.response.use(
  (response) => {
    authStore.login();
    loadingStore.setLoading(false);

    return response;
  },
  async (error) => {
    if (error.response.status === 401) {
      try {
        await axios.get("https://todo-app-xsm9.onrender.com/api/v1/refresh/", {
          // await axios.get("http://localhost:8000/api/v1/refresh/", {
          withCredentials: true,
        });

        return requestAPI.request(error.config);
      } catch (refreshError) {
        console.error("Error refreshing token:", refreshError);
        loadingStore.setLoading(false);
        authStore.logout();

        return Promise.reject(refreshError);
      }
    }
    loadingStore.setLoading(false);

    return Promise.reject(error);
  }
);

export default requestAPI;
