import { useUserStore } from '@/stores/user'

/**
 * 角色指令
 * 用法: v-role="'admin'"
 * 或: v-role="['admin', 'manager']"
 */
export default {
  mounted(el, binding) {
    const { value } = binding
    const userStore = useUserStore()

    if (value) {
      let hasRole = false

      if (Array.isArray(value)) {
        // 数组形式，拥有任一角色即可
        hasRole = value.some(role => userStore.hasRole(role))
      } else {
        // 字符串形式
        hasRole = userStore.hasRole(value)
      }

      if (!hasRole) {
        // 没有角色则移除元素
        el.parentNode && el.parentNode.removeChild(el)
      }
    }
  }
}
