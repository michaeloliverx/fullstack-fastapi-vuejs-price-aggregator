import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { Message } from 'element-ui';
import { UserMeModule } from '@/store/modules/me';

const http = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  headers: {'Content-Type': 'application/json'},
  timeout: 10000,
  responseType: 'json',
  validateStatus: (status: number) => status >= 200 && status < 300,
});

http.interceptors.request.use (
  function (config) {
    const token = UserMeModule.token;
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  function (error) {
    return Promise.reject (error);
  }
);

// Response interceptors
http.interceptors.response.use(
  // Everything went well, pass through
  (response) => {
    return response
  },
  // Do something with response error
  (error) => {
    // Display message with Element-UI
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    });
    console.log(error.response);
    return Promise.reject(error)

  }
);

export default http;
