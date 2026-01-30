<template>
  <div class="management-finance">
    <h1>期间费用表</h1>
    
    <!-- 竖向三栏布局 -->
    <div class="vertical-layout">
      <!-- 第一栏：部门月度期间费用柱状图 -->
      <div class="vertical-column">
        <div class="section-header">
          <h3>部门月度期间费用</h3>
          <div class="header-controls">
            <span class="current-department">当前部门：{{ selectedDepartment }}</span>
            <el-select v-model="selectedDepartment" placeholder="请选择部门" @change="handleDepartmentChange">
              <el-option
                v-for="dept in departmentOptions"
                :key="dept"
                :label="dept"
                :value="dept"
              />
            </el-select>
          </div>
        </div>
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <EChart :option="departmentCostOption" height="400px" />
          </el-card>
        </div>
      </div>
      
      <!-- 第二栏：费用占比饼图 -->
      <div class="vertical-column">
        <div class="section-header">
          <h3>部门费用占比分析</h3>
          <div class="header-controls">
            <span class="current-department">当前部门：{{ selectedDepartment }}</span>
          </div>
        </div>
        <div class="horizontal-card-layout">
          <el-card class="finance-card">
            <EChart :option="costRatioOption" height="400px" />
          </el-card>
        </div>
      </div>
      
      <!-- 第三栏：明细表格 -->
      <div class="vertical-column">
        <div class="section-header">
          <h3>费用明细</h3>
          <div class="table-header-controls">
            <!-- 合计模式切换 -->
            <div class="summary-mode-toggle">
              <span>合计模式：</span>
              <el-button 
                :type="summaryMode === 'all' ? 'primary' : 'default'"
                size="small"
                @click="toggleSummaryMode('all')"
              >
                全部合计
              </el-button>
              <el-button 
                :type="summaryMode === 'selected' ? 'primary' : 'default'"
                size="small"
                @click="toggleSummaryMode('selected')"
              >
                已选合计
              </el-button>
            </div>
            
            <!-- 重置按钮 -->
            <el-button @click="handleReset">重置</el-button>
          </div>
        </div>
        
        <div class="table-container">
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
            :row-class-name="getRowClassName"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="project" label="项目" min-width="120" />
            <el-table-column prop="department" label="部门" min-width="140" />
            <el-table-column 
              prop="month" 
              label="月份" 
              min-width="120"
            >
              <template #default="{ row }">
                {{ row.month }}月
              </template>
              <template #header>
                <div class="month-column-header" ref="monthHeader">
                  <span>月份</span>
                  <el-button 
                    type="text" 
                    size="small" 
                    @click.stop="toggleMonthFilter"
                    class="month-filter-button"
                    :class="{ active: showMonthFilter }"
                  >
                    <el-icon><Filter /></el-icon>
                  </el-button>
                </div>
              </template>
            </el-table-column>
            <el-table-column 
              prop="amount" 
              label="金额（元）" 
              sortable="custom"
              min-width="120"
              :formatter="formatCurrency"
            />
          </el-table>
          
          <!-- 月份筛选面板 -->
          <div 
            v-if="showMonthFilter" 
            class="month-filter-panel"
            :style="filterPanelStyle"
          >
            <div class="filter-header">
              <span>筛选月份</span>
              <div>
                <el-button type="text" size="small" @click="selectAllMonths">全选</el-button>
                <el-button type="text" size="small" @click="clearMonthFilter">清空</el-button>
                <el-button type="text" size="small" @click="applyMonthFilter">确定</el-button>
              </div>
            </div>
            <div class="month-checkboxes">
              <el-checkbox-group v-model="selectedMonths">
                <div v-for="month in monthOptions" :key="month.value" class="month-checkbox-item">
                  <el-checkbox :label="month.value">{{ month.label }}</el-checkbox>
                </div>
              </el-checkbox-group>
            </div>
          </div>
        </div>
        
        <!-- 合计金额显示 -->
        <div class="total-amount-display">
          <span>合计金额：{{ formatCurrency({}, {}, totalAmount) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { Filter } from '@element-plus/icons-vue';
import EChart from '@/components/EChart.vue';

// 部门选项
const departmentOptions = [
  '市场部',
  '工程一部',
  '工程二部',
  '技术与合作发展部',
  '信息智能部',
  '财务部',
  '人事行政部'
];

// 月份选项
const monthOptions = Array.from({ length: 12 }, (_, i) => ({
  value: i + 1,
  label: `${i + 1}月`
}));

// 选中的部门和月份
const selectedDepartment = ref('市场部');
const selectedMonths = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);

// 控制月份筛选面板显示
const showMonthFilter = ref(false);
const monthHeader = ref(null);

// 表格相关数据
const tableData = ref([]);
const selectedRows = ref([]);
const sortState = ref({
  prop: null,
  order: null
});
const summaryMode = ref('all'); // all: 全部合计, selected: 已选合计
const dataTable = ref();

// 计算筛选面板的位置
const filterPanelStyle = computed(() => {
  if (!monthHeader.value) return {};
  
  const rect = monthHeader.value.getBoundingClientRect();
  const tableRect = document.querySelector('.table-container').getBoundingClientRect();
  
  return {
    top: `${rect.bottom - tableRect.top}px`,
    left: `${rect.left - tableRect.left}px`,
    width: `${rect.width}px`
  };
});

// 格式化货币
const formatCurrency = (row, column, cellValue) => {
  if (cellValue === undefined || cellValue === null) return '-';
  return '¥' + Number(cellValue).toLocaleString('zh-CN');
};

// 切换月份筛选面板
const toggleMonthFilter = () => {
  showMonthFilter.value = !showMonthFilter.value;
};

// 全选月份
const selectAllMonths = () => {
  selectedMonths.value = monthOptions.map(month => month.value);
};

// 清空月份筛选
const clearMonthFilter = () => {
  selectedMonths.value = [];
};

// 应用月份筛选
const applyMonthFilter = () => {
  showMonthFilter.value = false;
};

// 模拟数据生成
const generateMockData = () => {
  const data = [];
  const costTypes = ['研发费用', '管理费用', '销售费用', '财务费用'];
  
  departmentOptions.forEach(department => {
    for (let month = 1; month <= 12; month++) {
      costTypes.forEach(costType => {
        // 生成模拟数据，不同部门、月份有不同基数
        const baseAmount = {
          '市场部': 50000,
          '工程一部': 80000,
          '工程二部': 75000,
          '技术与合作发展部': 60000,
          '信息智能部': 45000,
          '财务部': 30000,
          '人事行政部': 35000
        }[department];
        
        const variation = {
          '研发费用': 1.2,
          '管理费用': 1.0,
          '销售费用': 1.5,
          '财务费用': 0.8
        }[costType];
        
        const monthFactor = 1 + (month - 1) * 0.05; // 每月递增5%
        const randomFactor = 0.8 + Math.random() * 0.4; // 0.8-1.2的随机因子
        
        const amount = Math.round(baseAmount * variation * monthFactor * randomFactor);
        
        data.push({
          id: `${department}-${month}-${costType}`,
          project: costType,
          department: department,
          month: month,
          amount: amount
        });
      });
    }
  });
  
  return data;
};

// 获取部门月度费用数据
const getDepartmentMonthlyCosts = (department) => {
  const deptData = tableData.value.filter(item => item.department === department);
  const monthlyCosts = {
    research: Array(12).fill(0),
    management: Array(12).fill(0),
    sales: Array(12).fill(0),
    finance: Array(12).fill(0),
    total: Array(12).fill(0)
  };
  
  deptData.forEach(item => {
    const monthIndex = item.month - 1;
    const amount = item.amount;
    
    switch(item.project) {
      case '研发费用':
        monthlyCosts.research[monthIndex] += amount;
        break;
      case '管理费用':
        monthlyCosts.management[monthIndex] += amount;
        break;
      case '销售费用':
        monthlyCosts.sales[monthIndex] += amount;
        break;
      case '财务费用':
        monthlyCosts.finance[monthIndex] += amount;
        break;
    }
    monthlyCosts.total[monthIndex] += amount;
  });
  
  return monthlyCosts;
};

// 获取部门费用累计值
const getDepartmentCostTotals = (department) => {
  const deptData = tableData.value.filter(item => item.department === department);
  const totals = {
    research: 0,
    management: 0,
    sales: 0,
    finance: 0,
    total: 0
  };
  
  deptData.forEach(item => {
    const amount = item.amount;
    switch(item.project) {
      case '研发费用':
        totals.research += amount;
        break;
      case '管理费用':
        totals.management += amount;
        break;
      case '销售费用':
        totals.sales += amount;
        break;
      case '财务费用':
        totals.finance += amount;
        break;
    }
    totals.total += amount;
  });
  
  return totals;
};

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
    top: '15%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  },
  yAxis: {
    type: 'value',
    axisLabel: { 
      formatter: (value) => '¥' + value.toLocaleString('zh-CN')
    }
  }
};

// 部门费用柱状图配置
const departmentCostOption = ref({
  ...baseChartConfig,
  legend: {
    data: ['研发费用', '管理费用', '销售费用', '财务费用', '合计'],
    top: 10,
    right: 30
  },
  series: []
});

// 费用占比饼图配置
const costRatioOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c}元 ({d}%)'
  },
  legend: {
    orient: 'vertical',
    right: 10,
    top: 'center'
  },
  series: [{
    name: '费用占比',
    type: 'pie',
    radius: ['40%', '70%'],
    center: ['40%', '50%'],
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
    data: []
  }]
});

// 表格数据计算属性
const filteredTableData = computed(() => {
  return tableData.value.filter(item => 
    item.department === selectedDepartment.value && 
    selectedMonths.value.includes(item.month)
  );
});

// 排序后的数据
const sortedTableData = computed(() => {
  let data = [...filteredTableData.value];
  
  if (sortState.value.prop && sortState.value.order) {
    data.sort((a, b) => {
      const aVal = a[sortState.value.prop];
      const bVal = b[sortState.value.prop];
      
      if (sortState.value.order === 'ascending') {
        return aVal - bVal;
      } else {
        return bVal - aVal;
      }
    });
  }
  
  return data;
});

// 合计金额计算
const totalAmount = computed(() => {
  const currentSummaryData = summaryMode.value === 'all' 
    ? filteredTableData.value 
    : selectedRows.value;
  
  return currentSummaryData.reduce((sum, item) => sum + item.amount, 0);
});

// 表格合计行计算方法
const getSummaries = (param) => {
  const { columns, data } = param;
  const sums = [];
  
  // 计算当前显示数据的合计
  const currentSummaryData = summaryMode.value === 'all' 
    ? filteredTableData.value 
    : selectedRows.value;
  
  const summaryTotal = currentSummaryData.reduce((sum, item) => sum + item.amount, 0);
  
  columns.forEach((column, index) => {
    if (index === 0) {
      sums[index] = '合计';
      return;
    }
    
    if (index === 1 || index === 2 || index === 3) { // 项目、部门、月份列
      sums[index] = '-';
      return;
    }
    
    // 金额列显示合计
    if (column.property === 'amount') {
      sums[index] = '¥' + summaryTotal.toLocaleString('zh-CN');
    } else {
      sums[index] = '-';
    }
  });
  
  return sums;
};

// 行类名函数，用于控制行选择样式
const getRowClassName = ({ row, rowIndex }) => {
  const isSelected = selectedRows.value.some(selectedRow => selectedRow.id === row.id);
  return isSelected ? 'selected-row' : '';
};

/**
 * 处理部门切换
 */
const handleDepartmentChange = () => {
  updateCharts();
  // 重置选择状态
  nextTick(() => {
    if (dataTable.value) {
      dataTable.value.clearSelection();
    }
  });
};

/**
 * 处理表格排序变化
 */
const handleSortChange = ({ prop, order }) => {
  sortState.value = { prop, order };
};

/**
 * 处理重置
 */
const handleReset = () => {
  // 重置月份筛选
  selectedMonths.value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  showMonthFilter.value = false;
  
  // 重置排序状态
  sortState.value = {
    prop: null,
    order: null
  };
  
  // 清空选择
  selectedRows.value = [];
  
  // 重置合计模式
  summaryMode.value = 'all';
  
  // 重新全选
  nextTick(() => {
    if (dataTable.value) {
      dataTable.value.clearSelection();
    }
  });
};

/**
 * 处理行选择变化
 */
const handleSelectionChange = (selection) => {
  selectedRows.value = selection;
};

// 行点击事件
const handleRowClick = (row, column, event) => {
  // 如果点击的不是复选框，则切换选中状态
  if (column && column.type !== 'selection') {
    dataTable.value.toggleRowSelection(row);
  }
};

// 切换合计模式
const toggleSummaryMode = (mode) => {
  summaryMode.value = mode;
};

/**
 * 更新图表数据
 */
const updateCharts = () => {
  const monthlyCosts = getDepartmentMonthlyCosts(selectedDepartment.value);
  const costTotals = getDepartmentCostTotals(selectedDepartment.value);
  
  // 更新柱状图
  departmentCostOption.value = {
    ...departmentCostOption.value,
    series: [
      {
        name: '研发费用',
        type: 'bar',
        data: monthlyCosts.research,
        itemStyle: { color: '#5470c6' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => {
            return (params.value / 10000).toFixed(1) + '万';
          }
        }
      },
      {
        name: '管理费用',
        type: 'bar',
        data: monthlyCosts.management,
        itemStyle: { color: '#91cc75' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => {
            return (params.value / 10000).toFixed(1) + '万';
          }
        }
      },
      {
        name: '销售费用',
        type: 'bar',
        data: monthlyCosts.sales,
        itemStyle: { color: '#fac858' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => {
            return (params.value / 10000).toFixed(1) + '万';
          }
        }
      },
      {
        name: '财务费用',
        type: 'bar',
        data: monthlyCosts.finance,
        itemStyle: { color: '#ee6666' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => {
            return (params.value / 10000).toFixed(1) + '万';
          }
        }
      },
      {
        name: '合计',
        type: 'bar',
        data: monthlyCosts.total,
        itemStyle: { color: '#73c0de' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => {
            return (params.value / 10000).toFixed(1) + '万';
          }
        }
      }
    ]
  };
  
  // 更新饼图
  costRatioOption.value = {
    ...costRatioOption.value,
    series: [{
      ...costRatioOption.value.series[0],
      data: [
        { value: costTotals.research, name: '研发费用' },
        { value: costTotals.management, name: '管理费用' },
        { value: costTotals.sales, name: '销售费用' },
        { value: costTotals.finance, name: '财务费用' }
      ]
    }]
  };
};

/**
 * 从API获取数据（预留接口）
 */
const fetchCostData = async () => {
  // 实际开发中替换为真实的API调用
  try {
    // const response = await axios.get('/api/department-costs');
    // tableData.value = response.data;
    console.log('API接口预留，当前使用模拟数据');
  } catch (error) {
    console.error('获取数据失败:', error);
  }
};

// 页面加载时初始化
onMounted(() => {
  // 生成模拟数据
  tableData.value = generateMockData();
  // 也可以调用API：fetchCostData()
  
  // 初始化图表
  updateCharts();
  
  // 默认全选
  nextTick(() => {
    if (dataTable.value) {
      dataTable.value.clearSelection();
    }
  });
});
</script>

<style scoped>
.management-finance {
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

.management-finance h1 {
  color: #303133;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 500;
  text-align: center;
  padding-bottom: 15px;
  border-bottom: 1px solid #e6e6e6;
}

/* 竖向布局样式 */
.vertical-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.vertical-column {
  border: 1px solid #e6e6e6;
  border-radius: 4px;
  padding: 20px;
  background-color: #fff;
}

/* 栏目头部样式 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 {
  color: #303133;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

/* 头部控制区域样式 */
.header-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.current-department {
  font-weight: 600;
  color: #409EFF;
  white-space: nowrap;
}

/* 表格头部控制区域样式 */
.table-header-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

/* 合计模式切换按钮样式 */
.summary-mode-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-mode-toggle span {
  font-size: 14px;
  color: #606266;
  white-space: nowrap;
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

/* 表格容器 */
.table-container {
  margin-bottom: 15px;
  position: relative;
}

/* 月份列头部样式 */
.month-column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.month-filter-button {
  padding: 4px;
  margin-left: 8px;
  transition: all 0.3s;
}

.month-filter-button.active {
  color: #409EFF;
  background-color: #ecf5ff;
}

/* 月份筛选面板样式 */
.month-filter-panel {
  position: absolute;
  background: #fff;
  border: 1px solid #e6e6e6;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 1000;
  padding: 15px;
  max-height: 300px;
  overflow-y: auto;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid #e6e6e6;
}

.filter-header span {
  font-weight: 600;
  color: #303133;
}

.month-checkboxes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.month-checkbox-item {
  margin-bottom: 5px;
}

/* 合计金额显示 */
.total-amount-display {
  text-align: right;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-weight: 600;
  color: #303133;
  border: 1px solid #e6e6e6;
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

/* 行悬停效果 */
:deep(.el-table--enable-row-hover .el-table__body tr:hover>td) {
  background-color: #f0f7ff !important;
}

/* 选中行样式 */
:deep(.el-table__body tr.current-row>td) {
  background-color: #f0f7ff !important;
}

/* 被选中行的自定义样式 */
:deep(.selected-row) {
  background-color: #f0f9ff !important;
}

:deep(.selected-row:hover>td) {
  background-color: #e6f7ff !important;
}

/* 卡片样式 */
:deep(.el-card) {
  border-radius: 4px;
  border: 1px solid #e6e6e6;
}

:deep(.el-card__header) {
  padding: 12px 20px;
  border-bottom: 1px solid #e6e6e6;
  background-color: #f5f7fa;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .horizontal-card-layout {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .header-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .table-header-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .summary-mode-toggle {
    margin-left: 0;
  }
  
  .month-checkboxes {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .month-filter-panel {
    right: 10px;
    left: 10px;
    width: auto;
  }
}
</style>