<template>
  <div class="founder-assets">
    <h1>创始股东资产分析表</h1>
    
    <!-- 竖向两栏布局 -->
    <div class="vertical-layout">
      <!-- 资产与负债总览 -->
      <div class="vertical-column">
        <h3>资产与负债总览</h3>
        
        <!-- 资产与负债月度趋势柱状图 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card full-width">
            <template #header>
              <div class="card-header">
                <span>资产与负债月度趋势分析</span>
              </div>
            </template>
            <EChart :option="assetsLiabilitiesTrendOption" height="350px" />
          </el-card>
        </div>
        
        <!-- 核心指标卡片 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>资产总额</span>
              </div>
            </template>
            <div class="card-content">{{ assetLiabilityData.totalAssets.toLocaleString() }}元</div>
            <div class="card-subtitle">同比增长 12.5%</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>负债总额</span>
              </div>
            </template>
            <div class="card-content">{{ assetLiabilityData.totalLiabilities.toLocaleString() }}元</div>
            <div class="card-subtitle">同比增长 8.3%</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>股东权益</span>
              </div>
            </template>
            <div class="card-content">{{ assetLiabilityData.shareholdersEquity.toLocaleString() }}元</div>
            <div class="card-subtitle">同比增长 15.2%</div>
          </el-card>
        </div>
        
        <!-- 资产负债率仪表盘 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card full-width">
            <template #header>
              <div class="card-header">
                <span>资产负债率分析</span>
              </div>
            </template>
            <EChart :option="debtRatioOption" height="300px" />
          </el-card>
        </div>
      </div>
      
      <!-- 资产构成分析 -->
      <div class="vertical-column">
        <h3>资产构成分析</h3>
        
        <!-- 资产构成环形图 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card full-width">
            <template #header>
              <div class="card-header">
                <span>资产构成比例</span>
              </div>
            </template>
            <EChart :option="assetCompositionOption" height="400px" />
          </el-card>
        </div>
        
        <!-- 资产项目卡片 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>资金+理财</span>
              </div>
            </template>
            <div class="card-content">{{ assetCompositionData.fundsWealthManagement.toLocaleString() }}元</div>
            <div class="card-percentage">{{ calculatePercentage(assetCompositionData.fundsWealthManagement) }}%</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: calculatePercentage(assetCompositionData.fundsWealthManagement) + '%' }"></div>
            </div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>存货</span>
              </div>
            </template>
            <div class="card-content">{{ assetCompositionData.inventory.toLocaleString() }}元</div>
            <div class="card-percentage">{{ calculatePercentage(assetCompositionData.inventory) }}%</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: calculatePercentage(assetCompositionData.inventory) + '%' }"></div>
            </div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>预付账款</span>
              </div>
            </template>
            <div class="card-content">{{ assetCompositionData.prepaidAccounts.toLocaleString() }}元</div>
            <div class="card-percentage">{{ calculatePercentage(assetCompositionData.prepaidAccounts) }}%</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: calculatePercentage(assetCompositionData.prepaidAccounts) + '%' }"></div>
            </div>
          </el-card>
        </div>
        
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>应收票据及账款</span>
              </div>
            </template>
            <div class="card-content">{{ assetCompositionData.notesReceivableAccounts.toLocaleString() }}元</div>
            <div class="card-percentage">{{ calculatePercentage(assetCompositionData.notesReceivableAccounts) }}%</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: calculatePercentage(assetCompositionData.notesReceivableAccounts) + '%' }"></div>
            </div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>其他应收款</span>
              </div>
            </template>
            <div class="card-content">{{ assetCompositionData.otherReceivables.toLocaleString() }}元</div>
            <div class="card-percentage">{{ calculatePercentage(assetCompositionData.otherReceivables) }}%</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: calculatePercentage(assetCompositionData.otherReceivables) + '%' }"></div>
            </div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>非流动资产</span>
              </div>
            </template>
            <div class="card-content">{{ assetCompositionData.nonCurrentAssets.toLocaleString() }}元</div>
            <div class="card-percentage">{{ calculatePercentage(assetCompositionData.nonCurrentAssets) }}%</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: calculatePercentage(assetCompositionData.nonCurrentAssets) + '%' }"></div>
            </div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>进项税</span>
              </div>
            </template>
            <div class="card-content">{{ assetCompositionData.inputTax.toLocaleString() }}元</div>
            <div class="card-percentage">{{ calculatePercentage(assetCompositionData.inputTax) }}%</div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: calculatePercentage(assetCompositionData.inputTax) + '%' }"></div>
            </div>
          </el-card>
        </div>
        
        <!-- 占比统计摘要 -->
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>流动资产占比</span>
              </div>
            </template>
            <div class="card-content">{{ calculateCurrentAssetsPercentage() }}%</div>
          </el-card>
          
          <el-card class="finance-card">
            <template #header>
              <div class="card-header">
                <span>非流动资产占比</span>
              </div>
            </template>
            <div class="card-content">{{ calculatePercentage(assetCompositionData.nonCurrentAssets) }}%</div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import EChart from '@/components/EChart.vue'

// 数据格式化函数
const formatNumber = (value) => value.toLocaleString('zh-CN')
const formatCurrency = (value) => value.toLocaleString('zh-CN') + '元'

// 响应式数据定义
const assetLiabilityData = ref({
  totalAssets: 12000000,
  totalLiabilities: 8000000,
  shareholdersEquity: 4000000,
  debtRatio: 66.7
})

const assetCompositionData = ref({
  fundsWealthManagement: 3000000,
  inventory: 1800000,
  prepaidAccounts: 900000,
  notesReceivableAccounts: 1500000,
  otherReceivables: 600000,
  nonCurrentAssets: 3600000,
  inputTax: 600000
})

// 计算逻辑
const calculatePercentage = (value) => {
  const total = assetLiabilityData.value.totalAssets
  return ((value / total) * 100).toFixed(1)
}

const calculateCurrentAssetsPercentage = () => {
  const currentAssetsTotal = Object.values(assetCompositionData.value)
    .filter((_, index) => index !== 5)
    .reduce((sum, value) => sum + value, 0)
  
  return ((currentAssetsTotal / assetLiabilityData.value.totalAssets) * 100).toFixed(1)
}

// 图表配置
const assetsLiabilitiesTrendOption = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: { type: 'shadow' },
    formatter: function(params) {
      let result = params[0].name + '<br/>'
      params.forEach(item => {
        result += `${item.marker} ${item.seriesName}: ${formatCurrency(item.value)}<br/>`
      })
      return result
    }
  },
  legend: {
    data: ['资产总额', '负债总额'],
    top: 10,
    right: 30,
    orient: 'horizontal'
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
    name: '金额（元）',
    axisLabel: { formatter: (value) => value.toLocaleString('zh-CN') }
  },
  series: [
    {
      name: '资产总额',
      type: 'bar',
      data: [10000000, 10200000, 10500000, 10800000, 11000000, 11200000, 11500000, 11700000, 11800000, 11900000, 12000000, 12100000],
      itemStyle: { color: '#409EFF' },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => formatNumber(params.value),
        fontSize: 10
      }
    },
    {
      name: '负债总额',
      type: 'bar',
      data: [7000000, 7200000, 7400000, 7500000, 7600000, 7700000, 7800000, 7850000, 7900000, 7950000, 8000000, 8050000],
      itemStyle: { color: '#F56C6C' },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => formatNumber(params.value),
        fontSize: 10
      }
    }
  ]
})

const debtRatioOption = ref({
  tooltip: {
    formatter: function(params) {
      return `资产负债率: ${params.value}%<br/>
              健康区间: 40%-60%<br/>
              当前状态: ${params.value > 60 ? '偏高' : params.value < 40 ? '偏低' : '健康'}`
    }
  },
  series: [
    {
      type: 'gauge',
      center: ['50%', '60%'],
      radius: '90%',
      min: 0,
      max: 100,
      progress: { show: true, width: 20 },
      axisLine: {
        lineStyle: {
          width: 20,
          color: [
            [0.4, '#67C23A'],
            [0.6, '#409EFF'],
            [1, '#F56C6C']
          ]
        }
      },
      axisTick: {
        distance: -30,
        length: 8,
        lineStyle: { color: '#fff', width: 2 }
      },
      axisLabel: { distance: -40, color: '#999', fontSize: 12 },
      pointer: { length: '80%', width: 6, itemStyle: { color: 'inherit' } },
      detail: {
        valueAnimation: true,
        formatter: '{value}%',
        color: 'auto',
        fontSize: 20,
        fontWeight: 'bold'
      },
      data: [{ value: assetLiabilityData.value.debtRatio, name: '资产负债率' }]
    }
  ]
})

const assetCompositionOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: function(params) {
      return `${params.name}<br/>金额: ${formatCurrency(params.value)}<br/>占比: ${params.percent}%`
    }
  },
  legend: {
    orient: 'vertical',
    right: 10,
    top: 'center',
    formatter: function(name) {
      const data = assetCompositionOption.value.series[0].data
      const item = data.find(d => d.name === name)
      return `${name}: ${item.value.toLocaleString('zh-CN')}元 (${item.percentage}%)`
    }
  },
  series: [
    {
      name: '资产构成',
      type: 'pie',
      radius: ['30%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: true, formatter: '{b}\n{d}%', fontSize: 12 },
      emphasis: {
        label: {
          show: true,
          fontSize: 14,
          fontWeight: 'bold',
          formatter: '{b}\n金额: {c}元\n占比: {d}%'
        }
      },
      labelLine: { show: true },
      data: [
        { 
          value: assetCompositionData.value.fundsWealthManagement, 
          name: '资金+理财',
          percentage: calculatePercentage(assetCompositionData.value.fundsWealthManagement),
          itemStyle: { color: '#409EFF' }
        },
        { 
          value: assetCompositionData.value.inventory, 
          name: '存货',
          percentage: calculatePercentage(assetCompositionData.value.inventory),
          itemStyle: { color: '#67C23A' }
        },
        { 
          value: assetCompositionData.value.prepaidAccounts, 
          name: '预付账款',
          percentage: calculatePercentage(assetCompositionData.value.prepaidAccounts),
          itemStyle: { color: '#E6A23C' }
        },
        { 
          value: assetCompositionData.value.notesReceivableAccounts, 
          name: '应收票据及账款',
          percentage: calculatePercentage(assetCompositionData.value.notesReceivableAccounts),
          itemStyle: { color: '#F56C6C' }
        },
        { 
          value: assetCompositionData.value.otherReceivables, 
          name: '其他应收款',
          percentage: calculatePercentage(assetCompositionData.value.otherReceivables),
          itemStyle: { color: '#909399' }
        },
        { 
          value: assetCompositionData.value.nonCurrentAssets, 
          name: '非流动资产',
          percentage: calculatePercentage(assetCompositionData.value.nonCurrentAssets),
          itemStyle: { color: '#8E44AD' }
        },
        { 
          value: assetCompositionData.value.inputTax, 
          name: '进项税',
          percentage: calculatePercentage(assetCompositionData.value.inputTax),
          itemStyle: { color: '#16A085' }
        }
      ]
    }
  ]
})

// 数据初始化与后端数据获取
const updateChartData = (data) => {
  // 更新资产与负债数据
  if (data.assetLiability) {
    assetLiabilityData.value = { ...assetLiabilityData.value, ...data.assetLiability }
  }
  
  // 更新资产构成数据
  if (data.assetComposition) {
    assetCompositionData.value = { ...assetCompositionData.value, ...data.assetComposition }
  }
  
  // 更新图表数据
  if (data.chartData) {
    // 可以根据实际数据结构更新图表配置
    console.log('更新图表数据:', data.chartData)
  }
}

onMounted(() => {
  // 从后端获取数据的逻辑
  // 例如：fetchAssetData().then(data => updateChartData(data))
})
</script>

<style scoped>
.founder-assets {
  padding: 20px;
  background: #fff;
  border-radius: 4px;
  min-height: 500px;
}

.founder-assets h1 {
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
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  text-align: center;
  padding: 15px 0 5px 0;
}

.card-subtitle {
  font-size: 12px;
  color: #909399;
  text-align: center;
  margin-bottom: 10px;
}

.card-percentage {
  font-size: 16px;
  font-weight: bold;
  color: #67C23A;
  text-align: center;
  margin: 5px 0;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: #ebeef5;
  border-radius: 3px;
  overflow: hidden;
  margin-top: 8px;
}

.progress-fill {
  height: 100%;
  background-color: #409EFF;
  border-radius: 3px;
  transition: width 0.3s ease;
}
</style>