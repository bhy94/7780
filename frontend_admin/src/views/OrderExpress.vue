<template>
  <div class="tw-w-full tw-h-full tw-bg-gray-100 tw-flex tw-items-center tw-justify-center tw-pt-4 tw-px-4">
    <div class="tw-w-full tw-h-full tw-bg-gray-50 tw-rounded-xl tw-flex tw-flex-col tw-px-10">
      <div>
        <p class="tw-text-xl"> Order ID </p>
        <input v-model="order_id" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Express Number </p>
        <input v-model="express_number" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div class="tw-py-4">
				<el-button size="large" @click="submit">Submit</el-button>
			</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import axios from 'axios'
import { ref } from 'vue'
import { useStore } from '@/store/store'
import { ElMessageBox } from 'element-plus'


const store = useStore()


const order_id = ref('')
const express_number = ref('')


const submit = () => {
  console.log("submit")
  if (order_id.value == "" || express_number.value == "" ) {
    ElMessageBox.confirm('Some fields are empty!')
		.then(() => {
		})
		.catch(() => {
		})
    return
  }

  axios.post('/api/vendors/orders/express', {
    vendor_id: parseInt(store.vendor_id),
    order_id: parseInt(order_id.value),
    express_number: express_number.value
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      ElMessageBox.confirm('Submit Success!')
      .then(() => {
        order_id.value = ""
        express_number.value = ""
      })
      .catch(() => {
      })
    } else {
      throw new Error('Submit Fail!')
    }
  })
  .catch((err) => {
    ElMessageBox.confirm('Submit Fail!')
    .then(() => {
    })
    .catch(() => {
    })
  })
}
</script>

<style scoped>


</style>