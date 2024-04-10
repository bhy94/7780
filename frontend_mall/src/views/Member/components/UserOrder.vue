<script setup>
import { getUserOrder } from '@/apis/order'
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useStore } from '@/stores/pStore'
import axios from 'axios'
import { set } from '@vueuse/core'

const store = useStore()
// tab列表
const tabTypes = [
  { name: "all", label: "all" },
  { name: "created", label: "created" },
  { name: "payed", label: "payed" },
  { name: "received", label: "received" },
  { name: "complete", label: "complete" },
]
// 获取订单列表
const orderList = ref([])
const total = ref(0)
const params = ref({
  orderState: 0,
  page: 1,
  pageSize: 2
})
// const getOrderList = async () => {
//   const res = await getUserOrder(params.value)
//   orderList.value = res.result.items
//   total.value = res.result.counts
// }

const tableData = ref([])

const get_order_list = () => {
  axios.post('/api/users/orders', {
    user_id: store.user_id,
  })
  .then((res) => {
    console.log(res)
    if (res.data.code == 200 && res.data.data.success == 1) {
      // console.log(res.data.data)
      tableData.value = res.data.data.orders
    } else {
      throw new Error('get user orders failed')
    }
  })
  .catch(err => {
    ElMessage({ type: 'error', message: 'get user orders failed' })
  })
}

onMounted(() => {
  setTimeout(() => {
    get_order_list()
  }, 200)
})



const cancel_order = (order_id) => {
  axios.post('/api/orders/delete', {
    user_id: store.user_id,
    order_id: order_id
  })
  .then((res) => {
    console.log(res)
    if (res.data.code == 200 && res.data.data.success == 1) {
      ElMessage({ type: 'success', message: 'Cancel Order Succeed!' })
      setTimeout(() => {
        location.reload(true)
      }, 200)
    } else {
      throw new Error('Cancel Order failed')
    }
  })
  .catch(err => {
    ElMessage({ type: 'error', message: 'Cancel Order failed' })
  })
}

const pay_order = (order_id) => {
  axios.post('/api/payments/pay', {
    user_id: store.user_id,
    order_id: order_id
  })
  .then((res) => {
    console.log(res)
    if (res.data.code == 200 && res.data.data.success == 1) {
      ElMessage({ type: 'success', message: 'Pay Bill Succeed!' })
      setTimeout(() => {
        location.reload(true)
      }, 200)
    } else {
      throw new Error('Pay Bill failed')
    }
  })
  .catch(err => {
    ElMessage({ type: 'error', message: 'Pay Bill failed' })
  })
}


const recieve_order = (order_id) => {
  axios.post('/api/orders/recieve', {
    user_id: store.user_id,
    order_id: order_id
  })
  .then((res) => {
    console.log(res)
    if (res.data.code == 200 && res.data.data.success == 1) {
      ElMessage({ type: 'success', message: 'Recieve Succeed!' })
      setTimeout(() => {
        location.reload(true)
      }, 200)
    } else {
      throw new Error('Recieve failed')
    }
  })
  .catch(err => {
    ElMessage({ type: 'error', message: 'Recieve failed' })
  })
}
</script>

<template>
  <div class="order-container">
    <div style="width:100%;height:100%;min-height:500px">
      <el-table :data="tableData" :border="false" style="width: 100%;height:100%">
        <el-table-column type="expand">
          <template #default="props">
            <div m="4">
              <el-button @click="recieve_order(props.row.order_id)" v-if="props.row.status == 'shipping'"> Receive </el-button>
              <el-button @click="cancel_order(props.row.order_id)" v-if="props.row.status == 'placed' || props.row.status == 'paid'"> Cancel Full Order </el-button>
              <el-button @click="pay_order(props.row.order_id)" v-if="props.row.status == 'placed'"> Pay Bill </el-button>
              <div style="margin-bottom:10px"></div>
              <div v-for="(item, index) in props.row.items" style="width:100%;height:100%;border: 1px solid #555;padding:5px;margin-top:5px">
                <p m="t-0 b-2">OrderID: {{ item.order_id }}</p>
                <p m="t-0 b-2">ProductName: {{ item.product_name }}</p>
                <p m="t-0 b-2">Quantity: {{ item.quantity }}</p>
                <p m="t-0 b-2">TotalPrice: {{ item.total_price }}</p>
                <p m="t-0 b-2">Express Number: {{ item.express_number}}</p>
                <el-button @click="cancel_order(item.order_id)" :disabled="item.status != 'placed' && item.status != 'paid'" v-if="props.row.items.length != 1"> Cancel </el-button>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="OrderID" prop="order_id" />
        <el-table-column label="Date" prop="place_time" />
        <el-table-column label="Price" prop="total_price" />
        <el-table-column label="Status" prop="status">
          <template #default="scope">
            <el-tag
              :type="scope.row.status == 'placed' ? 'warning' : 'success'"
              disable-transitions
              >{{ scope.row.status }}</el-tag
            >
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<style scoped lang="scss">
.order-container {
  padding: 10px 20px;

  .pagination-container {
    display: flex;
    justify-content: center;
  }

  .main-container {
    min-height: 500px;

    .holder-container {
      min-height: 500px;
      display: flex;
      justify-content: center;
      align-items: center;
    }
  }
}

.order-item {
  margin-bottom: 20px;
  border: 1px solid #f5f5f5;

  .head {
    height: 50px;
    line-height: 50px;
    background: #f5f5f5;
    padding: 0 20px;
    overflow: hidden;

    span {
      margin-right: 20px;

      &.down-time {
        margin-right: 0;
        float: right;

        i {
          vertical-align: middle;
          margin-right: 3px;
        }

        b {
          vertical-align: middle;
          font-weight: normal;
        }
      }
    }

    .del {
      margin-right: 0;
      float: right;
      color: #999;
    }
  }

  .body {
    display: flex;
    align-items: stretch;

    .column {
      border-left: 1px solid #f5f5f5;
      text-align: center;
      padding: 20px;

      >p {
        padding-top: 10px;
      }

      &:first-child {
        border-left: none;
      }

      &.goods {
        flex: 1;
        padding: 0;
        align-self: center;

        ul {
          li {
            border-bottom: 1px solid #f5f5f5;
            padding: 10px;
            display: flex;

            &:last-child {
              border-bottom: none;
            }

            .image {
              width: 70px;
              height: 70px;
              border: 1px solid #f5f5f5;
            }

            .info {
              width: 220px;
              text-align: left;
              padding: 0 10px;

              p {
                margin-bottom: 5px;

                &.name {
                  height: 38px;
                }

                &.attr {
                  color: #999;
                  font-size: 12px;

                  span {
                    margin-right: 5px;
                  }
                }
              }
            }

            .price {
              width: 100px;
            }

            .count {
              width: 80px;
            }
          }
        }
      }

      &.state {
        width: 120px;

        .green {
          color: $xtxColor;
        }
      }

      &.amount {
        width: 200px;

        .red {
          color: $priceColor;
        }
      }

      &.action {
        width: 140px;

        a {
          display: block;

          &:hover {
            color: $xtxColor;
          }
        }
      }
    }
  }
}
</style>
