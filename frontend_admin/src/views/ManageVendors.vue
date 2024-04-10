<template>
  <el-table :data="tableData" style="width: 100%; height: 100%">
    <el-table-column fixed prop="vendor_id" label="Vendor ID" width="100" />
    <el-table-column prop="vendor_display_name" label="Display Name" width="150" />
    <el-table-column prop="product_count" label="Product Count" width="100" />
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
  axios.post('/api/admin/vendors/delete', {
    user_id: 0,
    vendor_id: parseInt(tableData.value[index].vendor_id),
    role: "vendors"
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

const get_vendors = () => {
  axios.post('/api/admin/vendors', {
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      for (let i = 0; i < resp.data.data.vendors.length; i++) {
        tableData.value.push({
          vendor_id: resp.data.data.vendors[i].vendor_id,
          vendor_display_name: resp.data.data.vendors[i].vendor_display_name,
          product_count: resp.data.data.vendors[i].product_count  
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
      get_vendors()
    }, 250)
  } else {
    get_vendors()
  }
})

</script>

<style scoped>


</style>