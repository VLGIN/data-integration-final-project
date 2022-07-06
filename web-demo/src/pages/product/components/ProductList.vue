<template>
  {{ productList }}
  <div class="product-list container">
    <ProductCard v-for="product in productStore.productsByKeyword" :key="product.source" :name="product['name']"
      :source="product['source']" :ram="product['ram']" :rom="product['bộ nhớ']" :date="product['date']"
      :price="product['price']" />
  </div>
  <!-- <div class="pagination">
    <el-pagination :background="true" :page-size="LIMIT_PRODUCT_IN_PAGE" layout="prev, pager, next" :total="100" />
  </div> -->
</template>

<script setup>
import { watch, ref, reactive } from 'vue';
import ProductCard from '@/components/ProductCard.vue';
import { LIMIT_PRODUCT_IN_PAGE } from '../constants';
import { useProductStore } from '../store';

const productStore = useProductStore();

// let productList = reactive();

// watch(() => productStore.productsByKeyword, (currentValue, oldValue) => {
//   productList = currentValue;
// })

</script>

<style lang="scss" scoped>
.product-list {
  display: grid;
  justify-content: space-between;
  row-gap: 40px;
  grid-template-columns: repeat(auto-fill, 250px);
  margin-bottom: 30px;
}

.pagination {
  display: flex;
  justify-content: center;
}
</style>