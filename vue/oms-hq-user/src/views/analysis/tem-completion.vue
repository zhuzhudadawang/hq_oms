<template>
  <div class="tem-completion">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>TEM人员完成率(月度)分析</span>
          <el-date-picker v-model="month" type="month" placeholder="选择月份" @change="fetchData" />
        </div>
      </template>

      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24">
          <div class="chart-container">
            <h3>TEM人员完成率</h3>
            <EChart :option="barChartOption_test" height="560px" />
          </div>
        </el-col>
      </el-row>
        <el-row :gutter="20" class="summary-row" style="margin-top:16px;">
          <el-col :span="8">
            <el-card class="summary-card green">
              <div class="summary-title">成功总和</div>
              <div class="summary-value">{{ formattedSuccessTotal }}</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="summary-card red">
              <div class="summary-title">失败总和</div>
              <div class="summary-value">{{ formattedFailTotal }}</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="summary-card blue">
              <div class="summary-title">平均成功率</div>
              <div class="summary-value">{{ avgRate }}</div>
            </el-card>
          </el-col>
        </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import EChart from "@/components/EChart.vue";
import { temCompletionApi } from "@/api/analysis";
const month = ref(new Date());



// 柱状图配置
const formattedSuccessTotal = ref(0);
const formattedFailTotal = ref(0);
const avgRate = ref("0%");
const barChartOption_test = reactive({
  // title: {
  //   text: "各人员成功率",
  //   textStyle: { fontSize: 20 },
  // },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
    // tooltip 中对成功率追加 % 符号
    formatter: (params) => {
      if (!Array.isArray(params)) return params;
      return params
        .map((p) => {
          if (p && p.seriesName === "成功率") {
            return `${p.seriesName}: ${p.value}%`;
          }
          return `${p.seriesName}: ${p.value}`;
        })
        .join("<br/>");
    },
  },
  legend: {
    data: ["成功数", "完成数", "成功率"],
  },
  xAxis: {
    type: "category",
    data: [],
  },
  yAxis: [
    {
      type: "value",
      name: "数量",
      position: "left",
    },
    {
      type: "value",
      name: "成功率(%)",
      position: "right",
      axisLabel: {
        formatter: "{value}%",
      },
    },
  ],
  series: [
    {
      name: "成功数",
      type: "bar",
      data: [],
      itemStyle: { color: "#67c23a" },
      // 柱顶显示数值
      label: {
        show: true,
        position: "top",
        fontSize: 16,
      },
    },
    {
      name: "完成数",
      type: "bar",
      data: [],
      itemStyle: { color: "#0080FF" },
      label: {
        show: true,
        position: "top",
        fontSize: 16,
      },
    },
    {
      name: "成功率",
      type: "line",
      yAxisIndex: 1,
      data: [],
      itemStyle: { color: "#409eff" },
      label: {
        show: true,
        position: "top",
        fontSize: 16,
        // 在图上显示带 % 的数值
        formatter: "{c}%",
      },
    },
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
    const response = await temCompletionApi.getData(params);

    if (response) {
      const {
        engineer_names,
        success_counts,
        completed_counts,
        success_rates,
        actual_total_completed,
        actual_total_success,
      } = response;

      // 赋值（数据填充到图表并更新 summary refs）
      barChartOption_test.xAxis.data = engineer_names; // 工程师姓名
      barChartOption_test.series[0].data = success_counts; // 成功数
      barChartOption_test.series[1].data = completed_counts; // 完成数
      barChartOption_test.series[2].data = success_rates; // 成功率

      // 计算并写入 refs，做空值与类型安全检查
      const successSum = success_counts.reduce((acc, cur) => acc + (Number(cur) || 0), 0);
      const completedSum = completed_counts.reduce((acc, cur) => acc + (Number(cur) || 0), 0);
      formattedSuccessTotal.value = successSum; // 成功总和
      formattedFailTotal.value = completedSum - successSum; // 失败总和
      avgRate.value =
        actual_total_completed === 0
          ? "0.00%"
          : ((actual_total_success / actual_total_completed) * 100).toFixed(2) +"%";
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
.tem-completion {
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
