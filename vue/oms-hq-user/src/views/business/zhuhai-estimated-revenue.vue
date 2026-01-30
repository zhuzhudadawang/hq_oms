<template>
  <div class="business-zhuhai-revenue">
    <el-card class="chart-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>珠海检测暂估收入（月度）</span>
          <el-tag type="success" effect="plain">覆盖2025-2026年</el-tag>
        </div>
      </template>

      <EChart :option="chartOption" height="440px" />

      <el-row :gutter="16" class="summary-row">
        <el-col :xs="24" :sm="12">
          <div class="summary-card primary">
            <div class="summary-label">{{ summary.prevYearLabel }}</div>
            <div class="summary-value">{{ summary.prevYearTotal }}万</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12">
          <div class="summary-card info">
            <div class="summary-label">{{ summary.currYearLabel }}</div>
            <div class="summary-value">{{ summary.currYearTotal }}万</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import EChart from '@/components/EChart.vue'
import { businessAnalysisApi } from '@/api/business'

const BAR_COLORS = {
  2024: '#409EFF',
  2025: '#67C23A',
  2026: '#F1C40F'
}
const DEFAULT_BAR_COLOR = '#409EFF'

const loading = ref(false)
const chartOption = ref(buildChartOption([], []))

const summary = reactive({
  prevYearTotal: '0',
  currYearTotal: '0',
  prevYearLabel: '上年暂估收入',
  currYearLabel: '本年暂估收入'
})


const formatMonthLabels = (list) =>
  (Array.isArray(list) ? list : []).map((item) => {
    if (!item && item !== 0) return ''
    const text = String(item)
    const numeric = Number(text)
    if (Number.isFinite(numeric)) {
      return `${numeric}月`
    }
    return text
  })

const normaliseSeries = (raw) => {
  if (!raw) return []
  if (Array.isArray(raw)) {
    return raw
      .map((item) => ({
        name: item?.year || item?.name || item?.label,
        data: Array.isArray(item?.values) ? item.values : Array.isArray(item?.data) ? item.data : []
      }))
      .filter((item) => item.name && item.data.length)
  }
  if (typeof raw === 'object') {
    return Object.entries(raw)
      .map(([name, values]) => ({
        name,
        data: Array.isArray(values) ? values : []
      }))
      .filter((item) => item.name && item.data.length)
  }
  return []
}

const toThousand = (value) =>
  Number(value || 0)
    .toFixed(2)
    .replace(/\B(?=(\d{3})+(?!\d))/g, ',')

const applyPayload = (payload) => {
  const months = formatMonthLabels(payload?.months || payload?.labels || payload?.xAxis || [])
  const allSeries = normaliseSeries(payload?.series || payload?.dataset || payload?.data)

  if (!months.length || !allSeries.length) {
    return false
  }

  const parseYear = (name) => {
    const match = String(name || '').match(/20\d{2}/)
    return match ? Number(match[0]) : null
  }

  const sortedSeries = [...allSeries]
    .filter((item) => parseYear(item.name) !== null)
    .sort((a, b) => parseYear(a.name) - parseYear(b.name))

  const latestTwoSeries = sortedSeries.slice(-2)

  const numericSeries = latestTwoSeries.map((item) => ({
    name: item.name,
    data: months.map((_, idx) => {
      const value = Array.isArray(item.data) ? item.data[idx] : undefined
      const num = Number(value)
      return Number.isFinite(num) ? num : 0
    })
  }))

  const yoySeries = buildYoYSeries(numericSeries)
  const momSeries = buildMoMSeries(numericSeries)
  chartOption.value = buildChartOption(months, numericSeries, yoySeries, momSeries)

  const totals = payload?.totals || {}
  const years = Object.keys(totals).sort((a, b) => Number(a) - Number(b))
  const prevYear = years[0]
  const currYear = years[1] || years[0]

  summary.prevYearTotal = toThousand(totals[prevYear] || 0)
  summary.currYearTotal = toThousand(totals[currYear] || 0)
  summary.prevYearLabel = `${prevYear}年暂估收入总额`
  summary.currYearLabel = `${currYear}年暂估收入总额`

  return true
}

const fetchData = async () => {
  loading.value = true
  try {
    const response = await businessAnalysisApi.getZhuhaiEstimatedRevenue()
    const applied = applyPayload(response)
    if (!applied) throw new Error('empty-data')
  } catch (error) {
    console.warn('珠海检测暂估收入数据获取失败。', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

function buildYoYSeries(series) {
  if (series.length < 2) {
    const length = series[0]?.data?.length || 0
    return { data: new Array(length).fill(null), label: '同比增长率' }
  }

  const baseSeries = series[0]
  const latestSeries = series[1]

  const parseYear = (name) => {
    const match = String(name || '').match(/20\d{2}/)
    return match ? Number(match[0]) : null
  }

  const baseYear = parseYear(baseSeries.name)
  const latestYear = parseYear(latestSeries.name)
  const label = `同比增长率(${baseYear}&${latestYear})`

  const baseData = Array.isArray(baseSeries.data) ? baseSeries.data : []
  const latestData = Array.isArray(latestSeries.data) ? latestSeries.data : []

  const data = latestData.map((value, index) => {
    const baseValue = Number(baseData[index])
    const currentValue = Number(value)
    if (!Number.isFinite(baseValue) || baseValue === 0 || !Number.isFinite(currentValue) || currentValue === 0) {
      return null
    }
    const rate = ((currentValue - baseValue) / baseValue) * 100
    return Number(rate.toFixed(2))
  })

  return { data, label }
}

function buildMoMSeries(series) {
  if (!series.length) return { data: [], label: '环比增长率' }

  const parseYear = (name) => {
    const match = String(name || '').match(/20\d{2}/)
    return match ? Number(match[0]) : null
  }

  const sorted = [...series].sort((a, b) => parseYear(a.name) - parseYear(b.name))
  const latestSeries = sorted[sorted.length - 1]
  const prevYearSeries = sorted.length >= 2 ? sorted[sorted.length - 2] : null
  const latestYear = parseYear(latestSeries.name)
  const label = `环比增长率(${latestYear})`

  const latestData = Array.isArray(latestSeries.data) ? latestSeries.data : []
  const prevYearData = prevYearSeries && Array.isArray(prevYearSeries.data) ? prevYearSeries.data : []

  const data = latestData.map((value, index) => {
    let prevValue
    if (index === 0) {
      prevValue = prevYearData.length >= 12 ? Number(prevYearData[11]) : null
    } else {
      prevValue = Number(latestData[index - 1])
    }
    const currentValue = Number(value)
    if (!Number.isFinite(prevValue) || prevValue === 0 || !Number.isFinite(currentValue) || currentValue === 0) {
      return null
    }
    const rate = ((currentValue - prevValue) / prevValue) * 100
    return Number(rate.toFixed(2))
  })

  return { data, label }
}

function resolveBarColor(name) {
  const match = String(name || '').match(/20\d{2}/)
  if (match && BAR_COLORS[match[0]]) {
    return BAR_COLORS[match[0]]
  }
  return DEFAULT_BAR_COLOR
}

function buildChartOption(months, series, yoySeries = { data: [], label: '同比增长率' }, momSeries = { data: [], label: '环比增长率' }) {
  const hasYoY = Array.isArray(yoySeries.data) && yoySeries.data.some((value) => Number.isFinite(value))
  const hasMoM = Array.isArray(momSeries.data) && momSeries.data.some((value) => Number.isFinite(value))

  const allRateValues = [
    ...(hasYoY ? yoySeries.data.filter((value) => Number.isFinite(value)) : []),
    ...(hasMoM ? momSeries.data.filter((value) => Number.isFinite(value)) : [])
  ]
  const rateMin = allRateValues.length ? Math.min(...allRateValues) : 0
  const rateMax = allRateValues.length ? Math.max(...allRateValues) : 0
  const rateRangeGap = rateMax - rateMin
  const ratePadding = (hasYoY || hasMoM) ? (rateRangeGap === 0 ? 5 : Math.max(2, Math.abs(rateRangeGap) * 0.1)) : 0

  const barSeries = series.map((item) => ({
    name: item.name,
    type: 'bar',
    barGap: '7%',
    barWidth: 28,
    itemStyle: {
      color: resolveBarColor(item.name)
    },
    label: {
      show: true,
      position: 'top',
      fontSize: 10,
      formatter: ({ value }) => {
        const num = Number(value)
        if (!Number.isFinite(num) || num === 0) return ''
        return num
      }
    },
    data: item.data
  }))

  const legendData = [...series.map((item) => item.name)]
  if (hasYoY) legendData.push(yoySeries.label)
  if (hasMoM) legendData.push(momSeries.label)

  const lineSeries = []
  if (hasYoY) {
    lineSeries.push({
      name: yoySeries.label,
      type: 'line',
      yAxisIndex: 1,
      smooth: true,
      itemStyle: {
        color: '#F56C6C'
      },
      label: {
        show: true,
        fontSize: 10,
        formatter: ({ value }) =>
          Number.isFinite(value) ? `${Number(value).toFixed(1)}%` : ''
      },
      data: yoySeries.data,
      connectNulls: true
    })
  }
  if (hasMoM) {
    lineSeries.push({
      name: momSeries.label,
      type: 'line',
      yAxisIndex: 1,
      smooth: true,
      lineStyle: {
        type: 'dashed'
      },
      itemStyle: {
        color: '#9B59B6'
      },
      label: {
        show: true,
        fontSize: 10,
        formatter: ({ value }) =>
          Number.isFinite(value) ? `${Number(value).toFixed(1)}%` : ''
      },
      data: momSeries.data,
      connectNulls: true
    })
  }

  return {
    tooltip: {
      trigger: 'axis',
      formatter: (items) => {
        if (!Array.isArray(items)) return ''
        return items
          .map((entry) => {
            if (entry.seriesName.includes('增长率')) {
              const val = Number(entry.value)
              if (!Number.isFinite(val)) return ''
              return `${entry.marker}${entry.seriesName}: ${val.toFixed(2)}%`
            }
            const val = Number(entry.value)
            return `${entry.marker}${entry.seriesName}: ${val.toFixed(2)}万`
          })
          .filter(Boolean)
          .join('<br/>')
      }
    },
    legend: {
      data: legendData
    },
    grid: {
      top: 52,
      left: '4%',
      right: '4%',
      bottom: 34,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: months
    },
    yAxis: [
      {
        type: 'value',
        name: '金额 (万元)',
        minInterval: 1
      },
      {
        type: 'value',
        name: '增长率 (%)',
        min: (hasYoY || hasMoM) ? Math.floor(rateMin - ratePadding) : 0,
        max: (hasYoY || hasMoM) ? Math.ceil(rateMax + ratePadding) : 0,
        axisLabel: {
          formatter: '{value}%'
        }
      }
    ],
    series: [...barSeries, ...lineSeries]
  }
}
</script>

<style lang="scss" scoped>
.business-zhuhai-revenue {
  .chart-card {
    min-height: 460px;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-weight: 600;
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
