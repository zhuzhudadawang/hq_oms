import request from '@/utils/request'

/**
 * 获取工序列表
 */
export function getProcessList(params) {
   return request({
    url: `/process/list`,
    method: 'get',
    params: params
  })
}

/**
 * 获取工序详情
 */
export function getProcessDetail(id) {
  return request({
    url: `/process/detail/${id}`,
    method: 'get'
  })
}

/**
 * 创建工序
 */
export function createProcess(data) {
  return request({
    url: '/process/create',
    method: 'post',
    data
  })
}

/**
 * 更新工序
 */
export function updateProcess(id, data) {
  return request({
    url: `/process/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除工序
 */
export function deleteProcess(id) {
  return request({
    url: `/process/delete/${id}`,
    method: 'delete'
  })
}

/**
 * 批量删除工序
 */
export function batchDeleteProcesses(ids) {
  return request({
    url: '/process/batch-delete',
    method: 'post',
    data: { ids }
  })
}
