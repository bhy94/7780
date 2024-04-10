<script setup>

import LayoutNav from './components/LayoutNav.vue'
import LayoutHeader from './components/LayoutHeader.vue'
import LayoutFooter from './components/LayoutFooter.vue'
import LayoutFixed from './components/LayoutFixed.vue'

// 触发获取导航列表的action

// import { useCategoryStore } from '@/stores/categoryStore'
import { onMounted } from 'vue'
import Cookies from 'js-cookie'


import { useStore } from '@/stores/pStore'

const store = useStore()



onMounted(() => {
  let token = Cookies.get("token")
  let role = Cookies.get("role")
  let user_username = Cookies.get("user_username")
  let user_id = Cookies.get("user_id")
  let token_is_string = typeof token === 'string'
  console.log(role == 'user' || token_is_string)
  if (role == 'user' || token_is_string) {
    store.set_role(role)
    store.set_user_id(user_id)
  }
  console.log(store.user_id)
})
</script>

<template>
  <LayoutFixed />
  <LayoutNav />
  <LayoutHeader />
  <!-- 添加key 破坏复用机制 强制销毁重建 -->
  <!-- <RouterView :key="$route.fullPath" /> -->
  <RouterView />
  <LayoutFooter />
</template>