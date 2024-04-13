<template>
    <el-table :data="tableData" style="width: 100%" min-height="250">
      <el-table-column fixed prop="user_id" label="User ID" width="150" />
      <el-table-column prop="balance_add" label="Balance Add" width="150" />
      <el-table-column prop="paypal_order_id" label="Paypal Order ID" width="200" />
    </el-table>
  </template>
  
  <script lang="ts" setup>
  
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useStore } from '@/store/store'
  import { ElMessageBox } from 'element-plus'
  
  
  const store = useStore()
  
  
  const tableData = ref([])
  const get_deposits = () => {
    axios.get('/api/vendors/deposits')
    .then((resp) => {
      if (resp.data.code == 200 && resp.data.data.success == 1) {
        console.log(resp.data)
        for (let i = 0; i < resp.data.data.deposits.length; i++) {
          tableData.value.push({
            user_id: resp.data.data.deposits[i].user_id,
            balance_add: resp.data.data.deposits[i].balance_add,
            paypal_order_id: resp.data.data.deposits[i].pporder_id,
          })
        }
      } else {
        throw new Error('Get deposits Fail!')
      }
    })
    .catch((err) => {
      console.log(err)
      ElMessageBox.confirm('Get deposits Fail!')
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
        get_deposits()
      }, 250)
    } else {
      get_deposits()
    }
  })
  
  </script>
  
  <style scoped>
  
  
  </style>