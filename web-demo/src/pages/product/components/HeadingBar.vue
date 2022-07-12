<template>
  <div class="heading-bar container">
    <div class="heading-bar__title">
      {{ t('product.heading.title') }}
    </div>
    <div class="heading-bar__right-content">
      <!-- <el-input class="search-bar" v-model="keyword" :prefix-icon="Search" @keyup.enter="searchProduct"
        :placeholder="t('product.heading.search.placeholder')">
      </el-input> -->
      <el-autocomplete ref="searchBox" v-model="keyword" :clearable="true" placeholder="Enter product name"
        :fetch-suggestions="onChangeKeyword" @select="onSelectKeyword" @keyup.enter="onSelectKeyword">
      </el-autocomplete>
      <el-select v-model="inputRam" class="m-2" placeholder="Ram" :clearable="true" @change="onChangeSpec">
        <el-option v-for="item in productStore.rams" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="inputStorage" class="m-2" placeholder="Storage" :clearable="true" @change="onChangeSpec">
        <el-option v-for="item in productStore.storages" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="inputColor" class="m-2" placeholder="Color" :clearable="true" @change="onChangeSpec">
        <el-option v-for="item in productStore.colors" :key="item" :label="item" :value="item" />
      </el-select>
      <el-button type="primary" class="button-export" @click="searchProduct"
        :disabled="keyword === '' || inputRam === '' || inputStorage === '' || inputColor === ''">
        {{ t('product.heading.search.button') }}
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, toRaw, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { Search } from '@element-plus/icons-vue';
import { useProductStore } from '../store';
import { debounce, uniqBy } from 'lodash';


const productStore = useProductStore();

const { t } = useI18n();

const searchBox = ref(null);
const keyword = ref('');

const inputRam = ref('');
const inputStorage = ref('');
const inputColor = ref('');

const resetSpecs = () => {
  inputRam.value = '';
  inputStorage.value = '';
  inputColor.value = '';
}

watch(() => keyword.value, (currentValue, oldValue) => {
  resetSpecs();
})


const onChangeKeyword = async (keyword, callback) => {
  debounce(async () => {
    await productStore.getProductsByKeyword(keyword);
    // console.log(productStore.productNamesByKeyword);
    const suggestionResults = uniqBy(
      productStore.productNamesByKeyword.map((result) => {
        return { value: result };
      }),
      'value',
    );
    callback(
      suggestionResults
    );
  }, 0)();
}



const onSelectKeyword = async () => {
  searchBox.value.suggestions = [];

  await productStore.getProductSpecs(keyword.value, {});
}

const onChangeSpec = async () => {
  const filters = {};

  if (inputRam.value !== '') {
    filters.ram = inputRam.value;
  }
  if (inputStorage.value !== '') {
    filters.storage = inputStorage.value;
  }
  if (inputColor.value !== '') {
    filters.color = inputColor.value;
  }

  await productStore.getProductSpecs(keyword.value, filters);
}

const searchProduct = async () => {
  await productStore.getCluster({
    name: keyword.value,
    ram: inputRam.value,
    storage: inputStorage.value,
    color: inputColor.value,
  })
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

.el-select {
  width: 120px;
}
</style>