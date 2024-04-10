<script setup>
import HomePanel from './HomePanel.vue'
import { findNewAPI } from '@/apis/home'
import { onMounted, ref } from 'vue'
import {insertCartAPI} from "@/apis/cart";

// 获取数据
const newList = ref([])

const getNewList = async () => {
  // const res = await findNewAPI()

  const res = await findNewAPI({
    tags :"",
    vendor_id : null
  })
  newList.value = res.data.products.slice(0, 4);
  console.log("新鲜",newList.value)
}

onMounted(() => getNewList())

</script>

<template>
  <HomePanel title="Recent Goods" sub-title="Newly Launched Products, Reliable Quality">    <ul class="goods-list">
      <li v-for="item in newList" :key="item[0]">
        <RouterLink :to="`/detail/${item[0]}`">
          <img :src="item[2]" alt="" />
          <p class="name">{{ item[1] }}</p>
          <p class="price">&yen;{{ item[3] }}</p>
        </RouterLink>
      </li>
    </ul>
  </HomePanel>
</template>


<style scoped lang='scss'>
.goods-list {
  display: flex;
  justify-content: space-between;
  height: 406px;

  li {
    width: 306px;
    height: 406px;

    background: #f0f9f4;
    transition: all .5s;

    &:hover {
      transform: translate3d(0, -3px, 0);
      box-shadow: 0 3px 8px rgb(0 0 0 / 20%);
    }

    img {
      width: 306px;
      height: 306px;
    }

    p {
      font-size: 22px;
      padding-top: 12px;
      text-align: center;
      text-overflow: ellipsis;
      overflow: hidden;
      white-space: nowrap;
    }

    .price {
      color: $priceColor;
    }
  }
}
</style>
