import request from '@/utils/request'

/**
 * 获取机台耗时列表
 */
export function getMachineList(params) {
   return request({
    url: `/machine/list`,
    method: 'get',
    params: params
  })
}

/**
 * 获取机台耗时详情
 */
export function getMachineDetail(id) {
  return request({
    url: `/machine/detail/${id}`,
    method: 'get'
  })
}

/**
 * 创建机台耗时
 */
export function createMachine(data) {
  return request({
    url: '/machine/create',
    method: 'post',
    data
  })
}

/**
 * 更新机台耗时
 */
export function updateMachine(id, data) {
  return request({
    url: `/machine/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除机台耗时
 */
export function deleteMachine(id) {
  return request({
    url: `/machine/delete/${id}`,
    method: 'delete'
  })
}

/**
 * 批量删除机台耗时
 */
export function batchDeleteMachines(ids) {
  return request({
    url: '/machine/batch-delete',
    method: 'post',
    data: { ids }
  })
}
