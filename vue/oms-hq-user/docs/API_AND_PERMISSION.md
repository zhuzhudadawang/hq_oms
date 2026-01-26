# API 集成和权限控制文档

## 📚 目录

1. [API 集成](#api-集成)
2. [权限系统](#权限系统)
3. [路由守卫](#路由守卫)
4. [使用示例](#使用示例)
5. [Mock 模式](#mock-模式)

---

## 🔌 API 集成

### 文件结构

```
src/
├── api/
│   ├── auth.js         # 认证相关 API
│   ├── order.js        # 订单相关 API
│   ├── customer.js     # 客户相关 API
│   ├── product.js      # 产品相关 API
│   └── analysis.js     # 数据分析相关 API
├── utils/
│   └── request.js      # Axios 封装
└── mock/
    └── auth.js         # Mock 数据
```

### Request 配置

**文件**: `src/utils/request.js`

特性：
- ✅ 自动添加 Token 到请求头
- ✅ 统一错误处理
- ✅ 401 自动跳转登录
- ✅ 请求/响应拦截器

### API 使用示例

```javascript
import { getOrderList, createOrder } from '@/api/order'

// 获取订单列表
const fetchOrders = async () => {
  try {
    const data = await getOrderList({ page: 1, pageSize: 10 })
    console.log('订单列表:', data)
  } catch (error) {
    console.error('获取失败:', error)
  }
}

// 创建订单
const addOrder = async (orderData) => {
  try {
    const result = await createOrder(orderData)
    ElMessage.success('创建成功')
  } catch (error) {
    ElMessage.error(error.message)
  }
}
```

---

## 🔐 权限系统

### 角色定义

系统内置三种角色：

| 角色 | 说明 | 权限范围 |
|------|------|----------|
| `admin` | 管理员 | 所有权限 |
| `manager` | 经理 | 大部分权限（不含删除） |
| `user` | 普通用户 | 查看权限 |

### 权限标识

权限采用 `模块:操作` 的格式：

```javascript
// 订单权限
'order:view'    // 查看订单
'order:create'  // 创建订单
'order:edit'    // 编辑订单
'order:delete'  // 删除订单

// 客户权限
'customer:view'
'customer:create'
'customer:edit'
'customer:delete'

// 产品权限
'product:view'
'product:create'
'product:edit'
'product:delete'

// 数据分析权限
'analysis:view'   // 查看分析数据
'analysis:export' // 导出报表
```

### Pinia Store

**文件**: `src/stores/user.js`

主要方法：
- `login(loginForm)` - 登录
- `logout()` - 登出
- `hasPermission(permission)` - 检查单个权限
- `hasAnyPermission(permissions)` - 检查任一权限
- `hasAllPermissions(permissions)` - 检查所有权限
- `hasRole(role)` - 检查角色

---

## 🛡️ 路由守卫

**文件**: `src/router/index.js`

### 路由元信息

```javascript
{
  path: '/order',
  meta: {
    title: '订单管理',
    requiresAuth: true,        // 需要登录
    roles: ['admin', 'manager'], // 允许的角色
    permissions: ['order:view']  // 需要的权限
  }
}
```

### 守卫逻辑

1. ✅ 检查登录状态
2. ✅ 验证用户信息
3. ✅ 检查角色权限
4. ✅ 检查操作权限
5. ✅ 无权限跳转 403

---

## 💡 使用示例

### 1. 模板中使用指令

```vue
<template>
  <!-- 按钮权限控制 -->
  <el-button v-permission="'order:create'" type="primary">
    新增订单
  </el-button>
  
  <!-- 多个权限（满足任一即可） -->
  <el-button v-permission="['order:edit', 'order:delete']">
    操作
  </el-button>
  
  <!-- 角色控制 -->
  <div v-role="'admin'">
    仅管理员可见
  </div>
  
  <!-- 多个角色 -->
  <div v-role="['admin', 'manager']">
    管理员和经理可见
  </div>
</template>
```

### 2. JS 中使用工具函数

```vue
<script setup>
import { hasPermission, hasRole, isAdmin } from '@/utils/permission'

// 检查权限
if (hasPermission('order:delete')) {
  console.log('有删除权限')
}

// 检查角色
if (hasRole('admin')) {
  console.log('是管理员')
}

// 检查是否是管理员
if (isAdmin()) {
  console.log('拥有所有权限')
}
</script>
```

### 3. Composition API 中使用

```vue
<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 检查权限
const canCreate = userStore.hasPermission('order:create')
const canEdit = userStore.hasPermission('order:edit')

// 检查角色
const isAdmin = userStore.isAdmin
const isManager = userStore.hasRole('manager')

// 条件渲染
const showDeleteButton = computed(() => {
  return userStore.hasPermission('order:delete')
})
</script>

<template>
  <el-button v-if="canCreate" type="primary">新增</el-button>
  <el-button v-if="showDeleteButton" type="danger">删除</el-button>
</template>
```

### 4. 动态菜单过滤

```vue
<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 根据权限过滤菜单
const menuList = computed(() => {
  return router.options.routes.filter(route => {
    // 检查角色
    if (route.meta?.roles) {
      return route.meta.roles.some(role => userStore.hasRole(role))
    }
    
    // 检查权限
    if (route.meta?.permissions) {
      return userStore.hasAnyPermission(route.meta.permissions)
    }
    
    return true
  })
})
</script>
```

---

## 🎭 Mock 模式

### 启用 Mock 模式

1. 设置环境变量：
```bash
# .env.development 或 .env.mock
VITE_USE_MOCK=true
```

2. 或在代码中判断：
```javascript
const useMock = import.meta.env.VITE_USE_MOCK === 'true'
```

### 测试账号

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| admin | 123456 | 管理员 | 拥有所有权限 |
| manager | 123456 | 经理 | 大部分权限 |
| user | 123456 | 普通用户 | 基础查看权限 |

### Mock 数据文件

**文件**: `src/mock/auth.js`

包含：
- 用户数据
- 角色配置
- 权限列表
- 菜单数据

---

## 🔧 环境配置

### 开发环境

```env
# .env.development
VITE_API_BASE_URL=http://localhost:8080/api
VITE_USE_MOCK=true
```

### 生产环境

```env
# .env.production
VITE_API_BASE_URL=https://api.example.com/api
VITE_USE_MOCK=false
```

---

## 📋 权限矩阵

| 功能模块 | admin | manager | user |
|---------|-------|---------|------|
| 首页 | ✅ | ✅ | ✅ |
| 订单查看 | ✅ | ✅ | ✅ |
| 订单创建 | ✅ | ✅ | ❌ |
| 订单编辑 | ✅ | ✅ | ❌ |
| 订单删除 | ✅ | ❌ | ❌ |
| 客户管理 | ✅ | ✅ | ❌ |
| 产品管理 | ✅ | ✅ | ❌ |
| 数据分析 | ✅ | ✅ | ✅ |
| 报表导出 | ✅ | ❌ | ❌ |

---

## 🚀 快速开始

### 1. 登录

```vue
<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const handleLogin = async () => {
  try {
    await userStore.login({
      username: 'admin',
      password: '123456'
    })
    
    console.log('登录成功')
    console.log('用户信息:', userStore.userInfo)
    console.log('权限列表:', userStore.permissions)
    console.log('角色列表:', userStore.roles)
  } catch (error) {
    console.error('登录失败:', error)
  }
}
</script>
```

### 2. 检查权限

```javascript
// 方式1: 使用 Store
const userStore = useUserStore()
if (userStore.hasPermission('order:create')) {
  // 有权限
}

// 方式2: 使用工具函数
import { hasPermission } from '@/utils/permission'
if (hasPermission('order:create')) {
  // 有权限
}

// 方式3: 使用指令
<el-button v-permission="'order:create'">新增</el-button>
```

### 3. 登出

```javascript
const userStore = useUserStore()
await userStore.logout()
```

---

## 📝 注意事项

1. ⚠️ **管理员角色** 默认拥有所有权限
2. ⚠️ **Token 失效** 会自动跳转登录页
3. ⚠️ **权限不足** 会显示错误提示或隐藏元素
4. ⚠️ **Mock 模式** 仅用于开发测试
5. ⚠️ **生产环境** 必须关闭 Mock 模式

---

## 🔗 相关文件

- `src/utils/request.js` - HTTP 请求封装
- `src/stores/user.js` - 用户状态管理
- `src/router/index.js` - 路由配置和守卫
- `src/directives/permission.js` - 权限指令
- `src/directives/role.js` - 角色指令
- `src/utils/permission.js` - 权限工具函数
- `src/mock/auth.js` - Mock 数据

---

**版本**: 1.0.0  
**更新日期**: 2025-10-13
