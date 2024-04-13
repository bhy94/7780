<script setup>
import LayoutHeaderUl from './LayoutHeaderUl.vue'
import HeaderCart from './HeaderCart.vue'
import {ref} from 'vue'
import axios from 'axios'
import { useStore } from '@/stores/pStore'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import Cookies from 'js-cookie'

const store = useStore()
const router = useRouter()

const is_search_page = ref(false)
// 获取当前路由
const current_route = router.currentRoute.value.path
if (current_route == '/search' || current_route == '/search/') {
  is_search_page.value = true
}

const search_text = ref('')

const start_search = () => {
  // 将search_text中的所有中文逗号替换为英文逗号
  let search_text_value = search_text.value.replace(/，/g, ',')

  axios.post('/api/products', {
    tags: search_text_value,
    vendor_id: null
  })
  .then((res) => {
    console.log(res, 'res')
    if (res.data.code == 200 && res.data.data.success == 1) {
      let search_results = res.data.data.products
      Cookies.set("search_results", JSON.stringify(search_results))
      router.push({ path: '/search' })
    } else {
      throw new Error('Search failed')
    }
  })
  .catch((err) => {
    console.log(err, 'err')
    ElMessage({ type: 'error', message: 'Search failed' })
  })

}
</script>

<template>
  <header class='app-header'>
    <div class="container">
      <h1 class="logo">
        <RouterLink to="/">GROUP29-7780</RouterLink>
      </h1>

      <LayoutHeaderUl />
      <div class="search" v-if="!is_search_page">
        <i class="iconfont icon-search"></i>
        <input type="text" placeholder="Search" @keyup.enter="start_search" v-model="search_text">
      </div>
      <!-- 头部购物车 -->
      <HeaderCart v-if="!is_search_page"/>
    </div>
</header>
</template>


<style scoped lang='scss'>
.app-header {
  background: #fff;

  .container {
    display: flex;
    align-items: center;
  }

  .logo {
    width: 200px;

    a {
      display: block;
      height: 132px;
      width: 100%;
      text-indent: -9999px;
      background: url('@/assets/logo.png') no-repeat center 18px / contain;
    }
  }


  .search {
    width: 170px;
    height: 32px;
    position: relative;
    border-bottom: 1px solid #e7e7e7;
    line-height: 32px;

    .icon-search {
      font-size: 18px;
      margin-left: 5px;
    }

    input {
      width: 140px;
      padding-left: 5px;
      color: #666;
    }
  }

  .cart {
    width: 50px;

    .curr {
      height: 32px;
      line-height: 32px;
      text-align: center;
      position: relative;
      display: block;

      .icon-cart {
        font-size: 22px;
      }

      em {
        font-style: normal;
        position: absolute;
        right: 0;
        top: 0;
        padding: 1px 6px;
        line-height: 1;
        background: $helpColor;
        color: #fff;
        font-size: 12px;
        border-radius: 10px;
        font-family: Arial;
      }
    }
  }
}
</style>
