<template>
  <div class="tw-w-full tw-h-full tw-bg-gray-100 tw-flex tw-items-center tw-justify-center tw-pt-4 tw-px-4">
    <div class="tw-w-full tw-h-full tw-bg-gray-50 tw-rounded-xl tw-flex tw-flex-col tw-px-10">
      <div>
        <p class="tw-text-xl"> Product Name </p>
        <input v-model="product_name" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Product Cover Url </p>
        <input v-model="product_cover" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Tags </p>
        <input v-model="tags" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Price </p>
        <input v-model="price" class="tw-h-8 tw-w-64" style="border:2px solid #d2d2d2"/>
      </div>
      <div>
        <p class="tw-text-xl"> Product Details </p>
        <textarea v-model="product_info" class="tw-w-64 tw-h-32" style="border:2px solid #d2d2d2"/>
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


const product_name = ref('')
const product_cover = ref('')
const tags = ref('')
const price = ref('')
const product_info = ref('')

const submit = () => {
  console.log("submit")
  console.log({
    vendor_id: parseInt(store.vendor_id),
    product_name: product_name.value,
    product_cover: product_cover.value,
    tags: tags.value,
    product_info: product_info.value
  })
  if (product_name.value == "" || product_cover.value == "" || tags.value == "" || price.value == "" || product_info.value == "" ) {
    ElMessageBox.confirm('Some fields are empty!')
		.then(() => {
		})
		.catch(() => {
		})
    return
  }

  axios.post('/api/vendors/products/create', {
    vendor_id: parseInt(store.vendor_id),
    product_name: product_name.value,
    product_cover: product_cover.value,
    tags: tags.value,
    price: parseInt(price.value),
    product_info: product_info.value
  })
  .then((resp) => {
    if (resp.data.code == 200 && resp.data.data.success == 1) {
      ElMessageBox.confirm('Submit Success!')
      .then(() => {
        product_name.value = ""
        product_cover.value = ""
        tags.value = ""
        price.value = ""
        product_info.value = ""
      })
      .catch(() => {
      })
    } else {
      ElMessageBox.confirm('Submit Fail!')
      .then(() => {
      })
      .catch(() => {
      })
    }
  })
  .catch((err) => {
    console.log(err)
  })
}
</script>

<style scoped>


</style>