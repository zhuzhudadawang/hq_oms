import { useUserStore } from '@/stores/user'

/**
 * 检查是否有权限
 * @param {string|array} permission 权限标识
 * @returns {boolean}
 */
export function hasPermission(permission) {
  const userStore = useUserStore()
  return userStore.hasPermission(permission)
}

/**
 * 检查是否有任一权限
 * @param {array} permissions 权限标识数组
 * @returns {boolean}
 */
export function hasAnyPermission(permissions) {
  const userStore = useUserStore()
  return userStore.hasAnyPermission(permissions)
}

/**
 * 检查是否有所有权限
 * @param {array} permissions 权限标识数组
 * @returns {boolean}
 */
export function hasAllPermissions(permissions) {
  const userStore = useUserStore()
  return userStore.hasAllPermissions(permissions)
}

/**
 * 检查是否有角色
 * @param {string|array} role 角色标识
 * @returns {boolean}
 */
export function hasRole(role) {
  const userStore = useUserStore()
  if (Array.isArray(role)) {
    return role.some(r => userStore.hasRole(r))
  }
  return userStore.hasRole(role)
}

/**
 * 检查是否是管理员
 * @returns {boolean}
 */
export function isAdmin() {
  const userStore = useUserStore()
  return userStore.isAdmin
}
