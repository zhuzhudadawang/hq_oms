<template>
  <div class="fib-completion">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>FIB人员产出饱和度(周度)分析</span>
          <div class="header-actions">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              @change="fetchData"
              value-format="YYYY-MM-DD"
              :disabled-date="disableFuture"
            />
            <el-button type="primary" icon="Refresh" @click="fetchData"
              >刷新</el-button
            >
          </div>
        </div>
      </template>
      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24">
          <div class="chart-container">
            <h3>人员产出饱和度</h3>
            <EChart :option="barChartOption" height="560px" />
          </div>
        </el-col>
      </el-row>
              <el-row :gutter="20" class="summary-row" style="margin-top:16px;">
          <el-col :span="8">
            <el-card class="summary-card green">
              <div class="summary-title">实际产出总和</div>
              <div class="summary-value">{{ formattedRealTotal }}</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="summary-card red">
              <div class="summary-title">应当产出总和</div>
              <div class="summary-value">{{ formattedIdealTotal }}</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="summary-card blue">
              <div class="summary-title">平均饱和度</div>
              <div class="summary-value">{{ avgRate }}</div>
            </el-card>
          </el-col>
        </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import EChart from "@/components/EChart.vue";
import { fibOutputApi } from "@/api/analysis";
import { useDateRangeStore } from "@/stores/dateRange";

const dateRangeStore = useDateRangeStore();
const dateRange = computed({
  get: () => dateRangeStore.dateRange,
  set: (val) => dateRangeStore.setDateRange(val)
});
// summary 数据
const formattedRealTotal = ref(0);
const formattedIdealTotal = ref(0);
const avgRate = ref("0%");

const disableFuture = (date) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return date.getTime() > today.getTime()
}

// 柱状图配置
const barChartOption = reactive({
  grid: {
    left: "6%",
    right: "1%",
    containLabel: true,
  },
  // title: {
  //   text: "一周人员产出饱和度",
  // },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
    // tooltip 中对饱和度追加 % 符号
    formatter: (params) => {
      if (!Array.isArray(params)) return params;
      return params
        .map((p) => {
          if (p && p.seriesName === "饱和度") {
            return `${p.seriesName}: ${p.value}%`;
          }
          return `${p.seriesName}: ${p.value}`;
        })
        .join("<br/>");
    },
  },
  legend: {
    data: ["应产出", "实产出", "饱和度"],
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
      name: "饱和度(%)",
      position: "right",
      axisLabel: {
        formatter: "{value}%",
      },
    },
  ],
  series: [
    {
      name: "应产出",
      type: "bar",
      data: [],
      itemStyle: { color: "#0080FF" },
      barWidth: 30,
      barCategoryGap: "50%",
      // 柱内显示数值
      label: {
        show: true,
        position: "top",
        fontSize: 14,
        color: "#303133",
        distance: 6,
      },
    },
    {
      name: "实产出",
      type: "bar",
      data: [],
      itemStyle: { color: "#67c23a" },
      barWidth: 30,
      barGap: "0%",
      label: {
        show: true,
        position: "top",
        fontSize: 14,
        color: "#303133",
        distance: 6,
      },
    },
    {
      name: "饱和度",
      type: "line",
      yAxisIndex: 1,
      data: [],
      itemStyle: { color: "#409eff" },
      label: {
        show: true,
        position: "top",
        fontSize: 16,
        formatter: "{c}%",
        offset: [0, -18],
        color: "#303133",
        padding: [2, 6],
        borderRadius: 4,
      },
      labelLayout: {
        moveOverlap: "shiftY",
        hideOverlap: true,
      },
    },
  ],
});

// 柱状图数据获取
const fetchData = async () => {
  try {
    const [start_date, end_date] = dateRange.value;
    const params = {
      start_date,
      end_date,
    };
    const response = await fibOutputApi.getData(params);

    if (response) {
      const {
        engineer_names,
        success_counts,
        required_counts,
        saturation_rates,
      } = response;
      console.log(response);
      // 赋值
      barChartOption.xAxis.data = engineer_names; // 工程师
      barChartOption.series[0].data = required_counts; // 应当产出数
      barChartOption.series[1].data = success_counts; // 实际产出数
      barChartOption.series[2].data = saturation_rates; // 饱和度
      const numericSuccess = Array.isArray(success_counts)
        ? success_counts.map((n) => Number(n) || 0)
        : [];
      const numericRequired = Array.isArray(required_counts)
        ? required_counts.map((n) => Number(n) || 0)
        : [];
      const barMax = Math.max(
        0,
        ...numericSuccess,
        ...numericRequired,
      );
  const paddedMax = barMax * 1.5 + 10 || 10;
  const roundedMax = Math.ceil(paddedMax / 10) * 10;
  const interval = Math.max(5, Math.ceil(roundedMax / 4 / 5) * 5);
  barChartOption.yAxis[0].max = roundedMax;
  barChartOption.yAxis[0].interval = interval;
      // 计算并写入 summary refs（防止直接覆盖变量）
      const successTotal = Array.isArray(success_counts)
        ? success_counts.reduce((a, b) => a + (Number(b) || 0), 0)
        : 0;
      const completedTotal = Array.isArray(required_counts)
        ? required_counts.reduce((a, b) => a + (Number(b) || 0), 0)
        : 0;
      formattedRealTotal.value = successTotal.toLocaleString();
      formattedIdealTotal.value = completedTotal.toLocaleString();
      if (Array.isArray(saturation_rates) && saturation_rates.length > 0) {
        const avg = saturation_rates.reduce((a, b) => a + (Number(b) || 0), 0) / saturation_rates.length;
        avgRate.value = avg.toFixed(2) + "%";
      } else {
        avgRate.value = "0%";
      }
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
.fib-completion {
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
