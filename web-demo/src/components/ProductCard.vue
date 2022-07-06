<template>
  <el-card class="product-card" :body-style="{ padding: '20px' }">
    <img class="product-card__image" :src="phoneImage">
    <div class="product-info">
      <div class="name">{{ name }}</div>
      <div class="price">{{ price }}</div>
      <div class="ram">Ram: {{ ram }}</div>
      <div class="rom">Bộ nhớ: {{ rom }}</div>
      <div class="source">Nguồn: {{ source }}</div>
      <div class="date">Date: {{ date }}</div>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  // image: {
  //   type: String,
  //   // required: true,
  // },
  name: String,
  source: String,
  ram: String,
  rom: String,
  date: String,
  price: String
})

const phoneImage = computed(() => {
  console.log(props.name);
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
  height: 470px;
  border-radius: 8px;

  &__image {
    max-width: 100%;
    height: 100%;
    margin-bottom: 12px;
  }
}

.product-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  // text-align: center;
}

.name {
  font-size: 20px;
  font-weight: 700;
}

.price {
  color: $color-red;
  font-size: 18px;
  font-weight: 500;
}
</style>