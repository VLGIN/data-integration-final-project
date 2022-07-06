import { axiosInstance } from '@/plugins/axios';
import { defineStore } from 'pinia';

export const useProductStore = defineStore('product', {
  state: () => ({
    productsByKeyword: [],
  }),
  actions: {
    async getProductsByKeyword(keyword) {
      try {
        const response = await axiosInstance.get('/products/' + keyword);
        console.log(response);
        this.productsByKeyword = response.data.data;
      } catch (error) {
        return error.message;
      }
    },
  },
});
