<template>
  <div class="tw-w-screen tw-h-full tw-bg-gray-100 tw-flex tw-flex-col" style="min-height: 100vh">
    <HeaderMain />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import HeaderMain from '@/components/HeaderMain.vue'
</script>

<style scoped>
</style>

