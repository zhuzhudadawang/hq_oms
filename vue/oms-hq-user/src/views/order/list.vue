<template>
  <div class="order-list">
    <el-card>
      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="订单号">
          <el-input
            v-model="searchForm.order_id"
            placeholder="请输入订单号"
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
        <el-form-item label="订单状态">
          <el-select
            v-model="searchForm.order_status"
            placeholder="请选择状态"
            clearable
          >
            <el-option label="同意" value="同意" />
            <el-option label="拒绝" value="拒绝" />
            <el-option label="已结案" value="已结案" />
            <el-option label="等待结案" value="等待结案" />
            <el-option label="待审核订单" value="待审核订单" />
            <el-option label="已生成对账单" value="已生成对账单" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleSearch"
            >搜索</el-button
          >
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
          <el-button type="success" icon="Plus" @click="handleAdd"
            >新增订单</el-button
          >
          <el-button type="danger" icon="Delete" @click="handleBatchDelete"
            >批量删除</el-button
          >
        </el-form-item>
      </el-form>

      <!-- 表格区域 -->
      <el-table
        :data="tableData"
        v-loading="loading"
        stripe
        border
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="order_id" label="订单号" width="150" />
        <el-table-column prop="customer" label="客户名称" width="120" />
        <el-table-column prop="customer_requirement" label="客户需求" />
        <el-table-column prop="sample_quantity" label="样点数量" width="80" />
        <el-table-column
          prop="validity_requirement_hours"
          label="时效要求(h)"
          width="120"
        />
        <el-table-column prop="order_status" label="订单状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.order_status)">{{
              row.order_status
            }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="execution_place" label="执行地" width="160" />
        <el-table-column prop="order_salesman" label="订单销售" width="160" />
        <el-table-column
          prop="requirement_confirm_date"
          label="需求确认日期"
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
        <el-form-item label="订单编号" prop="order_id">
          <el-input v-model="form.order_id" placeholder="请输入订单编号" />
        </el-form-item>
        <el-form-item label="用户名称" prop="customer">
          <el-input v-model="form.customer" placeholder="请输入用户名称" />
        </el-form-item>
        <el-form-item label="客户需求" prop="customer_requirement">
          <el-input
            v-model="form.customer_requirement"
            placeholder="请输入客户需求"
          />
        </el-form-item>
        <el-form-item label="样点数量" prop="sample_quantity">
          <el-input-number
            v-model="form.sample_quantity"
          />
        </el-form-item>
        <el-form-item label="时效要求(h)" prop="validity_requirement_hours">
          <el-input-number
            v-model="form.validity_requirement_hours"
          />
        </el-form-item>
        <el-form-item label="执行地" prop="execution_place">
          <el-input v-model="form.execution_place" placeholder="请输入执行地" />
        </el-form-item>
        <el-form-item label="订单销售" prop="order_salesman">
          <el-input
            v-model="form.order_salesman"
            placeholder="请输入订单销售"
          />
        </el-form-item>
        <el-form-item label="订单状态" prop="order_status">
          <el-select v-model="form.order_status" placeholder="请选择状态">
            <el-option label="已结案" value="已结案" />
            <el-option label="同意" value="同意" />
            <el-option label="已生成对账单" value="已生成对账单" />
            <el-option label="拒绝" value="拒绝" />
            <el-option label="等待结案" value="等待结案" />
            <el-option label="待审核订单" value="待审核订单" />
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item> -->
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
  getOrderList,
  createOrder,
  updateOrder,
  deleteOrder,
  batchDeleteOrders,
} from "@/api/order";

// 新增标记：true 表示编辑，false 表示新增
const isEdit = ref(false);
const router = useRouter();
const loading = ref(false);
const dialogVisible = ref(false);
const formRef = ref(null);
// 存储选中的行数据
const selectedRows = ref([]);

// 处理选中事件：更新选中的行数据
const handleSelectionChange = (rows) => {
  selectedRows.value = rows;
};

const searchForm = reactive({
  order_id: "",
  customer: "",
  order_status: "",
});

const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0,
});

// 表格数据
const tableData = ref([]);

const form = reactive({
  customer: "",
  customer_requirement: "",
  sample_quantity: 0,
  validity_requirement_hours: 0,
  execution_place: "",
  order_salesman: "",
  order_status: "",
});

const rules = {
  order_id: [{ required: true, message: "请输入订单编号", trigger: "blur" }],
  customer: [{ required: true, message: "请输入客户名称", trigger: "blur" }],
  // sample_quantity: [{ required: true, message: "请输入数量", trigger: "blur" }],
  // customer_requirement: [{ required: true, message: '请输入产品名称', trigger: 'blur' }],
  // execution_place: [{ required: true, message: '请选择状态', trigger: 'change' }],
  // order_salesman: [{ required: true, message: '请选择状态', trigger: 'change' }],
  order_status: [{ required: true, message: "请选择状态", trigger: "change" }],
};

const dialogTitle = computed(() => {
  return isEdit.value ? "编辑订单" : "新增订单";
});

const getStatusType = (status) => {
  const statusMap = {
    已结案: "success",
    同意: "success",
    已生成对账单: "warning",
    拒绝: "danger",
    等待结案: "info",
    待审核订单: "default",
  };
  return statusMap[status] || "info";
};

// 获取订单列表
const fetchOrderList = async () => {
  loading.value = true;
  try {
    // 构造分页参数
    const pageParams = {
      index: pagination.currentPage, // 当前页码
      size: pagination.pageSize, // 每页数量
      ...searchForm,
    };

    const response = await getOrderList(pageParams);
    // 根据实际返回的数据结构调整
    if (response.data) {
      tableData.value = response.data;
      // 如果后端返回了总数，使用后端的总数；否则使用当前数据长度
      pagination.total = response.total;
    }
  } catch (error) {
    console.error("获取订单列表失败：", error);
    if (error.response) {
      console.error("接口响应状态码：", error.response.status);
      console.error("接口返回数据：", error.response.data);
    }
    ElMessage.error("获取订单列表失败：" + (error.message || "未知错误"));
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  pagination.currentPage = 1;
  fetchOrderList();
};

const handleReset = () => {
  searchForm.order_id = "";
  searchForm.customer = "";
  searchForm.order_status = "";
  pagination.currentPage = 1;
  fetchOrderList();
};

const handleAdd = () => {
  isEdit.value = false; // 标记为新增
  Object.assign(form, {
    order_id: "",
    customer: "",
    customer_requirement: "",
    sample_quantity: null,
    validity_requirement_hours: null,
    execution_place: "",
    order_salesman: "",
    order_status: "",
  });
  dialogVisible.value = true;
};

const handleView = (row) => {
  router.push(`/order_test/detail/${row.order_id}`);
};

const handleEdit = (row) => {
  isEdit.value = true; // 标记为编辑
  Object.assign(form, { ...row });
  dialogVisible.value = true;
};

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm("确定要删除该订单吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    loading.value = true;
    console.log("删除订单：", row.order_id);
    await deleteOrder(row.order_id);
    ElMessage.success("删除成功");
    fetchOrderList();
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

        // 计算总金额
        // const amount = form.quantity * form.price
        // const orderData = {
        //   ...form,
        // };
        console.log(isEdit.value);
        if (isEdit.value) {
          // 编辑
          const orderData = (({ order_id, ...rest }) => rest)(form);
          await updateOrder(form.order_id, orderData);
          ElMessage.success("修改成功");
        } else {
          // 新增
          const orderData = { ...form };
          await createOrder(orderData);
          ElMessage.success("新增成功");
        }

        dialogVisible.value = false;
        fetchOrderList();
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

// 批量删除
const handleBatchDelete = async () => {
  // 校验是否选中数据
  if (selectedRows.value.length === 0) {
    ElMessage.warning("请先选择要删除的订单");
    return;
  }

  try {
    // 二次确认
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedRows.value.length} 条订单吗？`,
      "批量删除确认",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }
    );

    loading.value = true;
    // 提取选中行的 order_id
    const ids = selectedRows.value.map((row) => row.order_id);
    await batchDeleteOrders(ids);

    ElMessage.success(`成功删除 ${selectedRows.value.length} 条订单`);
    fetchOrderList();
    // 清空选中状态
    selectedRows.value = [];
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("批量删除失败：" + (error.message || "未知错误"));
    }
  } finally {
    loading.value = false;
  }
};

const handleSizeChange = (val) => {
  pagination.pageSize = val;
  pagination.currentPage = 1;
  fetchOrderList();
};

const handleCurrentChange = (val) => {
  pagination.currentPage = val;
  fetchOrderList();
};

// 页面加载时获取数据
onMounted(() => {
  fetchOrderList();
});
</script>

<style lang="scss" scoped>
.order-list {
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
