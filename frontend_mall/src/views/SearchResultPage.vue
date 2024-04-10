<script setup>

import LayoutNav from '@/views/Layout/components/LayoutNav.vue'
import LayoutHeader from '@/views/Layout/components/LayoutHeader.vue'
import LayoutFooter from '@/views/Layout/components/LayoutFooter.vue'
import LayoutFixed from '@/views/Layout/components/LayoutFixed.vue'
import HomePanel from '@/views/GoodsList.vue'

// 触发获取导航列表的action

// import { useCategoryStore } from '@/stores/categoryStore'
import { onMounted, ref } from 'vue'
import Cookies from 'js-cookie'
import { useRouter } from 'vue-router'

const router = useRouter()


import { useStore } from '@/stores/pStore'

const store = useStore()

const goods = ref([])

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
  

  let search_results = Cookies.get("search_results")
  
  
  if (search_results == undefined) {
    search_results = []
  } else {
    search_results = JSON.parse(search_results)
    for (let i = 0; i < search_results.length; i++) {
      goods.value.push(search_results[i])
    }
    console.log(goods.value)
  }
})


const gotoproduct = (pid) => {
  router.push({ path: '/detail/'+pid })
}

</script>

<template>
  <LayoutFixed />
  <LayoutNav />
  <LayoutHeader />
  <HomePanel title="Goods List" sub-title="Enjoy Your Life">
    <div class="body">
      <!-- <GoodsItem  v-for="good in goods" :goods="good" :key="good.id" /> -->
      <!-- <GoodsItem  v-for="good in goods"/> -->
      
    </div>
  </HomePanel>
  <div style="width:100%;height:100%;display:flex;flex-wrap:wrap;justify-content:space-around;padding-left:90px;padding-right:90px;margin-bottom:100px">
      <div v-for="good in goods" style="width:200px;height:200px;margin:20px;border:1px solid #ccc;margin-top:50px">
        <img :src="good[2]" alt="" style="width:100%;height:100%" @click="gotoproduct(good[0])">
        <div style="text-align:center;font-size:1.5rem;"><a @click="gotoproduct(good[0])">{{good[1]}}</a></div>
        <div style="text-align:center"><a @click="gotoproduct(good[0])">￥ {{good[3]}} </a></div>
      </div>

  </div>
  
  <LayoutFooter />
</template>