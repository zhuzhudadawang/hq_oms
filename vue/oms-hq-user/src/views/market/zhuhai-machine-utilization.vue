<template>
  <div class="market-zhuhai-machine-utilization">
    <el-card class="chart-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>珠海机台利用率统计</span>
          <div class="header-actions">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              size="small"
              unlink-panels
              value-format="YYYY-MM-DD"
              :disabled-date="disableFuture"
              @change="handleDateChange"
            />
            <el-button
              type="primary"
              size="small"
              @click="refresh"
              :loading="loading"
            >
              刷新
            </el-button>
          </div>
        </div>
      </template>

      <EChart :option="chartOption" height="440px" />

      <el-row :gutter="16" class="summary-row">
        <el-col :xs="24" :sm="6">
          <div class="summary-card primary">
            <div class="summary-label">平均利用率</div>
            <div class="summary-value">{{ summary.average }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="6">
          <div class="summary-card info">
            <div class="summary-label">峰值机台</div>
            <div class="summary-value">{{ summary.peakMachine }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="6">
          <div class="summary-card accent">
            <div class="summary-label">峰值利用率</div>
            <div class="summary-value">{{ summary.peakValue }}</div>
          </div>
        </el-col>
        <el-col :xs="24" :sm="6">
          <div class="summary-card highlight">
            <div class="summary-label">≥85%机台数</div>
            <div class="summary-value">{{ summary.highCount }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import EChart from "@/components/EChart.vue";
import { marketAnalysisApi } from "@/api/market";
import { useDateRangeStore } from "@/stores/dateRange";

const loading = ref(false);

const chartOption = ref(buildChartOption([], [], [], []));

const summary = reactive({
  average: "0.0%",
  peakMachine: "-",
  peakValue: "0.0%",
  highCount: "0",
});

const HIGH_THRESHOLD = 85;
const DEFAULT_LENGTH = 6;
const dateRangeStore = useDateRangeStore();
const dateRange = computed({
  get: () => dateRangeStore.dateRange,
  set: (val) => dateRangeStore.setDateRange(val)
});

const DEFAULT_DATA = {
  categories: ["TEM-01", "TEM-02", "FIB-01", "FIB-02", "SEM-01", "SEM-02"],
  actual: [82.5, 88.3, 91.2, 76.4, 84.8, 79.1],
  target: [85, 85, 90, 85, 85, 80],
  compare: [78.3, 82.1, 89.5, 72.6, 80.2, 75.4],
};

const fetchData = async () => {
  loading.value = true;
  try {
    const params = buildQueryParams(dateRange.value);
    const payload = await marketAnalysisApi.getZhuhaiMachineUtilization(params);
    console.log("珠海机台利用率数据获取成功。", payload);
    const normalized = normalizePayload(payload);
    if (!normalized) throw new Error("invalid-payload");
    applyData(normalized);
  } catch (error) {
    console.warn("珠海机台利用率数据获取失败，使用示例数据。", error);
    // applyData(DEFAULT_DATA);
  } finally {
    loading.value = false;
  }
};

const normalizePayload = (payload) => {
  if (!payload || typeof payload !== "object") return null;

  const rawCategories =
    payload.machines ||
    payload.machine_names ||
    payload.labels ||
    payload.names ||
    payload.categories ||
    payload.xAxis ||
    [];
  const categories = normalizeCategories(rawCategories);

  const actual = normalizeRates(
    payload.utilization ||
      payload.actual ||
      payload.actual_rate ||
      payload.actualRates ||
      payload.actuals ||
      []
  );

  const targetSource =
    payload.target ||
    payload.target_rate ||
    payload.targetRates ||
    payload.targets ||
    [];
  // compare 是工作时间（小时），不是百分比，直接取值不做转换
  const compareRaw = payload.compare || payload.history || [];
  const compare = Array.isArray(compareRaw) 
    ? compareRaw.map(v => {
        const num = Number(v);
        return Number.isFinite(num) ? num : 0;
      }) 
    : [];
  let target = [];
  if (Array.isArray(targetSource)) {
    target = normalizeRates(targetSource);
  } else if (
    targetSource !== undefined &&
    targetSource !== null &&
    targetSource !== ""
  ) {
    const single = normalizeRates([targetSource]);
    if (single.length) {
      target = single;
    }
  }

  const size = Math.max(
    categories.length,
    actual.length,
    target.length,
    compare.length
  );
  if (!size) return null;

  const resolvedCategories = categories.length
    ? categories
    : generateDefaultMachines(size);
  const resolvedActual = ensureLength(actual, size);
  const resolvedCompare = ensureLength(compare, size);
  const targetFill = target.length ? target[target.length - 1] : HIGH_THRESHOLD;
  const resolvedTarget = target.length
    ? ensureLength(target, size, targetFill)
    : Array(size).fill(HIGH_THRESHOLD);

  return composeResult(
    resolvedCategories,
    resolvedActual,
    resolvedTarget,
    resolvedCompare
  );
};

const normalizeCategories = (list) => {
  if (!Array.isArray(list)) return [];
  return list
    .map((item) => {
      if (item === null || item === undefined) return "";
      return String(item).trim();
    })
    .filter(Boolean);
};

const normalizeRates = (values) => {
  if (!Array.isArray(values)) return [];
  const numbers = values.map((value) => {
    if (value === null || value === undefined) return 0;
    const text = String(value).replace(/%/g, "").trim();
    const num = Number(text);
    return Number.isFinite(num) ? num : 0;
  });
  return numbers.map((val) => {
    if (!Number.isFinite(val)) return 0;
    if (Math.abs(val) <= 1.5) {
      return Number((val * 100).toFixed(1));
    }
    return Number(val.toFixed(1));
  });
};

const composeResult = (categories, actual, target, compare) => {
  const length = Math.min(
    categories.length,
    actual.length,
    target.length,
    compare.length
  );
  if (!length) return null;
  const resolvedCategories = categories.slice(0, length).map((value, index) => {
    const text = String(value || "").trim();
    return text || `机台${index + 1}`;
  });
  const resolvedActual = actual
    .slice(0, length)
    .map((value) => toNumber(value));
  const resolvedTarget = target
    .slice(0, length)
    .map((value) => toNumber(value));
  const resolvedCompare = compare
    .slice(0, length)
    .map((value) => toNumber(value));
  if (!resolvedActual.some((val) => Number.isFinite(val))) return null;
  return {
    categories: resolvedCategories,
    actual: resolvedActual,
    target: resolvedTarget,
    compare: resolvedCompare,
  };
};

const ensureLength = (list, length, fillValue = 0) => {
  const fallback = toNumber(fillValue);
  const result = [];
  for (let i = 0; i < length; i += 1) {
    const source = list[i];
    const value =
      source === undefined || source === null || source === ""
        ? fallback
        : toNumber(source);
    result.push(Number.isFinite(value) ? value : fallback);
  }
  return result;
};

const toNumber = (value) => {
  const num = Number(value);
  return Number.isFinite(num) ? Number(num.toFixed(1)) : 0;
};

const applyData = ({ categories, actual, target, compare }) => {
  chartOption.value = buildChartOption(categories, actual, target, compare);

  const sum = target.reduce((acc, cur) => acc + (Number(cur) || 0), 0);
  const avg = target.length ? sum / target.length : 0;
  summary.average = formatPercent(avg);

  if (target.length) {
    const peakIndex = target.reduce(
      (best, current, index) => (current > target[best] ? index : best),
      0
    );
    summary.peakMachine = categories[peakIndex] || "-";
    summary.peakValue = formatPercent(target[peakIndex]);
  } else {
    summary.peakMachine = "-";
    summary.peakValue = "0.0%";
  }

  const highCount = target.filter(
    (value) => Number(value) >= HIGH_THRESHOLD
  ).length;
  summary.highCount = String(highCount);
};

const formatPercent = (value) => {
  const num = Number(value);
  if (!Number.isFinite(num)) return "0.0%";
  return `${num.toFixed(1)}%`;
};

const refresh = () => {
  fetchData();
};

const handleDateChange = (value) => {
  if (value && value.length === 2) {
    dateRange.value = value;
    fetchData();
  } else {
    dateRangeStore.resetToCurrentWeek();
    fetchData();
  }
};

const disableFuture = (date) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  return date.getTime() > today.getTime();
};

onMounted(fetchData);

function buildQueryParams(range) {
  if (!Array.isArray(range) || range.length !== 2) return {};
  const [start, end] = range;
  return {
    start_date: formatDate(start),
    end_date: formatDate(end),
  };
}

function getDefaultRange() {
  const today = new Date();
  today.setHours(0, 0, 0, 0); // 将时间部分清零

  const dayOfWeek = today.getDay(); // 0 (周日) 到 6 (周六)

  // 计算本周一的日期
  const daysToSubtract = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
  const start = new Date(today);
  start.setDate(today.getDate() - daysToSubtract);

  // 计算本周日的日期
  const end = new Date(start);
  end.setDate(start.getDate() + 6);

  return [start, end];
}

function formatDate(raw) {
  const date = new Date(raw);
  if (Number.isNaN(date.getTime())) return "";
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function generateDefaultMachines(length) {
  const safeLength =
    Number.isFinite(length) && length > 0 ? Math.floor(length) : DEFAULT_LENGTH;
  return Array.from({ length: safeLength }, (_, idx) => `机台${idx + 1}`);
}

function buildChartOption(categories, actual, target, compare) {
  const rotate = categories.length > 7 ? 30 : 0;
  return {
    tooltip: {
      trigger: "axis",
      formatter: (params) => {
        if (!Array.isArray(params)) return "";
        const lines = params.map((item) => {
          const value = Number(item.value);
          const display = Number.isFinite(value) ? `${value.toFixed(1)}%` : "-";
          return `${item.marker}${item.seriesName}: ${display}`;
        });
        return [`${params[0]?.axisValue || ""}`].concat(lines).join("<br />");
      },
    },
    legend: {
      data: ["可用工作时间", "实际工作时间", "利用率"],
    },
    grid: {
      top: 60,
      left: "4%",
      right: "4%",
      bottom: rotate ? 64 : 36,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      data: categories,
      axisTick: {
        alignWithLabel: true,
      },
      axisLabel: {
        interval: 0,
        rotate,
      },
    },
    yAxis: [
      {
        type: "value",
        name: "数量",
        min: 0,
        max: (value) => {
          const source = Number(value.max) || 0;
          const padded = Math.ceil((source + 5) / 10) * 10;
          return Math.min(Math.max(padded, 100), 120);
        },
        axisLabel: {
          formatter: "{value}",
        },
      },
      {
        type: "value",
        name: "利用率",
        position: "right", // 放置在右侧
        min: 0,
        max: (value) => {
          const source = Number(value.max) || 0;
          const padded = Math.ceil((source + 5) / 10) * 10;
          return Math.min(Math.max(padded, 100), 120);
        },
        axisLabel: {
          formatter: "{value}%", // 不显示 %
        },
      },
    ],
    series: [
      {
        name: "可用工作时间",
        type: "bar",
        yAxisIndex: 0,
        barWidth: 32,
        itemStyle: {
          color: "#409EFF",
        },
        label: {
          show: true,
          position: "top",
          formatter: ({ value }) => {
            const num = Number(value);
            return Number.isFinite(num) ? `${num.toFixed(1)}` : "-";
          },
        },
        data: actual,
      },
      {
        name: "实际工作时间",
        yAxisIndex: 0,
        type: "bar",
        barWidth: 32,
        itemStyle: {
          // 使用不同的颜色加以区分
          color: "#67C23A",
        },
        label: {
          show: true,
          position: "top",
          formatter: ({ value }) => {
            const num = Number(value);
            return Number.isFinite(num) ? `${num.toFixed(1)}` : "-";
          },
        },
        data: compare,
      },
      {
        name: "利用率",
        yAxisIndex: 1,
        type: "line",
        smooth: true,
        symbol: "circle",
        symbolSize: 8,
        lineStyle: {
          width: 3,
          color: "#F56C6C",
        },
        itemStyle: {
          color: "#F56C6C",
        },
        label: {
          show: true,
          formatter: ({ value }) => {
            const num = Number(value);
            return Number.isFinite(num) ? `${num.toFixed(1)}%` : "-%";
          },
        },
        data: target,
      },
    ],
  };
}
</script>

<style lang="scss" scoped>
.market-zhuhai-machine-utilization {
  .alert {
    margin-bottom: 20px;
  }

  .chart-card {
    min-height: 460px;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-weight: 600;

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }

  .summary-row {
    margin-top: 18px;
  }

  .summary-card {
    border-radius: 10px;
    padding: 16px 20px;
    background: #f7f9fc;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 90px;
    box-shadow: inset 0 0 0 1px rgba(64, 158, 255, 0.08);

    &.primary {
      box-shadow: inset 0 0 0 1px rgba(64, 158, 255, 0.18);
    }

    &.info {
      box-shadow: inset 0 0 0 1px rgba(103, 194, 58, 0.2);
    }

    &.accent {
      box-shadow: inset 0 0 0 1px rgba(255, 153, 0, 0.24);
    }

    &.highlight {
      box-shadow: inset 0 0 0 1px rgba(255, 87, 34, 0.22);
    }

    .summary-label {
      font-size: 13px;
      color: #909399;
      margin-bottom: 6px;
    }

    .summary-value {
      font-size: 26px;
      font-weight: 700;
      color: #303133;
    }
  }
}
</style>
