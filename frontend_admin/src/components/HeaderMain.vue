<template>
  <div class="tw-h-14 tw-w-full tw-flex tw-items-center tw-flex-row-reverse" style="border-bottom: 0.5px solid #ddd;background: #fefefe" >
    <el-menu
      class="el-menu-demo"
      mode="horizontal"
      :collapse="false"
      :ellipsis="false"
    >
      <el-menu-item index="1" @click="urljump('/login/')">Login</el-menu-item>
      <el-menu-item index="2" @click="urljump('/register/')">Register</el-menu-item>
      <el-menu-item index="3" @click="urljump('/search/')">Search</el-menu-item>
      <el-menu-item index="4" @click="urljump('/user/my-orders')">My Orders</el-menu-item>
      <el-menu-item index="5" @click="urljump('/user/recharge')">Recharge</el-menu-item>
      <el-menu-item index="6" @click="urljump('/user/info')">Personal Info</el-menu-item>
      <el-menu-item index="7" @click="urljump('/user/chart')">My Chart</el-menu-item>
    </el-menu>
    <div class="tw-h-full tw-w-full tw-flex-none tw-flex">   
    </div>
  </div>
</template>

<script lang="ts" setup>


import { useStore } from '@/store/store'
import axios from 'axios'
import Cookies from 'js-cookie';
import { useRouter } from 'vue-router'

const store = useStore()



const router = useRouter()
let urljump = (url) => {  
  router.push(url)
}

</script>

<style scoped>


</style>