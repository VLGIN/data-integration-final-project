import axios from 'axios';

const options = {
  baseURL: process.env.VUE_APP_API_URL,
  responseType: 'json',
};

export const axiosInstance = axios.create(options);
