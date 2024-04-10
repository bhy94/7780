<template>
  <div class="tw-w-64   tw-m-4 tw-flex tw-flex-col tw-items-center" style="height:300px">
    <div class="tw-w-64 tw-h-64 tw-bg-red-200">image</div>
    <p class=" tw-text-xl tw-mt-1 tw-font-bold">Username</p>
    <p>Price</p>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useStore } from '@/store/store'

const store = useStore()


</script>