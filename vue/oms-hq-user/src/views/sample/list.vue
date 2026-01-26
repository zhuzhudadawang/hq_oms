<template>
  <div class="sample-list">
    <el-card>
      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="样点编号">
          <el-input
            v-model="searchForm.sample_id"
            placeholder="请输入样点编号"
            clearable
          />
        </el-form-item>
        <el-form-item label="客户名称">
          <el-input
            v-model="searchForm.customer_name"
            placeholder="请输入客户名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="样点状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="全部" value="" />
            <el-option label="已完成" value="已完成" />
            <el-option label="待开始" value="待开始" />
            <el-option label="已设定工序" value="已设定工序" />
            <el-option label="设定工序中" value="设定工序中" />
            <el-option label="等待设定工序" value="等待设定工序" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleSearch"
            >搜索</el-button
          >
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
          <el-button type="success" icon="Plus" @click="handleAdd"
            >新增样点</el-button
          >
        </el-form-item>
      </el-form>

      <!-- 表格区域 -->
      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="sample_id" label="样点编号" width="150" />
        <el-table-column prop="customer_name" label="客户名称" width="120" />
        <el-table-column prop="customer_sample_id" label="客户样点编号" />
        <el-table-column prop="sample_quantity" label="样点数量" width="80" />
        <el-table-column
          prop="sample_validity_hours"
          label="时效要求(h)"
          width="120"
        />
        <el-table-column prop="status" label="样点状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="order_id" label="关联订单" width="160" />
        <el-table-column prop="receive_time" label="接收时间" width="160" />
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              icon="View"
              @click="handleView(row)"
              >查看</el-button
            >
            <el-button
              type="warning"
              size="small"
              icon="Edit"
              @click="handleEdit(row)"
              >编辑</el-button
            >
            <el-button
              type="danger"
              size="small"
              icon="Delete"
              @click="handleDelete(row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
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

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="样点编号" prop="sample_id">
          <el-input v-model="form.sample_id" placeholder="请输入样点编号" />
        </el-form-item>
        <el-form-item label="客户名称" prop="customer_name">
          <el-input v-model="form.customer_name" placeholder="请输入客户名称" />
        </el-form-item>
        <el-form-item label="客户样点编号" prop="customer_sample_id">
          <el-input v-model="form.customer_sample_id" placeholder="请输入客户样点编号" />
        </el-form-item>
        <el-form-item label="样点数量" prop="sample_quantity">
          <el-input-number v-model="form.sample_quantity" placeholder="请输入样点数量"/>
        </el-form-item>
         <el-form-item label="样点时效(h)" prop="sample_validity_hours">
          <el-input-number v-model="form.sample_validity_hours" placeholder="请输入样点时效(h)"/>
        </el-form-item>
        <el-form-item label="送件人" prop="sender">
          <el-input v-model="form.sender" :min="0" placeholder="请输入送件人" />
        </el-form-item>
        <el-form-item label="关联订单" prop="order_id">
          <el-input v-model="form.order_id" :min="0" placeholder="关联订单" />
        </el-form-item>
        <el-form-item label="样点状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择样点状态">
            <el-option label="等待设定工序" value="等待设定工序" />
            <el-option label="设定工序中" value="设定工序中" />
            <el-option label="已设定工序" value="已设定工序" />
            <el-option label="待开始" value="待开始" />
            <el-option label="已完成" value="已完成" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  getSampleList,
  createSample,
  updateSample,
  deleteSample,
} from "@/api/sample";

// 新增标记：true 表示编辑，false 表示新增
const isEdit = ref(false);
const router = useRouter();
const loading = ref(false);
const dialogVisible = ref(false);
const formRef = ref(null);

const searchForm = reactive({
  sample_id: "",
  customer_name: "",
  status: "",
});

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0,
});

// 表格数据
const tableData = ref([]);

const form = reactive({
  order_id: "",
  customer_sample_id: "",
  customer_name: "",
  sender: "",
  sample_quantity: null,
  status: "",
  sample_id: "",
  sample_validity_hours: null,
});

const rules = {
  sample_id: [{ required: true, message: "请输入样点编号", trigger: "blur" }],
  customer_name: [{ required: true, message: "请输入客户名称", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "change" }],
};

const dialogTitle = computed(() => {
  return isEdit.value ? "编辑样点" : "新增样点";
});

const getStatusType = (status) => {
  const statusMap = {
    '已完成': 'success',
    '待开始': 'danger',
    '已设定工序': 'info',
    '设定工序中': 'warning',
    '等待设定工序': 'default'
  };
  return statusMap[status] || "info";
};

// 获取样点列表
const fetchSampleList = async () => {
  loading.value = true;
  try {
    // 构造分页参数
    const pageParams = {
      index: pagination.currentPage, // 当前页码
      size: pagination.pageSize, // 每页数量
      ...searchForm,
    };

    const response = await getSampleList(pageParams);
    // 根据实际返回的数据结构调整
    if (response.data) {
      tableData.value = response.data;
      // 如果后端返回了总数，使用后端的总数；否则使用当前数据长度
      pagination.total = response.total;
    }
  } catch (error) {
    console.error("获取样点列表失败：", error);
    if (error.response) {
      console.error("接口响应状态码：", error.response.status);
      console.error("接口返回数据：", error.response.data);
    }
    ElMessage.error("获取样点列表失败：" + (error.message || "未知错误"));
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  pagination.currentPage = 1;
  fetchSampleList();
};

const handleReset = () => {
  searchForm.sample_id = "";
  searchForm.customer_name = "";
  searchForm.status = "";
  pagination.currentPage = 1;
  fetchSampleList();
};

const handleAdd = () => {
  isEdit.value = false; // 标记为新增
  Object.assign(form, {
    order_id: "",
    customer_sample_id: "",
    customer_name: "",
    sender: "",
    sample_quantity: null,
    status: "",
    sample_id: "",
    sample_validity_hours: null,
  });
  dialogVisible.value = true;
};

const handleView = (row) => {
  router.push(`/sample/detail/${row.sample_id}`);
};

const handleEdit = (row) => {
  isEdit.value = true; // 标记为编辑
  Object.assign(form, { ...row, id: row.id });
  dialogVisible.value = true;
};

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm("确定要删除该样点吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    loading.value = true;
    await deleteSample(row.sample_id);
    ElMessage.success("删除成功");
    fetchSampleList();
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("删除失败：" + (error.message || "未知错误"));
    }
  } finally {
    loading.value = false;
  }
};

const handleSubmit = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        loading.value = true;

        if (isEdit.value) {
          // 编辑
          const sampleData = (({ sample_id, ...rest }) => rest)(form);
          await updateSample(form.sample_id, sampleData);
          ElMessage.success("修改成功");
        } else {
          // 新增
          const sampleData = { ...form };
          await createSample(sampleData);
          ElMessage.success("新增成功");
        }

        dialogVisible.value = false;
        fetchSampleList();
      } catch (error) {
        ElMessage.error(
          (form.id ? "修改" : "新增") + "失败：" + (error.message || "未知错误")
        );
      } finally {
        loading.value = false;
      }
    }
  });
};

const handleSizeChange = (val) => {
  pagination.pageSize = val;
  pagination.currentPage = 1;
  fetchSampleList();
};

const handleCurrentChange = (val) => {
  pagination.currentPage = val;
  fetchSampleList();
};

// 页面加载时获取数据
onMounted(() => {
  fetchSampleList();
});
</script>

<style lang="scss" scoped>
.sample-list {
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
