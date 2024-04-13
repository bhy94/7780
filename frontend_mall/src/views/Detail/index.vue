<script setup>
import DetailHot from './components/DetailHot.vue'
import { getDetail } from '@/apis/detail'
import { onMounted, ref } from 'vue'
import {useRoute, useRouter} from 'vue-router'
import { ElMessage } from 'element-plus'
// import { useCartStore } from '@/stores/cartStore'
// const cartStore = useCartStore()
const goods = ref({})
// const route = useRoute()
const router = useRouter()
const route = useRoute()

import Cookies from 'js-cookie'

import axios from 'axios'

import { useStore } from '@/stores/pStore'

const store = useStore()

const count = ref(1)

const getGoods = async () => {

  console.log("product_id",route.params.id)
  // const res = {
  //   result: {
  //     product_id: '123',
  //     product_cover: [
  //       'https://gw.alicdn.com/bao/uploaded/i3/734922009/O1CN01MuUmuo1QiAGFvZ8Ic_!!734922009.jpg_300x300q90.jpg_.webp'
  //     ],
  //     salesCount: 1000,
  //     commentCount: 200,
  //     collectCount: 500,
  //     brand: {
  //       name: '示例品牌'
  //     },
  //     product_name: '示例商品名称',
  //     product_info: '这是一段示例商品描述，用于展示商品详情。',
  //     oldPrice: '1299',
  //     price: '899',
  //     details: true // 确保v-if条件能够通过
  //   }
  // };
  const res =await getDetail(route.params.id)
  goods.value = res.data;
  console.log("detail=>",res.data);
}

onMounted(() => getGoods())

const countChange = (val) => {
  console.log(val)
  if (val < 1) {
    count.value = 1
  }
}

const add_to_chart = () => {
  if (store.user_id <= 0) {
    ElMessage({ type: 'error', message: 'Please login first' })
    return
  }

  store.add_chart({
    product_id: goods.value.product_id,
    product_name: goods.value.product_name,
    product_cover: goods.value.product_cover,
    price: goods.value.price,
    quantity: count.value
  })
  ElMessage({ type: 'success', message: 'Add to chart success' })
}




const gotosearch = (tag) => {
  axios.post('/api/products', {
    tags: tag,
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

const gotosearch2 = (vendor_id) => {
  axios.post('/api/products', {
    tags: "",
    vendor_id: parseInt(vendor_id)
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
  <div class="xtx-goods-page">
    <div class="container" >
      <!-- 商品信息 -->
      <div class="info-container">
        <div>
          <div class="goods-info">
            <div class="media">
              <!-- 图片预览区 -->
              <img :src="goods.product_cover"  style="width:350px;height:350px"/>
            </div>
            <div class="spec">
              <!-- 商品信息区 -->
              <p class="g-name"> {{ goods.product_name }} </p>

              <!-- <el-badge v-for="(tag, index) in goods.tags" :key="index" class="item" type="primary" style="margin-top:20px;margin-right:10px">
                <el-button @click="gotosearch(tag)">{{tag}}</el-button>
              </el-badge> -->


              <p class="g-price" style="font-size:20px">
<!--                <span>{{ goods.oldPrice }}</span>-->
                <span> {{ goods.price }}</span>
              </p>

              <div class="height:40px"></div>
              <!-- <XtxSku :goods="goods" @change="skuChange" /> -->
              <!-- 数据组件 -->
              <el-input-number v-model="count" @change="countChange" min="1" max="99"/>
              <!-- 按钮组件 -->
              <div>
                <el-button size="large" class="btn" @click="add_to_chart">
                  Add to Cart
                </el-button>
              </div>
              <h3 style="margin-top:30px">Company Name:</h3>
              <p class="g-desc"><a style="color:blue" @click="gotosearch2(goods.vendor_id)">{{ goods.vendor_display_name }} </a></p>
              <h3 style="margin-top:30px">Original Address:</h3>
              <p class="g-desc">{{ goods.origin_address }} </p>
              <h3 style="margin-top:30px">Description:</h3>
              <p class="g-desc">{{ goods.product_info }} </p>
            </div>
          </div>

        </div>
        <div class="width:100%:height:100vh;background:red">

        </div>
      </div>
    </div>
  </div>
</template>


<style scoped lang='scss'>
.xtx-goods-page {
  .goods-info {
    min-height: 600px;
    background: #fff;
    display: flex;

    .media {
      width: 580px;
      height: 600px;
      padding: 30px 50px;
    }

    .spec {
      flex: 1;
      padding: 30px 30px 30px 0;
    }
  }

  .goods-footer {
    display: flex;
    margin-top: 20px;

    .goods-article {
      width: 940px;
      margin-right: 20px;
    }

    .goods-aside {
      width: 280px;
      min-height: 1000px;
    }
  }

  .goods-tabs {
    min-height: 600px;
    background: #fff;
  }

  .goods-warn {
    min-height: 600px;
    background: #fff;
    margin-top: 20px;
  }

  .number-box {
    display: flex;
    align-items: center;

    .label {
      width: 60px;
      color: #999;
      padding-left: 10px;
    }
  }

  .g-name {
    font-size: 22px;
  }

  .g-desc {
    color: #999;
    margin-top: 10px;
  }

  .g-price {
    margin-top: 10px;

    span {
      &::before {
        content: "¥";
        font-size: 14px;
      }

      &:first-child {
        color: $priceColor;
        margin-right: 10px;
        font-size: 22px;
      }

      &:last-child {
        color: #999;
        //text-decoration: line-through;
        font-size: 16px;
      }
    }
  }

  .g-service {
    background: #f5f5f5;
    width: 500px;
    padding: 20px 10px 0 10px;
    margin-top: 10px;

    dl {
      padding-bottom: 20px;
      display: flex;
      align-items: center;

      dt {
        width: 50px;
        color: #999;
      }

      dd {
        color: #666;

        &:last-child {
          span {
            margin-right: 10px;

            &::before {
              content: "•";
              color: $xtxColor;
              margin-right: 2px;
            }
          }

          a {
            color: $xtxColor;
          }
        }
      }
    }
  }

  .goods-sales {
    display: flex;
    width: 400px;
    align-items: center;
    text-align: center;
    height: 140px;

    li {
      flex: 1;
      position: relative;

      ~li::after {
        position: absolute;
        top: 10px;
        left: 0;
        height: 60px;
        border-left: 1px solid #e4e4e4;
        content: "";
      }

      p {
        &:first-child {
          color: #999;
        }

        &:nth-child(2) {
          color: $priceColor;
          margin-top: 10px;
        }

        &:last-child {
          color: #666;
          margin-top: 10px;

          i {
            color: $xtxColor;
            font-size: 14px;
            margin-right: 2px;
          }

          &:hover {
            color: $xtxColor;
            cursor: pointer;
          }
        }
      }
    }
  }
}

.goods-tabs {
  min-height: 600px;
  background: #fff;

  nav {
    height: 70px;
    line-height: 70px;
    display: flex;
    border-bottom: 1px solid #f5f5f5;

    a {
      padding: 0 40px;
      font-size: 18px;
      position: relative;

      >span {
        color: $priceColor;
        font-size: 16px;
        margin-left: 10px;
      }
    }
  }
}

.goods-detail {
  padding: 40px;

  .attrs {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 30px;

    li {
      display: flex;
      margin-bottom: 10px;
      width: 50%;

      .dt {
        width: 100px;
        color: #999;
      }

      .dd {
        flex: 1;
        color: #666;
      }
    }
  }

  >img {
    width: 100%;
  }
}

.btn {
  margin-top: 20px;

}

.bread-container {
  padding: 25px 0;
}
</style>