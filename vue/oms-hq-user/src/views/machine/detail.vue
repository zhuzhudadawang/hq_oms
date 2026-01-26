<template>
  <div class="machine-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-button icon="ArrowLeft" @click="goBack">返回</el-button>
          <span>机台耗时详情</span>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="设备编码">{{ machineInfo.device_code }}</el-descriptions-item>
        <!-- <el-descriptions-item label="订单状态">
          <el-tag :type="getStatusType(machineInfo.status)">{{ machineInfo.order_status }}</el-tag>
        </el-descriptions-item> -->
        <el-descriptions-item label="机台">{{ machineInfo.machine_name }}</el-descriptions-item>
        <el-descriptions-item label="使用类型">{{ machineInfo.usage_type }}</el-descriptions-item>
        <el-descriptions-item label="耗时(min)">{{ machineInfo.duration_minutes }}</el-descriptions-item>
        <el-descriptions-item label="开始时间">{{ machineInfo.start_time }}</el-descriptions-item>
        <el-descriptions-item label="结束时间">{{ machineInfo.end_time }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ machineInfo.creator_name }}</el-descriptions-item>
        <!-- <el-descriptions-item label="创建时间">{{ machineInfo.create_time }}</el-descriptions-item> -->
        <!-- <el-descriptions-item label="更新时间">{{ machineInfo.modify_time }}</el-descriptions-item> -->
        <!-- <el-descriptions-item label="备注" :span="2">{{ machineInfo.remark || '无' }}</el-descriptions-item> -->
      </el-descriptions>
    </el-card>

    <el-card style="margin-top: 20px;">
      <template #header>
        <span>机台耗时流程</span>
      </template>
      <el-steps :active="activeStep" align-center>
        <el-step title="机台耗时创建" :description="machineInfo.createTime" />
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
import { getMachineDetail} from '@/api/machine'
import { id } from 'element-plus/es/locales.mjs'
const router = useRouter()
const route = useRoute()

const activeStep = ref(4)

// 机台耗时详情数据
const machineInfo = ref({})

const getStatusType = (status) => {
  const statusMap = {
    '已完成': 'success',
    '处理中': 'warning',
    '待付款': 'danger',
    '已取消': 'info'
  }
  return statusMap[status] || 'info'
}

const goBack = () => {
  router.back()
}

//获取机台耗时详情
const fetchMachineDetail = async () => {
  const id = route.params.record_id
  const response = await getMachineDetail(id)
  machineInfo.value = response
}

// 页面加载时获取数据
onMounted(() => {
  fetchMachineDetail();
});

</script>

<style lang="scss" scoped>
.machine-detail {
  .card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: bold;
    font-size: 16px;
  }
}
</style>
