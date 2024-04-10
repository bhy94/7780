<script setup>
import { useCartStore } from '@/stores/cartStore'
import {useRouter} from "vue-router";
import {findNewAPI} from "@/apis/home";
import {CreateOrder} from "@/apis/cart";
import {ElMessage} from "element-plus";
const cartStore = useCartStore()
const router = useRouter()
// 单选回调
const singleCheck = (i, selected) => {
  console.log(i, selected)
  // store cartList 数组 无法知道要修改谁的选中状态？
  // 除了selected补充一个用来筛选的参数 - skuId
  cartStore.singleCheck(i.skuId, selected)
}

// const pay = () => {
//   router.push({
//     path: '/pay',
//     query: {
//       product_id: 123
//     }
//   })
// }
const createOrder = async () => {

  console.log("购物车", cartStore.cartList)
  // const formattedCart = formatCart(cartStore.cartList, 1)
  // console.log("购物信息", formattedCart)
  const items = cartStore.cartList.map((item) => ({
    product_id: item.id,
    quantity: item.count,
  }))
  console.log("购物信息", items)
  const res = await CreateOrder({
    "user_id": 1,
    "items": items
  })
  console.log(res)
  ElMessage({ type: 'success', message: '购买成功' })
  router.push({
    path: '/pay'
  })
}

// const formatCart = (cartList, userId) => {
//   const items = cartList.map((item) => ({
//     product_id: item.id,
//     quantity: item.count,
//   }));
//   const formattedCart = {
//     user_id: userId,
//     items: items,
//   };
//   return formattedCart;
// };
const delCart=(i)=>{
  cartStore.delCart(i.id)
  console.log("点击了",i)
}

const allCheck = (selected) => {
  cartStore.allCheck(selected)
}
</script>

<template>
  <div class="xtx-cart-page">
    <div class="container m-top-20">
      <div class="cart">
        <table>
          <thead>
          <tr>
            <th width="120">
              <el-checkbox :model-value="cartStore.isAll" @change="allCheck" />
            </th>
            <th width="400">Product Information</th>
            <th width="220">Unit Price</th>
            <th width="180">Quantity</th>
            <th width="180">Subtotal</th>
            <th width="140">Action</th>
          </tr>
          </thead>
          <!-- Product list -->
          <tbody>
          <tr v-for="i in cartStore.cartList" :key="i.id">
            <td>
              <!-- Checkbox -->
              <el-checkbox :model-value="i.selected" @change="(selected) => singleCheck(i, selected)" />
            </td>
            <td>
              <div class="goods">
                <RouterLink to="/"><img :src="i.picture" alt="" /></RouterLink>
                <div>
                  <p class="name ellipsis">
                    {{ i.name }}
                  </p>
                </div>
              </div>
            </td>
            <td class="tc">
              <p>&yen;{{ i.price }}</p>
            </td>
            <td class="tc">
              <el-input-number v-model="i.count" />
            </td>
            <td class="tc">
              <p class="f16 red">&yen;{{ (i.price * i.count).toFixed(2) }}</p>
            </td>
            <td class="tc">
              <p>
                <el-popconfirm title="Are you sure you want to delete?" confirm-button-text="Confirm" cancel-button-text="Cancel" @confirm="delCart(i)">
                  <template #reference>
                    <a href="javascript:;">Delete</a>
                  </template>
                </el-popconfirm>
              </p>
            </td>
          </tr>
          <tr v-if="cartStore.cartList.length === 0">
            <td colspan="6">
              <div class="cart-none">
                <el-empty description="Shopping cart is empty">
                  <el-button type="primary">Browse</el-button>
                </el-empty>
              </div>
            </td>
          </tr>
          </tbody>

        </table>
      </div>
      <!-- Action bar -->
      <div class="action">
        <div class="batch">
          Total {{ cartStore.allCount }} items, selected {{ cartStore.selectedCount }} items, total amount:
          <span class="red">¥ {{ cartStore.selectedPrice.toFixed(2) }} </span>
        </div>
        <div class="total">
          <!--          <el-button size="large" type="primary" @click="$router.push('/checkout')">Checkout</el-button>-->
          <el-button size="large" class="btn" @click="createOrder">
            Place Order
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.xtx-cart-page {
  margin-top: 20px;

  .cart {
    background: #fff;
    color: #666;

    table {
      border-spacing: 0;
      border-collapse: collapse;
      line-height: 24px;

      th,
      td {
        padding: 10px;
        border-bottom: 1px solid #f5f5f5;

        &:first-child {
          text-align: left;
          padding-left: 30px;
          color: #999;
        }
      }

      th {
        font-size: 16px;
        font-weight: normal;
        line-height: 50px;
      }
    }
  }

  .cart-none {
    text-align: center;
    padding: 120px 0;
    background: #fff;

    p {
      color: #999;
      padding: 20px 0;
    }
  }

  .tc {
    text-align: center;

    a {
      color: $xtxColor;
    }

    .xtx-numbox {
      margin: 0 auto;
      width: 120px;
    }
  }

  .red {
    color: $priceColor;
  }

  .green {
    color: $xtxColor;
  }

  .f16 {
    font-size: 16px;
  }

  .goods {
    display: flex;
    align-items: center;

    img {
      width: 100px;
      height: 100px;
    }

    >div {
      width: 280px;
      font-size: 16px;
      padding-left: 10px;

      .attr {
        font-size: 14px;
        color: #999;
      }
    }
  }

  .action {
    display: flex;
    background: #fff;
    margin-top: 20px;
    height: 80px;
    align-items: center;
    font-size: 16px;
    justify-content: space-between;
    padding: 0 30px;

    .xtx-checkbox {
      color: #999;
    }

    .batch {
      a {
        margin-left: 20px;
      }
    }

    .red {
      font-size: 18px;
      margin-right: 20px;
      font-weight: bold;
    }
  }

  .tit {
    color: #666;
    font-size: 16px;
    font-weight: normal;
    line-height: 50px;
  }

}
</style>
