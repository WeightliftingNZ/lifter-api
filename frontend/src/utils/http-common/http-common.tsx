import axios from "axios";

const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8000/v1"
    : process.env.REACT_APP_API_URL;

console.log(process.env.REACT_APP_API_URL);

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-type": "application/json",
  },
});

export default apiClient;
