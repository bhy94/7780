<script setup>
import HomeCategory from './components/HomeCategory.vue'
import HomeBanner from './components/HomeBanner.vue'
import HomeNew from './components/HomeNew.vue'
import HomeHot from './components/HomeHot.vue'
import HomeProduct from './components/HomeProduct.vue'
import {useBanner} from "@/views/Category/composables/useBanner";
import GoodsItem from "@/views/Home/components/GoodsItem.vue";
const { bannerList } = useBanner()
const goods = ref([]);
import { findNewAPI } from '@/apis/home'
import { onMounted, ref } from 'vue'
import HomePanel from '@/views/Home/components/HomePanel.vue'

const getNewList = async () => {
  // const res = await findNewAPI()
  const res = await findNewAPI({
    tags :"",
    vendor_id : null
  })
  goods.value = res.data.products;
  console.log("goods=>",goods)
}

onMounted(() => getNewList())

</script>

<template>
  <div class="home-banner">
      <el-carousel height="500px">
        <el-carousel-item v-for="item in bannerList" :key="item.id">
          <img :src="item.imgUrl" alt="">
        </el-carousel-item>
      </el-carousel>
    </div>
  <div class="container">
<!--    <HomeCategory />-->
<!--    <HomeBanner />-->
  </div>
  <HomeNew />
  <!-- <HomePanel title="Goods List" sub-title="Enjoy Your Life">
    <div class="body">
      <GoodsItem  v-for="good in goods" :goods="good" :key="good.id" />
    </div>
  </HomePanel> -->



 <!-- <HomeHot /> -->
 <!-- <HomeProduct /> -->
</template>
<style scoped lang='scss'>

.body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* 每行最小宽度为200px，自动适应容器宽度 */
  gap: 20px; /* 子元素之间的间隔 */
  align-items: flex-start; /* 子元素在交叉轴上的起始位置对齐 */
}
.home-banner {
  width: 1240px;
  height: 500px;
  margin: 0 auto;

  img {
    width: 100%;
    height: 500px;
  }
}
</style>
