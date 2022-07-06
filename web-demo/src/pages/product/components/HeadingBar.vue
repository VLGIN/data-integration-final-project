<template>
  <div class="heading-bar container">
    <div class="heading-bar__title">
      {{ t('product.heading.title') }}
    </div>
    <div class="heading-bar__right-content">
      <el-input class="search-bar" v-model="keyword" :prefix-icon="Search" @keyup.enter="searchProduct"
        :placeholder="t('product.heading.search.placeholder')">
      </el-input>
      <el-button type="primary" class="button-export" @click="searchProduct">
        {{ t('product.heading.search.button') }}
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { Search } from '@element-plus/icons-vue';
import { useProductStore } from '../store';


const productStore = useProductStore();

const { t } = useI18n();

const keyword = ref('');

const searchProduct = async () => {
  // if (keyword.value.trim() === '') {
  console.log(keyword.value);
  await productStore.getProductsByKeyword(keyword.value);
  // }
} 
</script>

<style lang="scss" scoped>
.heading-bar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 25px;
  // border-bottom: 1px solid $color-grey;

  &__title {
    font-size: 24px;
    font-weight: 500;
  }

  &__right-content {
    display: flex;
    align-items: center;
    gap: 12px;

    &__search-bar {
      width: 250px;
    }
  }

  // .button
}
</style>