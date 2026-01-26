<template>
  <div class="fib-completion">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>内部机台工作时间饱和度(周度)分析</span>
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
            <h3>内部机台工作时间饱和度</h3>
            <EChart :option="barChartOption" height="560px" />
          </div>
        </el-col>
      </el-row>
              <el-row :gutter="20" class="summary-row" style="margin-top:16px;">
          <el-col :span="8">
            <el-card class="summary-card green">
              <div class="summary-title">实际工作时间总和</div>
              <div class="summary-value">{{ formattedRealTotal }}</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="summary-card red">
              <div class="summary-title">可用工作时间总和</div>
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
import { machineSaturationApi } from "@/api/analysis";
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
  // title: {
  //   text: "一周内部机台工作时间饱和度",
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
    data: ["可用工作时间", "实际工作时间", "饱和度"],
  },
  xAxis: {
    type: "category",
    data: ['上海-G5-UX','上海-G5-CX','上海-460','上海-Talos','上海-F20',],
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
      name: "可用工作时间",
      type: "bar",
      data: [],
      itemStyle: { color: "#0080FF" },
      // 柱顶显示数值
      label: {
        show: true,
        position: "top",
        fontSize: 16,
      },
    },
    {
      name: "实际工作时间",
      type: "bar",
      data: [],
      itemStyle: { color: "#67c23a" },
      label: {
        show: true,
        position: "top",
        fontSize: 16,
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
    const response = await machineSaturationApi.getData(params);

    if (response) {
      const {
        total_hours_list,
        total_available_duration_list,
        saturation_rates,
      } = response;

      // 赋值
      barChartOption.series[0].data = total_available_duration_list; // 可用工作时间
      barChartOption.series[1].data = total_hours_list; // 实际工作时间
      barChartOption.series[2].data = saturation_rates; // 饱和度
      // 计算并写入 summary refs（防止直接覆盖变量）
      const hoursTotal = Array.isArray(total_hours_list)
        ? total_hours_list.reduce((a, b) => a + (Number(b) || 0), 0)
        : 0;
      const duration = Array.isArray(total_available_duration_list)
        ? total_available_duration_list.reduce((a, b) => a + (Number(b) || 0), 0)
        : 0;
      formattedRealTotal.value = hoursTotal.toLocaleString();
      formattedIdealTotal.value = duration.toLocaleString();
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
