// 封装banner轮播图相关的业务代码
import { ref, onMounted } from 'vue'
import { getBannerAPI } from '@/apis/home'

export function useBanner () {
  const bannerList = ref([
    {
      id: 1,
      imgUrl: "https://imgur.com/9TpzGYX.png"
    },
    {
      id: 2,
      imgUrl: "https://imgur.com/9TpzGYX.png"
    },
    {
      id: 3,
      imgUrl: "https://imgur.com/9TpzGYX.png"
    },
    {
      id: 4,
      imgUrl: "https://imgur.com/9TpzGYX.png"
    }
  ])

  const getBanner = async () => {
    // const res = await getBannerAPI({
    //   distributionSite: '2'
    // })
    console.log(res)
    bannerList.value = res.result
  }

  onMounted(() => getBanner())

  return {
    bannerList
  }
}
