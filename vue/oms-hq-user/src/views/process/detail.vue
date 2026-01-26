<template>
  <div class="process-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button icon="ArrowLeft" @click="goBack">返回</el-button>
          <span>工序详情</span>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="工序编号">{{ processInfo.process_id }}</el-descriptions-item>
        <el-descriptions-item label="工序状态">
          <el-tag :type="getStatusType(processInfo.status)">{{ processInfo.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="客户名称">{{ processInfo.customer }}</el-descriptions-item>
        <el-descriptions-item label="检测项目">{{ processInfo.test_item }}</el-descriptions-item>
        <el-descriptions-item label="工序类别">{{ processInfo.process_category }}</el-descriptions-item>
        <el-descriptions-item label="关联样点">{{ processInfo.sample_id }}</el-descriptions-item>
        <el-descriptions-item label="样点时效(h)">{{ processInfo.sample_validity_hours }}</el-descriptions-item>
        <el-descriptions-item label="是否委外">{{ processInfo.is_outsource }}</el-descriptions-item>
        <el-descriptions-item label="样点接收日期">{{ processInfo.sample_receive_date }}</el-descriptions-item>
        <!-- <el-descriptions-item label="更新时间">{{ processInfo.modify_time }}</el-descriptions-item> -->
        <!-- <el-descriptions-item label="备注" :span="2">{{ processInfo.remark || '无' }}</el-descriptions-item> -->
      </el-descriptions>
    </el-card>

    <el-card style="margin-top: 20px;">
      <template #header>
        <span>工序流程</span>
      </template>
      <el-steps :active="activeStep" align-center>
        <el-step title="工序创建" :description="processInfo.createTime" />
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
import {getProcessDetail} from '@/api/process'
const router = useRouter()
const route = useRoute()

const activeStep = ref(4)

// 工序详情数据
const processInfo = ref({})

const getStatusType = (status) => {
   const statusMap = {
    '成功': 'success',
    '失败': 'danger',
    '返工返序': 'danger',
    '检测中': 'info',
    '等待委外工序': 'warning',
    '等待工程师执行': 'warning',
    '等待质审核工序': 'warning',
    '等待分配工序': 'default'
  }
  return statusMap[status] || 'info'
}

const goBack = () => {
  router.back()
}

//获取工序详情
const fetchProcessDetail = async () => {
  const id = route.params.process_id
  const response = await getProcessDetail(id)
  processInfo.value = response
}

// 页面加载时获取数据
onMounted(() => {
  fetchProcessDetail();
});

</script>

<style lang="scss" scoped>
.process-detail {
  .card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: bold;
    font-size: 16px;
  }
}
</style>
