import axios from "axios";

const requestAPI = axios.create({
  baseURL: "http://localhost:8080/api/v1",
});

export default requestAPI;
