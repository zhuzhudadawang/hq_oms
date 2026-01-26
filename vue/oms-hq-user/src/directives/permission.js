import { useUserStore } from '@/stores/user'

/**
 * 权限指令
 * 用法: v-permission="'order:create'"
 * 或: v-permission="['order:create', 'order:edit']"
 */
export default {
  mounted(el, binding) {
    const { value } = binding
    const userStore = useUserStore()

    if (value) {
      let hasPermission = false

      if (Array.isArray(value)) {
        // 数组形式，拥有任一权限即可
        hasPermission = userStore.hasAnyPermission(value)
      } else {
        // 字符串形式
        hasPermission = userStore.hasPermission(value)
      }

      if (!hasPermission) {
        // 没有权限则移除元素
        el.parentNode && el.parentNode.removeChild(el)
      }
    }
  }
}
