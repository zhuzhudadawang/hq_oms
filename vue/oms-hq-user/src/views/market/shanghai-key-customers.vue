<template>
  <div class="market-shanghai-key-customers">
    <div class="chart-container" v-loading="loading">
      <el-row v-if="chartConfigs.length" :gutter="16" class="chart-grid">
        <el-col v-for="config in chartConfigs" :key="config.key" :xs="24" :lg="12">
          <el-card class="chart-card" shadow="hover">
            <div class="chart-header">{{ config.title }}</div>
            <EChart :option="config.option" height="320px" />
          </el-card>
        </el-col>
      </el-row>
      <el-empty v-else-if="!loading" description="暂无数据" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import EChart from '@/components/EChart.vue'
import { marketAnalysisApi } from '@/api/market'

const BAR_COLORS = ['#409EFF', '#67C23A']

const loading = ref(false)
const chartConfigs = ref([])

const currentYear = new Date().getFullYear()
const primaryYear = ref(currentYear)
const comparisonYear = ref(currentYear - 1)

const DEFAULT_MONTHS = Array.from({ length: 12 }, (_, idx) => idx + 1)
const DEFAULT_DATA = {
  months: DEFAULT_MONTHS,
  customers: [
    {
      name: '五角场',
      series: [
        { label: '2024', data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] },
        { label: '2025', data: [0, 0, 0, 0, 231, 379, 491, 357, 363, 201, 117, 0] }
      ]
    },
    {
      name: '中科路（格科）',
      series: [
        { label: '2024', data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] },
        { label: '2025', data: [0, 0, 0, 274, 22, 0, 145, 276, 366, 201, 208, 0] }
      ]
    },
    {
      name: '洋山港（ZW）',
      series: [
        { label: '2024', data: [520, 261, 380, 388, 201, 127, 207, 214, 230, 214, 134, 103] },
        { label: '2025', data: [43, 79, 335, 536, 691, 415, 363, 383, 519, 629, 367, 0] }
      ]
    },
    {
      name: '新场镇（昕原）',
      series: [
        { label: '2024', data: [0, 0, 0, 0, 0, 40, 53, 59, 50, 36, 27, 57] },
        { label: '2025', data: [27, 41, 52, 71, 75, 27, 0, 8, 0, 17, 23, 0] }
      ]
    }
  ]
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      primary_year: primaryYear.value,
      comparison_year: comparisonYear.value
    }
    const payload = await marketAnalysisApi.getShanghaiKeyCustomers(params)
    const normalized = normalizePayload(payload)
    if (!normalized) throw new Error('invalid-payload')
    applyData(normalized)
  } catch (error) {
    console.warn('上海重要客户订单统计数据获取失败，使用示例数据。', error)
  } finally {
    loading.value = false
  }
}

const normalizePayload = (payload) => {
  if (!payload || typeof payload !== 'object') return null

  const customersSource = Array.isArray(payload.customers)
    ? payload.customers
    : Array.isArray(payload.groups)
      ? payload.groups
      : Array.isArray(payload.items)
        ? payload.items
        : []

  if (!customersSource.length) return null

  const baseMonths = normalizeMonths(
    payload.months || payload.labels || payload.xAxis || payload.periods || []
  )

  const normalizedGroups = customersSource
    .map((group, index) => normalizeGroup(group, index, baseMonths))
    .filter(Boolean)

  return normalizedGroups.length ? normalizedGroups : null
}

const normalizeGroup = (group, index, fallbackMonths) => {
  if (!group || typeof group !== 'object') return null

  const name = String(group.name || group.title || group.customer || `重要客户${index + 1}`).trim()
  const months = normalizeMonths(
    group.months || group.labels || group.periods || group.xAxis || fallbackMonths || []
  )
  const monthList = months.length ? months : [...DEFAULT_MONTHS]
  const series = normalizeSeries(group, monthList.length)

  if (!series.length) return null

  return {
    name: name || `重要客户${index + 1}`,
    months: monthList,
    series
  }
}

const normalizeMonths = (list) => {
  if (!Array.isArray(list)) return []
  return list
    .map((item, idx) => {
      if (item === null || item === undefined || item === '') {
        return DEFAULT_MONTHS[idx] || idx + 1
      }
      const text = String(item).trim()
      if (!text) {
        return DEFAULT_MONTHS[idx] || idx + 1
      }
      const numeric = Number(text)
      if (Number.isFinite(numeric) && numeric >= 1 && numeric <= 12) {
        return numeric
      }
      const match = text.match(/(\d{1,2})/)
      if (match) {
        const value = Number(match[1])
        if (Number.isFinite(value)) return value
      }
      return text
    })
    .slice(0, 12)
}

const normalizeSeries = (group, monthLength) => {
  const collection = []

  const pushSeries = (label, data) => {
    const normalizedLabel = formatSeriesLabel(label, collection.length)
    const normalizedData = ensureMonthlyNumbers(data, monthLength)
    if (normalizedData.some((value) => Number.isFinite(value))) {
      collection.push({ label: normalizedLabel, data: normalizedData })
    }
  }

  if (Array.isArray(group.series)) {
    group.series.forEach((item, idx) => {
      if (!item) return
      if (Array.isArray(item)) {
        pushSeries(idx === 0 ? primaryYear.value : comparisonYear.value, item)
      } else {
        pushSeries(item.label || item.name || item.year || idx, item.data || item.values || item.orders)
      }
    })
  }

  const seriesMap = group.seriesMap || group.series_map || group.years || group.datasets || group.data
  if (!collection.length && seriesMap && typeof seriesMap === 'object') {
    Object.keys(seriesMap).forEach((key) => {
      pushSeries(key, seriesMap[key])
    })
  }

  if (!collection.length && Array.isArray(group.values)) {
    group.values.forEach((item, idx) => {
      if (!item || typeof item !== 'object') return
      pushSeries(item.label || item.year || idx, item.data || item.orders)
    })
  }

  return collection
}

const ensureMonthlyNumbers = (data, length) => {
  const source = Array.isArray(data) ? data : []
  const result = []
  for (let i = 0; i < length; i += 1) {
    const value = source[i]
    const numeric = toNumber(value)
    result.push(Number.isFinite(numeric) && numeric >= 0 ? numeric : 0)
  }
  return result
}

const toNumber = (value) => {
  const num = Number(value)
  return Number.isFinite(num) ? num : 0
}

const formatSeriesLabel = (label, index) => {
  const text = String(label ?? '').trim()
  if (text) return text
  return index === 0 ? `${primaryYear.value}` : `${comparisonYear.value}`
}

const applyData = (groups) => {
  chartConfigs.value = groups.map((group, idx) => ({
    key: `${idx}-${group.name}`,
    title: group.name,
    option: buildChartOption(group)
  }))
}

const buildChartOption = (group) => {
  const categories = group.months.map((month) => formatMonthLabel(month))
  const legend = group.series.map((serie) => serie.label)
  const maxValue = computeMaxValue(group.series)

  const series = group.series.map((serie, index) => ({
    name: serie.label,
    type: 'bar',
    barWidth: 18,
    itemStyle: {
      color: BAR_COLORS[index] || BAR_COLORS[0]
    },
    label: {
      show: true,
      position: 'top'
    },
    data: serie.data
  }))

  return {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: legend,
      top: 4
    },
    grid: {
      top: 48,
      left: '4%',
      right: '4%',
      bottom: 32,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: 'value',
      name: '样点量',
      min: 0,
      max: maxValue,
      minInterval: 1
    },
    series
  }
}

const computeMaxValue = (series) => {
  const flat = series.flatMap((item) => item.data || [])
  const peak = flat.reduce((acc, cur) => (cur > acc ? cur : acc), 0)
  if (!Number.isFinite(peak) || peak <= 0) return 10
  const padded = peak + 2
  const bucket = Math.ceil(padded / 5) * 5
  return Math.max(bucket, 10)
}

const formatMonthLabel = (value) => {
  if (typeof value === 'number') {
    return `${value}月`
  }
  const numeric = Number(value)
  if (Number.isFinite(numeric)) {
    return `${numeric}月`
  }
  const text = String(value || '').trim()
  if (!text) return ''
  return /月$/.test(text) ? text : `${text}月`
}

onMounted(fetchData)
</script>

<style lang="scss" scoped>
.market-shanghai-key-customers {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .alert {
    margin-bottom: 0;
  }

  .chart-container {
    min-height: 420px;
  }

  .chart-grid {
    margin: 0;
  }

  .chart-card {
    margin-bottom: 16px;

    .chart-header {
      font-weight: 600;
      font-size: 15px;
      margin-bottom: 8px;
    }
  }
}
</style>
