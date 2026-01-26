import { defineStore } from 'pinia'
import { login, logout, getUserInfo, getUserPermissions, getUserMenus } from '@/api/auth'
import { useDateRangeStore } from '@/stores/dateRange'
import router from '@/router'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}'),
    permissions: JSON.parse(localStorage.getItem('permissions') || '[]'),
    menus: JSON.parse(localStorage.getItem('menus') || '[]'),
    roles: JSON.parse(localStorage.getItem('roles') || '[]')
  }),

  getters: {
    // 是否已登录
    isLoggedIn: (state) => !!state.token,
    
    // 获取用户名
    username: (state) => state.userInfo?.username || '',
    
    // 获取用户角色
    userRoles: (state) => state.roles,
    
    // 是否是管理员
    isAdmin: (state) => state.roles.includes('admin'),
    
    // 是否是工程管理员
    isEngineeringAdmin: (state) => state.roles.includes('engineering_admin'),
    
    // 是否是市场管理员
    isMarketAdmin: (state) => state.roles.includes('market_admin')
  },

  actions: {
    // 登录
    async login(loginForm) {
      try {
        const data = await login(loginForm)
        
        this.token = data.token
        this.userInfo = data.userInfo
        this.roles = data.roles || []
        
        // 保存到 localStorage
        localStorage.setItem('token', data.token)
        localStorage.setItem('userInfo', JSON.stringify(data.userInfo))
        localStorage.setItem('roles', JSON.stringify(data.roles || []))
        
        // 登录时重置日期为当前周
        const dateRangeStore = useDateRangeStore()
        dateRangeStore.resetToCurrentWeek()
        
        return data
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },

    // 登出
    async logout() {
      // 直接清除本地数据，不调用后端接口
      this.clearUserData()
      router.push('/login')
    },

    // 清除用户数据
    clearUserData() {
      this.token = ''
      this.userInfo = {}
      this.permissions = []
      this.menus = []
      this.roles = []
      
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      localStorage.removeItem('permissions')
      localStorage.removeItem('menus')
      localStorage.removeItem('roles')
      
      // 登出时重置日期为当前周
      const dateRangeStore = useDateRangeStore()
      dateRangeStore.resetToCurrentWeek()
    },

    // 获取用户信息
    async getUserInfo() {
      try {
        const data = await getUserInfo()
        this.userInfo = data
        localStorage.setItem('userInfo', JSON.stringify(data))
        return data
      } catch (error) {
        console.error('获取用户信息失败:', error)
        throw error
      }
    },

    // 获取用户权限
    async getPermissions() {
      try {
        const data = await getUserPermissions()
        this.permissions = data
        localStorage.setItem('permissions', JSON.stringify(data))
        return data
      } catch (error) {
        console.error('获取权限失败:', error)
        throw error
      }
    },

    // 获取用户菜单
    async getMenus() {
      try {
        const data = await getUserMenus()
        this.menus = data
        localStorage.setItem('menus', JSON.stringify(data))
        return data
      } catch (error) {
        console.error('获取菜单失败:', error)
        throw error
      }
    },

    // 检查是否有某个权限
    hasPermission(permission) {
      // 管理员拥有所有权限
      if (this.isAdmin) {
        return true
      }
      
      return this.permissions.includes(permission)
    },

    // 检查是否有某个角色
    hasRole(role) {
      return this.roles.includes(role)
    },

    // 检查是否有任一权限
    hasAnyPermission(permissions) {
      if (this.isAdmin) {
        return true
      }
      
      return permissions.some(permission => this.permissions.includes(permission))
    },

    // 检查是否有所有权限
    hasAllPermissions(permissions) {
      if (this.isAdmin) {
        return true
      }
      
      return permissions.every(permission => this.permissions.includes(permission))
    }
  }
})
