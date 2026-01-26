<template>
  <div class="fib-completion">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>FIB客户样点外部成功率</span>
          <el-select 
            v-model="currentType" 
            placeholder="请选择客户" 
            class="type-select" 
            @change="handleTypeChange" 
          >
            <el-option label="五角场" value="五角场"></el-option>
            <el-option label="中科路" value="中科路"></el-option>
            <el-option label="洋山港" value="洋山港"></el-option>
            <el-option label="新场镇" value="新场镇"></el-option>
          </el-select>
          <div class="header-actions">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              @change="handleDateChange" 
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
            <h3>FIB客户样点外部成功率</h3>
            <EChart :option="barChartOption" height="560px" />
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
import { ref, reactive, computed, onMounted } from "vue";
import EChart from "@/components/EChart.vue";
import { fibCustomerSampleSuccessApi } from "@/api/analysis";
import { useDateRangeStore } from "@/stores/dateRange";

const dateRangeStore = useDateRangeStore();
const dateRange = computed({
  get: () => dateRangeStore.dateRange,
  set: (val) => dateRangeStore.setDateRange(val)
});
// summary 数据
const formattedSuccessTotal = ref(0);
const formattedFailTotal = ref(0);
const avgRate = ref("0%");

const disableFuture = (date) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return date.getTime() > today.getTime()
}

// 当前选中的类型变量（默认选中"总成功"）
const currentType = ref('五角场');
// 新增单独的类型切换方法，避免递归
const handleTypeChange = () => {
  fetchData();
};
// 新增单独的日期切换方法，避免递归
const handleDateChange = () => {
  fetchData();
};

// 柱状图配置
const barChartOption = reactive({
  // title: {
  //   text: "一周样点成功率",
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
      // 柱内显示数值
      label: {
        show: true,
        position: "inside",
        fontSize: 14,
        color: "#303133",
      },
    },
    {
      name: "完成数",
      type: "bar",
      data: [],
      itemStyle: { color: "#0080FF" },
      label: {
        show: true,
        position: "inside",
        fontSize: 14,
        color: "#303133",
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
        formatter: "{c}%",
        offset: [0, -6],
        color: "#303133",
        // padding: [2, 6],
        borderRadius: 4,
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
      customer: currentType.value,
    };
    // 统一使用 fibCustomerSampleSuccessApi 接口
    const response = await fibCustomerSampleSuccessApi.getData(params);
    
    if (response) {
      const {
        dates,
        daily_success_counts,
        daily_completed_counts,
        daily_success_rates,
        actual_total_completed,
        actual_total_success,
      } = response;
      console.log("接口返回数据：", response);
      // 赋值
      barChartOption.xAxis.data = dates; // 日期
      barChartOption.series[0].data = daily_success_counts; // 成功数
      barChartOption.series[1].data = daily_completed_counts; // 完成数
      barChartOption.series[2].data = daily_success_rates; // 成功率
      // 计算并写入 summary refs（防止直接覆盖变量）
      const successSum = daily_success_counts.reduce((acc, cur) => acc + cur, 0);
      const completedSum = daily_completed_counts.reduce((acc, cur) => acc + cur, 0);
      formattedSuccessTotal.value = response.actual_total_success; // 成功总和
      formattedFailTotal.value = response.actual_total_completed - response.actual_total_success; // 失败总和
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
.fib-completion {
  .card-header {
    display: flex;
    align-items: center; // 垂直居中
    font-weight: bold;
    font-size: 16px;
    gap: 0; // 清除默认间距，让元素紧贴

    // 标题
    > span {
      margin-right: auto; 
    }

    // 下拉框
    .type-select {
      width: 160px; 
      margin-right: 8px; // 间距
      margin-left: 0;
      .el-input__wrapper {
        height: 32px;
        line-height: 32px;
      }
    }

    // 日期+按钮区域
    .header-actions {
      display: flex;
      align-items: center;
      gap: 0; 
    }
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
