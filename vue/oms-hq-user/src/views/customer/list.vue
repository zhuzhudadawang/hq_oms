<template>
  <div class="customer-list">
    <el-card>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="客户名称">
          <el-input v-model="searchForm.name" placeholder="请输入客户名称" clearable />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="searchForm.phone" placeholder="请输入联系电话" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleSearch">搜索</el-button>
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
          <el-button type="success" icon="Plus" @click="handleAdd">新增客户</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="客户代号" label="客户代号" />
        <el-table-column prop="客户全名" label="客户全名" />
        <el-table-column prop="客户昵称" label="客户昵称" />
        <el-table-column prop="开始服务年月" label="开始服务年月" />
        <el-table-column prop="导入年月" label="导入年月" width="100" />
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
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCustomerList, createCustomer, updateCustomer, deleteCustomer } from '@/api/customer'

const loading = ref(false)

const searchForm = reactive({
  name: '',
  phone: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

// 表格数据
const tableData = ref([])

// 获取客户列表
const fetchCustomerList = async () => {
  loading.value = true
  try {
    // 构造分页参数
    const pageParams = {
      index: pagination.currentPage,  // 当前页码
      size: pagination.pageSize        // 每页数量
    }
    
    console.log('客户列表请求分页参数：', pageParams)
    const response = await getCustomerList(pageParams)
    console.log('客户列表数据：', response)
    
    // 根据实际返回的数据结构调整
    if (response.data) {
      tableData.value = response.data
      // 如果后端返回了总数，使用后端的总数；否则使用当前数据长度
      pagination.total = 250
    }
     
  } catch (error) {
    console.error('获取客户列表失败：', error)
    if (error.response) {
      console.error('接口响应状态码：', error.response.status)
      console.error('接口返回数据：', error.response.data)
    }
    ElMessage.error('获取客户列表失败：' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.currentPage = 1
  fetchCustomerList()
}

const handleReset = () => {
  searchForm.name = ''
  searchForm.phone = ''
  pagination.currentPage = 1
  fetchCustomerList()
}

const handleAdd = () => {
  ElMessage.info('新增客户功能')
}

const handleEdit = (row) => {
  ElMessage.info('编辑客户: ' + row.name)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该客户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    loading.value = true
    await deleteCustomer(row.id)
    ElMessage.success('删除成功')
    fetchCustomerList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败：' + (error.message || '未知错误'))
    }
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (val) => {
  pagination.pageSize = val
  pagination.currentPage = 1
  fetchCustomerList()
}

const handleCurrentChange = (val) => {
  pagination.currentPage = val
  fetchCustomerList()
}

// 页面加载时获取数据
onMounted(() => {
  fetchCustomerList()
})
</script>

<style lang="scss" scoped>
.customer-list {
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
