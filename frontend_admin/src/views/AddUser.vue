<template>
  <div class="tw-w-full tw-h-full tw-bg-gray-100 tw-flex tw-items-center tw-justify-center tw-pt-4 tw-px-4">
    <div class="tw-w-full tw-h-full tw-bg-gray-50 tw-rounded-xl tw-flex tw-flex-col tw-px-10">
      <div>
        <p class="tw-text-xl"> Username </p>
        <input v-model="user_username" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Password </p>
        <input v-model="user_password" type="password" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> User Display Name </p>
        <input v-model="user_display_name" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Address </p>
        <input v-model="address" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Avatar </p>
        <input v-model="avatar" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Telephone Number </p>
        <input v-model="telephone_number" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
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


const user_username = ref('')
const user_password = ref('')
const user_display_name = ref('')
const address = ref('')
const avatar = ref('')
const telephone_number = ref('')

const submit = () => {
  console.log("submit")

  if (user_username.value == "" || user_password.value == "" || user_display_name.value == "" || address.value == "" || avatar.value == "" || telephone_number.value == "" ) {
    ElMessageBox.confirm('Some fields are empty!')
		.then(() => {
		})
		.catch(() => {
		})
    return
  }

  axios.post('/api/admin/users/create', {
    user_username: user_username.value,
    user_password: user_password.value,
    user_display_name: user_display_name.value,
    address: address.value,
    avatar: avatar.value,
    telephone_number: telephone_number.value
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      ElMessageBox.confirm('Submit Success!')
      .then(() => {
        user_username.value = ""
        user_password.value = ""
        user_display_name.value = ""
        address.value = ""
        avatar.value = ""
        telephone_number.value = ""
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