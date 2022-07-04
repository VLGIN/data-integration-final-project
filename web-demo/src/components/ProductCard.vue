<template>
  <el-card class="product-card" :body-style="{ padding: '20px' }">
    <img class="product-card__image" :src="image || 'https://cf.shopee.vn/file/47c367b694b0b6ffd5aee59641e2f15f'"
      alt="">
  </el-card>
</template>

<script setup>
const props = defineProps({
  image: {
    type: String,
    // required: true,
  }
})
</script>

<style lang="scss" scoped>
.product-card {
  width: 200px;
  height: 300px;
  border-radius: 8px;

  &__image {
    max-width: 100%;
    height: 100%;
  }
}
</style>