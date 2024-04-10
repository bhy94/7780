<template>
  <el-table :data="tableData" style="width: 100%; height: 100%">
    <el-table-column fixed prop="user_id" label="User ID" width="100" />
    <el-table-column prop="user_display_name" label="Display Name" width="150" />
    <el-table-column prop="balance" label="Balance" width="100" />
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
  axios.post('/api/admin/users/delete', {
    user_id: parseInt(tableData.value[index].user_id),
    vendor_id: 0,
    role: "users"
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

const get_users = () => {
  axios.post('/api/admin/users', {
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      for (let i = 0; i < resp.data.data.users.length; i++) {
        tableData.value.push({
          user_id: resp.data.data.users[i].user_id,
          user_display_name: resp.data.data.users[i].user_display_name,
          balance: resp.data.data.users[i].balance
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
      get_users()
    }, 250)
  } else {
    get_users()
  }
})

</script>

<style scoped>


</style>