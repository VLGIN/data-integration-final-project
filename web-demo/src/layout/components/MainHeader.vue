<template>
  <div class="container-fuild">
    <div class="main-header container">
      <img class="main-header__logo" src="@/assets/images/logo/logo.png">
      <div class="main-header__nav-bar">
        <router-link :to="nav.to" class="router-link" v-for="nav in navigations" :key="nav.label">
          <div class="nav-item" :class="currentActivedNav === nav.href ? 'nav-item--actived' : ''">
            {{ nav.label }}
          </div>
        </router-link>

      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';

import { useI18n } from 'vue-i18n';

import { PageName } from '@/common/constants';
import { useRoute } from 'vue-router';

const { t } = useI18n();
const route = useRoute();

const currentActivedNav = ref('');

onMounted(() => {
  currentActivedNav.value = route.path;
})

watch(() => route.path, (currentVale, oldValue) => {
  currentActivedNav.value = currentVale;
})

const navigations = [
  {
    label: t('app.navigations.home'),
    to: {
      name: PageName.HOME_PAGE
    },
    href: '/',
  },
  {
    label: t('app.navigations.product'),
    to: {
      name: PageName.PRODUCT_PAGE
    },
    href: '/product'
  }
]


</script>

<style lang="scss" scoped>
@mixin set-actived-color() {
  border-top: 3px solid $color-primary  !important;
  background-color: $color-grey  !important;
  box-sizing: border-box !important;
}

.container-fuild {
  background-color: $color-white;
}

.main-header {
  display: flex;
  align-items: center;
  gap: 50px;
  height: 44px;

  &__logo {
    width: 50px;
  }

  &__nav-bar {
    display: flex;
    height: 100%;
    font-size: 14px;
  }
}

.nav-item {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
  color: $color-dark-grey-1  !important;
  border-radius: 0;
  border: none;
  cursor: pointer;

  &--actived {
    @include set-actived-color();
  }
}
</style>