<template>
  <div class="laboratory-income-page">
    <h1>实验室收入</h1>
    
    <!-- 珠海实验室收入 -->
    <div class="section">
      <h2 class="section-title">珠海实验室收入</h2>
      <div class="section-content">
        <!-- 图表行 -->
        <div class="row">
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">柱状统计表</span>
                  <div class="chart-controls">
                    <span class="current-business-label">当前业务：{{ selectedBusinessTypeZhuhai }}</span>
                    <el-select v-model="selectedBusinessTypeZhuhai" placeholder="选择业务类型" size="small">
                      <el-option label="FA" value="FA"></el-option>
                      <el-option label="ESD" value="ESD"></el-option>
                      <el-option label="FIB+TEM" value="FIB+TEM"></el-option>
                      <el-option label="SIMS" value="SIMS"></el-option>
                      <el-option label="化学实验" value="化学实验"></el-option>
                      <el-option label="其他" value="其他"></el-option>
                    </el-select>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="zhuhaiBarOption" height="300px" />
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">比例图</span>
                  <div class="chart-controls">
                    <span class="current-business-label">当前业务：{{ selectedBusinessTypeZhuhai }}</span>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="zhuhaiPieOption" height="300px" />
              </div>
            </el-card>
          </div>
        </div>
        
        <!-- 数据汇总行 -->
        <div class="row">
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">小计</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(zhuhaiCurrentBusinessTotal) }}</div>
                <div class="data-desc">{{ selectedBusinessTypeZhuhai }}业务总收入</div>
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">实验室小计与占比</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(zhuhaiAllBusinessesTotal) }}</div>
                <div class="data-desc">所有业务总收入</div>
                <div class="data-sub-value">{{ formatPercentage(zhuhaiCurrentBusinessPercentage) }}</div>
                <div class="data-sub-desc">{{ selectedBusinessTypeZhuhai }}业务占比</div>
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">实验室毛利额与毛利率</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(zhuhaiLabGrossProfit) }} ({{ formatPercentage(zhuhaiLabGrossMargin) }})</div>
                <div class="data-desc">实验室总毛利额与毛利率</div>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>

    <!-- 上海+武汉实验室收入 -->
    <div class="section">
      <h2 class="section-title">上海+武汉实验室收入</h2>
      <div class="section-content">
        <!-- 图表行 -->
        <div class="row">
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">柱状统计表</span>
                  <div class="chart-controls">
                    <span class="current-business-label">当前业务</span>
                    <el-select v-model="selectedBusinessTypeShanghai" placeholder="选择业务类型" size="small" style="width: 120px">
                      <el-option label="FA" value="FA"></el-option>
                      <el-option label="ESD" value="ESD"></el-option>
                      <el-option label="FIB+TEM" value="FIB+TEM"></el-option>
                      <el-option label="SIMS" value="SIMS"></el-option>
                      <el-option label="化学实验" value="化学实验"></el-option>
                      <el-option label="其他" value="其他"></el-option>
                    </el-select>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="shanghaiBarOption" height="300px" />
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">比例图</span>
                  <div class="chart-controls">
                    <span class="current-business-label">当前业务：{{ selectedBusinessTypeShanghai }}</span>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="shanghaiPieOption" height="300px" />
              </div>
            </el-card>
          </div>
        </div>
        
        <!-- 数据汇总行 -->
        <div class="row">
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">小计</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(shanghaiCurrentBusinessTotal) }}</div>
                <div class="data-desc">{{ selectedBusinessTypeShanghai }}业务总收入</div>
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">实验室小计与占比</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(shanghaiAllBusinessesTotal) }}</div>
                <div class="data-desc">所有业务总收入</div>
                <div class="data-sub-value">{{ formatPercentage(shanghaiCurrentBusinessPercentage) }}</div>
                <div class="data-sub-desc">{{ selectedBusinessTypeShanghai }}业务占比</div>
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">实验室毛利额与毛利率</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(shanghaiLabGrossProfit) }} ({{ formatPercentage(shanghaiLabGrossMargin) }})</div>
                <div class="data-desc">实验室总毛利额与毛利率</div>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>

    <!-- 苏州实验室收入 -->
    <div class="section">
      <h2 class="section-title">苏州实验室收入</h2>
      <div class="section-content">
        <!-- 图表行 -->
        <div class="row">
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">柱状统计表</span>
                  <div class="chart-controls">
                    <span class="current-business-label">当前业务</span>
                    <el-select v-model="selectedBusinessTypeSuzhou" placeholder="选择业务类型" size="small" style="width: 120px">
                      <el-option label="FA" value="FA"></el-option>
                      <el-option label="ESD" value="ESD"></el-option>
                      <el-option label="FIB+TEM" value="FIB+TEM"></el-option>
                      <el-option label="SIMS" value="SIMS"></el-option>
                      <el-option label="化学实验" value="化学实验"></el-option>
                      <el-option label="其他" value="其他"></el-option>
                    </el-select>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="suzhouBarOption" height="300px" />
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">比例图</span>
                  <div class="chart-controls">
                    <span class="current-business-label">当前业务：{{ selectedBusinessTypeSuzhou }}</span>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="suzhouPieOption" height="300px" />
              </div>
            </el-card>
          </div>
        </div>
        
        <!-- 数据汇总行 -->
        <div class="row">
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">小计</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(suzhouCurrentBusinessTotal) }}</div>
                <div class="data-desc">{{ selectedBusinessTypeSuzhou }}业务总收入</div>
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">实验室小计与占比</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(suzhouAllBusinessesTotal) }}</div>
                <div class="data-desc">所有业务总收入</div>
                <div class="data-sub-value">{{ formatPercentage(suzhouCurrentBusinessPercentage) }}</div>
                <div class="data-sub-desc">{{ selectedBusinessTypeSuzhou }}业务占比</div>
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">实验室毛利额与毛利率</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(suzhouLabGrossProfit) }} ({{ formatPercentage(suzhouLabGrossMargin) }})</div>
                <div class="data-desc">实验室总毛利额与毛利率</div>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>

    <!-- 业务汇总 -->
    <div class="section">
      <h2 class="section-title">业务汇总</h2>
      <div class="section-content">
        <!-- 第一行：图表 -->
        <div class="row">
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">柱状统计表</span>
                  <div class="chart-controls">
                    <span class="current-business-label">当前业务：{{ selectedBusinessTypeSummary }}</span>
                    <el-select v-model="selectedBusinessTypeSummary" placeholder="选择业务类型" size="small">
                      <el-option label="FA" value="FA"></el-option>
                      <el-option label="ESD" value="ESD"></el-option>
                      <el-option label="FIB+TEM" value="FIB+TEM"></el-option>
                      <el-option label="SIMS" value="SIMS"></el-option>
                      <el-option label="化学实验" value="化学实验"></el-option>
                      <el-option label="其他" value="其他"></el-option>
                    </el-select>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="summaryBarOption" height="300px" />
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">比例图</span>
                  <div class="chart-controls">
                    <span class="current-business-label">当前业务：{{ selectedBusinessTypeSummary }}</span>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="summaryPieOption" height="300px" />
              </div>
            </el-card>
          </div>
        </div>
        
        <!-- 第二行：数据卡片 -->
        <div class="row">
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">该业务收入合计</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(summaryCurrentBusinessTotal) }}</div>
                <div class="data-desc">{{ selectedBusinessTypeSummary }}业务总收入</div>
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">业务毛利额</span>
                </div>
              </template>
              <div class="data-content">
                <div class="profit-detail">
                  <div class="profit-line">
                    <span class="profit-label">自持:</span>
                    <span class="profit-value">{{ formatCurrency(summaryOwnedGrossProfit) }}</span>
                  </div>
                  <div class="profit-line">
                    <span class="profit-label">委外:</span>
                    <span class="profit-value">{{ formatCurrency(summaryOutsourcedGrossProfit) }}</span>
                  </div>
                </div>
                <div class="profit-total">
                  <span class="total-label">合计:</span>
                  <span class="total-value">{{ formatCurrency(summaryGrossProfit) }}</span>
                </div>
                <div class="data-desc">{{ selectedBusinessTypeSummary }}业务毛利额</div>
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">该业务毛利率</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatPercentage(summaryGrossMargin) }}</div>
                <div class="data-desc">{{ selectedBusinessTypeSummary }}业务毛利率</div>
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="data-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">实验室收入总计</span>
                </div>
              </template>
              <div class="data-content">
                <div class="data-value">{{ formatCurrency(summaryAllLabsTotal) }}</div>
                <div class="data-desc">所有实验室收入总计</div>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>

    <!-- 时间维度分析 -->
<div class="section">
      <h2 class="section-title">时间维度分析</h2>
      <div class="section-content">
        <!-- 第一行：实验室维度分析 -->
        <div class="row">
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">实验室收入（月度）</span>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="labMonthlyBarOption" height="300px" />
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">实验室收入（当年累计）</span>
                  <div class="chart-controls">
                    <el-button 
                      size="small" 
                      :type="labViewMode === 'pie' ? 'primary' : ''"
                      @click="labViewMode = 'pie'"
                    >
                      饼图
                    </el-button>
                    <el-button 
                      size="small" 
                      :type="labViewMode === 'table' ? 'primary' : ''"
                      @click="labViewMode = 'table'"
                    >
                      毛利率表
                    </el-button>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart v-if="labViewMode === 'pie'" :option="labPieOption" height="300px" />
                <div v-else class="gross-margin-table">
                  <el-table :data="labGrossMarginData" size="small" stripe>
                    <el-table-column prop="lab" label="实验室" width="120" />
                    <el-table-column prop="grossMargin" label="毛利率" align="right">
                      <template #default="scope">
                        {{ formatPercentage(scope.row.grossMargin) }}
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </el-card>
          </div>
        </div>
        
        <!-- 第二行：业务维度分析 -->
        <div class="row">
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">业务收入（月度）</span>
                </div>
              </template>
              <div class="chart-content">
                <EChart :option="businessMonthlyBarOption" height="300px" />
              </div>
            </el-card>
          </div>
          <div class="col">
            <el-card class="chart-card">
              <template #header>
                <div class="card-header">
                  <span class="card-title">业务收入（当年累计）</span>
                  <div class="chart-controls">
                    <el-button 
                      size="small" 
                      :type="businessViewMode === 'pie' ? 'primary' : ''"
                      @click="businessViewMode = 'pie'"
                    >
                      饼图
                    </el-button>
                    <el-button 
                      size="small" 
                      :type="businessViewMode === 'table' ? 'primary' : ''"
                      @click="businessViewMode = 'table'"
                    >
                      毛利率表
                    </el-button>
                  </div>
                </div>
              </template>
              <div class="chart-content">
                <EChart v-if="businessViewMode === 'pie'" :option="businessPieOption" height="300px" />
                <div v-else class="gross-margin-table">
                  <el-table :data="businessGrossMarginData" size="small" stripe>
                    <el-table-column prop="business" label="业务类型" width="120" />
                    <el-table-column prop="grossMargin" label="毛利率" align="right">
                      <template #default="scope">
                        {{ formatPercentage(scope.row.grossMargin) }}
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import EChart from '@/components/EChart.vue'

// 格式化工具函数
const formatNumber = (value) => value.toLocaleString('zh-CN')
const formatCurrency = (value) => '¥ ' + value.toLocaleString('zh-CN')
const formatPercentage = (value) => (value * 100).toFixed(2) + '%'

// 视图模式控制
const labViewMode = ref('pie') // 'pie' 或 'table'
const businessViewMode = ref('pie') // 'pie' 或 'table'

// 实验室毛利率数据
const labGrossMarginData = [
  { lab: '珠海实验室', grossMargin: 0.339 },
  { lab: '上海+武汉实验室', grossMargin: 0.325 },
  { lab: '苏州实验室', grossMargin: 0.315 }
]

// 业务毛利率数据
const businessGrossMarginData = [
  { business: 'FA', grossMargin: 0.35 },
  { business: 'ESD', grossMargin: 0.32 },
  { business: 'FIB+TEM', grossMargin: 0.38 },
  { business: 'SIMS', grossMargin: 0.33 },
  { business: '化学实验', grossMargin: 0.30 },
  { business: '其他', grossMargin: 0.28 }
]

// 实验室月度收入数据（模拟数据）
const labMonthlyData = {
  zhuhai: [850000, 690000, 950000, 780000, 890000, 1000000, 920000, 980000, 1050000, 1100000, 1150000, 1200000],
  shanghaiWuhan: [680000, 550000, 750000, 620000, 710000, 800000, 740000, 780000, 820000, 860000, 900000, 940000],
  suzhou: [520000, 420000, 580000, 480000, 540000, 610000, 560000, 590000, 620000, 650000, 680000, 710000]
}

// 计算实验室月度总计
const labMonthlyTotal = computed(() => {
  return labMonthlyData.zhuhai.map((val, index) => 
    val + labMonthlyData.shanghaiWuhan[index] + labMonthlyData.suzhou[index]
  )
})

// 业务月度收入数据（模拟数据）
const businessMonthlyData = {
  FA: [420000, 340000, 470000, 380000, 440000, 500000, 460000, 490000, 520000, 540000, 570000, 600000],
  ESD: [280000, 230000, 310000, 250000, 290000, 330000, 300000, 320000, 340000, 360000, 380000, 400000],
  'FIB+TEM': [350000, 280000, 390000, 320000, 370000, 420000, 390000, 410000, 440000, 460000, 490000, 520000],
  SIMS: [180000, 150000, 200000, 170000, 190000, 220000, 200000, 210000, 220000, 230000, 240000, 250000],
  化学实验: [150000, 120000, 170000, 140000, 160000, 180000, 170000, 180000, 190000, 200000, 210000, 220000],
  其他: [90000, 70000, 100000, 80000, 95000, 110000, 100000, 110000, 115000, 120000, 125000, 130000]
}

// 计算业务月度合计
const businessMonthlyTotal = computed(() => {
  const businessTypes = ['FA', 'ESD', 'FIB+TEM', 'SIMS', '化学实验', '其他']
  return businessMonthlyData.FA.map((_, index) => 
    businessTypes.reduce((sum, type) => sum + businessMonthlyData[type][index], 0)
  )
})

// 实验室年度总收入
const labYearlyTotal = {
  zhuhai: labMonthlyData.zhuhai.reduce((sum, val) => sum + val, 0),
  shanghaiWuhan: labMonthlyData.shanghaiWuhan.reduce((sum, val) => sum + val, 0),
  suzhou: labMonthlyData.suzhou.reduce((sum, val) => sum + val, 0)
}

// 业务年度总收入
const businessYearlyTotal = {
  FA: businessMonthlyData.FA.reduce((sum, val) => sum + val, 0),
  ESD: businessMonthlyData.ESD.reduce((sum, val) => sum + val, 0),
  'FIB+TEM': businessMonthlyData['FIB+TEM'].reduce((sum, val) => sum + val, 0),
  SIMS: businessMonthlyData.SIMS.reduce((sum, val) => sum + val, 0),
  化学实验: businessMonthlyData.化学实验.reduce((sum, val) => sum + val, 0),
  其他: businessMonthlyData.其他.reduce((sum, val) => sum + val, 0)
}

// 实验室月度柱状图配置
const labMonthlyBarOption = computed(() => {
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        let result = params[0].name + '<br/>'
        params.forEach(item => {
          result += `${item.marker} ${item.seriesName}: ${formatCurrency(item.value)}<br/>`
        })
        return result
      }
    },
    legend: {
      data: ['珠海实验室', '上海+武汉实验室', '苏州实验室', '总计'],
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
      data: months
    },
    yAxis: {
      type: 'value',
      name: '元',
      axisLabel: { 
        formatter: (value) => formatNumber(value)
      }
    },
    series: [
      {
        name: '珠海实验室',
        type: 'bar',
        data: labMonthlyData.zhuhai,
        itemStyle: { color: '#409EFF' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      },
      {
        name: '上海+武汉实验室',
        type: 'bar',
        data: labMonthlyData.shanghaiWuhan,
        itemStyle: { color: '#67C23A' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      },
      {
        name: '苏州实验室',
        type: 'bar',
        data: labMonthlyData.suzhou,
        itemStyle: { color: '#E6A23C' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      },
      {
        name: '总计',
        type: 'bar',
        data: labMonthlyTotal.value,
        itemStyle: { color: '#F56C6C' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      }
    ]
  }
})

// 业务月度柱状图配置
const businessMonthlyBarOption = computed(() => {
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        let result = params[0].name + '<br/>'
        params.forEach(item => {
          result += `${item.marker} ${item.seriesName}: ${formatCurrency(item.value)}<br/>`
        })
        return result
      }
    },
    legend: {
      data: ['FA', 'ESD', 'FIB+TEM', 'SIMS', '化学实验', '其他', '合计'],
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
      data: months
    },
    yAxis: {
      type: 'value',
      name: '元',
      axisLabel: { 
        formatter: (value) => formatNumber(value)
      }
    },
    series: [
      {
        name: 'FA',
        type: 'bar',
        data: businessMonthlyData.FA,
        itemStyle: { color: '#409EFF' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      },
      {
        name: 'ESD',
        type: 'bar',
        data: businessMonthlyData.ESD,
        itemStyle: { color: '#67C23A' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      },
      {
        name: 'FIB+TEM',
        type: 'bar',
        data: businessMonthlyData['FIB+TEM'],
        itemStyle: { color: '#E6A23C' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      },
      {
        name: 'SIMS',
        type: 'bar',
        data: businessMonthlyData.SIMS,
        itemStyle: { color: '#F56C6C' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      },
      {
        name: '化学实验',
        type: 'bar',
        data: businessMonthlyData.化学实验,
        itemStyle: { color: '#909399' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      },
      {
        name: '其他',
        type: 'bar',
        data: businessMonthlyData.其他,
        itemStyle: { color: '#C0C4CC' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      },
      {
        name: '合计',
        type: 'bar',
        data: businessMonthlyTotal.value,
        itemStyle: { color: '#8B008B' },
        label: {
          show: true,
          position: 'top',
          formatter: (params) => formatNumber(params.value),
          fontSize: 10,
          fontWeight: 'bold'
        }
      }
    ]
  }
})

// 实验室饼图配置
const labPieOption = computed(() => {
  const total = labYearlyTotal.zhuhai + labYearlyTotal.shanghaiWuhan + labYearlyTotal.suzhou
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const percent = ((params.value / total) * 100).toFixed(2)
        return `${params.marker} ${params.name}: ${formatCurrency(params.value)} (${percent}%)`
      }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: ['珠海实验室', '上海+武汉实验室', '苏州实验室']
    },
    series: [
      {
        name: '实验室收入',
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
          formatter: (params) => {
            const percent = ((params.value / total) * 100).toFixed(2)
            return `${params.name}: ${formatCurrency(params.value)}\n(${percent}%)`
          },
          fontWeight: 'bold'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        labelLine: { show: true },
        data: [
          { 
            value: labYearlyTotal.zhuhai, 
            name: '珠海实验室',
            itemStyle: { color: '#409EFF' }
          },
          { 
            value: labYearlyTotal.shanghaiWuhan, 
            name: '上海+武汉实验室',
            itemStyle: { color: '#67C23A' }
          },
          { 
            value: labYearlyTotal.suzhou, 
            name: '苏州实验室',
            itemStyle: { color: '#E6A23C' }
          }
        ]
      }
    ]
  }
})

// 业务饼图配置
const businessPieOption = computed(() => {
  const total = Object.values(businessYearlyTotal).reduce((sum, val) => sum + val, 0)
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const percent = ((params.value / total) * 100).toFixed(2)
        return `${params.marker} ${params.name}: ${formatCurrency(params.value)} (${percent}%)`
      }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: ['FA', 'ESD', 'FIB+TEM', 'SIMS', '化学实验', '其他']
    },
    series: [
      {
        name: '业务收入',
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
          formatter: (params) => {
            const percent = ((params.value / total) * 100).toFixed(2)
            return `${params.name}: ${formatCurrency(params.value)}\n(${percent}%)`
          },
          fontWeight: 'bold'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        labelLine: { show: true },
        data: [
          { 
            value: businessYearlyTotal.FA, 
            name: 'FA',
            itemStyle: { color: '#409EFF' }
          },
          { 
            value: businessYearlyTotal.ESD, 
            name: 'ESD',
            itemStyle: { color: '#67C23A' }
          },
          { 
            value: businessYearlyTotal['FIB+TEM'], 
            name: 'FIB+TEM',
            itemStyle: { color: '#E6A23C' }
          },
          { 
            value: businessYearlyTotal.SIMS, 
            name: 'SIMS',
            itemStyle: { color: '#F56C6C' }
          },
          { 
            value: businessYearlyTotal.化学实验, 
            name: '化学实验',
            itemStyle: { color: '#909399' }
          },
          { 
            value: businessYearlyTotal.其他, 
            name: '其他',
            itemStyle: { color: '#C0C4CC' }
          }
        ]
      }
    ]
  }
})

// 业务类型选择
const selectedBusinessTypeZhuhai = ref('FA')
const selectedBusinessTypeShanghai = ref('FA')
const selectedBusinessTypeSuzhou = ref('FA')
const selectedBusinessTypeSummary = ref('FA') // 第四栏业务选择器

// 实验室业务数据
const zhuhaibusinessData = {
  FA: {
    owned: [120000, 135000, 145000, 130000, 150000, 160000, 155000, 165000, 170000, 175000, 180000, 185000],
    outsourced: [65000, 70000, 75000, 68000, 72000, 78000, 80000, 82000, 85000, 88000, 90000, 92000],
    pieData: [
      { value: 1850000, name: '自持设备' },
      { value: 920000, name: '委外设备' }
    ],
    businessTotal: 2770000
  },
  ESD: {
    owned: [80000, 85000, 90000, 82000, 95000, 100000, 105000, 110000, 115000, 120000, 125000, 130000],
    outsourced: [40000, 42000, 45000, 43000, 47000, 50000, 52000, 54000, 56000, 58000, 60000, 62000],
    pieData: [
      { value: 1200000, name: '自持设备' },
      { value: 600000, name: '委外设备' }
    ],
    businessTotal: 1800000
  },
  'FIB+TEM': {
    owned: [100000, 110000, 120000, 115000, 125000, 130000, 135000, 140000, 145000, 150000, 155000, 160000],
    outsourced: [50000, 55000, 60000, 57000, 62000, 65000, 68000, 70000, 72000, 75000, 78000, 80000],
    pieData: [
      { value: 1540000, name: '自持设备' },
      { value: 770000, name: '委外设备' }
    ],
    businessTotal: 2310000
  },
  SIMS: {
    owned: [60000, 65000, 70000, 68000, 72000, 75000, 78000, 80000, 82000, 85000, 88000, 90000],
    outsourced: [30000, 32000, 35000, 33000, 36000, 38000, 40000, 42000, 44000, 46000, 48000, 50000],
    pieData: [
      { value: 870000, name: '自持设备' },
      { value: 435000, name: '委外设备' }
    ],
    businessTotal: 1305000
  },
  化学实验: {
    owned: [50000, 55000, 60000, 58000, 62000, 65000, 67000, 69000, 71000, 73000, 75000, 77000],
    outsourced: [25000, 27000, 29000, 28000, 30000, 32000, 33000, 34000, 35000, 36000, 37000, 38000],
    pieData: [
      { value: 735000, name: '自持设备' },
      { value: 368000, name: '委外设备' }
    ],
    businessTotal: 1103000
  },
  其他: {
    owned: [30000, 32000, 35000, 34000, 36000, 38000, 39000, 40000, 41000, 42000, 43000, 44000],
    outsourced: [15000, 16000, 17000, 16500, 17500, 18500, 19000, 19500, 20000, 20500, 21000, 21500],
    pieData: [
      { value: 450000, name: '自持设备' },
      { value: 225000, name: '委外设备' }
    ],
    businessTotal: 675000
  }
}

// 上海+武汉实验室业务数据
const shanghaiBusinessData = {
  FA: {
    owned: [110000, 125000, 135000, 120000, 140000, 150000, 145000, 155000, 160000, 165000, 170000, 175000],
    outsourced: [60000, 65000, 70000, 63000, 68000, 73000, 75000, 77000, 80000, 82000, 85000, 87000],
    pieData: [
      { value: 1650000, name: '自持设备' },
      { value: 850000, name: '委外设备' }
    ],
    businessTotal: 2500000
  },
  ESD: {
    owned: [75000, 80000, 85000, 78000, 90000, 95000, 98000, 105000, 108000, 112000, 115000, 118000],
    outsourced: [38000, 40000, 42000, 41000, 45000, 48000, 50000, 52000, 54000, 56000, 58000, 60000],
    pieData: [
      { value: 1100000, name: '自持设备' },
      { value: 550000, name: '委外设备' }
    ],
    businessTotal: 1650000
  },
  'FIB+TEM': {
    owned: [95000, 105000, 115000, 110000, 120000, 125000, 130000, 135000, 140000, 145000, 150000, 155000],
    outsourced: [48000, 52000, 57000, 55000, 60000, 62000, 65000, 68000, 70000, 72000, 75000, 77000],
    pieData: [
      { value: 1450000, name: '自持设备' },
      { value: 720000, name: '委外设备' }
    ],
    businessTotal: 2170000
  },
  SIMS: {
    owned: [55000, 60000, 65000, 63000, 68000, 70000, 72000, 75000, 78000, 80000, 82000, 85000],
    outsourced: [28000, 30000, 32000, 31000, 33000, 35000, 37000, 39000, 41000, 43000, 45000, 47000],
    pieData: [
      { value: 820000, name: '自持设备' },
      { value: 410000, name: '委外设备' }
    ],
    businessTotal: 1230000
  },
  化学实验: {
    owned: [45000, 50000, 55000, 53000, 57000, 60000, 62000, 64000, 66000, 68000, 70000, 72000],
    outsourced: [22000, 24000, 26000, 25000, 27000, 29000, 30000, 31000, 32000, 33000, 34000, 35000],
    pieData: [
      { value: 690000, name: '自持设备' },
      { value: 345000, name: '委外设备' }
    ],
    businessTotal: 1035000
  },
  其他: {
    owned: [28000, 30000, 32000, 31000, 33000, 35000, 36000, 37000, 38000, 39000, 40000, 41000],
    outsourced: [14000, 15000, 16000, 15500, 16500, 17500, 18000, 18500, 19000, 19500, 20000, 20500],
    pieData: [
      { value: 420000, name: '自持设备' },
      { value: 210000, name: '委外设备' }
    ],
    businessTotal: 630000
  }
}

// 苏州实验室业务数据
const suzhouBusinessData = {
  FA: {
    owned: [100000, 115000, 125000, 110000, 130000, 140000, 135000, 145000, 150000, 155000, 160000, 165000],
    outsourced: [55000, 60000, 65000, 58000, 63000, 68000, 70000, 72000, 75000, 77000, 80000, 82000],
    pieData: [
      { value: 1550000, name: '自持设备' },
      { value: 800000, name: '委外设备' }
    ],
    businessTotal: 2350000
  },
  ESD: {
    owned: [70000, 75000, 80000, 73000, 85000, 90000, 93000, 98000, 102000, 105000, 108000, 110000],
    outsourced: [35000, 37000, 39000, 38000, 42000, 45000, 48000, 50000, 52000, 54000, 56000, 57000],
    pieData: [
      { value: 1050000, name: '自持设备' },
      { value: 525000, name: '委外设备' }
    ],
    businessTotal: 1575000
  },
  'FIB+TEM': {
    owned: [90000, 100000, 110000, 105000, 115000, 120000, 125000, 130000, 135000, 140000, 145000, 150000],
    outsourced: [45000, 49000, 54000, 52000, 57000, 59000, 62000, 65000, 67000, 69000, 72000, 74000],
    pieData: [
      { value: 1400000, name: '自持设备' },
      { value: 700000, name: '委外设备' }
    ],
    businessTotal: 2100000
  },
  SIMS: {
    owned: [50000, 55000, 60000, 58000, 63000, 65000, 67000, 70000, 73000, 75000, 77000, 80000],
    outsourced: [25000, 27000, 29000, 28000, 30000, 32000, 33000, 35000, 37000, 39000, 41000, 43000],
    pieData: [
      { value: 750000, name: '自持设备' },
      { value: 375000, name: '委外设备' }
    ],
    businessTotal: 1125000
  },
  化学实验: {
    owned: [40000, 45000, 50000, 48000, 52000, 55000, 57000, 59000, 61000, 63000, 65000, 67000],
    outsourced: [20000, 22000, 24000, 23000, 25000, 27000, 28000, 29000, 30000, 31000, 32000, 33000],
    pieData: [
      { value: 630000, name: '自持设备' },
      { value: 315000, name: '委外设备' }
    ],
    businessTotal: 945000
  },
  其他: {
    owned: [25000, 27000, 29000, 28000, 30000, 32000, 33000, 34000, 35000, 36000, 37000, 38000],
    outsourced: [12500, 13500, 14500, 14000, 15000, 16000, 16500, 17000, 17500, 18000, 18500, 19000],
    pieData: [
      { value: 380000, name: '自持设备' },
      { value: 190000, name: '委外设备' }
    ],
    businessTotal: 570000
  }
}

// 实验室固定数据
const zhuhailabFixedData = {
  allBusinessesTotal: 2770000 + 1800000 + 2310000 + 1305000 + 1103000 + 675000,
  labGrossProfit: 1010000,
  labGrossMargin: 0.339
}

const shanghaiLabFixedData = {
  allBusinessesTotal: 2500000 + 1650000 + 2170000 + 1230000 + 1035000 + 630000,
  labGrossProfit: 850000,
  labGrossMargin: 0.325
}

const suzhouLabFixedData = {
  allBusinessesTotal: 2350000 + 1575000 + 2100000 + 1125000 + 945000 + 570000,
  labGrossProfit: 750000,
  labGrossMargin: 0.315
}

// 实验室计算属性工厂函数
const createLabComputed = (businessData, fixedData, selectedBusinessRef) => {
  const currentData = computed(() => 
    businessData[selectedBusinessRef.value] || businessData.FA
  )
  
  const currentBusinessTotal = computed(() => currentData.value.businessTotal)
  const allBusinessesTotal = computed(() => fixedData.allBusinessesTotal)
  const currentBusinessPercentage = computed(() => 
    currentBusinessTotal.value / allBusinessesTotal.value
  )
  
  return {
    currentData,
    pieData: computed(() => currentData.value.pieData),
    currentBusinessTotal,
    allBusinessesTotal,
    currentBusinessPercentage,
    labGrossProfit: computed(() => fixedData.labGrossProfit),
    labGrossMargin: computed(() => fixedData.labGrossMargin)
  }
}

// 珠海实验室计算属性
const zhuhaiComputed = createLabComputed(zhuhaibusinessData, zhuhailabFixedData, selectedBusinessTypeZhuhai)
const zhuhaiCurrentData = zhuhaiComputed.currentData
const zhuhaiPieData = zhuhaiComputed.pieData
const zhuhaiCurrentBusinessTotal = zhuhaiComputed.currentBusinessTotal
const zhuhaiAllBusinessesTotal = zhuhaiComputed.allBusinessesTotal
const zhuhaiCurrentBusinessPercentage = zhuhaiComputed.currentBusinessPercentage
const zhuhaiLabGrossProfit = zhuhaiComputed.labGrossProfit
const zhuhaiLabGrossMargin = zhuhaiComputed.labGrossMargin

// 上海+武汉实验室计算属性
const shanghaiComputed = createLabComputed(shanghaiBusinessData, shanghaiLabFixedData, selectedBusinessTypeShanghai)
const shanghaiCurrentData = shanghaiComputed.currentData
const shanghaiPieData = shanghaiComputed.pieData
const shanghaiCurrentBusinessTotal = shanghaiComputed.currentBusinessTotal
const shanghaiAllBusinessesTotal = shanghaiComputed.allBusinessesTotal
const shanghaiCurrentBusinessPercentage = shanghaiComputed.currentBusinessPercentage
const shanghaiLabGrossProfit = shanghaiComputed.labGrossProfit
const shanghaiLabGrossMargin = shanghaiComputed.labGrossMargin

// 苏州实验室计算属性
const suzhouComputed = createLabComputed(suzhouBusinessData, suzhouLabFixedData, selectedBusinessTypeSuzhou)
const suzhouCurrentData = suzhouComputed.currentData
const suzhouPieData = suzhouComputed.pieData
const suzhouCurrentBusinessTotal = suzhouComputed.currentBusinessTotal
const suzhouAllBusinessesTotal = suzhouComputed.allBusinessesTotal
const suzhouCurrentBusinessPercentage = suzhouComputed.currentBusinessPercentage
const suzhouLabGrossProfit = suzhouComputed.labGrossProfit
const suzhouLabGrossMargin = suzhouComputed.labGrossMargin

// 第四栏业务汇总计算属性
const summaryCurrentData = computed(() => {
  // 汇总三个实验室的当前业务数据
  const zhuhaiData = zhuhaibusinessData[selectedBusinessTypeSummary.value] || zhuhaibusinessData.FA
  const shanghaiData = shanghaiBusinessData[selectedBusinessTypeSummary.value] || shanghaiBusinessData.FA
  const suzhouData = suzhouBusinessData[selectedBusinessTypeSummary.value] || suzhouBusinessData.FA
  
  // 合并数据
  return {
    owned: zhuhaiData.owned.map((val, index) => 
      val + shanghaiData.owned[index] + suzhouData.owned[index]
    ),
    outsourced: zhuhaiData.outsourced.map((val, index) => 
      val + shanghaiData.outsourced[index] + suzhouData.outsourced[index]
    ),
    pieData: [
      { 
        value: zhuhaiData.pieData[0].value + shanghaiData.pieData[0].value + suzhouData.pieData[0].value, 
        name: '自持设备' 
      },
      { 
        value: zhuhaiData.pieData[1].value + shanghaiData.pieData[1].value + suzhouData.pieData[1].value, 
        name: '委外设备' 
      }
    ],
    businessTotal: zhuhaiData.businessTotal + shanghaiData.businessTotal + suzhouData.businessTotal
  }
})

// 第四栏饼图数据
const summaryPieData = computed(() => summaryCurrentData.value.pieData)

// 第四栏业务总收入
const summaryCurrentBusinessTotal = computed(() => summaryCurrentData.value.businessTotal)

// 第四栏业务毛利额（模拟数据，实际应根据业务逻辑计算）
const summaryGrossProfit = computed(() => {
  // 模拟计算：业务总收入 × 毛利率（假设为30%）
  return summaryCurrentBusinessTotal.value * 0.3
})

// 第四栏自持设备毛利额
const summaryOwnedGrossProfit = computed(() => {
  return summaryGrossProfit.value * 0.7 // 假设自持占70%
})

// 第四栏委外设备毛利额
const summaryOutsourcedGrossProfit = computed(() => {
  return summaryGrossProfit.value * 0.3 // 假设委外占30%
})

// 第四栏业务毛利率
const summaryGrossMargin = computed(() => {
  return summaryGrossProfit.value / summaryCurrentBusinessTotal.value
})

// 第四栏所有实验室收入总计（不随业务选择变化）
const summaryAllLabsTotal = computed(() => {
  return zhuhailabFixedData.allBusinessesTotal + 
         shanghaiLabFixedData.allBusinessesTotal + 
         suzhouLabFixedData.allBusinessesTotal
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
    name: '元',
    axisLabel: { 
      formatter: (value) => formatNumber(value)
    }
  }
}

// 创建柱状图配置
const createBarOption = (currentData) => ({
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
    data: ['自持设备', '委外设备'],
    top: 10,
    right: 30,
    orient: 'horizontal'
  },
  series: [
    {
      name: '自持设备',
      type: 'bar',
      data: currentData.value.owned,
      itemStyle: { color: '#409EFF' },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => formatNumber(params.value),
        color: '#000000',
        fontSize: 10,
        fontWeight: 'bold'
      }
    },
    {
      name: '委外设备',
      type: 'bar',
      data: currentData.value.outsourced,
      itemStyle: { color: '#67C23A' },
      label: {
        show: true,
        position: 'top',
        formatter: (params) => formatNumber(params.value),
        color: '#000000',
        fontSize: 10,
        fontWeight: 'bold'
      }
    }
  ]
})

// 创建饼图配置
const createPieOption = (pieData) => {
  const total = pieData.value.reduce((sum, item) => sum + item.value, 0)
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const percent = ((params.value / total) * 100).toFixed(2)
        return `${params.marker} ${params.name}: ${formatCurrency(params.value)} (${percent}%)`
      }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: pieData.value.map(item => item.name)
    },
    series: [
      {
        name: '设备类型',
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
          formatter: (params) => {
            const percent = ((params.value / total) * 100).toFixed(2)
            return `${params.name}: ${formatCurrency(params.value)}\n(${percent}%)`
          },
          fontWeight: 'bold'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: true
        },
        data: pieData.value.map((item, index) => ({
          ...item,
          itemStyle: { 
            color: index === 0 ? '#409EFF' : '#67C23A'
          }
        }))
      }
    ]
  }
}

// 各实验室图表配置
const zhuhaiBarOption = computed(() => createBarOption(zhuhaiCurrentData))
const zhuhaiPieOption = computed(() => createPieOption(zhuhaiPieData))

const shanghaiBarOption = computed(() => createBarOption(shanghaiCurrentData))
const shanghaiPieOption = computed(() => createPieOption(shanghaiPieData))

const suzhouBarOption = computed(() => createBarOption(suzhouCurrentData))
const suzhouPieOption = computed(() => createPieOption(suzhouPieData))

// 第四栏图表配置
const summaryBarOption = computed(() => createBarOption(summaryCurrentData))
const summaryPieOption = computed(() => createPieOption(summaryPieData))
</script>

<style scoped>
.laboratory-income-page {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.section {
  margin-bottom: 30px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.section-title {
  color: #303133;
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: 600;
  border-left: 4px solid #409EFF;
  padding-left: 12px;
}

.section-content {
  width: 100%;
}

.row {
  display: flex;
  margin-bottom: 20px;
  gap: 20px;
}

.row:last-child {
  margin-bottom: 0;
}

.col {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0 0 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.card-title {
  color: #303133;
  font-weight: 600;
  font-size: 16px;
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.current-business-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
  white-space: nowrap;
}

.chart-card, .data-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0;
}

.data-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.chart-content {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #fafafa;
  border-radius: 0 0 4px 4px;
}

.data-content {
  padding: 20px;
  text-align: center;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.data-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 8px;
  line-height: 1.2;
}

.data-desc {
  color: #606266;
  font-size: 14px;
  margin-bottom: 12px;
  line-height: 1.4;
}

/* 毛利率表格样式 */
.gross-margin-table {
  width: 100%;
  height: 100%;
  padding: 10px;
}

.gross-margin-table :deep(.el-table) {
  height: 100%;
}

.gross-margin-table :deep(.el-table th) {
  background-color: #f5f7fa;
  color: #606266;
  font-weight: 600;
}

.gross-margin-table :deep(.el-table tr:hover) {
  background-color: #f0f9ff;
}

/* 第四栏业务毛利额特殊样式 */
.profit-detail {
  margin-bottom: 10px;
  padding: 8px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.profit-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.profit-label {
  font-size: 13px;
  color: #606266;
}

.profit-value {
  font-size: 13px;
  font-weight: 600;
  color: #409EFF;
}

.profit-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-top: 5px;
  border-top: 1px solid #e4e7ed;
}

.total-label {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.total-value {
  font-size: 16px;
  font-weight: 700;
  color: #67C23A;
}

.data-sub-value {
  font-size: 20px;
  font-weight: 600;
  color: #409EFF;
  margin-bottom: 4px;
  line-height: 1.2;
}

.data-sub-desc {
  color: #909399;
  font-size: 12px;
  line-height: 1.4;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .row {
    flex-direction: column;
  }
  
  .col {
    margin-bottom: 20px;
  }
  
  .col:last-child {
    margin-bottom: 0;
  }
}

@media (max-width: 768px) {
  .laboratory-income-page {
    padding: 10px;
  }
  
  .section {
    padding: 15px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .chart-controls {
    width: 100%;
    justify-content: space-between;
  }
  
  .data-value {
    font-size: 24px;
  }
  
  .profit-line, .profit-total {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }
}

/* 动画效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 卡片悬停效果 */
.chart-card:hover, .data-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.chart-card, .data-card {
  transition: all 0.3s ease;
}

/* 图表容器样式 */
.chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bar-chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.bar-chart-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #303133;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  width: 90%;
  height: 70%;
  position: relative;
}

.bar {
  width: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  position: relative;
  border-radius: 4px 4px 0 0;
  transition: all 0.3s ease;
}

.bar:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.bar-label {
  position: absolute;
  bottom: -25px;
  font-size: 12px;
  color: #606266;
}

.bar-value {
  position: absolute;
  top: -25px;
  font-size: 12px;
  font-weight: 600;
  color: #303133;
}

.pie-chart-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.pie-chart-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #303133;
}

.pie-chart {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  margin: 20px 0;
  background: conic-gradient(
    var(--color1) 0% var(--percentage1),
    var(--color2) 0% var(--percentage2),
    var(--color3) 0% var(--percentage3),
    var(--color4) 0% var(--percentage4)
  );
}

.pie-segment {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.segment-label {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.segment-value {
  font-size: 12px;
  color: #fff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.pie-legend {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  margin-top: 15px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #606266;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}
</style>