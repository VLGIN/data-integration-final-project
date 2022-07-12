import { defineStore } from 'pinia';

import { productApiService } from '@/common/services/product.api.service';
import { getRandomColorList } from '@/common/helper';

export const useProductStore = defineStore('product', {
  state: () => ({
    productNamesByKeyword: [],
    rams: [],
    storages: [],
    colors: [],
    productsInCluster: [],
    chartDataList: [],
  }),
  actions: {
    async getProductsByKeyword(keyword) {
      try {
        const response = await productApiService.searchProductByKeyword(keyword);
        this.productNamesByKeyword = response.data.data.items;
      } catch (error) {
        return error.message;
      }
    },
    async getProductSpecs(productName, options) {
      try {
        const response = await productApiService.getProductSpecs(productName, options);
        this.rams = response.data.data.rams;
        this.storages = response.data.data.storages;
        this.colors = response.data.data.colors;
      } catch (error) {
        return error.message;
      }
    },
    async getCluster(specs) {
      try {
        const response = await productApiService.getCluster(specs);
        this.productsInCluster = response.data.data.phoneList;
        // console.log(response.data.data.chartDataList);
        this.setChartData(response.data.data.chartDataList);
      } catch (error) {
        return error.message;
      }
    },

    setChartData(dataList) {
      const colorList = getRandomColorList(dataList.length);
      for (let [index, data] of dataList.entries()) {
        const chartData = {
          key: index,
          type: 'line',
          data: {
            labels: dataList[0].labels,
            datasets: [
              {
                label: data.unit,
                data: data.data,
                borderColor: colorList[index],
                backgroundColor: colorList[index],
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              legend: {
                position: 'bottom',
              },
              title: {
                display: true,
                text: 'Product prices over time',
              },
            },
          },
        };

        this.chartDataList.push(chartData);
      }
    },
  },
});
