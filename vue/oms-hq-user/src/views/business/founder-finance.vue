<template>
  <div class="founder-finance">
    <h1>创始股东财务概况表</h1>
    
    <!-- 竖向三栏布局 -->
    <div class="vertical-layout">
      <!-- 盈利能力分析 -->
      <div class="vertical-column">
        <h3>盈利能力分析</h3>
        
        <!-- 第一行：两个图表 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>营业收入与成本</span>
              </div>
            </template>
            <EChart :option="revenueCostOption" height="300px" />
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>营业外收入与支出</span>
              </div>
            </template>
            <EChart :option="nonOperatingOption" height="300px" />
          </el-card>
        </div>
        
        <!-- 第二行：三个卡片 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>毛利润</span>
              </div>
            </template>
            <div class="card-content">{{ profitabilityData.grossProfit.toLocaleString() }}</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>毛利率</span>
              </div>
            </template>
            <div class="card-content">{{ profitabilityData.grossMargin }}%</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>期间费用</span>
              </div>
            </template>
            <div class="card-content">{{ profitabilityData.periodExpenses.toLocaleString() }}</div>
          </el-card>
        </div>
        
        <!-- 第三行：净利润柱状图 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card full-width">
            <template #header>
              <div class="card-header">
                <span>净利润趋势分析</span>
              </div>
            </template>
            <EChart :option="netProfitOption" height="300px" />
          </el-card>
        </div>
      </div>
      
      <!-- 财务状况概览 -->
      <div class="vertical-column">
        <h3>财务状况概览</h3>
        
        <!-- 第一行：两个图表 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>资产结构分析</span>
              </div>
            </template>
            <EChart :option="assetStructureOption" height="300px" />
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>负债与权益比例</span>
              </div>
            </template>
            <EChart :option="liabilityEquityOption" height="300px" />
          </el-card>
        </div>
        
        <!-- 第二行：四个卡片 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>资产总额</span>
              </div>
            </template>
            <div class="card-content">{{ financialStatus.totalAssets.toLocaleString() }}</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>负债总额</span>
              </div>
            </template>
            <div class="card-content">{{ financialStatus.totalLiabilities.toLocaleString() }}</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>股东权益</span>
              </div>
            </template>
            <div class="card-content">{{ financialStatus.shareholdersEquity.toLocaleString() }}</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>资产负债率</span>
              </div>
            </template>
            <div class="card-content">{{ financialStatus.debtRatio }}%</div>
          </el-card>
        </div>
      </div>
      
      <!-- 资金状况分析 -->
      <div class="vertical-column">
        <h3>资金状况分析</h3>
        
        <!-- 第一行：两个图表 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>资金构成分析</span>
              </div>
            </template>
            <EChart :option="fundCompositionOption" height="300px" />
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>资金趋势分析</span>
              </div>
            </template>
            <EChart :option="fundTrendOption" height="300px" />
          </el-card>
        </div>
        
        <!-- 第二行：四个卡片 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>资金总额</span>
              </div>
            </template>
            <div class="card-content">{{ fundStatus.totalFunds.toLocaleString() }}</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>活期资金</span>
              </div>
            </template>
            <div class="card-content">{{ fundStatus.currentFunds.toLocaleString() }}</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>理财资金</span>
              </div>
            </template>
            <div class="card-content">{{ fundStatus.financialProducts.toLocaleString() }}</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>未使用贷款额度</span>
              </div>
            </template>
            <div class="card-content">{{ fundStatus.unusedLoanLimit.toLocaleString() }}</div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import EChart from '@/components/EChart.vue'

// 格式化函数
const formatNumber = (value) => {
  return value.toLocaleString('zh-CN')
}

const formatCurrency = (value) => {
  return value.toLocaleString('zh-CN') + '元'
}

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

// 数据定义
const profitabilityData = ref({
  grossProfit: 32000000,
  grossMargin: 25.6,
  periodExpenses: 12000000
})

const financialStatus = ref({
  totalAssets: 500000000,
  totalLiabilities: 200000000,
  shareholdersEquity: 300000000,
  debtRatio: 40
})

const fundStatus = ref({
  totalFunds: 80000000,
  currentFunds: 30000000,
  financialProducts: 40000000,
  unusedLoanLimit: 20000000
})

// 图表数据配置
const revenueCostData = {
  revenue: [1200000, 1380000, 1520000, 1650000, 1780000, 1880000, 1960000, 2050000, 2140000, 2280000, 2400000, 2550000],
  cost: [800000, 920000, 1050000, 1150000, 1250000, 1350000, 1420000, 1480000, 1550000, 1620000, 1680000, 1750000]
}

const nonOperatingData = {
  income: [150000, 180000, 220000, 250000, 280000, 300000, 320000, 350000, 380000, 400000, 420000, 450000],
  expense: [80000, 100000, 120000, 140000, 160000, 180000, 200000, 220000, 240000, 260000, 280000, 300000]
}

const netProfitData = {
  profit: [450000, 520000, 600000, 680000, 750000, 820000, 880000, 950000, 1020000, 1100000, 1180000, 1250000],
  growthRate: [12.5, 13.0, 15.4, 17.2, 15.4, 14.7, 15.8, 16.5, 17.2, 17.6, 18.0, 18.4]
}

// 图表配置
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
        fontSize: 10
      }
    }
  ]
})

const assetStructureOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c}元 ({d}%)'
  },
  legend: {
    orient: 'vertical',
    right: 10,
    top: 'center'
  },
  series: [
    {
      name: '资产结构',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {d}%',
        fontSize: 12
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: true
      },
      data: [
        { value: 200000000, name: '流动资产', itemStyle: { color: '#409EFF' } },
        { value: 150000000, name: '固定资产', itemStyle: { color: '#67C23A' } },
        { value: 100000000, name: '无形资产', itemStyle: { color: '#E6A23C' } },
        { value: 50000000, name: '其他资产', itemStyle: { color: '#909399' } }
      ]
    }
  ]
})

const liabilityEquityOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c}元 ({d}%)'
  },
  legend: {
    orient: 'vertical',
    right: 10,
    top: 'center'
  },
  series: [
    {
      name: '负债与权益',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {d}%',
        fontSize: 12
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: true
      },
      data: [
        { value: 200000000, name: '负债总额', itemStyle: { color: '#F56C6C' } },
        { value: 300000000, name: '股东权益', itemStyle: { color: '#409EFF' } }
      ]
    }
  ]
})

const fundCompositionOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c}元 ({d}%)'
  },
  legend: {
    orient: 'vertical',
    right: 10,
    top: 'center'
  },
  series: [
    {
      name: '资金构成',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {d}%',
        fontSize: 12
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: true
      },
      data: [
        { value: 30000000, name: '活期资金', itemStyle: { color: '#67C23A' } },
        { value: 40000000, name: '理财资金', itemStyle: { color: '#409EFF' } },
        { value: 10000000, name: '其他资金', itemStyle: { color: '#E6A23C' } }
      ]
    }
  ]
})

const fundTrendOption = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
  legend: {
    data: ['资金总额', '活期资金', '理财资金'],
    top: 10
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
    boundaryGap: false,
    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: (value) => value.toLocaleString('zh-CN') + '元'
    }
  },
  series: [
    {
      name: '资金总额',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: [60000000, 62000000, 65000000, 68000000, 70000000, 72000000, 75000000, 77000000, 78000000, 79000000, 80000000, 81000000],
      itemStyle: { color: '#409EFF' }
    },
    {
      name: '活期资金',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: [25000000, 26000000, 27000000, 28000000, 29000000, 29500000, 30000000, 30500000, 31000000, 30000000, 29500000, 30000000],
      itemStyle: { color: '#67C23A' }
    },
    {
      name: '理财资金',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: [30000000, 32000000, 34000000, 36000000, 37000000, 38500000, 40000000, 41500000, 42000000, 44000000, 45500000, 46000000],
      itemStyle: { color: '#E6A23C' }
    }
  ]
})

// 数据初始化
onMounted(() => {
  // 这里可以添加从后端获取数据的逻辑
  // 例如：fetchFinancialData().then(data => updateChartData(data))
})
</script>

<style scoped>
.founder-finance {
  padding: 20px;
  background: #fff;
  border-radius: 4px;
  min-height: 500px;
}

.founder-finance h1 {
  color: #303133;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: 500;
  text-align: center;
}

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

.horizontal-card-layout {
  display: flex;
  gap: 15px;
  justify-content: space-between;
  margin-bottom: 20px;
}

.finance-card {
  flex: 1;
  min-height: 150px;
}

.finance-card.full-width {
  flex: 0 0 100%;
}

.card-header {
  font-weight: 600;
  color: #303133;
  font-size: 16px;
  text-align: left;
  padding: 0;
}

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