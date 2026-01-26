<template>
  <div class="market-zhuhai-weekly">

    <el-card class="chart-card" v-loading="weeklyLoading">
      <template #header>
        <div class="card-header">
          <span>珠海订单统计（周度）</span>
          <el-date-picker v-model="month" type="month" placeholder="选择月份" @change="handleMonthChange" />
          <!-- <el-date-picker
            v-model="selectedWeekRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            size="small"
            unlink-panels
            @change="handleWeekRangeChange"
          /> -->
        </div>
      </template>

      <EChart :option="weeklyOption" height="400px" />

      <el-row :gutter="16" class="summary-row">
        <el-col :xs="24" :sm="8">
          <div class="summary-card primary">
            <div class="summary-label">监控周数</div>
            <div class="summary-value">{{ weeklySummary.weekCount }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="8">
          <div class="summary-card info">
            <div class="summary-label">平均每周订单</div>
            <div class="summary-value">{{ weeklySummary.average }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="8">
          <div class="summary-card accent">
            <div class="summary-label">峰值周</div>
            <div class="summary-value">{{ weeklySummary.peakWeek }}</div>
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

const weeklyLoading = ref(false)

const weeklySummary = reactive({
  weekCount: '0',
  average: '0',
  peakWeek: '-'
})

const weeklyOption = ref(buildWeeklyOption([], []))

// const selectedWeekRange = ref(null)
// 新增一个响应式变量用于存储选中的月份
const month = ref(new Date());

const DEFAULT_WEEKLY_DATA = {
  weeks: Array.from({ length: 12 }, (_, idx) => `第${idx + 1}周`),
  data: [82, 95, 104, 110, 123, 118, 130, 142, 137, 148, 155, 162]
}

const applyWeeklyPayload = (payload) => {
  const weeks = Array.isArray(payload?.weeks) ? payload.weeks : payload?.labels || []
  const values = Array.isArray(payload?.data) ? payload.data : payload?.values || []

  if (!weeks.length || !values.length) {
    return false
  }

  weeklyOption.value = buildWeeklyOption(weeks, values)

  const total = values.reduce((sum, val) => sum + Number(val || 0), 0)
  const average = weeks.length ? (total / weeks.length) : 0
  const peakIndex = values.reduce((maxIdx, current, idx) => (current > values[maxIdx] ? idx : maxIdx), 0)

  weeklySummary.weekCount = weeks.length.toString()
  weeklySummary.average = Number.isFinite(average) ? average.toFixed(1) : '0.0'
  weeklySummary.peakWeek = `${weeks[peakIndex] || '-'} (${values[peakIndex] || 0})`
  return true
}

const fetchWeeklyData = async (params) => {
  weeklyLoading.value = true
  try {
    const response = await marketAnalysisApi.getZhuhaiWeekly(params)
    const applied = applyWeeklyPayload(response)
    console.log('周度数据获取成功。', response)
    if (!applied) throw new Error('empty-weekly')
  } catch (error) {
    console.warn('市场周度数据获取失败，使用示例数据。', error)
  } finally {
    weeklyLoading.value = false
  }
}

// const handleWeekRangeChange = (value) => {
//   if (!value || value.length !== 2) {
//     fetchWeeklyData()
//     return
//   }
//   const [start, end] = value
//   fetchWeeklyData({
//     start_date: formatDate(start),
//     end_date: formatDate(end)
//   })
// }

const handleMonthChange = (value) => {
  if (!value) {
    fetchWeeklyData();
    return;
  }
  
  const year = value.getFullYear();
  const monthNum = value.getMonth() + 1;
  // 格式化为 'YYYY-MM' 格式
  const formattedMonth = `${year}-${String(monthNum).padStart(2, '0')}`;
  
  fetchWeeklyData({
    month: formattedMonth
  })
}

const formatDate = (raw) => {
  const date = new Date(raw)
  if (Number.isNaN(date.getTime())) {
    return ''
  }
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// onMounted(() => fetchWeeklyData())
onMounted(() => {
  handleMonthChange(month.value);
})

function buildWeeklyOption(weeks, data) {
  return {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      top: 40,
      left: '4%',
      right: '4%',
      bottom: 25,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: weeks
    },
    yAxis: {
      type: 'value',
      name: '订单数',
      minInterval: 1
    },
    series: [
      {
        name: '周订单量',
        type: 'bar',
        barWidth: 28,
        itemStyle: {
          color: '#409EFF'
        },
        label: {
          show: true,
          position: 'top'
        },
        data
      }
    ]
  }
}
</script>

<style lang="scss" scoped>
.market-zhuhai-weekly {
  .alert {
    margin-bottom: 20px;
  }

  .chart-card {
    min-height: 420px;
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
