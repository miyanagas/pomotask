import axios from "axios";
import { useAuthStore } from "@/auth";

const authStore = useAuthStore();

const requestAPI = axios.create({
  baseURL: "https://todo-app-xsm9.onrender.com/api/v1",
});

requestAPI.interceptors.response.use(
  (response) => {
    authStore.isAuthenticated = true;
    return response;
  },
  async (error) => {
    if (error.response.status === 401) {
      try {
        await axios.get("https://todo-app-xsm9.onrender.com/api/v1/refresh/", {
          withCredentials: true,
        });

        return requestAPI.request(error.config);
      } catch (refreshError) {
        console.error("Error refreshing token:", refreshError);
        authStore.isAuthenticated = false;
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default requestAPI;
