<script setup>
import Cookies from 'js-cookie'
import axios from 'axios'

// 定义props
defineProps({
  // 主标题
  title: {
    type: String
  },
  // 副标题
  subTitle: {
    type: String
  }
})

const showallgoods = () => {
  axios.post('/api/products', {
    tags: "",
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
  <div class="home-panel">
    <div class="container">
      <div class="head">
        <!-- 主标题和副标题 -->
        <h3 @click="showallgoods()">
          {{ title }}<small>{{ subTitle }}</small>
        </h3>
      </div>
      <!-- 主体内容区域 -->
      <slot />

      <!-- <div class="margin-top:20px"> <a @click="showallgoods">MORE + </a></div> -->
    </div>
  </div>
</template>

<style scoped lang='scss'>
.home-panel {
  background-color: #fff;

  .head {
    padding: 40px 0;
    display: flex;
    align-items: flex-end;

    h3 {
      flex: 1;
      font-size: 32px;
      font-weight: normal;
      margin-left: 6px;
      height: 35px;
      line-height: 35px;

      small {
        font-size: 16px;
        color: #999;
        margin-left: 20px;
      }
    }
  }
}
</style>