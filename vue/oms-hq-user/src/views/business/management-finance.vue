<template>
  <div class="management-finance">
    <h1>管理层财务概况表</h1>
    
    <!-- 竖向三栏布局 -->
    <div class="vertical-layout">
      <!-- 第一栏：收入与成本 -->
      <div class="vertical-column">
        <h3>收入与成本</h3>
        <div class="horizontal-card-layout">
          <!-- 营业收入与成本图表 -->
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>营业收入与成本</span>
              </div>
            </template>
            <EChart :option="revenueCostOption" height="300px" />
          </el-card>
          
          <!-- 营业外收入与支出图表 -->
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>营业外收入与支出</span>
              </div>
            </template>
            <EChart :option="nonOperatingOption" height="300px" />
          </el-card>
        </div>
      </div>
      
      <!-- 第二栏：利润分析卡片 -->
      <div class="vertical-column">
        <h3>利润分析</h3>
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>毛利润</span>
              </div>
            </template>
            <div class="card-content">{{ profitData.grossProfit.toLocaleString() }}</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>毛利率</span>
              </div>
            </template>
            <div class="card-content">{{ profitData.grossProfitRate }}%</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>期间费用</span>
              </div>
            </template>
            <div class="card-content">{{ profitData.periodCost.toLocaleString() }}</div>
          </el-card>
        </div>
      </div>
      
      <!-- 第三栏：净利润图表 -->
      <div class="vertical-column">
        <h3>净利润</h3>
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>净利润</span>
              </div>
            </template>
            <EChart :option="netProfitOption" height="300px" />
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import EChart from '@/components/EChart.vue'

/**
 * 格式化数值为千分位（用于图表标签显示）
 * @param {number} value - 数值（单位：元）
 * @returns {string} 格式化后的字符串
 */
const formatNumber = (value) => {
  return value.toLocaleString('zh-CN')
}

/**
 * 格式化数值为千分位加单位（用于tooltip显示）
 * @param {number} value - 数值（单位：元）
 * @returns {string} 格式化后的字符串
 */
const formatCurrency = (value) => {
  return value.toLocaleString('zh-CN') + '元'
}

// 利润分析数据（可从后端获取）
const profitData = ref({
  grossProfit: 40000000, // 毛利润（元）
  grossProfitRate: 25.6, // 毛利率（%）
  periodCost: 12000000   // 期间费用（元）
})

// 图表基础配置
const baseChartConfig = {
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '20%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  },
  yAxis: {
    type: 'value',
    name: '',
    axisLabel: { formatter: (value) => value.toLocaleString('zh-CN') }
  }
}

// 营业收入与成本数据（可从后端获取）
const revenueCostData = {
  revenue: [1200000, 1380000, 1520000, 1650000, 1780000, 1880000, 1960000, 2050000, 2140000, 2280000, 2400000, 2550000], // 营业收入（元）
  cost: [800000, 920000, 1050000, 1150000, 1250000, 1350000, 1420000, 1480000, 1550000, 1620000, 1680000, 1750000] // 营业成本（元）
}

// 营业收入与成本图表配置
const revenueCostOption = ref({
  ...baseChartConfig,
  tooltip: {
    ...baseChartConfig.tooltip,
    formatter: (params) => {
      let result = params[0].name + '<br/>'
      params.forEach(item => {
        result += `${item.marker} ${item.seriesName}: ${formatCurrency(item.value)}<br/>`
      })
      return result
    }
  },
  legend: {
    data: ['营业收入', '营业成本'],
    top: 10,
    right: 30,
    orient: 'horizontal'
  },
  series: [
    {
      name: '营业收入',
      type: 'bar',
      data: revenueCostData.revenue,
      itemStyle: { color: '#409EFF' },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => formatNumber(params.value),
        fontSize: 10
      }
    },
    {
      name: '营业成本',
      type: 'bar',
      data: revenueCostData.cost,
      itemStyle: { color: '#67C23A' },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => formatNumber(params.value),
        fontSize: 10
      }
    }
  ]
})

// 营业外收入与支出数据（可从后端获取）
const nonOperatingData = {
  income: [150000, 180000, 220000, 250000, 280000, 300000, 320000, 350000, 380000, 400000, 420000, 450000], // 营业外收入（元）
  expense: [80000, 100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000, 260000, 280000, 300000] // 营业外支出（元）
}

// 营业外收入与支出图表配置
const nonOperatingOption = ref({
  ...baseChartConfig,
  tooltip: {
    ...baseChartConfig.tooltip,
    formatter: (params) => {
      let result = params[0].name + '<br/>'
      params.forEach(item => {
        result += `${item.marker} ${item.seriesName}: ${formatCurrency(item.value)}<br/>`
      })
      return result
    }
  },
  legend: {
    data: ['营业外收入', '营业外支出'],
    top: 10,
    right: 30,
    orient: 'horizontal'
  },
  series: [
    {
      name: '营业外收入',
      type: 'bar',
      data: nonOperatingData.income,
      itemStyle: { color: '#F1C40F' },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => formatNumber(params.value),
        fontSize: 10
      }
    },
    {
      name: '营业外支出',
      type: 'bar',
      data: nonOperatingData.expense,
      itemStyle: { color: '#909399' },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => formatNumber(params.value),
        fontSize: 10
      }
    }
  ]
})

// 净利润数据（可从后端获取）
const netProfitData = {
  profit: [450000, 520000, 600000, 680000, 750000, 820000, 880000, 950000, 1020000, 1100000, 1180000, 1250000], // 净利润（元）
  growthRate: [12.5, 13.0, 15.4, 17.2, 15.4, 14.7, 15.8, 16.5, 17.2, 17.6, 18.0, 18.4] // 同比增长率（%）
}

// 净利润图表配置
const netProfitOption = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      crossStyle: { color: '#999' }
    },
    formatter: (params) => {
      let result = params[0].name + '<br/>'
      params.forEach(item => {
        if (item.seriesName === '净利润') {
          result += `${item.marker} ${item.seriesName}: ${formatCurrency(item.value)}<br/>`
        } else {
          result += `${item.marker} ${item.seriesName}: ${item.value}%<br/>`
        }
      })
      return result
    }
  },
  legend: {
    data: ['净利润', '同比增长率'],
    top: 10,
    left: 'center',
    orient: 'horizontal'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '20%',
    containLabel: true
  },
  xAxis: [{
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
    axisPointer: { type: 'shadow' }
  }],
  yAxis: [
    {
      type: 'value',
      name: '净利润（元）',
      min: 0,
      axisLabel: { formatter: (value) => value.toLocaleString('zh-CN') + '元' }
    },
    {
      type: 'value',
      name: '同比增长率（%）',
      min: -20,
      max: 50,
      axisLabel: { formatter: '{value}%' }
    }
  ],
  series: [
    {
      name: '净利润',
      type: 'bar',
      data: netProfitData.profit,
      itemStyle: { color: '#409EFF' },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => formatNumber(params.value),
        fontSize: 10
      }
    },
    {
      name: '同比增长率',
      type: 'line',
      yAxisIndex: 1,
      data: netProfitData.growthRate,
      itemStyle: { color: '#F56C6C' },
      lineStyle: { width: 3 },
      symbol: 'circle',
      symbolSize: 8,
      label: {
        show: true,
        position: 'top',
        formatter: '{c}%',
        fontSize: 12,
        color: '#F56C6C'
      }
    }
  ]
})

// 页面加载时初始化数据（可替换为从后端获取数据）
onMounted(() => {
  // 这里可以添加从后端获取数据的逻辑
  // 例如：fetchFinancialData().then(data => updateChartData(data))
})
</script>

<style scoped>
.management-finance {
  padding: 20px;
  background: #fff;
  border-radius: 4px;
  min-height: 500px;
}

.management-finance h1 {
  color: #303133;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 500;
  text-align: center;
}

/* 竖向布局样式 */
.vertical-layout {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.vertical-column {
  border: 1px solid #e6e6e6;
  border-radius: 4px;
  padding: 20px;
  background-color: #f9f9f9;
}

.vertical-column h3 {
  color: #303133;
  margin-bottom: 15px;
  font-size: 18px;
  font-weight: 600;
  text-align: center;
}

/* 横向卡片布局样式 */
.horizontal-card-layout {
  display: flex;
  gap: 15px;
  justify-content: space-between;
}

/* 财务卡片样式 */
.finance-card {
  flex: 1;
  min-height: 150px;
}

/* 卡片标题样式 */
.card-header {
  font-weight: 600;
  color: #303133;
  font-size: 16px;
  text-align: left;
  padding: 0;
}

/* 覆盖 Element Plus 卡片标题样式 */
:deep(.el-card__header) {
  padding: 12px 20px;
  border-bottom: 1px solid #e6e6e6;
}

.card-content {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
  text-align: center;
  padding: 20px 0;
}
</style>