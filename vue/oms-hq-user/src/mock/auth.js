/**
 * Mock 数据服务
 * 用于模拟后端API响应
 */

// 模拟延迟
const delay = (ms = 500) => new Promise(resolve => setTimeout(resolve, ms))

// 模拟用户数据库
const mockUsers = {
  admin: {
    username: 'admin',
    password: '123456',
    token: 'mock-token-admin-' + Date.now(),
    userInfo: {
      id: 1,
      username: 'admin',
      nickname: '管理员',
      email: 'admin@example.com',
      avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
    },
    roles: ['admin'],
    permissions: [
      'order:view', 'order:create', 'order:edit', 'order:delete',
      'customer:view', 'customer:create', 'customer:edit', 'customer:delete',
      'product:view', 'product:create', 'product:edit', 'product:delete',
      'analysis:view', 'analysis:export'
    ]
  },
  manager: {
    username: 'manager',
    password: '123456',
    token: 'mock-token-manager-' + Date.now(),
    userInfo: {
      id: 2,
      username: 'manager',
      nickname: '经理',
      email: 'manager@example.com',
      avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
    },
    roles: ['manager'],
    permissions: [
      'order:view', 'order:create', 'order:edit',
      'customer:view', 'customer:create',
      'product:view',
      'analysis:view'
    ]
  },
  user: {
    username: 'user',
    password: '123456',
    token: 'mock-token-user-' + Date.now(),
    userInfo: {
      id: 3,
      username: 'user',
      nickname: '普通用户',
      email: 'user@example.com',
      avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
    },
    roles: ['user'],
    permissions: [
      'order:view',
      'analysis:view'
    ]
  }
}

/**
 * Mock 登录
 */
export async function mockLogin(username, password) {
  await delay(800)
  
  const user = mockUsers[username]
  
  if (!user) {
    throw new Error('用户名不存在')
  }
  
  if (user.password !== password) {
    throw new Error('密码错误')
  }
  
  return {
    code: 200,
    message: '登录成功',
    data: {
      token: user.token,
      userInfo: user.userInfo,
      roles: user.roles
    }
  }
}

/**
 * Mock 获取用户信息
 */
export async function mockGetUserInfo(token) {
  await delay(300)
  
  const user = Object.values(mockUsers).find(u => u.token === token)
  
  if (!user) {
    throw new Error('无效的token')
  }
  
  return {
    code: 200,
    data: user.userInfo
  }
}

/**
 * Mock 获取用户权限
 */
export async function mockGetPermissions(token) {
  await delay(300)
  
  const user = Object.values(mockUsers).find(u => u.token === token)
  
  if (!user) {
    throw new Error('无效的token')
  }
  
  return {
    code: 200,
    data: user.permissions
  }
}

/**
 * Mock 获取用户菜单
 */
export async function mockGetMenus(token) {
  await delay(300)
  
  const user = Object.values(mockUsers).find(u => u.token === token)
  
  if (!user) {
    throw new Error('无效的token')
  }
  
  // 根据权限返回菜单
  const allMenus = [
    {
      path: '/dashboard',
      name: 'Dashboard',
      meta: { title: '首页', icon: 'DataLine' }
    },
    {
      path: '/order',
      name: 'Order',
      meta: { title: '订单管理', icon: 'ShoppingCart' },
      children: [
        { path: '/order/list', name: 'OrderList', meta: { title: '订单列表', icon: 'List' } }
      ]
    },
    {
      path: '/customer',
      name: 'Customer',
      meta: { title: '客户管理', icon: 'User' },
      children: [
        { path: '/customer/list', name: 'CustomerList', meta: { title: '客户列表', icon: 'List' } }
      ]
    },
    {
      path: '/product',
      name: 'Product',
      meta: { title: '产品管理', icon: 'Goods' },
      children: [
        { path: '/product/list', name: 'ProductList', meta: { title: '产品列表', icon: 'List' } }
      ]
    },
    {
      path: '/analysis',
      name: 'Analysis',
      meta: { title: '工程数据分析', icon: 'TrendCharts' },
      children: [
        { path: '/analysis/sample-success', name: 'SampleSuccess', meta: { title: '样点成功率' } },
        { path: '/analysis/fib-output', name: 'FibOutput', meta: { title: 'FIB人员产出' } },
        { path: '/analysis/tem-output', name: 'TemOutput', meta: { title: 'TEM人员产出' } }
      ]
    }
  ]
  
  return {
    code: 200,
    data: allMenus
  }
}

/**
 * Mock 登出
 */
export async function mockLogout() {
  await delay(300)
  
  return {
    code: 200,
    message: '登出成功'
  }
}
