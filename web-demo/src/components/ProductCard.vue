<template>
  <a :href="productUrl" class="router-link" target="_blank">
    <el-card class="product-card" :body-style="{ padding: '20px' }">
      <img class="product-card__image" :src="phoneImage">
      <div class="product-info">
        <div class="name">{{ name }}</div>
        <div class="price">{{ price }}<sup>đ</sup></div>
        <div class="ram">Ram: {{ ram }}</div>
        <div class="rom">Bộ nhớ: {{ rom }}</div>
        <div class="rom">Màu sắc: {{ color }}</div>
        <div class="source">Nguồn: <span style="color: #D67F7A;">{{ source }}</span></div>
        <div class="date">Date: {{ date }}</div>
      </div>
    </el-card>
  </a>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  // image: {
  //   type: String,
  //   // required: true,
  // },
  productUrl: String,
  name: String,
  source: String,
  ram: String,
  rom: String,
  color: String,
  date: String,
  price: String
})

const phoneImage = computed(() => {
  if (props.name.includes('iphone')) {
    return 'https://cdn.tgdd.vn/comment/51789883/iphone-13-pro-max-gold-1-600x600-20220621154044.jpg';
  } else if (props.name.includes('galaxy')) {
    return 'https://www.xtmobile.vn/vnt_upload/product/12_2021/thumbs/(600x600)_crop_s20-5g.jpg';
  } else if (props.name.includes('redmi')) {
    return 'https://cdn.hoanghamobile.com/i/productlist/dsp/Uploads/2022/03/17/image-removebg-preview-5.png';
  }
  return 'https://cdn.tgdd.vn/comment/51789883/iphone-13-pro-max-gold-1-600x600-20220621154044.jpg';
})
</script>

<style lang="scss" scoped>
.product-card {
  width: 250px;
  border-radius: 8px;
  text-align: center;

  &__image {
    max-width: 80%;
    height: 100%;
    margin-bottom: 12px;
  }
}

.product-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  font-size: 15px;

  // text-align: center;
  .name {
    font-size: 19px;
    font-weight: 700;
  }

  .price {
    color: $color-red;
    font-size: 17px;
    font-weight: 500;
  }
}
</style>