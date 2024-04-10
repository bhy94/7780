import httpInstance from '@/utils/http'
import request from "@/utils/http";


// 获取banner

export function getBannerAPI (params = {}) {
  // 默认为1 商品为2
  const { distributionSite = '1' } = params
  return httpInstance({
    url: '/home/banner',
    params: {
      distributionSite
    }
  })
}

/**
 * @description: 获取新鲜好物
 * @param {*}
 * @return {*}
 */
// export const findNewAPI = () => {
//   return httpInstance({
//     url: '/products'
//   })
// }
// export const findNewAPI = ({ tags, vendor_id }) => {
//   return request({
//     url: '/products',
//     method: 'POST',
//     data: {
//       tags,
//       vendor_id
//     }
//   })
// }
export const findNewAPI = (data) => {
  return request({
    url: '/products',
    method: 'POST',
    data
  })
}
/**
 * @description: 获取人气推荐
 * @param {*}
 * @return {*}
 */
export const getHotAPI = () => {
  return httpInstance({
    url: '/home/hot'
  })
}

/**
 * @description: 获取所有商品模块
 * @param {*}
 * @return {*}
 */
export const getGoodsAPI = () => {
  return httpInstance({
    url: '/home/goods'
  })
}
