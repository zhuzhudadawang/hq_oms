<template>
  <div class="business-container">
    <el-card class="main-card">
      <template #header>
        <div class="card-header">
          <span>经营数据分析</span>
        </div>
      </template>
      
      <!-- 第一行：饼图 + 横向条形图 -->
      <el-row :gutter="10" class="equal-height-row">
        <el-col :span="12">
          <el-card class="chart-card" shadow="hover">
            <div class="chart-container">
              <h3>各业务板块收入结构分析</h3>
              <EChart :option="pieChartOption" height="400px" />
              <div class="chart-summary-wrapper">
                <div class="chart-summary">
                  <p>总收入：<span class="highlight">1200万元</span></p>
                  <p>平均板块收入：<span class="highlight">300万元</span></p>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="chart-card" shadow="hover">
            <div class="chart-container">
              <h3>公司资产负债结构分析</h3>
              <EChart :option="barHorizontalOption" height="400px" />
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 第二行：柱状+折线图 -->
      <el-row :gutter="10" style="margin-top: 10px">
        <el-col :span="24">
          <el-card class="chart-card" shadow="hover">
            <div class="chart-container">
              <h3>公司经营概况核心指标可视化分析</h3>
              <p class="chart-subtitle">主营业务费用变化趋势分析</p>
              <EChart :option="mixedChartOption" height="450px" />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import EChart from "@/components/EChart.vue";

// 饼图配置 - 各业务板块收入结构分析
const pieChartOption = reactive({
  tooltip: {
    trigger: "item",
    formatter: "{b}: {c}万元 ({d}%)"
  },
  legend: {
    orient: "vertical",
    left: "left"
  },
  series: [
    {
      name: "业务板块",
      type: "pie",
      radius: ["40%", "70%"],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: "#fff",
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: "{b}\n{d}%"
      },
      data: [
        { value: 500, name: "上海+武汉实验室", itemStyle: { color: "#91cc75" } },
        { value: 250, name: "苏州实验室", itemStyle: { color: "#fac858" } },
        { value: 150, name: "其他业务", itemStyle: { color: "#ee6666" } },
        { value: 300, name: "珠海实验室", itemStyle: { color: "#73c0de" } }
      ]
    }
  ]
});

// 横向条形图配置 - 公司资产负债结构分析
const barHorizontalOption = reactive({
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow"
    },
    formatter: "{b}: {c}万元"
  },
  legend: {
    data: ["资产"],
    top: 0
  },
  grid: {
    left: "25%",
    right: "15%",
    bottom: "3%",
    top: "15%"
  },
  xAxis: {
    type: "value",
    axisLabel: {
      formatter: "{value}"
    }
  },
  yAxis: {
    type: "category",
    data: ["流动资产", "固定资产", "无形资产", "应收账款", "长期负债"]
  },
  series: [
    {
      name: "资产",
      type: "bar",
      data: [
        { value: 1200, itemStyle: { color: "#91cc75" } },
        { value: 850, itemStyle: { color: "#91cc75" } },
        { value: 320, itemStyle: { color: "#91cc75" } },
        { value: 650, itemStyle: { color: "#fac858" } },
        { value: 380, itemStyle: { color: "#ee6666" } }
      ],
      label: {
        show: true,
        position: "right",
        formatter: "{c}万元"
      }
    }
  ],
  graphic: [
    {
      type: "text",
      right: 10,
      top: 25,
      style: {
        text: "净资产：1340万元\n净资产：56.8%",
        fontSize: 12,
        fill: "#666"
      }
    }
  ]
});

// 柱状+折线混合图配置 - 公司经营概况核心指标
const mixedChartOption = reactive({
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "cross"
    }
  },
  legend: {
    data: ["研发费用", "管理费用", "销售费用", "总费用"],
    bottom: 0
  },
  grid: {
    left: "3%",
    right: "4%",
    bottom: "10%",
    top: "10%",
    containLabel: true
  },
  xAxis: {
    type: "category",
    data: ["1月", "2月", "3月", "4月", "5月", "6月"],
    axisLabel: {
      formatter: "{value}"
    }
  },
  yAxis: [
    {
      type: "value",
      name: "费用(万元)",
      position: "left",
      axisLabel: {
        formatter: "{value}"
      }
    },
    {
      type: "value",
      name: "总费用(万元)",
      position: "right",
      axisLabel: {
        formatter: "{value}"
      }
    }
  ],
  series: [
    {
      name: "研发费用",
      type: "bar",
      data: [35, 40, 52, 60, 92, 95],
      itemStyle: { color: "#ee6666" }
    },
    {
      name: "管理费用",
      type: "bar",
      data: [28, 32, 41, 58, 69, 72],
      itemStyle: { color: "#73c0de" }
    },
    {
      name: "销售费用",
      type: "bar",
      data: [22, 25, 38, 42, 45, 50],
      itemStyle: { color: "#91cc75" }
    },
    {
      name: "总费用",
      type: "line",
      yAxisIndex: 1,
      data: [85, 97, 131, 160, 206, 217],
      itemStyle: { color: "#fc8452" },
      label: {
        show: true,
        position: "top",
        formatter: "{c}"
      }
    }
  ]
});
</script>

<style lang="scss" scoped>
.business-container {
  .main-card {
    :deep(.el-card__body) {
      padding: 10px;
    }
  }

  .card-header {
    display: flex;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
  }

  .chart-card {
    border-radius: 8px;
    height: 100%;
    
    :deep(.el-card__body) {
      padding: 16px;
    }
  }

  .equal-height-row {
    .el-col {
      margin-bottom: 0;
    }
  }

  .chart-container {
    h3 {
      margin: 0 0 10px 0;
      font-size: 14px;
      color: #303133;
      text-align: center;
    }

    .chart-subtitle {
      text-align: center;
      font-size: 12px;
      color: #909399;
      margin: 0 0 10px 0;
    }

    .chart-summary {
      display: inline-block;
      margin-top: 10px;
      padding: 8px 16px;
      background: #f5f7fa;
      border-radius: 4px;
      text-align: center;

      p {
        margin: 3px 0;
        font-size: 13px;
        color: #606266;
      }

      .highlight {
        color: #409eff;
        font-weight: bold;
      }
    }

    .chart-summary-wrapper {
      text-align: center;
    }
  }
}
</style>
