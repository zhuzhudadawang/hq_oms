<template>
  <div class="order-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button icon="ArrowLeft" @click="goBack">返回</el-button>
          <span>订单详情</span>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单号">{{ orderInfo.order_id }}</el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusType(orderInfo.order_status)">{{ orderInfo.order_status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="客户名称">{{ orderInfo.customer }}</el-descriptions-item>
        <el-descriptions-item label="客户需求">{{ orderInfo.customer_requirement }}</el-descriptions-item>
        <el-descriptions-item label="样点数量">{{ orderInfo.sample_quantity }}</el-descriptions-item>
        <el-descriptions-item label="时效要求(h)">{{ orderInfo.validity_requirement_hours }}</el-descriptions-item>
        <el-descriptions-item label="执行地">{{ orderInfo.execution_place }}</el-descriptions-item>
        <el-descriptions-item label="订单销售">{{ orderInfo.order_salesman }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ orderInfo.create_time }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ orderInfo.modify_time }}</el-descriptions-item>
        <!-- <el-descriptions-item label="备注" :span="2">{{ orderInfo.remark || '无' }}</el-descriptions-item> -->
      </el-descriptions>
    </el-card>

    <el-card style="margin-top: 20px;">
      <template #header>
        <span>订单流程</span>
      </template>
      <el-steps :active="activeStep" align-center>
        <el-step title="订单创建" :description="orderInfo.createTime" />
        <el-step title="待付款" description="2025-10-13 10:35:00" />
        <el-step title="处理中" description="2025-10-13 11:00:00" />
        <el-step title="已完成" description="2025-10-13 15:30:00" />
      </el-steps>
    </el-card>
  </div>
</template>

<script setup>
import { ref,onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getOrderDetail } from '@/api/order'
import { id } from 'element-plus/es/locales.mjs'
const router = useRouter()
const route = useRoute()

const activeStep = ref(4)

// 订单详情数据
const orderInfo = ref({})

const getStatusType = (status) => {
  const statusMap = {
    '已结案': 'success',
    '同意': 'success',
    '已生成对账单': 'warning',
    '拒绝': 'danger',
    '等待结案': 'info',
    '待审核订单': 'default'
  }
  return statusMap[status] || 'info'
}

const goBack = () => {
  router.back()
}

//获取订单详情
const fetchOrderDetail = async () => {
  const id = route.params.order_id
  const response = await getOrderDetail(id)
  orderInfo.value = response
}

// 页面加载时获取数据
onMounted(() => {
  fetchOrderDetail();
});

</script>

<style lang="scss" scoped>
.order-detail {
  .card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: bold;
    font-size: 16px;
  }
}
</style>
