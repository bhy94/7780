// 封装banner轮播图相关的业务代码
import { ref, onMounted } from 'vue'
import { getBannerAPI } from '@/apis/home'

export function useBanner () {
  const bannerList = ref([
    {
      id: 1,
      imgUrl: "https://img.ltwebstatic.com/images3_ccc/2024/03/25/4d/1711334730b0df19346e3d654c3e10dcac54c307f7_thumbnail_2000x.jpg"
    },
    {
      id: 2,
      imgUrl: "https://img.ltwebstatic.com/images3_ccc/2024/03/25/4d/1711334730b0df19346e3d654c3e10dcac54c307f7_thumbnail_2000x.jpg"
    },
    {
      id: 3,
      imgUrl: "https://img.ltwebstatic.com/images3_ccc/2024/03/25/4d/1711334730b0df19346e3d654c3e10dcac54c307f7_thumbnail_2000x.jpg"
    },
    {
      id: 4,
      imgUrl: "https://img.ltwebstatic.com/images3_ccc/2024/03/25/4d/1711334730b0df19346e3d654c3e10dcac54c307f7_thumbnail_2000x.jpg"
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
