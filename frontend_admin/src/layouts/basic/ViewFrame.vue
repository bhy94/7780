<template>
  <div class="tw-w-screen tw-h-screen tw-flex tw-flex-row">
    <SidePanel />
    <div class="tw-flex tw-h-full tw-w-full tw-flex-col">
      <Header1 />
      <router-view />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'
import axios from 'axios'
import SidePanel from '@/components/SidePanel.vue'
import Header1 from '@/components/Header1.vue'
import { useStore } from '@/store/store'
import Cookies from "js-cookie";

const store = useStore()

onMounted(() => {
  let vendor_id = Cookies.get("vendor_id")
  let role = Cookies.get("role")
  store.set_vendor_id(vendor_id)
  store.set_role(role)
  const params = {
    vendor_id: vendor_id
  }
  if (role != "admin") {
    axios.get('/api/vendors/info', {
      params: params
    })
    .then((resp) => {
      // store.vemdor_display_name = resp.data.data.vendor_display_name
      store.set_display_name(resp.data.data.vendor_display_name)
    })
  } else {
    store.set_display_name("Admin")
  }
  
})
</script>

<style scoped>


</style>