<template>
  <div class="heading-bar container">
    <div class="heading-bar__title">
      {{ t('product.heading.title') }}
    </div>
    <div class="heading-bar__right-content">
      <el-input class="search-bar" v-model="keyword" :prefix-icon="Search" :placeholder="t('product.heading.searchBar')"
        @keyup.enter="searchProduct">
      </el-input>
      <el-button class="button-export" :prefix="Search">
        <el-icon class="el-icon--left">
          <Download />
        </el-icon>
        {{ t('product.heading.export') }}
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { Search, Download } from '@element-plus/icons-vue';

const { t } = useI18n();

const keyword = ref('');

const searchProduct = () => {
  if (keyword.value.trim() === '') {
    return;
  }
  console.log(keyword.value);
} 
</script>

<style lang="scss" scoped>
.heading-bar {
  display: flex;
  justify-content: space-between;
  padding-top: 25px;
  padding-bottom: 25px;

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