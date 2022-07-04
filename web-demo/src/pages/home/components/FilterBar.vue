<template>
  <div class="filter-bar container">
    <div class="title">
      {{ t('home.filter.title') }}
    </div>
    <el-button class="filter-option" color="#e7e7e7" v-for="option in filterOptions" :key="option.label"
      :class="currentOption === option.label ? 'filter-option--selected' : ''" @click="chooseOption(option)">
      {{ option.label }}
    </el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

import { useI18n } from 'vue-i18n';
import { useHomeStore } from '../store';

const { t } = useI18n();
const homeStore = useHomeStore();

const props = defineProps({
  filterOptions: {
    type: Object,
    required: true,
  },
})



const currentOption = ref(props.filterOptions[0].label);

const chooseOption = (option) => {
  currentOption.value = option.label;
  homeStore.getData(option.query);
}
</script>

<style lang="scss" scoped>
.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  box-sizing: border-box;
  padding-top: 16px;
  padding-bottom: 16px;
  background-color: $color-light-grey;
  margin-bottom: 20px;
  border-radius: 4px;
  border: 1px solid $color-grey-1;
}

.title {
  margin-left: 16px;
  margin-right: 16px;
  font-weight: 700;
}

.filter-option {
  width: fit-content;
  padding: 8px 12px;
  font-size: 14px;
  border-radius: 20px;
  cursor: pointer;

  &--selected {
    background-color: $color-green;

    &:hover,
    &:focus {
      background-color: $color-green;
    }
  }
}
</style>