<template>
  <div class="business-page">
    <h1>核心运营指标表</h1>
    <el-card class="development-card">
      <div class="development-content">
        <el-icon size="48" color="#909399"><InfoFilled /></el-icon>
        <h3>页面开发中</h3>
        <p>核心运营指标表功能正在紧张开发中，敬请期待...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { InfoFilled } from '@element-plus/icons-vue'
</script>

<style scoped>
.business-page {
  padding: 20px;
}

.development-card {
  margin-top: 20px;
  text-align: center;
  padding: 40px 0;
}

.development-content h3 {
  margin: 16px 0 8px;
  color: #606266;
}

.development-content p {
  color: #909399;
  margin: 0;
}
</style>
