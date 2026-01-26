<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6" v-for="item in stats" :key="item.title">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-title">{{ item.title }}</div>
              <div class="stat-value">{{ item.value }}</div>
            </div>
            <div class="stat-icon" :style="{ backgroundColor: item.color }">
              <el-icon :size="30">
                <component :is="item.icon" />
              </el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近订单</span>
            </div>
          </template>
          <el-table :data="recentOrders" style="width: 100%">
            <el-table-column prop="orderNo" label="订单号" width="150" />
            <el-table-column prop="customer" label="客户" width="120" />
            <el-table-column prop="amount" label="金额" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>待办事项</span>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(item, index) in todos"
              :key="index"
              :timestamp="item.timestamp"
              placement="top"
            >
              {{ item.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const stats = ref([
  {
    title: '总订单',
    value: '1,258',
    icon: 'ShoppingCart',
    color: '#409eff'
  },
  {
    title: '待处理',
    value: '46',
    icon: 'Clock',
    color: '#e6a23c'
  },
  {
    title: '总客户',
    value: '328',
    icon: 'User',
    color: '#67c23a'
  },
  {
    title: '总收入',
    value: '¥256,890',
    icon: 'TrendCharts',
    color: '#f56c6c'
  }
])

const recentOrders = ref([
  {
    orderNo: 'ORD20231013001',
    customer: '张三',
    amount: '¥1,280',
    status: '已完成'
  },
  {
    orderNo: 'ORD20231013002',
    customer: '李四',
    amount: '¥3,560',
    status: '处理中'
  },
  {
    orderNo: 'ORD20231013003',
    customer: '王五',
    amount: '¥890',
    status: '待付款'
  },
  {
    orderNo: 'ORD20231013004',
    customer: '赵六',
    amount: '¥2,100',
    status: '已完成'
  }
])

const todos = ref([
  {
    content: '处理订单 ORD20231013002',
    timestamp: '2025-10-13 10:30'
  },
  {
    content: '联系客户张三确认收货',
    timestamp: '2025-10-13 11:00'
  },
  {
    content: '更新产品库存信息',
    timestamp: '2025-10-13 14:00'
  }
])

const getStatusType = (status) => {
  const statusMap = {
    '已完成': 'success',
    '处理中': 'warning',
    '待付款': 'danger'
  }
  return statusMap[status] || 'info'
}
</script>

<style lang="scss" scoped>
.dashboard {
  .stat-card {
    .stat-content {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .stat-info {
        .stat-title {
          font-size: 14px;
          color: #909399;
          margin-bottom: 10px;
        }

        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: #303133;
        }
      }

      .stat-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
      }
    }
  }

  .card-header {
    font-weight: bold;
    font-size: 16px;
  }
}
</style>
