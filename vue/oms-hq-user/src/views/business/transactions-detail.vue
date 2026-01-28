<template>
  <div class="current-account-detail">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>往来款明细表</h1>
    </div>

    <!-- 第一栏：资产/负债饼图 -->
    <div class="row">
      <div class="chart-section">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>负债构成分析</span>
            </div>
          </template>
          <EChart :option="liabilityPieOption" height="400px" />
        </el-card>
        
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>资产构成分析</span>
            </div>
          </template>
          <EChart :option="assetPieOption" height="400px" />
        </el-card>
      </div>
    </div>

    <!-- 第二栏：月度趋势柱状图 -->
    <div class="row">
      <el-card class="full-width-card">
        <template #header>
          <div class="card-header">
            <span>月度余额趋势分析</span>
            <div class="chart-controls">
              <el-radio-group v-model="chartViewType" @change="updateBarChart">
                <el-radio-button label="management">管理层</el-radio-button>
                <el-radio-button label="founder">创始股东</el-radio-button>
                <el-radio-button label="all">全部显示</el-radio-button>
              </el-radio-group>
            </div>
          </div>
        </template>
        <EChart :option="monthlyBarOption" height="400px" />
      </el-card>
    </div>

    <!-- 第三栏：明细表格 -->
    <div class="row">
      <el-card class="full-width-card">
        <template #header>
          <div class="card-header">
            <span>{{ currentTableView === 'asset' ? '资产' : '负债' }}往来款明细数据</span>
            <div class="table-controls">
              <el-input
                v-model="tableFilters.keyword"
                placeholder="搜索科目名称或往来单位"
                style="width: 200px; margin-right: 10px;"
                clearable
              />
              <el-button 
                :type="currentTableView === 'asset' ? 'primary' : 'default'"
                @click="switchTableView('asset')"
              >
                资产表格
              </el-button>
              <el-button 
                :type="currentTableView === 'liability' ? 'primary' : 'default'"
                @click="switchTableView('liability')"
              >
                负债表格
              </el-button>
              <el-button @click="resetFilters">重置</el-button>
              
              <!-- 合计模式切换按钮 -->
              <div class="summary-mode-toggle">
                <span>合计模式：</span>
                <el-button 
                  :type="summaryMode === 'all' ? 'primary' : 'default'"
                  size="small"
                  @click="toggleSummaryMode('all')"
                >
                  全部数据
                </el-button>
                <el-button 
                  :type="summaryMode === 'selected' ? 'primary' : 'default'"
                  size="small"
                  @click="toggleSummaryMode('selected')"
                >
                  已选数据
                </el-button>
              </div>
            </div>
          </div>
        </template>
        
        <el-table
          ref="dataTable"
          :data="sortedTableData"
          stripe
          border
          style="width: 100%"
          @sort-change="handleSortChange"
          @selection-change="handleSelectionChange"
          @row-click="handleRowClick"
          :summary-method="getSummaries"
          show-summary
          max-height="500"
          highlight-current-row
        >
          <el-table-column type="selection" width="55" :selectable="selectable" />
          
          <el-table-column prop="subjectName" label="科目名称" min-width="120" />
          <el-table-column prop="relatedUnit" label="往来单位" min-width="150" />
          <el-table-column 
            prop="balance" 
            label="余额(元)" 
            sortable="custom"
            min-width="120"
            :formatter="formatCurrency"
          />
          <el-table-column 
            prop="period0to1" 
            label="0-1年账期金额" 
            sortable="custom"
            min-width="140"
            :formatter="formatCurrency"
          />
          <el-table-column 
            prop="period1to2" 
            label="1-2年账期金额" 
            sortable="custom"
            min-width="140"
            :formatter="formatCurrency"
          />
          <el-table-column 
            prop="periodOver2" 
            label="2年以上账期金额" 
            sortable="custom"
            min-width="150"
            :formatter="formatCurrency"
          />
          <el-table-column prop="details" label="具体情况" min-width="120">
            <template #default="scope">
              <el-button 
                type="text" 
                @click="showDetailDialog(scope.row)"
              >
                查看详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>

    <!-- 第四栏：合计卡片 -->
    <div class="row">
      <div class="summary-cards">
        <el-card class="summary-card">
          <template #header>
            <div class="card-header">
              <span>余额合计</span>
            </div>
          </template>
          <div class="summary-value">{{ formatCurrency({}, {}, totalData.totalBalance) }}</div>
        </el-card>
        
        <el-card class="summary-card">
          <template #header>
            <div class="card-header">
              <span>0-1年账期合计</span>
            </div>
          </template>
          <div class="summary-value">{{ formatCurrency({}, {}, totalData.totalPeriod0to1) }}</div>
        </el-card>
        
        <el-card class="summary-card">
          <template #header>
            <div class="card-header">
              <span>1-2年账期合计</span>
            </div>
          </template>
          <div class="summary-value">{{ formatCurrency({}, {}, totalData.totalPeriod1to2) }}</div>
        </el-card>
        
        <el-card class="summary-card">
          <template #header>
            <div class="card-header">
              <span>2年以上账期合计</span>
            </div>
          </template>
          <div class="summary-value">{{ formatCurrency({}, {}, totalData.totalPeriodOver2) }}</div>
        </el-card>
      </div>
    </div>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="往来款详情"
      width="600px"
    >
      <div class="detail-content">
        <p><strong>科目名称：</strong>{{ currentDetail.subjectName }}</p>
        <p><strong>往来单位：</strong>{{ currentDetail.relatedUnit }}</p>
        <p><strong>余额：</strong>{{ formatCurrency({}, {}, currentDetail.balance) }}</p>
        <p><strong>具体情况：</strong>{{ currentDetail.details }}</p>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import EChart from '@/components/EChart.vue'

// 图表视图类型
const chartViewType = ref('all')

// 表格视图类型
const currentTableView = ref('asset') // asset: 资产, liability: 负债

// 表格相关数据
const tableData = ref([])
const tableFilters = ref({
  keyword: '',
})

// 排序状态
const sortState = ref({
  prop: null,
  order: null
})

// 详情对话框
const detailDialogVisible = ref(false)
const currentDetail = ref({})

// 表格选择相关
const dataTable = ref()
const selectedRows = ref([])
const isAllSelected = ref(true)
const summaryMode = ref('all') // all: 全部数据, selected: 仅已选数据

// 获取图表颜色函数
const getChartColor = (name) => {
  const colorMap = {
    '预收账款': '#409EFF',
    '应付账款': '#67C23A',
    '其他应付账款': '#E6A23C',
    '预付账款': '#F56C6C',
    '其他应收款': '#909399',
    '应收账款': '#9B59B6',
    '应收票据': '#1ABC9C'
  }
  return colorMap[name] || '#409EFF'
}

// 格式化货币
const formatCurrency = (row, column, cellValue) => {
  return '¥' + Number(cellValue).toLocaleString('zh-CN')
}

// 模拟数据 - 负债饼图数据
const liabilityPieData = [
  { value: 4500000, name: '预收账款' },
  { value: 3200000, name: '应付账款' },
  { value: 1800000, name: '其他应付账款' }
]

// 模拟数据 - 资产饼图数据
const assetPieData = [
  { value: 2800000, name: '预付账款' },
  { value: 1500000, name: '其他应收款' },
  { value: 5200000, name: '应收账款' },
  { value: 1200000, name: '应收票据' }
]

// 模拟月度数据
const monthlyData = {
  months: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
  management: {
    liability: [1200000, 1250000, 1180000, 1300000, 1350000, 1400000, 1450000, 1420000, 1380000, 1350000, 1320000, 1280000],
    asset: [1800000, 1850000, 1900000, 1950000, 2000000, 2050000, 2100000, 2150000, 2200000, 2250000, 2300000, 2350000]
  },
  founder: {
    liability: [800000, 820000, 850000, 880000, 900000, 920000, 950000, 980000, 1000000, 1020000, 1050000, 1080000],
    asset: [1500000, 1550000, 1600000, 1650000, 1700000, 1750000, 1800000, 1850000, 1900000, 1950000, 2000000, 2050000]
  }
}

// 负债饼图配置
const liabilityPieOption = ref({
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
      name: '负债构成',
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
      data: liabilityPieData.map(item => ({
        ...item,
        itemStyle: { color: getChartColor(item.name) }
      }))
    }
  ]
})

// 资产饼图配置
const assetPieOption = ref({
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
      name: '资产构成',
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
      data: assetPieData.map(item => ({
        ...item,
        itemStyle: { color: getChartColor(item.name) }
      }))
    }
  ]
})

// 月度柱状图配置
const monthlyBarOption = ref({})

// 更新柱状图
const updateBarChart = () => {
  const series = []
  const legendData = []
  
  if (chartViewType.value === 'management' || chartViewType.value === 'all') {
    series.push({
      name: '管理层-负债',
      type: 'bar',
      data: monthlyData.management.liability,
      itemStyle: { color: '#F56C6C' }
    })
    series.push({
      name: '管理层-资产',
      type: 'bar',
      data: monthlyData.management.asset,
      itemStyle: { color: '#409EFF' }
    })
    legendData.push('管理层-负债', '管理层-资产')
  }
  
  if (chartViewType.value === 'founder' || chartViewType.value === 'all') {
    series.push({
      name: '创始股东-负债',
      type: 'bar',
      data: monthlyData.founder.liability,
      itemStyle: { color: '#E6A23C' }
    })
    series.push({
      name: '创始股东-资产',
      type: 'bar',
      data: monthlyData.founder.asset,
      itemStyle: { color: '#67C23A' }
    })
    legendData.push('创始股东-负债', '创始股东-资产')
  }
  
  monthlyBarOption.value = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        let result = params[0].name + '<br/>'
        params.forEach(item => {
          result += `${item.marker} ${item.seriesName}: ¥${item.value.toLocaleString('zh-CN')}<br/>`
        })
        return result
      }
    },
    legend: {
      data: legendData,
      top: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: monthlyData.months
    },
    yAxis: {
      type: 'value',
      name: '余额(元)',
      axisLabel: {
        formatter: (value) => '¥' + value.toLocaleString('zh-CN')
      }
    },
    series: series
  }
}

// 科目名称定义
const assetSubjects = ['应收账款', '预付账款', '其他应收款']
const liabilitySubjects = ['预收账款', '应付账款', '其他应付款']

// 生成表格数据
const generateTableData = () => {
  const units = ['单位A有限公司', '单位B集团', '单位C股份', '单位D实业', '单位E科技']
  const data = []
  
  // 生成资产数据
  assetSubjects.forEach(subject => {
    for (let i = 0; i < 15; i++) {
      data.push({
        id: data.length + 1,
        subjectName: subject,
        relatedUnit: units[Math.floor(Math.random() * units.length)],
        balance: Math.floor(Math.random() * 10000000) + 500000,
        period0to1: Math.floor(Math.random() * 5000000) + 100000,
        period1to2: Math.floor(Math.random() * 3000000) + 50000,
        periodOver2: Math.floor(Math.random() * 2000000) + 10000,
        details: `这是${subject}的详细往来情况说明`,
        type: 'asset'
      })
    }
  })
  
  // 生成负债数据
  liabilitySubjects.forEach(subject => {
    for (let i = 0; i < 15; i++) {
      data.push({
        id: data.length + 1,
        subjectName: subject,
        relatedUnit: units[Math.floor(Math.random() * units.length)],
        balance: Math.floor(Math.random() * 10000000) + 500000,
        period0to1: Math.floor(Math.random() * 5000000) + 100000,
        period1to2: Math.floor(Math.random() * 3000000) + 50000,
        periodOver2: Math.floor(Math.random() * 2000000) + 10000,
        details: `这是${subject}的详细往来情况说明`,
        type: 'liability'
      })
    }
  })
  
  return data
}

// 切换表格视图
const switchTableView = (viewType) => {
  currentTableView.value = viewType
  // 重置选择状态
  isAllSelected.value = true
  summaryMode.value = 'all'
  nextTick(() => {
    if (dataTable.value) {
      dataTable.value.clearSelection()
      dataTable.value.toggleAllSelection()
    }
  })
}

// 计算当前视图的数据
const currentViewData = computed(() => {
  return tableData.value.filter(item => item.type === currentTableView.value)
})

// 计算合计数据（全部数据）
const totalData = computed(() => {
  const totals = {
    totalBalance: 0,
    totalPeriod0to1: 0,
    totalPeriod1to2: 0,
    totalPeriodOver2: 0
  }
  
  currentViewData.value.forEach(item => {
    totals.totalBalance += item.balance
    totals.totalPeriod0to1 += item.period0to1
    totals.totalPeriod1to2 += item.period1to2
    totals.totalPeriodOver2 += item.periodOver2
  })
  
  return totals
})

// 过滤后的数据
const filteredTableData = computed(() => {
  let data = currentViewData.value
  
  if (tableFilters.value.keyword) {
    const keyword = tableFilters.value.keyword.toLowerCase()
    data = data.filter(item => 
      item.subjectName.toLowerCase().includes(keyword) || 
      item.relatedUnit.toLowerCase().includes(keyword)
    )
  }
  
  return data
})

// 排序后的数据
const sortedTableData = computed(() => {
  let data = [...filteredTableData.value]
  
  if (sortState.value.prop && sortState.value.order) {
    data.sort((a, b) => {
      const aVal = a[sortState.value.prop]
      const bVal = b[sortState.value.prop]
      
      if (sortState.value.order === 'ascending') {
        return aVal - bVal
      } else {
        return bVal - aVal
      }
    })
  }
  
  return data
})

// 表格合计行计算方法
const getSummaries = (param) => {
  const { columns, data } = param
  const sums = []
  
  // 计算当前显示数据的合计
  const currentSummaryData = summaryMode.value === 'all' 
    ? filteredTableData.value 
    : selectedRows.value
  
  const summaryTotals = {
    balance: 0,
    period0to1: 0,
    period1to2: 0,
    periodOver2: 0
  }
  
  currentSummaryData.forEach(item => {
    summaryTotals.balance += item.balance
    summaryTotals.period0to1 += item.period0to1
    summaryTotals.period1to2 += item.period1to2
    summaryTotals.periodOver2 += item.periodOver2
  })
  
  columns.forEach((column, index) => {
    if (index === 0) {
      sums[index] = '合计'
      return
    }
    
    if (index === 1 || index === 6) { // 科目名称、往来单位和具体情况列
      sums[index] = '-'
      return
    }
    
    // 数值列显示合计
    if (column.property === 'balance') {
      sums[index] = '¥' + summaryTotals.balance.toLocaleString('zh-CN')
    } else if (column.property === 'period0to1') {
      sums[index] = '¥' + summaryTotals.period0to1.toLocaleString('zh-CN')
    } else if (column.property === 'period1to2') {
      sums[index] = '¥' + summaryTotals.period1to2.toLocaleString('zh-CN')
    } else if (column.property === 'periodOver2') {
      sums[index] = '¥' + summaryTotals.periodOver2.toLocaleString('zh-CN')
    } else {
      sums[index] = '-'
    }
  })
  
  return sums
}

// 表格选择相关方法
const handleSelectionChange = (selection) => {
  selectedRows.value = selection
  // 更新全选状态
  isAllSelected.value = selection.length === filteredTableData.value.length && filteredTableData.value.length > 0
}

// 行点击事件
const handleRowClick = (row, column, event) => {
  // 如果点击的不是复选框，则切换选中状态
  if (column && column.type !== 'selection') {
    dataTable.value.toggleRowSelection(row)
  }
}

const handleSelectAllChange = (value) => {
  if (dataTable.value) {
    if (value) {
      dataTable.value.toggleAllSelection()
    } else {
      dataTable.value.clearSelection()
    }
  }
}

const selectable = (row, index) => {
  return true // 所有行都可选
}

// 切换合计模式
const toggleSummaryMode = (mode) => {
  summaryMode.value = mode
}

// 表格排序
const handleSortChange = ({ prop, order }) => {
  sortState.value = { prop, order }
}

// 重置筛选
const resetFilters = () => {
  // 清空搜索关键词
  tableFilters.value = {
    keyword: '',
  }
  
  // 清空所有选择的数据
  if (dataTable.value) {
    dataTable.value.clearSelection()
  }
  selectedRows.value = []
  
  // 重置合计模式为全部数据
  summaryMode.value = 'all'
  isAllSelected.value = true
  
  // 重置排序状态
  sortState.value = {
    prop: null,
    order: null
  }
  
  // 重新全选
  nextTick(() => {
    if (dataTable.value) {
      dataTable.value.toggleAllSelection()
    }
  })
}

// 显示详情对话框
const showDetailDialog = (row) => {
  currentDetail.value = row
  detailDialogVisible.value = true
}

// 初始化
onMounted(() => {
  // 模拟数据加载
  tableData.value = generateTableData()
  updateBarChart()
  
  // 默认全选
  nextTick(() => {
    if (dataTable.value) {
      dataTable.value.toggleAllSelection()
    }
  })
})
</script>

<style scoped>
.current-account-detail {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e6e6e6;
}

.page-header h1 {
  color: #303133;
  margin: 0;
  font-size: 24px;
  font-weight: 500;
}

.row {
  margin-bottom: 20px;
}

.chart-section {
  display: flex;
  gap: 20px;
}

.chart-card {
  flex: 1;
}

.full-width-card {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #303133;
  font-size: 16px;
}

:deep(.el-card__header) {
  padding: 12px 20px;
  border-bottom: 1px solid #e6e6e6;
}

.summary-cards {
  display: flex;
  gap: 20px;
}

.summary-card {
  flex: 1;
  text-align: center;
}

.summary-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  padding: 20px 0;
}

.table-controls {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.detail-content p {
  margin: 10px 0;
  line-height: 1.6;
}

.chart-controls {
  margin-left: 20px;
}

/* 合计模式切换按钮样式 */
.summary-mode-toggle {
  display: flex;
  align-items: center;
  margin-left: auto;
  gap: 8px;
}

.summary-mode-toggle span {
  font-size: 14px;
  color: #606266;
}

/* 表格样式优化 */
:deep(.el-table) {
  cursor: pointer;
}

:deep(.el-table__footer) .el-table__cell {
  background-color: #f5f7fa !important;
  font-weight: bold;
}

:deep(.el-table__footer) .el-table__cell .cell {
  color: #409eff !important;
  font-size: 14px;
}

/* 表格滚动区域样式 */
:deep(.el-table__body-wrapper) {
  overflow-y: auto;
}

/* 行悬停效果 */
:deep(.el-table--enable-row-hover .el-table__body tr:hover>td) {
  background-color: #f0f7ff !important;
}

/* 选中行样式 */
:deep(.el-table__body tr.current-row>td) {
  background-color: #f0f7ff !important;
}
</style>