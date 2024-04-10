<template>
  <div class="tw-w-full tw-h-full tw-bg-gray-100 tw-flex tw-items-center tw-justify-center tw-pt-4 tw-px-4">
    <div class="tw-w-full tw-h-full tw-bg-gray-50 tw-rounded-xl tw-flex tw-flex-col tw-px-10">
      <div>
        <p class="tw-text-xl"> Username </p>
        <input v-model="vendor_username" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Password </p>
        <input v-model="vendor_password" type="password" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> User Display Name </p>
        <input v-model="vendor_display_name" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Origin Address </p>
        <input v-model="origin_address" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Avatar </p>
        <input v-model="avatar" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
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


const vendor_username = ref('')
const vendor_password = ref('')
const vendor_display_name = ref('')
const origin_address = ref('')
const avatar = ref('')


const submit = () => {
  console.log("submit")

  if (vendor_username.value == "" || vendor_password.value == "" || vendor_display_name.value == "" || origin_address.value == "" || avatar.value == "" ) {
    ElMessageBox.confirm('Some fields are empty!')
		.then(() => {
		})
		.catch(() => {
		})
    return
  }

  axios.post('/api/admin/vendors/create', {
    vendor_username: vendor_username.value,
    vendor_password: vendor_password.value,
    vendor_display_name: vendor_display_name.value,
    origin_address: origin_address.value,
    avatar: avatar.value,
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      ElMessageBox.confirm('Submit Success!')
      .then(() => {
        vendor_username.value = ""
        vendor_password.value = ""
        vendor_display_name.value = ""
        origin_address.value = ""
        avatar.value = ""
      })
      .catch(() => {
        throw new Error('Submit Fail!')
      })
    } else {
      ElMessageBox.confirm('Submit Fail!')
      .then(() => {
      })
      .catch(() => {
      })
    }
  })
}
</script>

<style scoped>


</style>