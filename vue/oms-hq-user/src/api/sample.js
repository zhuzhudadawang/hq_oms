import request from '@/utils/request'

/**
 * 获取样点列表
 */
export function getSampleList(params) {
   return request({
    url: `/sample/list`,
    method: 'get',
    params: params
  })
}

/**
 * 获取样点详情
 */
export function getSampleDetail(id) {
  return request({
    url: `/sample/detail/${id}`,
    method: 'get'
  })
}

/**
 * 创建样点
 */
export function createSample(data) {
  return request({
    url: '/sample/create',
    method: 'post',
    data
  })
}

/**
 * 更新样点
 */
export function updateSample(id, data) {
  return request({
    url: `/sample/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除样点
 */
export function deleteSample(id) {
  return request({
    url: `/sample/delete/${id}`,
    method: 'delete'
  })
}

/**
 * 批量删除样点
 */
export function batchDeleteSamples(ids) {
  return request({
    url: '/sample/batch-delete',
    method: 'post',
    data: { ids }
  })
}
