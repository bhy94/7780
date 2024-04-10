<template>
  <div class="tw-w-full tw-h-full tw-flex tw-items-center tw-justify-center" style="min-height: 90vh">
    <div class="tw-bg-gray-50 tw-rounded-2xl tw-flex tw-flex-col tw-items-center tw-justify-center" style="width:300px; height:400px">
    <p class="tw-text-xl"> User Login </p>
    <div class="tw-rounded-2xl tw-text-xl tw-p-6">
      <input v-model="inputUsername" type="text" placeholder="Username" />
    </div>
    <div class="tw-rounded-2xl tw-text-xl">
      <input v-model="inputPassword" type="password" placeholder="Password" />
    </div>
    <div class="tw-p-4">
      <el-button @click="login">Login</el-button>
    </div>
  </div>
  </div>
</template>

<script lang="ts" setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '@/store/store'
import { ElMessageBox } from 'element-plus'
import Cookies from 'js-cookie'

const store = useStore()
const router = useRouter()
const inputUsername = ref('')
const inputPassword = ref('')

const login_result = (success) => {
	if (success) {
		ElMessageBox.confirm('Login Success!')
		.then(() => {
			window.location.href = "/"
		})
		.catch(() => {
			window.location.href = "/"
		})
	} else {
		ElMessageBox.confirm('Login Fail!')
		.then(() => {
		})
		.catch(() => {
		})
	}
}

const login = () => {
  axios.post('/api/login', {
		username: inputUsername.value,
		password: inputPassword.value,
		destination: "front_end"
	})
	.then((resp) => {
		console.log(resp)
		if (resp.data.code == 200 && resp.data.data.success == 1) {
			Cookies.set("token", resp.data.data.token, {expires: 30});
			Cookies.set("user_username", inputUsername.value, {expires: 30});
			Cookies.set("user_id", resp.data.data.vendor_id, {expires: 30});
			Cookies.set("role", resp.data.data.role, {expires: 30});
			login_result(true)
		} else {
			login_result(false)
		}
	})
	.catch((err) => {
		console.log(err)
		login_result(false)
	})
}

</script>

<style scoped>


</style>