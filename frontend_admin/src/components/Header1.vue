<template>
    <div class="tw-h-10 tw-bg-gray-50 tw-w-full tw-flex-none">
        <div class="tw-h-3"></div>
        <el-header style="text-align: right; font-size: 12px">
          <div class="toolbar">
            <el-dropdown>
              <el-icon style="margin-right: 8px; margin-top: 1px"
                ><setting
              /></el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="logout">Logout</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <span> {{store.vendor_display_name}} </span>
          </div>
        </el-header>
      </div>
</template>

<script lang="ts" setup>


import { useStore } from '@/store/store'
import axios from 'axios'
import Cookies from 'js-cookie';
const store = useStore()


const logout = () => {
	axios.post('/api/logout', {
	}).then((res) => {
		console.log(res)
		store.set_display_name("")
		store.set_vendor_id("")
		store.set_role("")
		Cookies.remove("vendor_id")
		Cookies.remove("vendor_username")
		Cookies.remove("role")
		Cookies.remove("token")
		Cookies.remove("user_id")
		Cookies.remove("user_username")
		window.location.href = "/panel/login/"
	}).catch((err) => {
		console.log(err)
		store.set_display_name("")
		store.set_vendor_id("")
		store.set_role("")
		Cookies.remove("vendor_id")
		Cookies.remove("vendor_username")
		Cookies.remove("role")
		Cookies.remove("token")
		Cookies.remove("user_id")
		Cookies.remove("user_username")
		window.location.href = "/panel/login/"
	})
}

</script>

<style scoped>


</style>