<template>
  <div class="product-page">
    <HeadingBar />
    <ProductList />
    <!-- <BaseChart :chart-data="productStore.chartDataList[0]" /> -->

    <div class="list-chart">
      <!-- <BaseChart :chart-data="chartData" v-for="chartData in productStore.chartDataList" :key="chartData" /> -->

      <!-- <BaseChart :chart-data="productStore.chartDataList[0]" v-for="index in productStore.chartDataList.length"
        :key="index" /> -->

      <BaseChart :chart-data="productStore.chartDataList[0]" />
      <BaseChart :chart-data="productStore.chartDataList[1]" />
      <BaseChart :chart-data="productStore.chartDataList[2]" />
      <BaseChart :chart-data="productStore.chartDataList[3]" />
      <BaseChart :chart-data="productStore.chartDataList[4]" />

      <!-- <BaseChart :chart-data="productStore.chartDataList[1]" /> -->
    </div>
  </div>
</template>

<script setup>
import HeadingBar from './components/HeadingBar.vue';
import ProductList from './components/ProductList.vue';
import BaseChart from '@/components/BaseChart.vue';
import { useProductStore } from './store';
import { watch } from 'vue';
import { useRoute } from 'vue-router';

const productStore = useProductStore();

const route = useRoute();
watch(() => route.path, () => {
  productStore.productsInCluster = [];
})
</script>

<style lang="scss" scoped>
.product-page {
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