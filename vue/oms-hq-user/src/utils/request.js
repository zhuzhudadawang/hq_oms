import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 清除登录状态并跳转
const clearAuthAndRedirect = () => {
  // 清除 localStorage
  localStorage.removeItem('token')
  localStorage.removeItem('userInfo')
  localStorage.removeItem('roles')
  localStorage.removeItem('permissions')
  localStorage.removeItem('menus')
  
  // 延迟1.5秒跳转，让用户看到提示
  setTimeout(() => {
    window.location.href = '/login'
  }, 1500)
}

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const { code, data, message, error } = response.data
    
    if (error === 0 || code === 0 || code === 200) {
      return data ? data : response.data
    } else if (code === 401) {
      ElMessage.error('登录已过期，请重新登录')
      clearAuthAndRedirect()
      return Promise.reject(new Error(message || '未授权'))
    } else {
      ElMessage.error(message || '请求失败')
      return Promise.reject(new Error(message || '请求失败'))
    }
  },
  (error) => {
    console.error('响应错误:', error)
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          ElMessage.error('登录已过期，请重新登录')
          clearAuthAndRedirect()
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误')
          break
        default:
          ElMessage.error(data?.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查网络连接')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default request
