import request from '@/utils/request'

/**
 * 经营数据分析 API
 */
export const businessAnalysisApi = {
  // FIB/TEM检测暂估收入（月度）- 上海
  getFibTemEstimatedRevenue: (params) => {
    return request({
      url: '/business/fib-tem-estimated-revenue',
      method: 'get',
      params
    })
  },
  // 珠海检测暂估收入（月度）
  getZhuhaiEstimatedRevenue: (params) => {
    return request({
      url: '/business/zhuhai-estimated-revenue',
      method: 'get',
      params
    })
  }
}
