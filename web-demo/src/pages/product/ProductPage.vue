<template>
  <div class="product-page">
    <HeadingBar />
    <ProductList />
  </div>
</template>

<script setup>
import HeadingBar from './components/HeadingBar.vue';
import ProductList from './components/ProductList.vue';

</script>

<style lang="scss" scoped>
.product-page {
  min-height: calc(100vh - 44px);
  padding-top: 25px;
  padding-bottom: 25px;
  background-color: $color-light-grey-1;
}
</style>