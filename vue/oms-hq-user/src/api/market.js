import request from '@/utils/request'

/**
 * 市场数据分析 API
 */
export const marketAnalysisApi = {
  // 珠海订单月度统计
  getZhuhaiMonthly: (params) => {
    return request({
      url: '/market/zhuhai/monthly',
      method: 'get',
      params
    })
  },
  // 珠海订单周度统计
  getZhuhaiWeekly: (params) => {
    return request({
      url: '/market/zhuhai/weekly',
      method: 'get',
      params
    })
  },
  // 珠海订单与样点统计
  getZhuhaiOrderSample: (params) => {
    return request({
      url: '/market/zhuhai/order-sample',
      method: 'get',
      params
    })
  },
  // 珠海机台利用率统计
  getZhuhaiMachineUtilization: (params) => {
    return request({
      url: '/market/zhuhai/machine-utilization',
      method: 'get',
      params
    })
  },
   // 珠海重点客户统计
  getZhuhaiKeyCustomers: (params) => {
    return request({
      url: '/market/zhuhai/key-customers', 
      method: 'get',
      params
    })
  },
  // 上海订单与样点统计
  getShanghaiOrderSample: (params) => {
    return request({
      url: '/market/shanghai/order-sample',
      method: 'get',
      params
    })
  },
  // 珠海重点客户统计
  getShanghaiKeyCustomers: (params) => {
    return request({
      url: '/market/shanghai/key-customers', 
      method: 'get',
      params
    })
  },
   // 上海订单月度统计
  getShanghaiMonthly: (params) => {
    return request({
      url: '/market/shanghai/monthly',
      method: 'get',
      params
    })
  },
}