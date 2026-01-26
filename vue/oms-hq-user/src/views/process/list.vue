<template>
  <div class="process-list">
    <el-card>
      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="工序编号">
          <el-input
            v-model="searchForm.process_id"
            placeholder="请输入工序编号"
            clearable
          />
        </el-form-item>
        <el-form-item label="客户名称">
          <el-input
            v-model="searchForm.customer"
            placeholder="请输入客户名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="工序状态">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
          >
            <el-option label="全部" value="" />
            <el-option label="成功" value="成功" />
            <el-option label="失败" value="失败" />
            <el-option label="返工返序" value="返工返序" />
            <el-option label="检测中" value="检测中" />
            <el-option label="等待委外工序" value="等待委外工序" />
            <el-option label="等待工程师执行" value="等待工程师执行" />
            <el-option label="等待质审核工序" value="等待质审核工序" />
            <el-option label="等待分配工序" value="等待分配工序" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleSearch"
            >搜索</el-button
          >
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
          <el-button type="success" icon="Plus" @click="handleAdd"
            >新增工序</el-button
          >
        </el-form-item>
      </el-form>

      <!-- 表格区域 -->
      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="process_id" label="工序编号" width="150" />
        <el-table-column prop="customer" label="客户名称" width="120" />
        <el-table-column prop="test_item" label="检测项目" />
        <el-table-column prop="process_category" label="工序类别" width="80" />
        <el-table-column prop="sample_id" label="关联样点" width="120" />
        <el-table-column prop="status" label="工序状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="sample_validity_hours"
          label="样点时效(h)"
          width="160"
        />
        <el-table-column prop="is_outsource" label="是否委外" width="160" />
        <el-table-column
          prop="sample_receive_date"
          label="样点接收日期"
          width="160"
        />
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
        <el-form-item label="工序编号" prop="process_id">
          <el-input v-model="form.process_id" placeholder="请输入订单编号" />
        </el-form-item>
        <el-form-item label="客户名称" prop="customer">
          <el-input v-model="form.customer" placeholder="请输入用户名称" />
        </el-form-item>
        <el-form-item label="检测项目" prop="test_item">
          <el-input
            v-model="form.test_item"
            placeholder="请输入检测项目"
          />
        </el-form-item>
        <el-form-item label="工序类别" prop="process_category">
          <el-input
            v-model="form.process_category"
            placeholder="请输入工序类别"
          />
        </el-form-item>
        <el-form-item label="关联样点" prop="sample_id">
          <el-input
            v-model="form.sample_id"
            placeholder="请输入关联样点"
          />
        </el-form-item>
        <el-form-item label="是否委外" prop="is_outsource">
          <el-input v-model="form.is_outsource" placeholder="请输入是否委外" />
        </el-form-item>
        <el-form-item label="工序状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态">
            <el-option label="成功" value="成功" />
            <el-option label="失败" value="失败" />
            <el-option label="返工返序" value="返工返序" />
            <el-option label="检测中" value="检测中" />
            <el-option label="等待委外工序" value="等待委外工序" />
            <el-option label="等待工程师执行" value="等待工程师执行" />
            <el-option label="等待质审核工序" value="等待质审核工序" />
            <el-option label="等待分配工序" value="等待分配工序" />
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
  getProcessList,
  createProcess,
  updateProcess,
  deleteProcess,
} from "../../api/process";

// 新增标记：true 表示编辑，false 表示新增
const isEdit = ref(false);
const router = useRouter();
const loading = ref(false);
const dialogVisible = ref(false);
const formRef = ref(null);

const searchForm = reactive({
  process_id: "",
  customer: "",
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
  process_id: "",
  customer: "",
  test_item: "",
  process_category: "",
  sample_id: "",
  status: "",
  is_outsource: "",
});

const rules = {
  process_id: [{ required: true, message: "请输入工序编号", trigger: "blur" }],
  customer: [{ required: true, message: "请输入客户名称", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "change" }],
};

const dialogTitle = computed(() => {
  return isEdit.value ? "编辑工序" : "新增工序";
});

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
  };
  return statusMap[status] || "info";
};

// 获取工序列表
const fetchProcessList = async () => {
  loading.value = true;
  try {
    // 构造分页参数
    const pageParams = {
      index: pagination.currentPage, // 当前页码
      size: pagination.pageSize, // 每页数量
      ...searchForm,
    };

    const response = await getProcessList(pageParams);
    console.log(response);
    // 根据实际返回的数据结构调整
    if (response.data) {
      tableData.value = response.data;
      // 如果后端返回了总数，使用后端的总数；否则使用当前数据长度
      pagination.total = response.total;
    }
  } catch (error) {
    console.error("获取工序列表失败：", error);
    if (error.response) {
      console.error("接口响应状态码：", error.response.status);
      console.error("接口返回数据：", error.response.data);
    }
    ElMessage.error("获取工序列表失败：" + (error.message || "未知错误"));
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  pagination.currentPage = 1;
  fetchProcessList();
};

const handleReset = () => {
  searchForm.process_id = "";
  searchForm.customer = "";
  searchForm.status = "";
  pagination.currentPage = 1;
  fetchProcessList();
};

const handleAdd = () => {
  isEdit.value = false; // 标记为新增
  Object.assign(form, {
    process_id: "",
    customer: "",
    test_item: "",
    process_category: "",
    sample_id: "",
    status: "",
    is_outsource: "",
  });
  dialogVisible.value = true;
};

const handleView = (row) => {
  router.push(`/process/detail/${row.process_id}`);
};

const handleEdit = (row) => {
  isEdit.value = true; // 标记为编辑
  Object.assign(form, { ...row, process_id: row.process_id });
  dialogVisible.value = true;
};

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm("确定要删除该工序吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    loading.value = true;
    console.log("删除订单：", row.order_id);
    await deleteProcess(row.process_id);
    ElMessage.success("删除成功");
    fetchProcessList();
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
          const processData = (({ process_id, ...rest }) => rest)(form);
          await updateProcess(form.process_id, processData);
          ElMessage.success("修改成功");
        } else {
          // 新增
          const processData = { ...form };
          await createProcess(processData);
          ElMessage.success("新增成功");
        }

        dialogVisible.value = false;
        fetchProcessList();
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
  fetchProcessList();
};

const handleCurrentChange = (val) => {
  pagination.currentPage = val;
  fetchProcessList();
};

// 页面加载时获取数据
onMounted(() => {
  fetchProcessList();
});
</script>

<style lang="scss" scoped>
.process-list {
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
