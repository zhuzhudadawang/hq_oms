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
        <el-col :xs="24" :sm="8">
          <div class="summary-card primary">
            <div class="summary-label">{{ monthlySummary.prevYearLabel }}</div>
            <div class="summary-value">{{ monthlySummary.total2024 }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="8">
          <div class="summary-card info">
            <div class="summary-label">{{ monthlySummary.currYearLabel }}</div>
            <div class="summary-value">{{ monthlySummary.total2025 }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="8">
          <div class="summary-card accent">
            <div class="summary-label">同比增长</div>
            <div class="summary-value">{{ monthlySummary.yoyGrowth }}</div>
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

const monthlyOption = ref(buildMonthlyOption([], [], []))

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

  monthlyOption.value = buildMonthlyOption(months, numericSeries, yoySeries)

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
  if (!series.length) return []

  const parseYear = (name) => {
    const match = String(name || '').match(/20\d{2}/)
    return match ? Number(match[0]) : null
  }

  const yearSeries = series.filter((item) => parseYear(item.name) !== null)
  if (yearSeries.length < 2) {
    const length = series[0]?.data?.length || 0
    return new Array(length).fill(null)
  }

  // 按年份排序，取最新两年计算同比
  const sorted = [...yearSeries].sort((a, b) => parseYear(a.name) - parseYear(b.name))
  const baseSeries = sorted[sorted.length - 2] // 倒数第二年
  const latestSeries = sorted[sorted.length - 1] // 最新年

  if (!baseSeries || !latestSeries || baseSeries === latestSeries) {
    return new Array((latestSeries?.data?.length) || 0).fill(null)
  }

  const baseData = Array.isArray(baseSeries.data) ? baseSeries.data : []
  const latestData = Array.isArray(latestSeries.data) ? latestSeries.data : []

  return latestData.map((value, index) => {
    const baseValue = Number(baseData[index])
    const currentValue = Number(value)
    // 当前值为0或无效时不显示同比
    if (!Number.isFinite(baseValue) || baseValue === 0 || !Number.isFinite(currentValue) || currentValue === 0) {
      return null
    }
    const rate = ((currentValue - baseValue) / baseValue) * 100
    return Number(rate.toFixed(2))
  })
}

function buildMonthlyOption(months, series, yoySeries) {
  const palette = ['#409EFF', '#67C23A', '#F1C40F ', '#909399']
  const hasYoY = Array.isArray(yoySeries) && yoySeries.some((value) => Number.isFinite(value))
  const yoyValues = hasYoY ? yoySeries.filter((value) => Number.isFinite(value)) : []
  const yoyMin = yoyValues.length ? Math.min(...yoyValues) : 0
  const yoyMax = yoyValues.length ? Math.max(...yoyValues) : 0
  const yoyRangeGap = yoyMax - yoyMin
  const yoyPadding = hasYoY ? (yoyRangeGap === 0 ? 5 : Math.max(2, Math.abs(yoyRangeGap) * 0.1)) : 0

  return {
    tooltip: {
      trigger: 'axis',
      formatter: (items) => {
        if (!Array.isArray(items)) return ''
        return items
          .map((entry) => {
            if (entry.seriesName === '同比增长率') {
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
      data: [
        ...series.map((item) => item.name),
        ...(hasYoY ? ['同比增长率'] : [])
      ]
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
        name: '同比 (%)',
        min: hasYoY ? Math.floor(yoyMin - yoyPadding) : 0,
        max: hasYoY ? Math.ceil(yoyMax + yoyPadding) : 0,
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
      ...(hasYoY
        ? [
            {
              name: '同比增长率',
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
              data: yoySeries,
              connectNulls: true
            }
          ]
        : [])
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
