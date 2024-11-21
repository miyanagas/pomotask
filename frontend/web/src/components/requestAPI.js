import axios from "axios";

const requestAPI = axios.create({
  baseURL: "https://todo-app-xsm9.onrender.com/",
});

export default requestAPI;
