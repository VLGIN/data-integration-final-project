import { defineStore } from 'pinia';
import { getRandomColorList } from '@/common/helper';

export const useHomeStore = defineStore('home', {
  state: () => ({
    chartData: {},
  }),
  actions: {
    async getData() {
      const data = [65, 59, 80, 81, 56, 55, 40];
      const labels = ['1', '2', '3', '4', '5', '6', '7'];
      this.setChartData('Overview Data', data, labels);
    },

    setChartData(title, data, labels) {
      if (data.length !== labels.length) {
        return;
      }
      this.chartData = {
        type: 'bar',
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
          // maintainAspectRatio: false,
        },
      };
    },
  },
});
