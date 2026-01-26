import request from '@/utils/request'

/**
 * 获取订单列表
 */
// export function getOrderList(pageParams = {}) {
//   const { index = 1, size = 10 } = pageParams
  
//   return request({
//     url: 'http://ftp.hq-nano.com:10001/api/bmapi/v1/data/64e577b3094fc3a856105278/64e5cf8e72b119a857ce7073/query',
//     method: 'post',
//     data: {
//       "view": "collection-64e5cf8e72b119a857ce7073-1692934901286",
//       "option": {
//         "simple": true
//       },
//       "page": {
//         "index": index,
//         "size": size
//       }
//     },
//     headers: {
//       'Content-Type': 'application/json',
//       'bm-x-token': '26a3778470ee44e7b3205df317d1285e'
//     }
//   })
// }

// 后端获取
export function getOrderList(params) {
   return request({
    url: `/order/list`,
    method: 'get',
    params: params
  })
}

/**
 * 获取订单详情
 */
export function getOrderDetail(id) {
  return request({
    url: `/order/detail/${id}`,
    method: 'get'
  })
}

/**
 * 创建订单
 */
export function createOrder(data) {
  return request({
    url: '/order/create',
    method: 'post',
    data
  })
}

/**
 * 更新订单
 */
export function updateOrder(id, data) {
  return request({
    url: `/order/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除订单
 */
export function deleteOrder(id) {
  return request({
    url: `/order/delete/${id}`,
    method: 'delete'
  })
}

/**
 * 批量删除订单
 */
export function batchDeleteOrders(ids) {
  return request({
    url: '/order/batch-delete',
    method: 'post',
    data: { ids }
  })
}
