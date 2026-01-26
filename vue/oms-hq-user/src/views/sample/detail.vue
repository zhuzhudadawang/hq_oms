<template>
  <div class="sample-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button icon="ArrowLeft" @click="goBack">返回</el-button>
          <span>样点详情</span>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="样点编号">{{ sampleInfo.sample_id }}</el-descriptions-item>
        <el-descriptions-item label="样点状态">
          <el-tag :type="getStatusType(sampleInfo.status)">{{ sampleInfo.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="客户名称">{{ sampleInfo.customer_name }}</el-descriptions-item>
        <el-descriptions-item label="客户样点编号">{{ sampleInfo.customer_sample_id }}</el-descriptions-item>
        <el-descriptions-item label="样点数量">{{ sampleInfo.sample_quantity }}</el-descriptions-item>
        <el-descriptions-item label="时效要求(h)">{{ sampleInfo.sample_validity_hours }}</el-descriptions-item>
        <el-descriptions-item label="关联订单">{{ sampleInfo.order_id }}</el-descriptions-item>
        <el-descriptions-item label="接收时间">{{ sampleInfo.receive_time }}</el-descriptions-item>
        <el-descriptions-item label="交期日期">{{ sampleInfo.delivery_date }}</el-descriptions-item>
        <!-- <el-descriptions-item label="更新时间">{{ sampleInfo.modify_time }}</el-descriptions-item> -->
        <!-- <el-descriptions-item label="备注" :span="2">{{ sampleInfo.remark || '无' }}</el-descriptions-item> -->
      </el-descriptions>
    </el-card>

    <el-card style="margin-top: 20px;">
      <template #header>
        <span>样点流程</span>
      </template>
      <el-steps :active="activeStep" align-center>
        <el-step title="样点创建" :description="sampleInfo.createTime" />
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
import { getSampleDetail} from '@/api/sample.js'
import { id } from 'element-plus/es/locales.mjs'
const router = useRouter()
const route = useRoute()

const activeStep = ref(4)

// 样点详情数据
const sampleInfo = ref({})

const getStatusType = (status) => {
  const statusMap = {
    '已完成': 'success',
    '待开始': 'danger',
    '已设定工序': 'info',
    '设定工序中': 'warning',
    '等待设定工序': 'default'
  }
  return statusMap[status] || 'info'
}

const goBack = () => {
  router.back()
}

//获取样点详情
const fetchSampleDetail = async () => {
  const id = route.params.sample_id
  const response = await getSampleDetail(id)
  sampleInfo.value = response
}

// 页面加载时获取数据
onMounted(() => {
  fetchSampleDetail();
});

</script>

<style lang="scss" scoped>
.sample-detail {
  .card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: bold;
    font-size: 16px;
  }
}
</style>
