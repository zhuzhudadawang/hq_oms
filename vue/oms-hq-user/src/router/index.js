import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import Layout from '@/layout/index.vue'

// 公开路由（不需要登录）
export const constantRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '首页', icon: 'DataLine', requiresAuth: true }
      }
    ]
  }
]

// 需要权限的路由
export const asyncRoutes = [
  // {
  //   path: '/order',
  //   component: Layout,
  //   redirect: '/order/list',
  //   meta: {
  //     title: '订单管理',
  //     icon: 'ShoppingCart',
  //     requiresAuth: true,
  //     roles: ['admin', 'manager', 'user'],
  //     permissions: ['order:view']
  //   },
  //   children: [
  //     {
  //       path: 'list',
  //       name: 'OrderList',
  //       component: () => import('@/views/order/list.vue'),
  //       meta: {
  //         title: '订单列表',
  //         icon: 'List',
  //         permissions: ['order:view']
  //       }
  //     },
  //     {
  //       path: 'detail/:id',
  //       name: 'OrderDetail',
  //       component: () => import('@/views/order/detail.vue'),
  //       meta: {
  //         title: '订单详情',
  //         hidden: true,
  //         permissions: ['order:view']
  //       }
  //     },
  //   ]
  // },
  // {
  //   path: '/process',
  //   component: Layout,
  //   redirect: '/process/list',
  //   meta: {
  //     title: '工序管理',
  //     icon: 'ShoppingCart',
  //     requiresAuth: true,
  //     roles: ['admin', 'manager', 'user'],
  //     permissions: ['process:view']
  //   },
  //   children: [
  //     {
  //       path: 'list',
  //       name: 'ProcessList',
  //       component: () => import('@/views/process/list.vue'),
  //       meta: {
  //         title: '工序列表',
  //         icon: 'List',
  //         permissions: ['process:view']
  //       }
  //     },
  //     {
  //       path: 'detail/:process_id',
  //       name: 'ProcessDetail',
  //       component: () => import('@/views/process/detail.vue'),
  //       meta: {
  //         title: '工序详情',
  //         hidden: true,
  //         permissions: ['process:view']
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/sample',
  //   component: Layout,
  //   redirect: '/sample/list',
  //   meta: {
  //     title: '样点管理',
  //     icon: 'ShoppingCart',
  //     requiresAuth: true,
  //     roles: ['admin', 'manager', 'user'],
  //     permissions: ['sample:view']
  //   },
  //   children: [
  //     {
  //       path: 'list',
  //       name: 'SampleList',
  //       component: () => import('@/views/sample/list.vue'),
  //       meta: {
  //         title: '样点列表',
  //         icon: 'List',
  //         permissions: ['sample:view']
  //       }
  //     },
  //     {
  //       path: 'detail/:sample_id',
  //       name: 'SampleDetail',
  //       component: () => import('@/views/sample/detail.vue'),
  //       meta: {
  //         title: '样点详情',
  //         hidden: true,
  //         permissions: ['sample:view']
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/machine',
  //   component: Layout,
  //   redirect: '/machine/list',
  //   meta: {
  //     title: '机台管理',
  //     icon: 'ShoppingCart',
  //     requiresAuth: true,
  //     roles: ['admin', 'manager', 'user'],
  //     permissions: ['machine:view']
  //   },
  //   children: [
  //     {
  //       path: 'list',
  //       name: 'MachineList',
  //       component: () => import('@/views/machine/list.vue'),
  //       meta: {
  //         title: '机台耗时列表',
  //         icon: 'List',
  //         permissions: ['machine:view']
  //       }
  //     },
  //     {
  //       path: 'detail/:record_id',
  //       name: 'MachineDetail',
  //       component: () => import('@/views/machine/detail.vue'),
  //       meta: {
  //         title: '机台耗时详情',
  //         hidden: true,
  //         permissions: ['machine:view']
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/customer',
  //   component: Layout,
  //   redirect: '/customer/list',
  //   meta: {
  //     title: '客户管理',
  //     icon: 'User',
  //     requiresAuth: true,
  //     roles: ['admin', 'manager'],
  //     permissions: ['customer:view']
  //   },
  //   children: [
  //     {
  //       path: 'list',
  //       name: 'CustomerList',
  //       component: () => import('@/views/customer/list.vue'),
  //       meta: {
  //         title: '客户列表',
  //         icon: 'List',
  //         permissions: ['customer:view']
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/product',
  //   component: Layout,
  //   redirect: '/product/list',
  //   meta: {
  //     title: '产品管理',
  //     icon: 'Goods',
  //     requiresAuth: true,
  //     roles: ['admin', 'manager'],
  //     permissions: ['product:view']
  //   },
  //   children: [
  //     {
  //       path: 'list',
  //       name: 'ProductList',
  //       component: () => import('@/views/product/list.vue'),
  //       meta: {
  //         title: '产品列表',
  //         icon: 'List',
  //         permissions: ['product:view']
  //       }
  //     }
  //   ]
  // },
  {
    path: '/analysis',
    component: Layout,
    redirect: '/analysis/fib-sample-success',
    meta: {
      title: '工程数据分析',
      icon: 'TrendCharts',
      requiresAuth: true,
      roles: ['admin', 'engineering_admin'],
      permissions: ['analysis:view']
    },
    children: [
      {
        path: 'fib-sample-success',
        name: 'FibSampleSuccess',
        component: () => import('@/views/analysis/fib-sample-success.vue'),
        meta: {
          title: 'FIB样点成功率',
          icon: 'DataAnalysis',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'tem-sample-success',
        name: 'TemSampleSuccess',
        component: () => import('@/views/analysis/tem-sample-success.vue'),
        meta: {
          title: 'Tem样点成功率',
          icon: 'DataAnalysis',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'fib-output',
        name: 'FibOutput',
        component: () => import('@/views/analysis/fib-output.vue'),
        meta: {
          title: 'FIB人员产出',
          icon: 'DataLine',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'tem-output',
        name: 'TemOutput',
        component: () => import('@/views/analysis/tem-output.vue'),
        meta: {
          title: 'TEM人员产出',
          icon: 'DataLine',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'saturation',
        name: 'Saturation',
        component: () => import('@/views/analysis/saturation.vue'),
        meta: {
          title: '人员平均饱和度',
          icon: 'PieChart',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'machine-saturation',
        name: 'MachineSaturation',
        component: () => import('@/views/analysis/machine-saturation.vue'),
        meta: {
          title: '内部机台饱和度',
          icon: 'PieChart',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'fib-utilization',
        name: 'FibUtilization',
        component: () => import('@/views/analysis/fib-utilization.vue'),
        meta: {
          title: 'FIB内外部利用率',
          icon: 'Histogram',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'tem-utilization',
        name: 'TemUtilization',
        component: () => import('@/views/analysis/tem-utilization.vue'),
        meta: {
          title: 'TEM内外部利用率',
          icon: 'Histogram',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'fib-completion',
        name: 'FibCompletion',
        component: () => import('@/views/analysis/fib-completion.vue'),
        meta: {
          title: 'FIB人员完成率(月度)',
          icon: 'Calendar',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'tem-completion',
        name: 'TemCompletion',
        component: () => import('@/views/analysis/tem-completion.vue'),
        meta: {
          title: 'TEM人员完成率(月度)',
          icon: 'Calendar',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'fib-performance',
        name: 'FibPerformance',
        component: () => import('@/views/analysis/fib-performance.vue'),
        meta: {
          title: 'FIB人员绩效(月度)',
          icon: 'Calendar',
          permissions: ['analysis:view']
        }
      },
      {
        path: 'tem-performance',
        name: 'TemPerformance',
        component: () => import('@/views/analysis/tem-performance.vue'),
        meta: {
          title: 'TEM人员绩效(月度)',
          icon: 'Calendar',
          permissions: ['analysis:view']
        }
      },
   
    ]
  },
  {
    path: '/market',
    component: Layout,
    redirect: '/market/zhuhai-monthly',
    meta: {
      title: '市场数据分析',
      icon: 'Histogram',
      requiresAuth: true,
      roles: ['admin', 'market_admin'],
      permissions: ['market:view']
    },
    children: [
      {
        path: 'zhuhai-monthly',
        name: 'MarketZhuhaiMonthly',
        component: () => import('@/views/market/zhuhai-monthly.vue'),
        meta: {
          title: '珠海订单统计（月度）',
          icon: 'TrendCharts',
          permissions: ['market:view']
        }
      },
      {
        path: 'zhuhai-weekly',
        name: 'MarketZhuhaiWeekly',
        component: () => import('@/views/market/zhuhai-weekly.vue'),
        meta: {
          title: '珠海订单统计（周度）',
          icon: 'Calendar',
          permissions: ['market:view']
        }
      },
      {
        path: 'zhuhai-order-sample',
        name: 'MarketZhuhaiOrderSample',
        component: () => import('@/views/market/zhuhai-order-sample.vue'),
        meta: {
          title: '珠海订单&样点统计',
          icon: 'Histogram',
          permissions: ['market:view']
        }
      },
      {
        path: 'zhuhai-key-customers',
        name: 'MarketZhuhaiKeyCustomers',
        component: () => import('@/views/market/zhuhai-key-customers.vue'),
        meta: {
          title: '珠海重要客户统计',
          icon: 'UserFilled',
          permissions: ['market:view']
        }
      },
      {
        path: 'zhuhai-machine-utilization',
        name: 'MarketZhuhaiMachineUtilization',
        component: () => import('@/views/market/zhuhai-machine-utilization.vue'),
        meta: {
          title: '珠海机台利用率统计',
          icon: 'Operation',
          permissions: ['market:view']
        }
      },
      {
        path: 'shanghai-monthly',
        name: 'MarketShanghaiMonthly',
        component: () => import('@/views/market/shanghai-monthly.vue'),
        meta: {
          title: '上海case统计（月度）',
          icon: 'TrendCharts',
          permissions: ['market:view']
        }
      },
      {
        path: 'shanghai-order-sample',
        name: 'MarketShanghaiOrderSample',
        component: () => import('@/views/market/shanghai-order-sample.vue'),
        meta: {
          title: '上海订单&样点统计',
          icon: 'Histogram',
          permissions: ['market:view']
        }
      },
      {
        path: 'shanghai-key-customers',
        name: 'MarketShanghaiKeyCustomers',
        component: () => import('@/views/market/shanghai-key-customers.vue'),
        meta: {
          title: '上海重要客户统计',
          icon: 'User',
          permissions: ['market:view']
        }
      },
      {
        path: 'customer-sample-success',
        name: 'CustomerSampleSuccess',
        component: () => import('@/views/analysis/fib-customer-sample-success.vue'),
        meta: {
          title: 'FIB客户样点成功率',
          icon: 'User'
        }
      }
    ]
  },
  {
  path: '/business',
  component: Layout,
  redirect: '/business/management-finance', // 修改重定向到第一个子菜单
  meta: {
    title: '经营数据分析',
    icon: 'DataAnalysis',
    requiresAuth: true,
    roles: ['admin']
  },
  children: [
    {
      path: 'management-finance',
      name: 'ManagementFinance',
      component: () => import('@/views/business/management-finance.vue'),
      meta: {
        title: '管理层财务概况表',
        icon: 'DataLine',
        permissions: ['business:view']
      }
    },
    {
      path: 'founder-finance',
      name: 'FounderFinance',
      component: () => import('@/views/business/founder-finance.vue'),
      meta: {
        title: '创始股东财务概况表',
        icon: 'DataLine',
        permissions: ['business:view']
      }
    },
    {
      path: 'founder-assets',
      name: 'FounderAssets',
      component: () => import('@/views/business/founder-assets.vue'),
      meta: {
        title: '创始股东资产分析表',
        icon: 'DataLine',
        permissions: ['business:view']
      }
    },
    {
      path: 'transactions-detail',
      name: 'TransactionsDetail',
      component: () => import('@/views/business/transactions-detail.vue'),
      meta: {
        title: '往来款明细表',
        icon: 'DataLine',
        permissions: ['business:view']
      }
    }
  ]
}
]

const routes = [...constantRoutes, ...asyncRoutes]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 白名单：不需要登录的页面
const whiteList = ['/login']

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - OMS` : 'OMS'
  
  if (userStore.isLoggedIn) {
    // 已登录
    if (to.path === '/login') {
      // 已登录，跳转到首页
      next({ path: '/' })
    } else {
      // 检查是否有用户信息
      if (!userStore.userInfo || !userStore.userInfo.username) {
        try {
          // 获取用户信息
          await userStore.getUserInfo()
          await userStore.getPermissions()
          next({ ...to, replace: true })
        } catch (error) {
          // 获取用户信息失败，清除token并跳转到登录页
          userStore.clearUserData()
          ElMessage.error('获取用户信息失败，请重新登录')
          next({ path: '/login', query: { redirect: to.path } })
        }
      } else {
        // 检查权限
        if (to.meta.requiresAuth) {
          // 需要登录
          if (to.meta.roles && to.meta.roles.length > 0) {
            // 有角色配置时，只检查角色
            if (to.meta.roles.some(role => userStore.hasRole(role))) {
              next()
            } else {
              ElMessage.error('您没有权限访问该页面')
              next({ path: '/403' })
            }
          } else if (to.meta.permissions && to.meta.permissions.length > 0) {
            // 没有角色配置时，检查权限
            if (userStore.hasAnyPermission(to.meta.permissions)) {
              next()
            } else {
              ElMessage.error('您没有权限访问该页面')
              next({ path: '/403' })
            }
          } else {
            // 只需要登录即可
            next()
          }
        } else {
          // 不需要登录
          next()
        }
      }
    }
  } else {
    // 未登录
    if (whiteList.includes(to.path)) {
      // 在白名单中，直接进入
      next()
    } else {
      // 不在白名单中，重定向到登录页
      next({ path: '/login', query: { redirect: to.path } })
    }
  }
})

router.afterEach(() => {
  // 可以在这里添加页面加载完成后的逻辑
})

export default router
