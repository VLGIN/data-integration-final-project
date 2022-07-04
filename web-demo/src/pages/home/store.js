import { axiosInstance } from '@/plugins/axios';
import { defineStore } from 'pinia';
import { getRandomColorList } from '@/common/helper';

export const useHomeStore = defineStore('home', {
  state: () => ({
    barChartData: {},
    lineChartData: {},
  }),
  actions: {
    async getData(query) {
      try {
        console.log(query);
        // const response = await axiosInstance.get(`/chart?${query}`);

        const type = 'bar';
        const unit = 'Averagage Price (vnd)';
        const data = [7402500, 3214213, 5321421, 5452211, 2393931];
        const labels = ['Thegioididong', 'Shopee', 'Sendo', 'Mediamart', 'Lazada'];

        this.setChartData(type, unit, data, labels);
      } catch (error) {
        return error.response.data.message;
      }
    },

    setChartData(type, title, data, labels) {
      if (data.length !== labels.length) {
        return;
      }
      /* fake data */
      const chartData = {
        type: type,
        data: {
          labels,
          datasets: [
            {
              label: title,
              data,
              backgroundColor: getRandomColorList(data.length),
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
        },
      };

      switch (type) {
        case 'bar':
          this.barChartData = chartData;
          break;
        case 'line':
          this.barChartData = chartData;
          break;
        case 'doughnut':
          this.barChartData = chartData;
          break;
      }
    },
  },
});
