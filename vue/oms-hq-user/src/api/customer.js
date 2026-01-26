import request from '@/utils/request'

/**
 * 获取客户列表
 */
export function getCustomerList(pageParams = {}) {
  const { index = 1, size = 10 } = pageParams
  
  return request({
    url: 'http://ftp.hq-nano.com:10001/api/bmapi/v1/data/64e577b3094fc3a856105278/64e5d12e094fc3a8561196d4/query',
    method: 'post',
    data: {
      "view": "collection-64e5d12e094fc3a8561196d4-1692934567773",
      "option": {
        "simple": true
      },
      "page": {
        "index": index,
        "size": size
      }
    },
    headers: {
      'Content-Type': 'application/json',
      'bm-x-token': '26a3778470ee44e7b3205df317d1285e'
    }
  })
}

/**
 * 获取客户详情
 */
export function getCustomerDetail(id) {
  return request({
    url: `/customer/detail/${id}`,
    method: 'get'
  })
}

/**
 * 创建客户
 */
export function createCustomer(data) {
  return request({
    url: '/customer/create',
    method: 'post',
    data
  })
}

/**
 * 更新客户
 */
export function updateCustomer(id, data) {
  return request({
    url: `/customer/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除客户
 */
export function deleteCustomer(id) {
  return request({
    url: `/customer/delete/${id}`,
    method: 'delete'
  })
}
