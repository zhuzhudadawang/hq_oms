<template>
  <div class="market-zhuhai-monthly">
    <el-card class="chart-card" v-loading="monthlyLoading">
      <template #header>
        <div class="card-header">
          <span>珠海订单统计（月度）</span>
          <el-tag type="success" effect="plain">覆盖2024-2026年</el-tag>
        </div>
      </template>

      <EChart :option="monthlyOption" height="440px" />

      <el-row :gutter="16" class="summary-row">
        <el-col :xs="24" :sm="12">
          <div class="summary-card primary">
            <div class="summary-label">{{ monthlySummary.prevYearLabel }}</div>
            <div class="summary-value">{{ monthlySummary.total2024 }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12">
          <div class="summary-card info">
            <div class="summary-label">{{ monthlySummary.currYearLabel }}</div>
            <div class="summary-value">{{ monthlySummary.total2025 }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import EChart from '@/components/EChart.vue'
import { marketAnalysisApi } from '@/api/market'

const monthlyLoading = ref(false)

const monthlySummary = reactive({
  total2024: '0',
  total2025: '0',
  yoyGrowth: '0.00%',
  prevYearLabel: '上年订单总量',
  currYearLabel: '本年订单总量'
})

const monthlyOption = ref(buildMonthlyOption([], [], { data: [], label: '同比增长率' }, { data: [], label: '环比增长率' }))

const DEFAULT_MONTHLY_DATA = {
  months: [
    '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
    '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12'
  ],
  series: [
    {
      name: '2024',
      data: [120, 138, 152, 165, 178, 188, 196, 205, 214, 228, 240, 255]
    },
    {
      name: '2025',
      data: [148, 160, 175, 189, 205, 220, 236, 245, 258, 270, 285, 302]
    },
    {
      name: '2026',
      data: [175, 188, 202, 218, 235, 252, 268, 280, 295, 310, 328, 350]
    }
  ]
}

const formatMonthLabels = (list) =>
  (Array.isArray(list) ? list : []).map((item) => {
    if (!item) return ''
    const monthPart = String(item).split('-').pop()
    const numeric = parseInt(monthPart, 10)
    if (Number.isFinite(numeric)) {
      return `${numeric.toString().padStart(2, '0')}月`
    }
    return item
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
    .toFixed(0)
    .replace(/\B(?=(\d{3})+(?!\d))/g, ',')

const calcYoY = (base, current) => {
  const baseNum = Number(base)
  const currentNum = Number(current)
  // 当前值为0或基准值无效时显示"—"
  if (!Number.isFinite(baseNum) || baseNum === 0 || currentNum === 0) {
    return '—'
  }
  const percent = ((currentNum - baseNum) / baseNum) * 100
  return `${percent >= 0 ? '+' : ''}${percent.toFixed(2)}%`
}

const applyMonthlyPayload = (payload) => {
  const months = formatMonthLabels(payload?.months || payload?.labels || payload?.xAxis || [])
  const series = normaliseSeries(payload?.series || payload?.dataset || payload?.data)

  if (!months.length || !series.length) {
    return false
  }

  const numericSeries = series.map((item) => ({
    name: item.name,
    data: months.map((_, idx) => {
      const value = Array.isArray(item.data) ? item.data[idx] : undefined
      const num = Number(value)
      return Number.isFinite(num) ? num : 0
    })
  }))

  const totals = numericSeries.reduce((acc, item) => {
    const sum = item.data.reduce((total, current) => total + Number(current || 0), 0)
    const key = /20\d{2}/.test(item.name) ? item.name.match(/20\d{2}/)[0] : item.name
    acc[key] = sum
    return acc
  }, {})

  const yoySeries = buildYoYSeries(numericSeries)
  const momSeries = buildMoMSeries(numericSeries)

  monthlyOption.value = buildMonthlyOption(months, numericSeries, yoySeries, momSeries)

  // 按年份排序，取最新两年用于统计卡片
  const parseYear = (name) => {
    const match = String(name || '').match(/20\d{2}/)
    return match ? Number(match[0]) : null
  }
  const sortedYears = Object.keys(totals)
    .map(k => ({ key: k, year: parseYear(k) || 0 }))
    .filter(item => item.year > 0)
    .sort((a, b) => a.year - b.year)

  const latestTwo = sortedYears.slice(-2)
  const prevYear = latestTwo[0]
  const currYear = latestTwo[1]

  monthlySummary.total2024 = toThousand(prevYear ? totals[prevYear.key] : 0)
  monthlySummary.total2025 = toThousand(currYear ? totals[currYear.key] : 0)
  monthlySummary.yoyGrowth = calcYoY(prevYear ? totals[prevYear.key] : 0, currYear ? totals[currYear.key] : 0)
  monthlySummary.prevYearLabel = prevYear ? `${prevYear.year}年订单总量` : '上年订单总量'
  monthlySummary.currYearLabel = currYear ? `${currYear.year}年订单总量` : '本年订单总量'
  return true
}

const fetchMonthlyData = async () => {
  monthlyLoading.value = true
  try {
    const response = await marketAnalysisApi.getZhuhaiMonthly()
    const applied = applyMonthlyPayload(response)
    if (!applied) throw new Error('empty-monthly')
  } catch (error) {
    console.warn('市场月度数据获取失败，使用示例数据。', error)
    applyMonthlyPayload(DEFAULT_MONTHLY_DATA)
  } finally {
    monthlyLoading.value = false
  }
}

onMounted(fetchMonthlyData)

function buildYoYSeries(series) {
  if (!series.length) return { data: [], label: '同比增长率' }

  const parseYear = (name) => {
    const match = String(name || '').match(/20\d{2}/)
    return match ? Number(match[0]) : null
  }

  const yearSeries = series.filter((item) => parseYear(item.name) !== null)
  if (yearSeries.length < 2) {
    const length = series[0]?.data?.length || 0
    return { data: new Array(length).fill(null), label: '同比增长率' }
  }

  // 按年份排序，取最新两年计算同比
  const sorted = [...yearSeries].sort((a, b) => parseYear(a.name) - parseYear(b.name))
  const baseSeries = sorted[sorted.length - 2] // 倒数第二年
  const latestSeries = sorted[sorted.length - 1] // 最新年

  if (!baseSeries || !latestSeries || baseSeries === latestSeries) {
    return { data: new Array((latestSeries?.data?.length) || 0).fill(null), label: '同比增长率' }
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

// 计算环比增长率（最新一年的月环比，1月份与上一年12月对比）
function buildMoMSeries(series) {
  if (!series.length) return { data: [], label: '环比增长率' }

  const parseYear = (name) => {
    const match = String(name || '').match(/20\d{2}/)
    return match ? Number(match[0]) : null
  }

  const yearSeries = series.filter((item) => parseYear(item.name) !== null)
  if (!yearSeries.length) {
    const length = series[0]?.data?.length || 0
    return { data: new Array(length).fill(null), label: '环比增长率' }
  }

  // 按年份排序
  const sorted = [...yearSeries].sort((a, b) => parseYear(a.name) - parseYear(b.name))
  const latestSeries = sorted[sorted.length - 1]
  const prevYearSeries = sorted.length >= 2 ? sorted[sorted.length - 2] : null
  const latestYear = parseYear(latestSeries.name)
  const label = `环比增长率(${latestYear})`

  const latestData = Array.isArray(latestSeries.data) ? latestSeries.data : []
  const prevYearData = prevYearSeries && Array.isArray(prevYearSeries.data) ? prevYearSeries.data : []

  const data = latestData.map((value, index) => {
    let prevValue
    if (index === 0) {
      // 1月份与上一年12月对比
      prevValue = prevYearData.length >= 12 ? Number(prevYearData[11]) : null
    } else {
      // 其他月份与本年上个月对比
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

function buildMonthlyOption(months, series, yoySeries, momSeries) {
  const palette = ['#409EFF', '#67C23A', '#F1C40F ', '#909399']
  const hasYoY = Array.isArray(yoySeries.data) && yoySeries.data.some((value) => Number.isFinite(value))
  const hasMoM = Array.isArray(momSeries.data) && momSeries.data.some((value) => Number.isFinite(value))
  
  // 合并同比和环比数据计算Y轴范围
  const allRateValues = [
    ...(hasYoY ? yoySeries.data.filter((value) => Number.isFinite(value)) : []),
    ...(hasMoM ? momSeries.data.filter((value) => Number.isFinite(value)) : [])
  ]
  const rateMin = allRateValues.length ? Math.min(...allRateValues) : 0
  const rateMax = allRateValues.length ? Math.max(...allRateValues) : 0
  const rateRangeGap = rateMax - rateMin
  const ratePadding = (hasYoY || hasMoM) ? (rateRangeGap === 0 ? 5 : Math.max(2, Math.abs(rateRangeGap) * 0.1)) : 0

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
            return `${entry.marker}${entry.seriesName}: ${entry.value}`
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
        name: '订单数',
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
    series: [
      ...series.map((item, index) => ({
        name: item.name,
        type: 'bar',
        barGap: '7%',
        barWidth: 23,
        itemStyle: {
          color: palette[index % palette.length]
        },
        label: {
          show: true,
          position: 'top',
          fontSize: 10
        },
        data: item.data
      })),
      ...lineSeries
    ]
  }
}
</script>

<style lang="scss" scoped>
.market-zhuhai-monthly {
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
