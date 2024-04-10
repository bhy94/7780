import request from '@/utils/http'


export const getDetail = (product_id) => {
  return request({
    url: '/products/info',
    params: {
      product_id
    }
  })
}

export const getHotGoodsAPI = ({ id, type, limit = 3 }) => {
  return request({
    url: '/goods/hot',
    params: {
      id,
      type,
      limit
    }
  })
}
