<template>
  <div class="base-chart container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';

import Chart from 'chart.js/dist/chart';

let myChart = reactive(null);

const chart = ref(null);

const props = defineProps({
  chartData: {
    type: Object,
    required: true,
  }
})

watch(() => props.chartData, (currentValue, oldValue) => {
  if (!myChart) {
    myChart = new Chart(chart.value, currentValue);
    return;
  }
  Object.assign(myChart, currentValue);
  myChart.update();
}, { deep: true });

</script>

<style lang="scss" scoped>
.base-chart {
  display: flex;
  justify-content: center;
}
</style>