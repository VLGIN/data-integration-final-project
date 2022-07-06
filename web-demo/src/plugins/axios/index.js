import axios from 'axios';

const options = {
  baseURL: process.env.VUE_APP_API_URL,
  responseType: 'json',
};

console.log(options);

export const axiosInstance = axios.create(options);
