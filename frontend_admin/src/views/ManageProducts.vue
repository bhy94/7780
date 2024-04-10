<template>
  <el-table :data="tableData" style="width: 100%" min-height="250">
    <el-table-column fixed prop="product_name" label="Product Name" width="150" />
    <el-table-column prop="product_cover" label="Product Cover" width="150" />
    <el-table-column prop="product_info" label="Product Info" width="120" />
    <el-table-column prop="price" label="Price" width="120" />
    <el-table-column prop="score" label="Score" width="120" />
    <el-table-column prop="tags" label="Tags" width="120" />
    <el-table-column fixed="right" label="Operations" width="120">
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
  axios.post('/api/vendors/products/delete', {
    vendor_id: parseInt(store.vendor_id),
    product_id: tableData.value[index].product_id
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      ElMessageBox.confirm('Delete Product Success!')
      .then(() => {
        tableData.value.splice(index, 1)
      })
      .catch(() => {
        tableData.value.splice(index, 1)
      })
    } else {
      throw new Error('Delete Product Fail!')
    }
  })
  .catch((err) => {
    console.log(err)
    ElMessageBox.confirm('Delete Product Fail!')
  })
}
const tableData = ref([])
const get_products = () => {
  axios.post('/api/vendors/products', {
    vendor_id: parseInt(store.vendor_id)
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      for (let i = 0; i < resp.data.data.products.length; i++) {
        tableData.value.push({
          product_id: resp.data.data.products[i].product_id,
          product_name: resp.data.data.products[i].product_name,
          product_cover: resp.data.data.products[i].product_cover,
          product_info: resp.data.data.products[i].product_info,
          price: resp.data.data.products[i].price,
          score: resp.data.data.products[i].product_score,
          tags: resp.data.data.products[i].tags
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
onMounted(() => {
  if (store.vendor_id == 0) {
    setTimeout(() => {
      get_products()
    }, 250)
  } else {
    get_products()
  }
})

</script>

<style scoped>


</style>