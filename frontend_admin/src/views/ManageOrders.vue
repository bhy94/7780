<template>
  <el-table :data="tableData" style="width: 100%; height: 100%">
    <el-table-column fixed prop="order_id" label="Order ID" width="100" />
    <el-table-column prop="user_id" label="User ID" width="100" />
    <el-table-column prop="product_id" label="Product ID" width="100" />
    <el-table-column prop="sub_order" label="SubOrder" width="120" />
    <el-table-column prop="quantity" label="Quantity" width="120" />
    <el-table-column prop="total_price" label="Volume" width="120" />
    <el-table-column prop="place_time" label="Time" width="120" />
    <el-table-column prop="status" label="Status" width="100" />
    <el-table-column prop="express_number" label="Express Number" width="150"></el-table-column>
    <el-table-column fixed="right" label="Operation" width="150">
      <template #default="scope">
        <el-button
          link
          type="primary"
          size="small"
          @click.prevent="deleteRow(scope.$index)"
        >
          Remove
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script lang="ts" setup>

import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useStore } from '@/store/store'
import { ElMessageBox } from 'element-plus'


const store = useStore()

const deleteRow = (index: number) => {
  // tableData.value.splice(index, 1)
  axios.post('/api/vendors/orders/delete', {
    vendor_id: parseInt(store.vendor_id),
    order_id: tableData.value[index].order_id
  })
  .then((resp) => {
    console.log(resp)
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      ElMessageBox.confirm('Delete Order Success!')
      .then(() => {
        tableData.value.splice(index, 1)
      })
      .catch(() => {
        tableData.value.splice(index, 1)
      })
    } else {
      throw new Error('Delete Order Fail!')
    }
  })
  .catch((err) => {
    console.log(err)
    ElMessageBox.confirm('Delete Order Fail!')
  })
}

const get_orders = () => {
  axios.post('/api/vendors/orders', {
    vendor_id: parseInt(store.vendor_id)
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      for (let i = 0; i < resp.data.data.orders.length; i++) {
        let sub_order = 'false'
        if (resp.data.data.orders[i].parent_order_id != resp.data.data.orders[i].order_id) {
          sub_order = 'true'
        }
        tableData.value.push({
          order_id: resp.data.data.orders[i].order_id,
          user_id: resp.data.data.orders[i].user_id,
          product_id: resp.data.data.orders[i].product_id,
          sub_order: sub_order,
          quantity: resp.data.data.orders[i].quantity,
          total_price: resp.data.data.orders[i].total_price,
          place_time: resp.data.data.orders[i].place_time,
          status: resp.data.data.orders[i].status,
          express_number: resp.data.data.orders[i].express_number
        })
      }
    } else {
      throw new Error('Get Products Fail!')
    }
  })
  .catch((err) => {
    console.log(err)
    ElMessageBox.confirm('Get Products Fail!')
    .then(() => {
      location.reload()
    })
    .catch(() => {
      location.reload()
    })
  })
}

const tableData = ref([])
onMounted(() => {
  if (store.vendor_id == 0) {
    setTimeout(() => {
      get_orders()
    }, 250)
  } else {
    get_orders()
  }
})

</script>

<style scoped>


</style>