<template>
  <div class="machine-list">
    <el-card>
      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="设备编码">
          <el-input
            v-model="searchForm.device_code"
            placeholder="请输入设备编码"
            clearable
          />
        </el-form-item>
        <el-form-item label="创建人">
          <el-input
            v-model="searchForm.creator_name"
            placeholder="请输入创建人"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleSearch"
            >搜索</el-button
          >
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
          <el-button type="success" icon="Plus" @click="handleAdd"
            >新增机台耗时</el-button
          >
        </el-form-item>
      </el-form>

      <!-- 表格区域 -->
      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column type="selection" width="55" />
        <el-table-column prop="device_code" label="设备编码" width="150" />
        <el-table-column prop="machine_name" label="机台" width="120" />
        <el-table-column prop="usage_type" label="使用类型" />
        <el-table-column prop="duration_minutes" label="耗时(min)" width="80" />
        <el-table-column prop="start_time" label="开始时间" width="120" />
        <el-table-column prop="end_time" label="结束时间" width="160" />
        <el-table-column prop="creator_name" label="创建人" width="160" />
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
        <el-form-item label="机台名称" prop="machine_name">
          <el-input v-model="form.machine_name" placeholder="请输入机台名称" />
        </el-form-item>
        <el-form-item label="使用类型" prop="usage_type">
          <el-input v-model="form.usage_type" placeholder="请输入使用类型" />
        </el-form-item>
        <el-form-item label="设备编码" prop="device_code">
          <el-input v-model="form.device_code" placeholder="请输入设备编码" />
        </el-form-item>
        <el-form-item label="耗时(min)" prop="duration_minutes">
          <el-input
            v-model="form.duration_minutes"
            placeholder="请输入耗时(min)"
          />
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-input v-model="form.start_time" placeholder="请输入开始时间" />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-input v-model="form.end_time" placeholder="请输入结束时间" />
        </el-form-item>
        <el-form-item label="创建时间" prop="creation_time">
          <el-input v-model="form.creation_time" placeholder="请输入创建时间" />
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
  getMachineList,
  createMachine,
  updateMachine,
  deleteMachine,
} from "@/api/machine";

// 新增标记：true 表示编辑，false 表示新增
const isEdit = ref(false);
const router = useRouter();
const loading = ref(false);
const dialogVisible = ref(false);
const formRef = ref(null);

const searchForm = reactive({
  creator_name: "",
  device_code: "",
});

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0,
});

// 表格数据
const tableData = ref([]);

const form = reactive({
  record_id: "",
  machine_name: "",
  usage_type: "",
  start_time: null,
  duration_minutes: "",
  end_time: null,
  creator_name: "",
  creation_time: null,
  device_code: "",
});

const rules = {
  customer: [{ required: true, message: "请输入客户名称", trigger: "blur" }],
  product: [{ required: true, message: "请输入产品名称", trigger: "blur" }],
  quantity: [{ required: true, message: "请输入数量", trigger: "blur" }],
  price: [{ required: true, message: "请输入单价", trigger: "blur" }],
  status: [{ required: true, message: "请选择状态", trigger: "change" }],
};

const dialogTitle = computed(() => {
  return form.id ? "编辑机台耗时" : "新增机台耗时";
});

const getStatusType = (status) => {
  const statusMap = {
    已结案: "已结案",
    同意: "同意",
    拒绝: "拒绝",
    待审核订单: "待审核订单",
  };
  return statusMap[status] || "info";
};

// 获取机台耗时列表
const fetchMachineList = async () => {
  loading.value = true;
  try {
    // 构造分页参数
    const pageParams = {
      index: pagination.currentPage, // 当前页码
      size: pagination.pageSize, // 每页数量
      ...searchForm,
    };

    const response = await getMachineList(pageParams);
    console.log("获取订单列表成功：", response);
    // 根据实际返回的数据结构调整
    if (response.data) {
      tableData.value = response.data;
      // 如果后端返回了总数，使用后端的总数；否则使用当前数据长度
      pagination.total = response.total;
    }
  } catch (error) {
    console.error("获取机台耗时列表失败：", error);
    if (error.response) {
      console.error("接口响应状态码：", error.response.status);
      console.error("接口返回数据：", error.response.data);
    }
    ElMessage.error("获取机台耗时列表失败：" + (error.message || "未知错误"));
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  pagination.currentPage = 1;
  fetchMachineList();
};

const handleReset = () => {
  searchForm.creator_name = "";
  searchForm.device_code = "";
  pagination.currentPage = 1;
  fetchMachineList();
};

const handleAdd = () => {
  isEdit.value = false; // 标记为新增
  Object.assign(form, {
    record_id: "",
    machine_name: "",
    usage_type: "",
    start_time: null,
    duration_minutes: null,
    end_time: null,
    creator_name: "",
    creation_time: null,
    device_code: "",
  });
  dialogVisible.value = true;
};

const handleView = (row) => {
  router.push(`/machine/detail/${row.record_id}`);
};

const handleEdit = (row) => {
  isEdit.value = true; // 标记为编辑
  Object.assign(form, { ...row, record_id: row.record_id });
  dialogVisible.value = true;
};

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm("确定要删除该机台耗时吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    loading.value = true;
    await deleteMachine(row.record_id);
    ElMessage.success("删除成功");
    fetchMachineList();
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
          const machineData = (({ record_id, ...rest }) => rest)(form);
          await updateMachine(form.record_id, machineData);
          ElMessage.success("修改成功");
        } else {
          // 新增
          const machineData = { ...form };
          await createMachine(machineData);
          ElMessage.success("新增成功");
        }

        dialogVisible.value = false;
        fetchMachineList();
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
  fetchMachineList();
};

const handleCurrentChange = (val) => {
  pagination.currentPage = val;
  fetchMachineList();
};

// 页面加载时获取数据
onMounted(() => {
  fetchMachineList();
});
</script>

<style lang="scss" scoped>
.machine-list {
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
