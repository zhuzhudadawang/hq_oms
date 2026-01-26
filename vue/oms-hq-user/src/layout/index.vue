<template>
  <div class="layout-container">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar">
        <div class="logo">
          <img 
            v-if="!isCollapse" 
            src="@/assets/images/logo.png" 
            alt="Logo" 
            class="logo-image"
          />
          <h2 v-if="!isCollapse">OMS</h2>
          <img 
            v-else 
            src="@/assets/images/logo.png" 
            alt="Logo" 
            class="logo-icon"
          />
        </div>
        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapse"
          :unique-opened="true"
          router
        >
          <template v-for="route in menuRoutes" :key="route.path">
            <el-sub-menu v-if="route.children && route.children.length > 1" :index="route.path">
              <template #title>
                <el-icon v-if="route.meta?.icon">
                  <component :is="route.meta.icon" />
                </el-icon>
                <span>{{ route.meta?.title }}</span>
              </template>
              <el-menu-item
                v-for="child in route.children.filter(c => !c.meta?.hidden)"
                :key="child.path"
                :index="route.path + '/' + child.path"
              >
                <el-icon v-if="child.meta?.icon">
                  <component :is="child.meta.icon" />
                </el-icon>
                <span>{{ child.meta?.title }}</span>
              </el-menu-item>
            </el-sub-menu>
            <el-menu-item v-else :index="route.redirect || route.path">
              <el-icon v-if="route.meta?.icon">
                <component :is="route.meta.icon" />
              </el-icon>
              <span>{{ route.meta?.title }}</span>
            </el-menu-item>
          </template>
        </el-menu>
      </el-aside>

      <!-- 主体内容 -->
      <el-container>
        <!-- 顶部导航栏 -->
        <el-header class="header">
          <div class="header-left">
            <el-icon class="collapse-icon" @click="toggleCollapse">
              <Expand v-if="isCollapse" />
              <Fold v-else />
            </el-icon>
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item v-if="breadcrumbs.length > 0">
                {{ breadcrumbs[breadcrumbs.length - 1] }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <el-dropdown>
              <span class="user-info">
                <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
                <span class="username">{{ username }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人中心</el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>

        <!-- 主内容区 -->
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const isCollapse = ref(false)

// 获取菜单路由（根据权限过滤）
const menuRoutes = computed(() => {
  const allRoutes = router.options.routes.filter(route => 
    route.path !== '/login' && route.meta?.title
  )
  
  // 根据权限过滤路由
  return allRoutes.filter(route => {
    if (!route.meta) return true
    
    // 检查角色权限（角色匹配就通过，不再检查 permissions）
    if (route.meta.roles && route.meta.roles.length > 0) {
      return route.meta.roles.some(role => userStore.hasRole(role))
    }
    
    // 没有设置 roles 时，检查操作权限
    if (route.meta.permissions && route.meta.permissions.length > 0) {
      if (!userStore.hasAnyPermission(route.meta.permissions)) {
        return false
      }
    }
    
    return true
  })
})

// 当前激活的菜单
const activeMenu = computed(() => {
  return route.path
})

// 面包屑
const breadcrumbs = computed(() => {
  return [route.meta?.title].filter(Boolean)
})

// 用户名
const username = computed(() => {
  return userStore.username || '用户'
})

// 切换侧边栏折叠
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

// 退出登录
const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await userStore.logout()
      ElMessage.success('退出成功')
    } catch (error) {
      console.error('退出失败:', error)
    }
  }).catch(() => {
    // 取消退出
  })
}
</script>

<style lang="scss" scoped>
.layout-container {
  height: 100vh;
  
  .el-container {
    height: 100%;
  }

  .sidebar {
    background-color: #304156;
    transition: width 0.3s;
    
    .logo {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #2b3a4a;
      color: #fff;
      gap: 10px;
      
      .logo-image {
        width: 50px;
        height: 50px;
        object-fit: contain;
      }
      
      .logo-icon {
        width: 40px;
        height: 40px;
        object-fit: contain;
      }
      
      h2 {
        color: #fff;
        font-size: 24px;
        margin: 0;
      }
    }

    .el-menu {
      border-right: none;
      background-color: #304156;

      :deep(.el-menu-item),
      :deep(.el-sub-menu__title) {
        color: #bfcbd9;
        
        &:hover {
          background-color: #263445 !important;
          color: #fff;
        }
      }

      :deep(.el-menu-item.is-active) {
        background-color: #409eff !important;
        color: #fff;
      }

      :deep(.el-sub-menu .el-menu-item) {
        background-color: #1f2d3d !important;
        
        &:hover {
          background-color: #001528 !important;
        }
      }
    }
  }

  .header {
    background-color: #fff;
    border-bottom: 1px solid #e6e6e6;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;

    .header-left {
      display: flex;
      align-items: center;
      gap: 20px;

      .collapse-icon {
        font-size: 20px;
        cursor: pointer;
        
        &:hover {
          color: #409eff;
        }
      }
    }

    .header-right {
      .user-info {
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        
        .username {
          font-size: 14px;
        }
      }
    }
  }

  .main-content {
    background-color: #f0f2f5;
    padding: 20px;
  }
}
</style>
