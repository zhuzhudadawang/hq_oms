import request from '@/utils/request'

/**
 * 样点成功率相关 API
 */
export const SampleSuccessApi = {
  // 获取样点成功率数据
  getData: (params) => {
    return request({
      url: '/analysis/sample-success',
      method: 'get',
      params
    })
  },
  
  // 获取统计数据
  getStats: (params) => {
    return request({
      url: '/analysis/sample-success/stats',
      method: 'get',
      params
    })
  },
  
  // 导出报表
  exportReport: (params) => {
    return request({
      url: '/analysis/sample-success/export',
      method: 'post',
      data: params,
      responseType: 'blob'
    })
  }
}
// 获取FIB样点成功率数据
export const fibSampleSuccessApi = {
  // 获取样点成功率数据
  getData: (params) => {
    return request({
      url: '/analysis/fib-sample-success',
      method: 'get',
      params
    })
  }
}
// 获取FIB内部样点成功率数据
export const fibInternalSampleSuccessApi = {
  // 获取样点成功率数据
  getData: (params) => {
    return request({
      url: '/analysis/fib-internal-sample-success',
      method: 'get',
      params
    })
  }
}
// 获取FIB外部样点成功率数据
export const fibExternalSampleSuccessApi = {
  // 获取样点成功率数据
  getData: (params) => {
    return request({
      url: '/analysis/fib-external-sample-success',
      method: 'get',
      params
    })
  }
}
// 获取TEM样点成功率数据
export const temSampleSuccessApi = {
  // 获取样点成功率数据
  getData: (params) => {
    return request({
      url: '/analysis/tem-sample-success',
      method: 'get',
      params
    })
  },
}
// 获取TEM内部样点成功率数据
export const temInternalSampleSuccessApi = {
  // 获取样点成功率数据
  getData: (params) => {
    return request({
      url: '/analysis/tem-internal-sample-success',
      method: 'get',
      params
    })
  },
}
// 获取TEM外部样点成功率数据
export const temExternalSampleSuccessApi = {
  // 获取样点成功率数据
  getData: (params) => {
    return request({
      url: '/analysis/tem-external-sample-success',
      method: 'get',
      params
    })
  },
}
// 获取FIB客户样点成功率数据
export const fibCustomerSampleSuccessApi = {
  // 获取样点成功率数据
  getData: (params) => {
    return request({
      url: '/analysis/fib-customer/daily-stats',
      method: 'get',
      params
    })
  },
}



/**
 * FIB人员产出相关 API
 */
export const fibOutputApi = {
  // 获取人员产出数据
  getData: (params) => {
    return request({
      url: '/analysis/fib-output',
      method: 'get',
      params
    })
  },
  
  // 获取人员列表
  getPersonList: () => {
    return request({
      url: '/analysis/fib-output/persons',
      method: 'get'
    })
  },
  
  // 获取人员详情
  getPersonDetail: (id) => {
    return request({
      url: `/analysis/fib-output/person/${id}`,
      method: 'get'
    })
  }
}

/**
 * TEM人员产出相关 API
 */
export const temOutputApi = {
  // 获取人员产出数据
  getData: (params) => {
    return request({
      url: '/analysis/tem-output',
      method: 'get',
      params
    })
  },
  
  // 获取人员列表
  getPersonList: () => {
    return request({
      url: '/analysis/tem-output/persons',
      method: 'get'
    })
  }
}

/**
 * 人员饱和度相关 API
 */
export const saturationApi = {
  // 获取饱和度数据
  getData: (params) => {
    return request({
      url: '/analysis/saturation',
      method: 'get',
      params
    })
  },
  
  // 获取饱和度趋势
  getTrend: (params) => {
    return request({
      url: '/analysis/saturation/trend',
      method: 'get',
      params
    })
  }
}
  // 获取FIB平均饱和度数据
export const fibSaturationApi = {
  getData: (params) => {
    return request({
      url: '/analysis/fib-saturation',
      method: 'get',
      params
    })
  },
} 
// 获取TEM平均饱和度数据
export const temSaturationApi = {
  getData: (params) => {
    return request({
      url: '/analysis/tem-saturation',
      method: 'get',
      params
    })
  },
}  
/**
 * 机台饱和度相关 API
 */
export const machineSaturationApi = {
  // 获取机台饱和度数据
  getData: (params) => {
    return request({
      url: '/analysis/machine-saturation',
      method: 'get',
      params
    })
  },
  
  // 获取机台列表
  getMachineList: () => {
    return request({
      url: '/analysis/machine-saturation/machines',
      method: 'get'
    })
  },
  
  // 获取机台详情
  getMachineDetail: (id) => {
    return request({
      url: `/analysis/machine-saturation/machine/${id}`,
      method: 'get'
    })
  }
}

/**
 * FIB利用率相关 API
 */
export const fibInternalUtilizationApi = {
  // 获取内部利用率数据
  getData: (params) => {
    return request({
      url: '/analysis/fib-utilization-internal',
      method: 'get',
      params
    })
  }
}

export const fibExternalUtilizationApi = {
  // 获取外部利用率数据
  getData: (params) => {
    return request({
      url: '/analysis/fib-utilization-external',
      method: 'get',
      params
    })
  }
}

/**
 * TEM利用率相关 API
 */
export const temInternalUtilizationApi = {
  // 获取内部利用率数据
  getData: (params) => {
    return request({
      url: '/analysis/tem-utilization-internal',
      method: 'get',
      params
    })
  }
}
export const temExternalUtilizationApi = {
  // 获取外部利用率数据
  getData: (params) => {
    return request({
      url: '/analysis/tem-utilization-external',
      method: 'get',
      params
    })
  }
}

/**
 * FIB完成率相关 API
 */
export const fibCompletionApi = {
  // 获取完成率数据
  getData: (params) => {
    return request({
      url: '/analysis/fib-completion',
      method: 'get',
      params
    })
  }
}

/**
 * TEM完成率相关 API
 */
export const temCompletionApi = {
  // 获取完成率数据
  getData: (params) => {
    return request({
      url: '/analysis/tem-completion',
      method: 'get',
      params
    })
  }
}

/**
 * FIB人员绩效相关 API
 */
export const fibPerformanceApi = {
  // 获取完成率数据
  getData: (params) => {
    return request({
      url: '/analysis/fib-performance',
      method: 'get',
      params
    })
  }
}
/**
 * TEM人员绩效相关 API
 */
export const temPerformanceApi = {
  // 获取完成率数据
  getData: (params) => {
    return request({
      url: '/analysis/tem-performance',
      method: 'get',
      params
    })
  }
}

/**
 * 市场数据分析 API
 */
export const marketAnalysisApi = {
  // 珠海订单月度统计
  getZhuhaiMonthly: (params) => {
    return request({
      url: '/analysis/market/zhuhai/monthly',
      method: 'get',
      params
    })
  },
  // 珠海订单周度统计
  getZhuhaiWeekly: (params) => {
    return request({
      url: '/analysis/market/zhuhai/weekly',
      method: 'get',
      params
    })
  },
  // 珠海订单与样点统计
  getZhuhaiOrderSample: (params) => {
    return request({
      url: '/analysis/market/zhuhai/order-sample',
      method: 'get',
      params
    })
  },
  // 珠海机台利用率统计
  getZhuhaiMachineUtilization: (params) => {
    return request({
      url: '/analysis/market/zhuhai/machine-utilization',
      method: 'get',
      params
    })
  },
  // 上海订单与样点统计
  getShanghaiOrderSample: (params) => {
    return request({
      url: '/analysis/market/shanghai/order-sample',
      method: 'get',
      params
    })
  }
}
