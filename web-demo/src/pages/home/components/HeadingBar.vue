<template>
  <div class="heading-bar container">
    <div class="heading-bar__title">
      {{ t('home.heading.title') }}
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

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

}
</style>