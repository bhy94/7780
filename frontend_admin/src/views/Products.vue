<template>
  <div class="tw-w-full tw-h-full tw-flex tw-flex-wrap tw-justify-between tw-p-10" style="min-height: 90vh">
    <ProductItem />
    <ProductItem />
    <ProductItem />
    <ProductItem />
    <ProductItem />
    <ProductItem />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useStore } from '@/store/store'
import ProductItem from '@/components/ProductItem.vue';

const store = useStore()


</script>

<style scoped>
</style>
```