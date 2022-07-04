<template>
  <div class="home-page">
    <HeadingBar />
    <div class="list-chart">
      <BarChart />
      <LineChart />

    </div>
  </div>

</template>

<script setup>
import { onMounted } from 'vue';

import { useHomeStore } from './store';
import HeadingBar from './components/HeadingBar.vue';
import BarChart from './components/BarChart.vue';
import LineChart from './components/BarChart.vue';

const homeStore = useHomeStore();

onMounted(async () => {
  await homeStore.getData();
})
</script>

<style lang="scss" scoped>
.home-page {
  min-height: calc(100vh - 44px);
  padding-top: 25px;
  padding-bottom: 25px;
  background-color: $color-light-grey-1;
}

.list-chart {
  display: flex;
  flex-direction: column;
  gap: 30px;
}
</style>