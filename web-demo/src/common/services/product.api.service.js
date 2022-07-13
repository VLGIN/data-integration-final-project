import { axiosInstance } from '@/plugins/axios';
import qs from 'qs';

class ProductApiService {
  async searchProductByKeyword(keyword) {
    return await axiosInstance.get(`/products/search?keyword=${keyword}`);
  }
  async getProductSpecs(productName, options) {
    return await axiosInstance.get(
      `/products/get-specs/${productName}?${qs.stringify(options)}`,
    );
  }
  async getCluster(specs) {
    return await axiosInstance.post(`/products/cluster`, specs);
  }
}

export const productApiService = new ProductApiService();
