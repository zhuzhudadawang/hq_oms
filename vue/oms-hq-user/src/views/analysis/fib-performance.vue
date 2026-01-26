<template>
  <div class="fib-performance">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>FIB人员绩效(月度)分析</span>
          <el-date-picker v-model="month" type="month" placeholder="选择月份" @change="fetchData" />
        </div>
      </template>

      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24">
          <div class="chart-container">
            <h3>FIB人员绩效工时</h3>
            <EChart :option="barChartOption_test" height="560px" />
          </div>
        </el-col>
      </el-row>
        <el-row :gutter="20" class="summary-row" style="margin-top:16px;">
          <el-col :span="12">
            <el-card class="summary-card green">
              <div class="summary-title">绩效工时总和</div>
              <div class="summary-value">{{ performanceHoursTotal }}</div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="summary-card blue">
              <div class="summary-title">平均绩效工时</div>
              <div class="summary-value">{{ avgPerformanceHours }}</div>
            </el-card>
          </el-col>
        </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import EChart from "@/components/EChart.vue";
import { fibPerformanceApi } from "@/api/analysis";
const month = ref(new Date());

// 柱状图配置
const performanceHoursTotal = ref(0);
const avgPerformanceHours = ref("0");
const barChartOption_test = reactive({
    grid: {
    left: "6%",
    right: "1%",
    containLabel: true,
  },
  // title: {
  //   text: "各人员成功率",
  //   textStyle: { fontSize: 20 },
  // },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
  },
  legend: {
    data: ["绩效工时"],
  },
  xAxis: {
    type: "category",
    data: [],
  },
  yAxis: [
    {
      type: "value",
      name: "绩效工时",
      position: "left",
    }
  ],
  series: [
    {
      name: "绩效工时",
      type: "bar",
      data: [],
      itemStyle: { color: "#67c23a" },
      // 柱顶显示数值
      label: {
        show: true,
        position: "top",
        fontSize: 16,
      },
    }
  ],
});

// 柱状图数据获取
const fetchData = async () => {
  try {
    // 转换为 YYYY-MM 格式
    const year = month.value.getFullYear(); // 获取年份（如 2025）
    const monthNum = month.value.getMonth() + 1; // 获取月份（0-11 → 1-12）
    const formattedDate = `${year}-${monthNum.toString().padStart(2, "0")}`;

    const params = { month: formattedDate };
    const response = await fibPerformanceApi.getData(params);

    if (response) {
      const {
        engineer_names,
        performance_hours,
        total_performance_hours,
      } = response;

      // 赋值（数据填充到图表并更新 summary refs）
      barChartOption_test.xAxis.data = engineer_names; // 工程师姓名
      barChartOption_test.series[0].data = performance_hours; // 成功数

      // const numericSuccess = Array.isArray(success_counts)
      //   ? success_counts.map((n) => Number(n) || 0)
      //   : [];
      // const numericCompleted = Array.isArray(completed_counts)
      //   ? completed_counts.map((n) => Number(n) || 0)
      //   : [];
      // const barMax = Math.max(0, ...numericSuccess, ...numericCompleted);
      // const paddedMax = (barMax * 1.5 + 10) || 10;
      // const roundedMax = Math.ceil(paddedMax / 10) * 10;
      // const interval = Math.max(5, Math.ceil(roundedMax / 4 / 5) * 5);
      // barChartOption_test.yAxis[0].max = roundedMax;
      // barChartOption_test.yAxis[0].interval = interval;

      // 计算并写入 refs，做空值与类型安全检查
      performanceHoursTotal.value = total_performance_hours; // 绩效工时总和
      avgPerformanceHours.value = Number((total_performance_hours / engineer_names.length).toFixed(2)); // 平均绩效工时
    } else {
      console.error("数据获取失败：", response.message);
    }
  } catch (error) {
    console.error("接口请求异常：", error);
  }
};
onMounted(() => {
  fetchData();
});
</script>

<style lang="scss" scoped>
.fib-performance {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
  }

  .chart-container {
    h3 {
      margin: 0 0 10px 0;
      font-size: 14px;
      color: #606266;
    }
  }
    .summary-row {
    margin-top: 16px;
  }
  .summary-card {
    text-align: center;
    padding: 18px 0;
    border-radius: 8px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
    min-height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: #fff;
  }
  .summary-card.green .summary-value { color: #67c23a; }
  .summary-card.red .summary-value { color: #f56c6c; }
  .summary-card.blue .summary-value { color: #409eff; }

  .summary-title {
    color: #909399;
    font-size: 13px;
    margin-bottom: 6px;
  }
  .summary-value {
    font-size: 26px;
    font-weight: 700;
    color: #303133;
  }
}
</style>
