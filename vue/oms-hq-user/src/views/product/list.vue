<template>
  <div class="product-list">
    <el-card>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="产品名称">
          <el-input v-model="searchForm.name" placeholder="请输入产品名称" clearable />
        </el-form-item>
        <el-form-item label="产品分类">
          <el-select v-model="searchForm.category" placeholder="请选择分类" clearable>
            <el-option label="全部" value="" />
            <el-option label="电子产品" value="电子产品" />
            <el-option label="办公用品" value="办公用品" />
            <el-option label="配件" value="配件" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleSearch">搜索</el-button>
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
          <el-button type="success" icon="Plus" @click="handleAdd">新增产品</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="产品名称" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="price" label="价格" width="120" />
        <el-table-column prop="stock" label="库存" width="100" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === '在售' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" icon="Edit" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" icon="Delete" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const loading = ref(false)

const searchForm = reactive({
  name: '',
  category: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 50
})

const tableData = ref([
  {
    id: 1,
    name: '笔记本电脑',
    category: '电子产品',
    price: '¥6,400',
    stock: 50,
    unit: '台',
    status: '在售',
    createTime: '2025-10-01 10:30:00'
  },
  {
    id: 2,
    name: '机械键盘',
    category: '配件',
    price: '¥680',
    stock: 120,
    unit: '个',
    status: '在售',
    createTime: '2025-10-02 14:20:00'
  },
  {
    id: 3,
    name: '显示器',
    category: '电子产品',
    price: '¥2,890',
    stock: 30,
    unit: '台',
    status: '在售',
    createTime: '2025-10-03 09:15:00'
  },
  {
    id: 4,
    name: 'A4纸',
    category: '办公用品',
    price: '¥25',
    stock: 500,
    unit: '包',
    status: '在售',
    createTime: '2025-10-04 11:00:00'
  }
])

const handleSearch = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    ElMessage.success('搜索完成')
  }, 500)
}

const handleReset = () => {
  searchForm.name = ''
  searchForm.category = ''
  handleSearch()
}

const handleAdd = () => {
  ElMessage.info('新增产品功能')
}

const handleEdit = (row) => {
  ElMessage.info('编辑产品: ' + row.name)
}

const handleDelete = (row) => {
  ElMessage.info('删除产品: ' + row.name)
}
</script>

<style lang="scss" scoped>
.product-list {
  .search-form {
    margin-bottom: 20px;
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
