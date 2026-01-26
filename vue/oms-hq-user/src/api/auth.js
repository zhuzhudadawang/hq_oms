import request from '@/utils/request'
import { 
  mockLogin, 
  mockLogout, 
  mockGetUserInfo, 
  mockGetPermissions, 
  mockGetMenus 
} from '@/mock/auth'

// 是否使用 Mock 数据
const useMock = import.meta.env.VITE_USE_MOCK === 'true'

/**
 * 用户登录
 */
export function login(data) {
  if (useMock) {
    return mockLogin(data.username, data.password).then(res => res.data)
  }
  
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

/**
 * 用户登出
 */
export function logout() {
  if (useMock) {
    return mockLogout().then(res => res.data)
  }
  
  return request({
    url: '/auth/logout',
    method: 'post'
  })
}

/**
 * 获取用户信息
 */
export function getUserInfo() {
  if (useMock) {
    const token = localStorage.getItem('token')
    return mockGetUserInfo(token).then(res => res.data)
  }
  
  return request({
    url: '/auth/user-info',
    method: 'get'
  })
}

/**
 * 刷新 Token
 */
export function refreshToken() {
  return request({
    url: '/auth/refresh-token',
    method: 'post'
  })
}

/**
 * 获取用户权限
 */
export function getUserPermissions() {
  if (useMock) {
    const token = localStorage.getItem('token')
    return mockGetPermissions(token).then(res => res.data)
  }
  
  return request({
    url: '/auth/permissions',
    method: 'get'
  })
}

/**
 * 获取用户菜单
 */
export function getUserMenus() {
  if (useMock) {
    const token = localStorage.getItem('token')
    return mockGetMenus(token).then(res => res.data)
  }
  
  return request({
    url: '/auth/menus',
    method: 'get'
  })
}
