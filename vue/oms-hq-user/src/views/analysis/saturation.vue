<template>
  <div class="completion">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>人员平均饱和度(周度)分析</span>
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
            <h3>人员平均饱和度</h3>
            <EChart :option="barChartOption" height="560px" />
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20" class="summary-row" style="margin-top: 16px">
        <el-col :span="12">
          <el-card class="summary-card green">
            <div class="summary-title">FIB实际产出总和</div>
            <div class="summary-value">{{ fibFormattedRealTotal }}</div>
          </el-card>
        </el-col>
        <!-- <el-col :span="8">
          <el-card class="summary-card red">
            <div class="summary-title">应当产出总和</div>
            <div class="summary-value">{{ formattedIdealTotal }}</div>
          </el-card>
        </el-col> -->
        <el-col :span="12">
          <el-card class="summary-card blue">
            <div class="summary-title">FIB工作人数</div>
            <div class="summary-value">{{ fibEngineerCount }}</div>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter="20" class="summary-row" style="margin-top: 16px">
        <el-col :span="12">
          <el-card class="summary-card green">
            <div class="summary-title">TEM实际产出总和</div>
            <div class="summary-value">{{ temFormattedRealTotal }}</div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="summary-card blue">
            <div class="summary-title">TEM工作人数</div>
            <div class="summary-value">{{ temEngineerCount }}</div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import EChart from "@/components/EChart.vue";
import { fibSaturationApi, temSaturationApi } from "@/api/analysis";
import { useDateRangeStore } from "@/stores/dateRange";

const dateRangeStore = useDateRangeStore();
const dateRange = computed({
  get: () => dateRangeStore.dateRange,
  set: (val) => dateRangeStore.setDateRange(val)
});
// summary 数据
const formattedIdealTotal = ref(0);

const fibFormattedRealTotal = ref(0);
const fibEngineerCount = ref(0);

const temFormattedRealTotal = ref(0);
const temEngineerCount = ref(0);

const disableFuture = (date) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return date.getTime() > today.getTime()
}

// 柱状图配置
const barChartOption = reactive({
  // title: {
  //   text: "一周人员平均饱和度",
  // },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "shadow",
    },
    // // tooltip 中对饱和度追加 % 符号
    // formatter: (params) => {
    //   if (!Array.isArray(params)) return params;
    //   return params
    //     .map((p) => {
    //       if (p && p.seriesName === "饱和度") {
    //         return `${p.seriesName}: ${p.value}%`;
    //       }
    //       return `${p.seriesName}: ${p.value}`;
    //     })
    //     .join("<br/>");
    // },
  },
  legend: {
    data: ["平均饱和度"],
  },
  xAxis: {
    type: "category",
    data: ["FIB","TEM"],
  },
  yAxis: [
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
      name: "平均饱和度",
      type: "bar",
      data: [],
      itemStyle: { color: "#0080FF" },
      // 柱顶显示数值
      label: {
        show: true,
        position: "top",
        fontSize: 16,
        formatter: "{c}%",
      },
    }
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
    const fibResponse = await fibSaturationApi.getData(params);
    const temResponse = await temSaturationApi.getData(params);
    if (fibResponse && temResponse) {
      // 赋值
      barChartOption.series[0].data = [fibResponse.statistics.core_index,temResponse.statistics.core_index]; // 平均饱和率

      fibFormattedRealTotal.value = fibResponse.statistics.total_success_count;
      fibEngineerCount.value = fibResponse.statistics.involved_engineer_count;

      temFormattedRealTotal.value = temResponse.statistics.total_success_count;
      temEngineerCount.value = temResponse.statistics.involved_engineer_count;

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
.completion {
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
  .summary-card.green .summary-value {
    color: #67c23a;
  }
  .summary-card.red .summary-value {
    color: #f56c6c;
  }
  .summary-card.blue .summary-value {
    color: #409eff;
  }

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
