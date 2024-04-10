<template>
  <div class="tw-w-64  tw-h-full tw-flex tw-flex-none">
    <el-aside width="255px">
      <el-scrollbar>
        <el-menu :default-openeds="['1', '3']">
          <el-sub-menu index="1">
            <template #title>
              <span class="tw-text-2xl" style="font-weight:800">Admin Panel</span>
            </template>
            <el-menu-item-group v-if="store.role=='vendor'">
              <template #title>Vendor Management</template>
              <el-menu-item index="1-1" @click="urljump('/panel/add-product')">Add Product</el-menu-item>
              <el-menu-item index="1-2" @click="urljump('/panel/manage-products')">Products Management</el-menu-item>
              <el-menu-item index="1-3" @click="urljump('/panel/manage-orders')">Orders Management</el-menu-item>
              <el-menu-item index="1-4" @click="urljump('/panel/order-express')">Order Express</el-menu-item>
              <el-menu-item index="1-9" ></el-menu-item>
              <el-menu-item index="1-10" ></el-menu-item>
              <el-menu-item index="1-11" ></el-menu-item>
              <el-menu-item index="1-12" ></el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group v-if="store.role=='admin'">
              <template #title>Administration</template>
              <el-menu-item index="1-5" @click="urljump('/panel/add-user')">Add User</el-menu-item>
              <el-menu-item index="1-6" @click="urljump('/panel/manage-users')">Users Management</el-menu-item>
              <el-menu-item index="1-7" @click="urljump('/panel/add-vendor')">Add Vendor</el-menu-item>
              <el-menu-item index="1-8" @click="urljump('/panel/manage-vendors')">Vendors Management</el-menu-item>
              <el-menu-item index="1-9" ></el-menu-item>
              <el-menu-item index="1-10" ></el-menu-item>
              <el-menu-item index="1-11" ></el-menu-item>
              <el-menu-item index="1-12" ></el-menu-item>
            </el-menu-item-group>
          </el-sub-menu>
        </el-menu>
      </el-scrollbar>
    </el-aside>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useStore } from '@/store/store'

const store = useStore()
if (store.role == 'vendor') {

}

const router = useRouter()
let urljump = (url) => {  
  router.push(url)
}
</script>