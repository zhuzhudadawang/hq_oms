<template>
  <div class="market-zhuhai-order-sample">
  

    <el-card class="chart-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>珠海订单 & 样点统计（日度柱状）</span>
          <div class="header-actions">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              size="small"
              unlink-panels
              value-format="YYYY-MM-DD"
              :disabled-date="disableFuture"
              @change="handleDateChange"
            />
            <el-button type="primary" size="small" @click="refresh" :loading="loading">
              刷新
            </el-button>
          </div>
        </div>
      </template>

      <EChart :option="chartOption" height="440px" />

      <el-row :gutter="16" class="summary-row">
        <el-col :xs="24" :sm="6">
          <div class="summary-card primary">
            <div class="summary-label">订单总量</div>
            <div class="summary-value">{{ summary.totalOrders }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="6">
          <div class="summary-card info">
            <div class="summary-label">样点总量</div>
            <div class="summary-value">{{ summary.totalSamples }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="6">
          <div class="summary-card accent">
            <div class="summary-label">样点 / 订单</div>
            <div class="summary-value">{{ summary.samplePerOrder }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="6">
          <div class="summary-card highlight">
            <div class="summary-label">峰值客户</div>
            <div class="summary-value">{{ summary.peakCustomer }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import EChart from '@/components/EChart.vue'
import { marketAnalysisApi } from '@/api/market'
import { useDateRangeStore } from '@/stores/dateRange'

const loading = ref(false)

const chartOption = ref(buildChartOption([], [], []))

const summary = reactive({
  totalOrders: '0',
  totalSamples: '0',
  samplePerOrder: '0.00',
  peakCustomer: '-'
})

const dateRangeStore = useDateRangeStore()
const dateRange = computed({
  get: () => dateRangeStore.dateRange,
  set: (val) => dateRangeStore.setDateRange(val)
})

const DEFAULT_LENGTH = 7
const DEFAULT_DATA = {
  categories: generateDefaultCustomers(DEFAULT_LENGTH),
  orders: [88, 94, 90, 97, 103, 108, 112],
  samples: [37, 40, 38, 41, 44, 47, 49]
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = buildQueryParams(dateRange.value)
    const payload = await marketAnalysisApi.getZhuhaiOrderSample(params)
    console.log('订单与样点统计数据获取成功。', payload)
    const normalized = normalizePayload(payload)
    if (!normalized) throw new Error('invalid-payload')
    applyData(normalized)
  } catch (error) {
    console.warn('订单与样点统计数据获取失败，使用示例数据。', error)
  } finally {
    loading.value = false
  }
}

const normalizePayload = (payload) => {
  if (!payload || typeof payload !== 'object') return null

  const rawCategories =
    payload.customers ||
    payload.customer_names ||
    payload.labels ||
    payload.names ||
    payload.categories ||
    payload.xAxis ||
    []
  const categories = normalizeCategories(rawCategories)

  let orders = []
  let samples = []

  if (Array.isArray(payload.orders)) {
    orders = payload.orders
  } else if (Array.isArray(payload.order_counts)) {
    orders = payload.order_counts
  }

  if (Array.isArray(payload.samples)) {
    samples = payload.samples
  } else if (Array.isArray(payload.sample_counts)) {
    samples = payload.sample_counts
  }

  if ((!orders.length || !samples.length) && Array.isArray(payload.series)) {
    payload.series.forEach((serie) => {
      const name = String(serie?.name || '').trim()
      if (/样点/.test(name)) {
        samples = serie.data || serie.values || []
      } else if (/订单|order/i.test(name)) {
        orders = serie.data || serie.values || []
      }
    })
  }

  if (!categories.length) {
    const len = Math.max(orders.length, samples.length)
    if (!len) return null
    const paddingDays = Array.from({ length: len }, (_, index) => `第${index + 1}天`)
    return composeResult(paddingDays, orders, samples)
  }

  return composeResult(categories, orders, samples)
}

const normalizeCategories = (list) => {
  if (!Array.isArray(list)) return []
  return list
    .map((item) => {
      if (item === null || item === undefined) return ''
      return String(item).trim()
    })
    .filter(Boolean)
}

const composeResult = (categories, orderValues, sampleValues) => {
  const len = categories.length
  const normalizedCategories = categories.map((value) =>
    value === null || value === undefined ? '' : String(value)
  )
  const orders = normalizedCategories.map((_, idx) => toNumber(orderValues[idx]))
  const samples = normalizedCategories.map((_, idx) => toNumber(sampleValues[idx]))

  if (!orders.some((val) => Number.isFinite(val)) && !samples.some((val) => Number.isFinite(val))) {
    return null
  }

  return {
    categories: normalizedCategories,
    orders,
    samples
  }
}

const toNumber = (value) => {
  const num = Number(value)
  return Number.isFinite(num) ? num : 0
}

const applyData = ({ categories, orders, samples }) => {
  const resolvedCategories = resolveCategories(categories, orders.length)

  chartOption.value = buildChartOption(resolvedCategories, orders, samples)

  const totalOrders = orders.reduce((acc, cur) => acc + (Number(cur) || 0), 0)
  const totalSamples = samples.reduce((acc, cur) => acc + (Number(cur) || 0), 0)
  summary.totalOrders = formatNumber(totalOrders)
  summary.totalSamples = formatNumber(totalSamples)
  summary.samplePerOrder = totalOrders ? (totalSamples / totalOrders).toFixed(2) : '0.00'

  if (orders.length) {
    const peakIndex = orders.reduce((acc, current, index) =>
      current > orders[acc] ? index : acc
    , 0)
    summary.peakCustomer = resolvedCategories[peakIndex] || '-'
  } else {
    summary.peakCustomer = '-'
  }
}

const formatNumber = (value) =>
  Number(value || 0)
    .toFixed(0)
    .replace(/\B(?=(\d{3})+(?!\d))/g, ',')

const refresh = () => {
  fetchData()
}

const handleDateChange = (value) => {
  if (value && value.length === 2) {
    dateRange.value = value;
    fetchData();
  } else {
    dateRangeStore.resetToCurrentWeek();
    fetchData();
  }
}

const disableFuture = (date) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return date.getTime() > today.getTime()
}

onMounted(fetchData)

function buildQueryParams(range) {
  if (!Array.isArray(range) || range.length !== 2) return {}
  const [start, end] = range
  return {
    start_date: typeof start === 'string' ? start : formatDate(start),
    end_date: typeof end === 'string' ? end : formatDate(end)
  }
}

function getDefaultRange() {
  const today = new Date();
  today.setHours(0, 0, 0, 0); // 将时间部分清零

  const dayOfWeek = today.getDay(); // 0 (周日) 到 6 (周六)

  // 计算本周一的日期
  const daysToSubtract = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
  const start = new Date(today);
  start.setDate(today.getDate() - daysToSubtract);

  // 计算本周日的日期
  const end = new Date(start);
  end.setDate(start.getDate() + 6);

  return [start, end]
}

function formatDate(raw) {
  const date = new Date(raw)
  if (Number.isNaN(date.getTime())) return ''
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function resolveCategories(categories, length) {
  const sanitized = Array.isArray(categories)
    ? categories.filter((item, idx) => idx < length).map((value) => String(value || '').trim())
    : []

  if (!sanitized.length) {
    return generateDefaultCustomers(length)
  }

  if (isPlaceholderSequence(sanitized, length)) {
    return generateDefaultCustomers(length)
  }

  return sanitized.map((value, index) => (value ? value : `客户${index + 1}`))
}

function isPlaceholderSequence(values, length) {
  if (!length) return false
  return values.every((text, index) => {
    if (!text) return true
    if (/^\d+$/.test(text)) return true
    if (/^第\d+天$/.test(text)) return true
    return false
  })
}

function generateDefaultCustomers(length) {
  const safeLength = Number.isFinite(length) && length > 0 ? Math.floor(length) : DEFAULT_LENGTH
  return Array.from({ length: safeLength }, (_, idx) => `客户${idx + 1}`)
}

function buildChartOption(categories, orders, samples) {
  // 1. 根据 categories 的长度决定是否旋转 X 轴标签
  const rotate = categories.length > 7 ? 30 : 0;

  return {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['订单量', '样点数']
    },
    grid: {
      top: 54,
      left: '4%',
      right: '4%',
      // 2. 当标签旋转时，增加底部的边距，防止标签被截断
      bottom: rotate ? 64 : 36,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisTick: {
        alignWithLabel: true
      },
      axisLabel: {
        // 3. 强制显示所有标签，不自动隐藏
        interval: 0,
        // 4. 应用计算出的旋转角度
        rotate: rotate
      }
    },
    yAxis: {
      type: 'value',
      name: '数量',
      minInterval: 1
    },
    series: [
      {
        name: '订单量',
        type: 'bar',
        barWidth: 28,
        itemStyle: {
          color: '#409EFF'
        },
        label: {
          show: true,
          position: 'top'
        },
        data: orders
      },
      {
        name: '样点数',
        type: 'bar',
        barWidth: 28,
        barGap: '12%',
        itemStyle: {
          color: '#67C23A'
        },
        label: {
          show: true,
          position: 'top'
        },
        data: samples
      }
    ]
  }
}
</script>

<style lang="scss" scoped>
.market-zhuhai-order-sample {
  .alert {
    margin-bottom: 20px;
  }

  .chart-card {
    min-height: 460px;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-weight: 600;

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }

  .summary-row {
    margin-top: 18px;
  }

  .summary-card {
    border-radius: 10px;
    padding: 16px 20px;
    background: #f7f9fc;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 90px;
    box-shadow: inset 0 0 0 1px rgba(64, 158, 255, 0.08);

    &.primary {
      box-shadow: inset 0 0 0 1px rgba(64, 158, 255, 0.18);
    }

    &.info {
      box-shadow: inset 0 0 0 1px rgba(103, 194, 58, 0.2);
    }

    &.accent {
      box-shadow: inset 0 0 0 1px rgba(255, 153, 0, 0.24);
    }

    &.highlight {
      box-shadow: inset 0 0 0 1px rgba(255, 87, 34, 0.22);
    }

    .summary-label {
      font-size: 13px;
      color: #909399;
      margin-bottom: 6px;
    }

    .summary-value {
      font-size: 26px;
      font-weight: 700;
      color: #303133;
    }
  }
}
</style>
