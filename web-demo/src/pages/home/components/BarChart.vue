<template>
  <div class="bar-chart">
    <canvas id="planet-chart"></canvas>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue';

import Chart from 'chart.js/dist/chart';
import { useHomeStore } from '../store';

const homeStore = useHomeStore();

let myChart = reactive(null);

watch(() => homeStore.chartData, (currentValue, oldValue) => {
  if (!myChart) {
    myChart = new Chart(document.getElementById('planet-chart'), homeStore.chartData);
    return;
  }
  Object.assign(myChart, homeStore.chartData);
  myChart.update();
}, { deep: true });

</script>

<style lang="scss" scoped>
.bar-chart {
  display: flex;
  justify-content: center;
}

#planet-chart {
  width: 1125px !important;
  height: auto !important;
}
</style>