<template>
  <FilterBar :filter-options="barFilterOptions" />
  <BaseChart :chart-data="homeStore.barChartData" />
</template>

<script setup>
import FilterBar from './FilterBar.vue';
import BaseChart from '@/components/BaseChart.vue';
import { useI18n } from 'vue-i18n';
import { useHomeStore } from '../store';

const { t } = useI18n();

const homeStore = useHomeStore();

const barFilterOptions = [
  {
    label: 'Average price',
    query: 'option=price:average',
  },
  {
    label: 'The number of products',
    query: 'option=product:number',
  },
  {
    label: 'Number of products sold',
    query: 'option=product:sold',
  },
];

</script>

<style lang="scss" scoped>
</style>