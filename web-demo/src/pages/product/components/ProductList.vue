<template>
  <div class="product-list container">
    <ProductCard v-for="product in productStore.productsInCluster" :key="product.source" :product-url="product['url']"
      :name="product['name']" :source="product['source']" :ram="product['ram']" :rom="product['bộ nhớ']"
      :color="product['color']" :date="product['date']" :price="parsePrice(product['price'])" />
  </div>
</template>

<script setup>
import { watch, ref, reactive } from 'vue';
import ProductCard from '@/components/ProductCard.vue';
import { LIMIT_PRODUCT_IN_PAGE } from '../constants';
import { useProductStore } from '../store';
import { parsePrice } from '@/common/helper';

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