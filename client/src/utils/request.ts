import axios from 'axios';
import { Message, MessageBox } from 'element-ui';
import { UserModule } from '@/store/modules/user';

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API,
  timeout: 5000
});

// Request interceptors
service.interceptors.request.use(
  (config) => {
    // Add X-Access-Token header to every request, you can add other custom headers here
    if (UserModule.token) {
      config.headers['Authorization'] = `Bearer ${UserModule.token}`;
    }
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
);

// Response interceptors
service.interceptors.response.use(
  (response) => {
    if (response.status !== 200) {
      Message({
        message: response.data || 'Error',
        type: 'error',
        duration: 5 * 1000
      });
      if (response.status === 50008 || response.status === 50012 || response.status === 50014) {
        MessageBox.confirm(
          'You have been logged out, try to login again.',
          'Log out',
          {
            confirmButtonText: 'Relogin',
            cancelButtonText: 'Cancel',
            type: 'warning'
          }
        ).then(() => {
          UserModule.ResetToken();
          location.reload(); // To prevent bugs from vue-router
        });
      }
      return Promise.reject(new Error(response.data || 'Error'));
    } else {
      return response;
    }
  },
  (error) => {
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    });
    return Promise.reject(error);
  }
);

export default service;
