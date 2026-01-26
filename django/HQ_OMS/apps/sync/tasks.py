"""
白码数据同步任务
功能：定时从白码 API 拉取数据同步到本地 MySQL
"""
import requests
import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from apps.sync.models import Process, MachineUsageRecord, Order, Machine, Sample

# ==================== 配置区域（方便修改） ====================

# 白码 API 通用配置
API_BASE_URL = "http://ftp.hq-nano.com:10001"
API_TOKEN = "442741653dd94e1e9bdee5a6e4b1c9e2"

# 定时任务时间配置（24小时制，北京时间）
# 格式：(小时, 分钟)
SYNC_TIMES = [
    (8, 0),    # 8:00
    (14, 0),   # 14:00
    (21, 0),   # 21:00
]

# 每页拉取数量
PAGE_SIZE = 10000

# ==================== 工序表配置 ====================

PROCESS_API_URL = f"{API_BASE_URL}/api/bmapi/v1/data/64e577b3094fc3a856105278/64e6d128094fc3a85612c552/query"
PROCESS_VIEW_ID = "collection-64e6d128094fc3a85612c552-1695095861332"

# 工序表字段映射：白码字段名 -> 模型字段名
PROCESS_FIELD_MAPPING = {
    "工序编号": "process_id",
    "订单编号": "order_id",
    "客户昵称": "customer",
    "工序类别": "process_category",
    "检测项目": "test_item",
    "检测样点": "sample_id",
    "客户样点编号": "customer_sample_id",
    "Lot/Wafer/Sample ID": "lot_wafer_sample_id",
    "最后工艺步骤": "last_process_step",
    "主要关注信息": "main_attention_info",
    "切片位置": "slice_position",
    "制样方向": "sample_preparation_direction",
    "注意事项": "notes",
    "等效点数量": "equivalent_point_quantity",
    "样点接收时间": "sample_receive_time",
    "加急程度": "urgency_level",
    "工序备注": "process_note",
    "执行方案(文件)": "execution_plan",
    "是否委外": "is_outsource",
    "检测工程师": "testing_engineer",
    "工程师区域": "engineer_region",
    "标准工时（分钟）": "standard_working_hours_minutes",
    "检测机台": "testing_machine",
    "开始时间": "start_time",
    "结束时间": "end_time",
    "状态": "status",
    "是否为返工工序": "is_rework_process",
    "是否计算绩效": "is_calculate_performance",
    "是否上传结果": "is_upload_result",
    "关联机台(隐藏)": "associated_machine",
    "优先级": "priority_level",
    "耗时（分钟）": "time_consumption_minutes",
    "审核备注": "review_comment",
    "是否取消": "is_canceled",
    "委外结果文件": "outsourcing_result_file",
    "收费数量": "charge_quantity",
    "计费数量": "billing_quantity",
    "加急系数": "urgency_coefficient",
    "工程师对账状态": "engineer_reconciliation_status",
    "机台对账状态": "machine_reconciliation_status",
    "样点确认日期": "sample_confirmation_date",
    "样点接收日期": "sample_receive_date",
    "失败证明": "failure_proof",
    "关联客户": "associated_customer",
    "结案日期": "closing_date",
    "工序开始日期": "process_start_date",
    "绩效工时":"performance_working_hours",
}

# ==================== 机台耗时记录表配置 ====================

MACHINE_USAGE_API_URL = f"{API_BASE_URL}/api/bmapi/v1/data/64e577b3094fc3a856105278/68c12c386870189e0baec2ae/query"
MACHINE_USAGE_VIEW_ID = "collection-68c12c386870189e0baec2ae-1757674225417"

# 机台耗时记录字段映射：白码字段名 -> 模型字段名
MACHINE_USAGE_FIELD_MAPPING = {
    "机台": "machine_name",
    "使用类型": "usage_type",
    "开始时间": "start_time",
    "耗时(min)": "duration_minutes",
    "结束时间": "end_time",
    "创建人": "creator_name",
    "创建时间": "creation_time",
    "班次": "shift",
}

# ==================== 订单表配置 ====================

ORDER_API_URL = f"{API_BASE_URL}/api/bmapi/v1/data/64e577b3094fc3a856105278/64e5cf8e72b119a857ce7073/query"
ORDER_VIEW_ID = "collection-64e5cf8e72b119a857ce7073-1692934901286"

# 订单表字段映射：白码字段名 -> 模型字段名
ORDER_FIELD_MAPPING = {
    "订单编号": "order_id",
    "客户": "customer",
    "优先级": "priority",
    "订单状态": "order_status",
    "样点状态": "sample_status",
    "工序状态": "process_status",
    "订单类目": "order_category",
    "样点数量": "sample_quantity",
    "送件人名称": "sender_name",
    "送件人电话": "sender_phone",
    "送件人邮箱": "sender_email",
    "送件人": "sender",
    "订单销售": "order_salesman",
    "是否委外": "is_outsource",
    "客户编号": "customer_id",
    "时效要求(h)": "validity_requirement_hours",
    "执行地": "execution_place",
    # "接收日期": "receive_time",
    "需求确认日期": "requirement_confirm_date",
    # "需求确认时间": "requirement_confirm_time",  # 白码返回纯时间字符串，跳过
    # "时效起算日期": "validity_start_time",
    "客户需求": "customer_requirement",
    "是否需要报告": "is_report_required",
    "报告形式": "report_format",
    "样品处理方式": "sample_processing_method",
}

# ==================== 样点表配置 ====================

SAMPLE_API_URL = f"{API_BASE_URL}/api/bmapi/v1/data/64e577b3094fc3a856105278/64e6bdd472b119a857cf57ba/query"
SAMPLE_VIEW_ID = "collection-64e6bdd472b119a857cf57ba-1692934909379"

# 样点表字段映射：白码字段名 -> 模型字段名
SAMPLE_FIELD_MAPPING = {
    "样点编号": "sample_id",
    "关联订单": "order_id",
    "客户样点编号": "customer_sample_id",
    "客户名": "customer_name",
    "Lot/Wafer/Sample ID": "lot_wafer_sample_id",
    "项目分类": "project_category",
    "样品数量": "sample_quantity",
    # "样点时效(h)": "sample_validity_hours",
    "最后工艺步骤": "last_process_step",
    "切片位置": "slice_position",
    "制样方向": "sample_preparation_direction",
    "样点确认日期": "sample_confirmation_date",
    "样点确认时间": "sample_confirmation_time",
    "注意事项": "notes",
    "主要关注信息": "main_attention_info",
    "封装形式": "packaging_form",
    "状态": "status",
    "订单状态": "order_status",
    "关联客户": "related_customer",
    "时效起算日期": "validity_start_date",
    # "时效起算时间": "validity_start_time",
    # "交期日期": "delivery_date",
    # "交期时间": "delivery_time",
    "工序状态": "process_status",
    "工序审核状态": "process_audit_status",
}

# ==================== 机台表配置 ====================

MACHINE_API_URL = f"{API_BASE_URL}/api/bmapi/v1/data/64e577b3094fc3a856105278/64e5d4d372b119a857ce9363/query"
MACHINE_VIEW_ID = "collection-64e5d4d372b119a857ce9363-1692934542216"

# 机台表字段映射：白码字段名 -> 模型字段名
MACHINE_FIELD_MAPPING = {
    "工序设备编码": "process_equipment_code",
    "城市": "city",
    "类别": "category",
    "子类": "sub_category",
    "单位": "unit",
    "所属供应商": "supplier",
    "详细型号": "detailed_model",
    "内外部区分": "internal_external_distinction",
    "机台配置": "machine_configuration",
    "项目开始时间": "project_start_time",
    "机台预设价格(￥/分钟)(未税)": "preset_price_before_tax",
    "机台预设价格(￥/分钟)(含税)": "preset_price_after_tax",
    # "税率": "tax_rate",
}

# ==================== 通用函数 ====================

def parse_datetime(value):
    """解析日期时间字符串"""
    if not value or value == "":
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return None


def parse_int(value):
    """解析整数，处理空值和小数"""
    if not value or value == "":
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def parse_float(value):
    """解析浮点数"""
    if not value or value == "":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_decimal(value):
    """解析 Decimal 类型"""
    if not value or value == "":
        return None
    try:
        return float(value)  # Django 会自动转换
    except (ValueError, TypeError):
        return None


def fetch_all_records(api_url, view_id, query=None):
    """获取白码所有数据（分页拉取）"""
    headers = {
        'Content-Type': 'application/json',
        'bm-x-token': API_TOKEN
    }
    
    if query is None:
        query = {"$and": []}
    
    all_records = []
    page = 1
    
    while True:
        payload = json.dumps({
            "view": view_id,
            "query": query,
            "page": {"index": page, "size": PAGE_SIZE},
            # "sort": "-ctime",
            "option": {"simple": True}
        })
        
        try:
            response = requests.post(api_url, headers=headers, data=payload, timeout=60)
            result = response.json()
        except Exception as e:
            print(f"[SYNC] API 请求异常: {e}")
            break
        
        if result.get("error") != 0:
            print(f"[SYNC] API 请求失败: {result.get('msg')}")
            break
        
        records = result.get("data", {}).get("data", [])
        if not records:
            break
        
        all_records.extend(records)
        print(f"[SYNC] 已获取第 {page} 页，{len(records)} 条，累计 {len(all_records)} 条")
        page += 1
    
    return all_records


# ==================== 工序表同步 ====================

def sync_process():
    """同步工序表（全量同步）"""
    print("=" * 50)
    print(f"[SYNC] 开始同步工序表 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 查询条件：排除已取消
    query = {
        "$and": [
            {"$or": [{"$and": [{"652cfd465ae946316f129d4e": {"$ne": "已取消"}}]}]}
        ]
    }
    
    # 1. 获取所有数据
    print("[SYNC] [1/3] 获取白码数据...")
    records = fetch_all_records(PROCESS_API_URL, PROCESS_VIEW_ID, query)
    print(f"[SYNC] 共获取 {len(records)} 条数据")
    
    if not records:
        print("[SYNC] 没有数据，跳过同步")
        return
    
    # 2. 清空表数据
    print("[SYNC] [2/3] 清空表数据...")
    deleted_count = Process.objects.all().delete()[0]
    print(f"[SYNC] 已删除 {deleted_count} 条旧数据")
    
    # 3. 写入新数据（批量写入，去重）
    print("[SYNC] [3/3] 写入新数据...")
    objects_to_create = []
    seen_ids = set()  # 用于去重
    error_count = 0
    duplicate_count = 0
    
    for record in records:
        try:
            process_id = record.get("工序编号", None)
            
            # 跳过重复的工序编号
            if process_id in seen_ids:
                duplicate_count += 1
                continue
            seen_ids.add(process_id)
            
            data = {}
            for baima_field, model_field in PROCESS_FIELD_MAPPING.items():
                value = record.get(baima_field, None)
                
                # test_item 字段：清理多余空格（如 "SEM/EDS分 析服务" -> "SEM/EDS分析服务"）
                if model_field == "test_item" and value and isinstance(value, str):
                    value = ''.join(value.split())  # 去除所有空格
                
                # 根据字段类型处理
                if model_field in ["start_time", "end_time", "sample_receive_time", 
                                   "sample_confirmation_date",
                                   "sample_receive_date", "closing_date", "process_start_date"]:
                    value = parse_datetime(value)
                elif model_field in ["equivalent_point_quantity",
                                     "priority_level", "time_consumption_minutes"]:
                    value = parse_int(value)
                elif model_field in ["charge_quantity", "billing_quantity"]:
                    value = parse_float(value)
                elif model_field in ["standard_working_hours_minutes", "urgency_coefficient"]:
                    value = parse_decimal(value)
                elif value == "":
                    value = None
                
                data[model_field] = value
            
            objects_to_create.append(Process(**data))
            
        except Exception as e:
            error_count += 1
            process_id = record.get("工序编号", "未知")
            print(f"[SYNC] 数据处理失败 [{process_id}]: {e}")
    
    if duplicate_count > 0:
        print(f"[SYNC] 跳过 {duplicate_count} 条重复数据")
    
    # 批量写入，每 5000 条一批
    if objects_to_create:
        Process.objects.bulk_create(objects_to_create, batch_size=5000)
    
    print(f"[SYNC] 同步完成: 成功 {len(objects_to_create)} 条, 失败 {error_count} 条")
    print("=" * 50)


# ==================== 机台耗时记录同步 ====================

def sync_machine_usage():
    """同步机台耗时记录表（全量同步）
    注意：需要先执行 sync_machine() 同步机台表，才能正确关联 device_code
    """
    print("=" * 50)
    print(f"[SYNC] 开始同步机台耗时记录表 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 0. 建立 详细型号 -> 设备编码 的映射（从 Machine 表获取）
    machine_mapping = dict(
        Machine.objects.values_list('detailed_model', 'process_equipment_code')
    )
    print(f"[SYNC] 已加载 {len(machine_mapping)} 条机台映射")
    
    # 1. 获取所有数据
    print("[SYNC] [1/3] 获取白码数据...")
    records = fetch_all_records(MACHINE_USAGE_API_URL, MACHINE_USAGE_VIEW_ID)
    print(f"[SYNC] 共获取 {len(records)} 条数据")
    
    if not records:
        print("[SYNC] 没有数据，跳过同步")
        return
    
    # 2. 清空表数据
    print("[SYNC] [2/3] 清空表数据...")
    deleted_count = MachineUsageRecord.objects.all().delete()[0]
    print(f"[SYNC] 已删除 {deleted_count} 条旧数据")
    
    # 3. 写入新数据（批量写入，用_id去重）
    print("[SYNC] [3/3] 写入新数据...")
    objects_to_create = []
    seen_ids = set()  # 用于去重
    error_count = 0
    duplicate_count = 0
    unmapped_count = 0  # 未匹配到设备编码的记录数
    
    for record in records:
        try:
            record_id = record.get("_id", None)
            
            # 跳过重复的记录
            if record_id in seen_ids:
                duplicate_count += 1
                continue
            seen_ids.add(record_id)
            
            data = {}
            for baima_field, model_field in MACHINE_USAGE_FIELD_MAPPING.items():
                value = record.get(baima_field, None)
                
                # 根据字段类型处理
                if model_field in ["start_time", "end_time", "creation_time"]:
                    value = parse_datetime(value)
                elif model_field == "duration_minutes":
                    value = parse_int(value)
                elif value == "":
                    value = None
                
                data[model_field] = value
            
            # 通过 machine_name 查找对应的 device_code
            machine_name = data.get("machine_name")
            device_code = machine_mapping.get(machine_name)
            if device_code:
                data["device_code"] = device_code
            else:
                unmapped_count += 1
            
            objects_to_create.append(MachineUsageRecord(**data))
            
        except Exception as e:
            error_count += 1
            print(f"[SYNC] 数据处理失败: {e}")
    
    if duplicate_count > 0:
        print(f"[SYNC] 跳过 {duplicate_count} 条重复数据")
    if unmapped_count > 0:
        print(f"[SYNC] 有 {unmapped_count} 条记录未匹配到设备编码")
    
    # 批量写入，每 1000 条一批
    if objects_to_create:
        MachineUsageRecord.objects.bulk_create(objects_to_create, batch_size=1000)
    
    print(f"[SYNC] 同步完成: 成功 {len(objects_to_create)} 条, 失败 {error_count} 条")
    print("=" * 50)


# ==================== 机台表同步 ====================

def sync_machine():
    """同步机台表（全量同步）"""
    print("=" * 50)
    print(f"[SYNC] 开始同步机台表 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 获取所有数据
    print("[SYNC] [1/3] 获取白码数据...")
    records = fetch_all_records(MACHINE_API_URL, MACHINE_VIEW_ID)
    print(f"[SYNC] 共获取 {len(records)} 条数据")
    
    if not records:
        print("[SYNC] 没有数据，跳过同步")
        return
    
    # 2. 清空表数据
    print("[SYNC] [2/3] 清空表数据...")
    deleted_count = Machine.objects.all().delete()[0]
    print(f"[SYNC] 已删除 {deleted_count} 条旧数据")
    
    # 3. 写入新数据（批量写入，用工序设备编码去重）
    print("[SYNC] [3/3] 写入新数据...")
    objects_to_create = []
    seen_ids = set()  # 用于去重
    error_count = 0
    duplicate_count = 0
    
    for record in records:
        try:
            equipment_code = record.get("工序设备编码", None)
            
            # 跳过重复的记录
            if equipment_code in seen_ids:
                duplicate_count += 1
                continue
            seen_ids.add(equipment_code)
            
            data = {}
            for baima_field, model_field in MACHINE_FIELD_MAPPING.items():
                value = record.get(baima_field, None)
                
                # 根据字段类型处理
                if model_field == "project_start_time":
                    value = parse_datetime(value)
                elif model_field in ["preset_price_before_tax", "preset_price_after_tax"]:
                    value = parse_decimal(value)
                elif model_field == "tax_rate":
                    # 税率格式如 "6%"，需要转换为小数
                    if value and isinstance(value, str) and value.endswith('%'):
                        try:
                            value = float(value.rstrip('%'))
                        except ValueError:
                            value = None
                    else:
                        value = parse_decimal(value)
                elif value == "":
                    value = None
                
                data[model_field] = value
            
            objects_to_create.append(Machine(**data))
            
        except Exception as e:
            error_count += 1
            print(f"[SYNC] 数据处理失败: {e}")
    
    if duplicate_count > 0:
        print(f"[SYNC] 跳过 {duplicate_count} 条重复数据")
    
    # 批量写入，每 1000 条一批
    if objects_to_create:
        Machine.objects.bulk_create(objects_to_create, batch_size=1000)
    
    print(f"[SYNC] 同步完成: 成功 {len(objects_to_create)} 条, 失败 {error_count} 条")
    print("=" * 50)


# ==================== 订单表同步 ====================

def sync_order():
    """同步订单表（全量同步）"""
    print("=" * 50)
    print(f"[SYNC] 开始同步订单表 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 1. 获取所有数据
    print("[SYNC] [1/3] 获取白码数据...")
    records = fetch_all_records(ORDER_API_URL, ORDER_VIEW_ID)
    print(f"[SYNC] 共获取 {len(records)} 条数据")
    
    if not records:
        print("[SYNC] 没有数据，跳过同步")
        return
    
    # 2. 清空表数据
    print("[SYNC] [2/3] 清空表数据...")
    deleted_count = Order.objects.all().delete()[0]
    print(f"[SYNC] 已删除 {deleted_count} 条旧数据")
    
    # 3. 写入新数据（批量写入，用订单编号去重）
    print("[SYNC] [3/3] 写入新数据...")
    objects_to_create = []
    seen_ids = set()
    error_count = 0
    duplicate_count = 0
    
    for record in records:
        try:
            order_id = record.get("订单编号", None)
            
            # 跳过重复的记录
            if order_id in seen_ids:
                duplicate_count += 1
                continue
            seen_ids.add(order_id)
            
            data = {}
            for baima_field, model_field in ORDER_FIELD_MAPPING.items():
                value = record.get(baima_field, None)
                
                # 根据字段类型处理
                if model_field in ["requirement_confirm_date"]:
                    value = parse_datetime(value)
                elif model_field == "sample_quantity":
                    value = parse_int(value)
                elif model_field == "validity_requirement_hours":
                    value = parse_float(value)
                elif value == "":
                    value = None
                
                data[model_field] = value
            
            # 设置创建时间和修改时间
            data["create_time"] = datetime.now()
            data["modify_time"] = datetime.now()
            
            objects_to_create.append(Order(**data))
            
        except Exception as e:
            error_count += 1
            print(f"[SYNC] 数据处理失败: {e}")
    
    if duplicate_count > 0:
        print(f"[SYNC] 跳过 {duplicate_count} 条重复数据")
    
    # 批量写入
    if objects_to_create:
        Order.objects.bulk_create(objects_to_create, batch_size=5000)
    
    print(f"[SYNC] 同步完成: 成功 {len(objects_to_create)} 条, 失败 {error_count} 条")
    print("=" * 50)


# ==================== 样点表同步 ====================

def sync_sample():
    """同步样点表（全量同步）"""
    print("=" * 50)
    print(f"[SYNC] 开始同步样点表 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 查询条件：排除拒绝、待审核订单、完全委外订单
    query = {
        "$and": [
            {
                "$or": [
                    {
                        "$and": [
                            {"64e6c40872b119a857cf6fe7": {"$ne": "拒绝"}},
                            {"share_1709114647363": {"$ne": "待审核订单"}},
                            {"share_1718189549595": {"$ne": "完全委外订单"}}
                        ]
                    }
                ]
            }
        ]
    }
    
    # 1. 获取所有数据
    print("[SYNC] [1/3] 获取白码数据...")
    records = fetch_all_records(SAMPLE_API_URL, SAMPLE_VIEW_ID, query)
    print(f"[SYNC] 共获取 {len(records)} 条数据")
    
    if not records:
        print("[SYNC] 没有数据，跳过同步")
        return
    
    # 2. 清空表数据
    print("[SYNC] [2/3] 清空表数据...")
    deleted_count = Sample.objects.all().delete()[0]
    print(f"[SYNC] 已删除 {deleted_count} 条旧数据")
    
    # 3. 写入新数据（批量写入，用样点编号去重）
    print("[SYNC] [3/3] 写入新数据...")
    objects_to_create = []
    seen_ids = set()
    duplicate_ids = []  # 记录重复的样点编号
    error_count = 0
    duplicate_count = 0
    
    for record in records:
        try:
            sample_id = record.get("样点编号", None)
            
            # 跳过重复的记录
            if sample_id in seen_ids:
                duplicate_count += 1
                duplicate_ids.append(sample_id)
                continue
            seen_ids.add(sample_id)
            
            data = {}
            for baima_field, model_field in SAMPLE_FIELD_MAPPING.items():
                value = record.get(baima_field, None)
                
                # 根据字段类型处理
                if model_field in ["sample_confirmation_date", "validity_start_date",]:
                    value = parse_datetime(value)
                elif model_field in ["sample_quantity"]:
                    value = parse_int(value)
                elif value == "":
                    value = None
                
                data[model_field] = value
            
            objects_to_create.append(Sample(**data))
            
        except Exception as e:
            error_count += 1
            print(f"[SYNC] 数据处理失败: {e}")
    
    if duplicate_count > 0:
        print(f"[SYNC] 跳过 {duplicate_count} 条重复数据")
        print(f"[SYNC] 重复的样点编号: {duplicate_ids}")
    
    # 批量写入
    if objects_to_create:
        Sample.objects.bulk_create(objects_to_create, batch_size=5000)
    
    print(f"[SYNC] 同步完成: 成功 {len(objects_to_create)} 条, 失败 {error_count} 条")
    print("=" * 50)


# ==================== 统一同步入口 ====================

def sync_all():
    """按顺序同步所有表（每个表独立执行，互不影响）"""
    # 关闭旧连接，防止长时间空闲后 MySQL 连接超时 (Server has gone away)
    from django.db import connection
    connection.close()
    
    print("=" * 60)
    print(f"[SYNC] 开始执行全量同步 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 同步任务列表（按顺序执行）
    sync_tasks = [
        ("机台表", sync_machine),
        ("机台耗时记录表", sync_machine_usage),
        ("订单表", sync_order),
        ("样点表", sync_sample),
        ("工序表", sync_process),
    ]
    
    success_count = 0
    fail_count = 0
    
    for task_name, sync_func in sync_tasks:
        try:
            sync_func()
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"[SYNC] ❌ {task_name}同步失败: {e}")
    
    print("=" * 60)
    print(f"[SYNC] 全量同步完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[SYNC] 结果: 成功 {success_count} 个表, 失败 {fail_count} 个表")
    print("=" * 60)


# ==================== 定时任务调度器 ====================

scheduler = None

def start_scheduler():
    """启动定时任务调度器"""
    global scheduler
    
    if scheduler is not None:
        return
    
    from pytz import timezone
    china_tz = timezone('Asia/Shanghai')
    
    scheduler = BackgroundScheduler(timezone=china_tz)
    
    # 添加全量同步任务（每天多次执行）
    for i, (hour, minute) in enumerate(SYNC_TIMES):
        scheduler.add_job(
            sync_all,
            'cron',
            hour=hour,
            minute=minute,
            id=f'sync_all_{i}',
            replace_existing=True
        )
    
    scheduler.start()
    times_str = '、'.join(f"{h:02d}:{m:02d}" for h, m in SYNC_TIMES)
    print(f"[SYNC] 定时任务已启动，将在每天 {times_str} (北京时间) 执行同步")


def stop_scheduler():
    """停止定时任务调度器"""
    global scheduler
    if scheduler:
        scheduler.shutdown()
        scheduler = None
        print("[SYNC] 定时任务已停止")
