<template>
  <HeadingBar />
  <FilterBar />
  <BarChart />
</template>

<script setup>
import { onMounted } from 'vue';

import HeadingBar from './components/HeadingBar.vue';
import BarChart from './components/BarChart.vue';
import FilterBar from './components/FilterBar.vue';
import { useHomeStore } from './store';

const homeStore = useHomeStore();

onMounted(async () => {
  await homeStore.getData();
})
</script>

<style lang="scss" scoped>
</style>