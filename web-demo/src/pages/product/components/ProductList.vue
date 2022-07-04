<template>
  <div class="product-list container">
    <ProductCard v-for="index in 5" :key="index" />
  </div>
  <div class="pagination">
    <el-pagination :background="true" :page-size="LIMIT_PRODUCT_IN_PAGE" layout="prev, pager, next" :total="100" />
  </div>
</template>

<script setup>
import ProductCard from '@/components/ProductCard.vue';
import { LIMIT_PRODUCT_IN_PAGE } from '../constants';


</script>

<style lang="scss" scoped>
.product-list {
  display: grid;
  justify-content: space-between;
  row-gap: 40px;
  grid-template-columns: repeat(auto-fill, 200px);
  margin-bottom: 30px;
}

.pagination {
  display: flex;
  justify-content: center;
}
</style>