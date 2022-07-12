<template>
  <MainHeader />
  <router-view></router-view>
  <MainFooter />
</template>

<script setup>
import MainFooter from './components/MainFooter.vue';
import MainHeader from './components/MainHeader.vue';

</script>

<style lang="scss" scoped>
</style>