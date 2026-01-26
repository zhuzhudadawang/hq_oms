import { defineStore } from 'pinia'

export const usePermissionStore = defineStore('permission', {
  state: () => ({
    routes: [],
    addRoutes: []
  }),

  actions: {
    // 生成路由
    generateRoutes(roles) {
      // 这里可以根据角色动态生成路由
      // 目前返回所有路由
      return new Promise(resolve => {
        // 实际项目中应该根据角色过滤路由
        const accessedRoutes = []
        this.addRoutes = accessedRoutes
        resolve(accessedRoutes)
      })
    }
  }
})
