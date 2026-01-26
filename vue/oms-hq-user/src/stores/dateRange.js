import { defineStore } from 'pinia'

// 格式化日期为 YYYY-MM-DD
function formatDateYMD(d) {
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

// 获取当前周范围（周一到周日）
function getCurrentWeekRange() {
  const today = new Date()
  const day = today.getDay()
  const diffToMonday = (day + 6) % 7
  const monday = new Date(today)
  monday.setDate(today.getDate() - diffToMonday)
  const sunday = new Date(monday)
  sunday.setDate(monday.getDate() + 6)
  return [formatDateYMD(monday), formatDateYMD(sunday)]
}

// 从 localStorage 获取日期范围，没有则返回当前周
function getStoredDateRange() {
  const stored = localStorage.getItem('dateRange')
  if (stored) {
    try {
      return JSON.parse(stored)
    } catch {
      return getCurrentWeekRange()
    }
  }
  return getCurrentWeekRange()
}

export const useDateRangeStore = defineStore('dateRange', {
  state: () => ({
    dateRange: getStoredDateRange()
  }),

  actions: {
    setDateRange(range) {
      this.dateRange = range
      localStorage.setItem('dateRange', JSON.stringify(range))
    },

    // 重置为当前周
    resetToCurrentWeek() {
      const range = getCurrentWeekRange()
      this.dateRange = range
      localStorage.removeItem('dateRange')
    }
  }
})
