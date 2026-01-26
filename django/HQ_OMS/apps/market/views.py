from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from rest_framework.views import APIView
from datetime import datetime, timedelta

from utils.Response import ApiResponse
from .models import Order, Process, Sample



# --- 珠海订单统计(月度) ---
class ZhuhaiOrderStatisticsAPI(APIView):
    TARGET_YEARS = [2024, 2025, 2026]
    MONTHS_LABELS = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    # 需要动态计算的月份
    DYNAMIC_MONTHS_2025 = [10, 11, 12]
    ALL_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # 死数据
    FIXED_DATA_2024 = [89, 85, 85, 105, 97, 94, 136, 134, 114, 105, 119, 108]
    FIXED_DATA_2025 = [48, 56, 86, 106, 76, 60, 66, 110, 97]   # 2025年前9个月数据

    def _calculate_dynamic_data(self, year, months):
        """计算指定年份中指定月份列表的动态数据。"""
        dynamic_data = []
        for month in months:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            count = Order.objects.filter(
                execution_place__icontains='珠海',
                requirement_confirm_date__gte=start_date,
                requirement_confirm_date__lt=end_date
            ).count()

            dynamic_data.append(count)

        return dynamic_data

    def get(self, request):
        series = []
        for year in self.TARGET_YEARS:
            if year == 2024:
                series.append({'name': str(year), 'data': self.FIXED_DATA_2024})

            elif year == 2025:
                # 2025年数据 = 前9个月写死数据 + 后3个月动态计算数据
                dynamic_data = self._calculate_dynamic_data(year, self.DYNAMIC_MONTHS_2025)
                full_data = self.FIXED_DATA_2025 + dynamic_data
                series.append({'name': str(year), 'data': full_data})

            elif year == 2026:
                # 2026年数据 = 全部动态计算
                full_data = self._calculate_dynamic_data(year, self.ALL_MONTHS)
                series.append({'name': str(year), 'data': full_data})

        response_data = {
            'months': self.MONTHS_LABELS,
            'series': series
        }

        return ApiResponse.success(data=response_data, message="获取珠海订单统计数据成功")

# --- 珠海订单统计(周度) ---
class ZhuhaiOrderWeeklyStatsAPI(APIView):
    def _generate_week_labels(self, year, month):
        week_labels = []

        # 本月第一天
        current_week_start = datetime(year, month, 1)

        # 计算下个月第一天，用于判断边界
        if month == 12:
            next_month_first_day = datetime(year + 1, 1, 1)
        else:
            next_month_first_day = datetime(year, month + 1, 1)

        week_number = 1

        # 循环生成周标签，直到周的起始日期超出本月
        while current_week_start < next_month_first_day:
            # 计算本周的结束日期（理论上是7天后，但不能超过本月最后一天）
            current_week_end_theoretical = current_week_start + timedelta(days=6)  # +6天得到周日
            current_week_end_actual = min(current_week_end_theoretical, next_month_first_day - timedelta(days=1))

            # 构建标签
            label = f"W{week_number}({current_week_start.day}-{current_week_end_actual.day})"
            week_labels.append(label)

            # 进入下一周
            current_week_start += timedelta(weeks=1)
            week_number += 1

        return week_labels

    def get(self, request, format=None):
        month_param = request.query_params.get("month")
        if not month_param:
            return ApiResponse.failed(
                code=400,
                message="月份参数不能为空，请传入YYYY-MM格式（如2024-05）"
            )

        try:
            year, month = map(int, month_param.split("-"))
            start_date = datetime(year, month, 1)
            end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
            query_month = start_date.strftime("%Y-%m")

            # 生成周标签
            weeks = self._generate_week_labels(year, month)

            # 如果没有生成任何周标签（理论上不可能）
            if not weeks:
                return ApiResponse.success(
                    data={"weeks": [], "data": []},
                    message=f"{query_month} 没有有效周数据"
                )

            # 初始化订单计数器，长度与周标签一致，默认值为0
            order_counts = [0] * len(weeks)

            # 查询该月份内所有珠海地区的订单
            orders = Order.objects.filter(
                execution_place__icontains='珠海',
                requirement_confirm_date__gte=start_date,
                requirement_confirm_date__lt=end_date
            ).only('requirement_confirm_date')

            # 按“每月1号为起点，7天一周”统计订单量
            for order in orders:
                # 使用 requirement_confirm_date 进行计算
                confirm_time = order.requirement_confirm_date
                # 计算订单距离当月1号的天数差
                days_diff = (confirm_time - start_date).days
                # 计算所属周数（1-based）
                week_num = (days_diff // 7) + 1

                # 确保周数在有效范围内（防止异常数据导致数组越界）
                if 1 <= week_num <= len(weeks):
                    order_counts[week_num - 1] += 1  # 转换为0-based索引

            response_data = {
                "weeks": weeks,
                "data": order_counts
            }

            return ApiResponse.success(
                data=response_data,
                message=f"成功获取 {query_month} 珠海地区订单周统计"
            )

        except (ValueError, TypeError):
            return ApiResponse.failed(
                code=400,
                message="月份参数格式错误，请传入YYYY-MM格式（如2024-05）",
                data={"valid_example": "2024-05", "invalid_param": month_param}
            )
        except Exception as e:
            # # 打印异常信息到控制台，方便调试
            # import traceback
            # traceback.print_exc()
            return ApiResponse.http_error(
                status_code=500,
                message=f"获取订单周统计失败：{str(e)}"
            )

# --- 珠海订单&样品 ---
class ZhuhaiCustomerStatisticsAPI(APIView):
    def get(self, request, format=None):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if start_date > end_date:
            return ApiResponse.failed(code=400, message="开始日期不能晚于结束日期")
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        common_filter = {
            'execution_place__icontains': '珠海',
            'requirement_confirm_date__gte': start_datetime,
            'requirement_confirm_date__lte': end_datetime,
        }

        # 1. 先统计每个客户的订单数
        order_queryset = Order.objects.filter(**common_filter).values('customer').annotate(
            order_count=Count('order_id')
        )

        # 2. 获取符合条件的所有订单ID
        order_ids = Order.objects.filter(**common_filter).values_list('order_id', flat=True)

        # 3. 通过 Sample 表统计每个客户的样品数量（通过 order_id 关联）
        sample_queryset = Sample.objects.filter(
            order_id__in=order_ids
        ).values('related_customer').annotate(
            sample_sum=Sum('sample_quantity')
        )

        # 4. 构建客户->样品数量的映射
        customer_sample_map = {item['related_customer']: item['sample_sum'] or 0 for item in sample_queryset}

        categories = []
        orders = []
        samples = []

        for item in order_queryset:
            customer_name = item['customer'] or '未知客户'
            categories.append(customer_name)
            orders.append(item['order_count'])
            # 从映射中获取样品数量，如果没有则为0
            samples.append(customer_sample_map.get(customer_name, 0))

        response_data = {
            "categories": categories,
            "orders": orders,
            "samples": samples
        }

        return ApiResponse.success(data=response_data, message="获取珠海客户统计数据成功")

# --- 上海订单&样点 ---
class ShanghaiCustomerStatisticsAPI(APIView):
    def get(self, request, format=None):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if start_date > end_date:
            return ApiResponse.failed(code=400, message="开始日期不能晚于结束日期")

        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        common_filter = {
            'execution_place__icontains': '上海',
            'requirement_confirm_date__gte': start_datetime,
            'requirement_confirm_date__lte': end_datetime,
        }

        # 使用annotate进行分组聚合，Count计算订单数，Sum计算样点数
        queryset = Order.objects.filter(**common_filter).values('customer').annotate(
            order_count=Count('order_id'),  # 按订单ID计数，确保唯一性
            sample_sum=Sum('sample_quantity')  # 求和sample_quantity字段
        ).order_by('customer')  # 按客户名称排序，保证结果顺序一致

        categories = []
        orders = []
        samples = []

        for item in queryset:
            customer_name = item['customer'] or '未知客户'
            categories.append(customer_name)
            orders.append(item['order_count'])
            samples.append(item['sample_sum'] or 0) # 如果sum为None，用0代替

        response_data = {
            "categories": categories,
            "orders": orders,
            "samples": samples
        }

        return ApiResponse.success(data=response_data, message="获取上海客户统计数据成功")

# --- 珠海机台利用率 ---
class ZhuhaiMachineUtilizationAPI(APIView):
    def _calculate_available_hours(self, start_date, end_date):
        """计算两个日期之间的理论可用工作小时数（每周5天，每天8小时）"""
        if start_date > end_date:
            return 0.0

        available_hours = 0.0
        workdays = [0, 1, 2, 3, 4]  # Monday to Friday (0=Mon, 4=Fri)
        work_hours_per_day = 8

        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() in workdays:
                available_hours += work_hours_per_day
            current_date += timedelta(days=1)

        return available_hours

    def get(self, request, format=None):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        if start_date > end_date:
            return ApiResponse.failed(
                code=400,
                message="日期范围错误：开始日期不能晚于结束日期")

        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

        total_available_hours = self._calculate_available_hours(start_date, end_date)

        if total_available_hours <= 0:
            return ApiResponse.success(
                data={
                    "machine_names": [],
                    "utilization_rates": [],
                    "total_working_hours": []
                },
                message=f"在日期范围 {start_date_str} 至 {end_date_str} 内没有可用的工作时间。"
            )

        all_process_records = Process.objects.filter(
            engineer_region='珠海实验室',
            start_time__lt=end_datetime,
            end_time__gt=start_datetime,
        ).only('testing_machine', 'start_time', 'end_time')

        # 按机台分组
        machine_records_dict = {}
        for record in all_process_records:
            machine_code = record.testing_machine or "未知机台"
            # 如果字典中没有该机台，则初始化一个空列表
            if machine_code not in machine_records_dict:
                machine_records_dict[machine_code] = []
            # 将当前记录添加到对应机台的列表中
            machine_records_dict[machine_code].append(record)

        machine_names = []
        utilization_rates = []
        total_working_hours_list = []

        # 遍历字典的键值对 (机台名称, 对应的工序记录列表)
        for machine_code, process_records in machine_records_dict.items():
            total_work_seconds = 0

            # 遍历当前机台的所有工序记录
            for record in process_records:
                # 应用时间窗口裁剪逻辑，计算有效工作时间
                actual_start = max(record.start_time, start_datetime)
                actual_end = min(record.end_time, end_datetime)

                if actual_start < actual_end:
                    work_delta = actual_end - actual_start
                    total_work_seconds += work_delta.total_seconds()

            # 将总秒数转换为小时
            total_working_hours = total_work_seconds / 3600.0

            # 计算利用率
            if total_available_hours < 1e-9:  # 避免除以零
                utilization_rate = 0.0
            else:
                utilization_rate = (total_working_hours / total_available_hours) * 100

            machine_names.append(machine_code)
            utilization_rates.append(round(utilization_rate, 2))
            total_working_hours_list.append(round(total_working_hours, 2))

        total_available_hours_list = [total_available_hours] * len(machine_names)

        response_data = {
            "categories": machine_names,
            "target": utilization_rates,
            "actual":total_available_hours_list,
            "compare": total_working_hours_list
        }

        return ApiResponse.success(
            data=response_data,
            message=f"成功获取珠海实验室机台利用率 (时间范围: {start_date_str} 至 {end_date_str})"
        )

# --- 珠海重要客户统计 ---
class ZhuhaiImportantCustomerAPI(APIView):
    TARGET_CUSTOMERS = ["淇澳岛", "情侣路", "唐淇路", "开普"]

    # 客户名称映射关系
    CUSTOMER_MAPPING = {
        "淇澳岛": "淇澳岛（全志）",
        "情侣路": "情侣路（极海）",
        "唐淇路": "唐淇路（博雅）",
        "开普": "凌霄岩（开普）"
    }

    DYNAMIC_MONTHS_2025 = [10, 11, 12]
    ALL_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # 写死的数据
    FIXED_DATA = {
        2024: {
            "淇澳岛": [9, 9, 9, 13, 13, 9, 15, 9, 16, 31, 20, 16],
            "情侣路": [7, 5, 6, 7, 7, 6, 7, 9, 10, 15, 8, 10],
            "唐淇路": [2, 5, 4, 4, 2, 0, 1, 4, 7, 14, 9, 5],
            "开普": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        },
        2025: {
            # 2025年1-9月的数据
            "淇澳岛": [12, 17, 18, 15, 7, 10, 12, 14, 8],
            "情侣路": [5, 6, 9, 5, 12, 5, 5, 14, 5],
            "唐淇路": [3, 1, 4, 11, 4, 3, 1, 2, 0],
            "开普": [0, 3, 8, 6, 9, 4, 8, 2, 1],
        }
    }

    def _get_dynamic_monthly_data(self, year, customer_name, months):
        """动态查询指定年份、指定客户在指定月份中的订单量。"""
        dynamic_data = []
        for month in months:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            count = Order.objects.filter(
                customer=customer_name,
                execution_place__icontains='珠海',
                requirement_confirm_date__gte=start_date,
                requirement_confirm_date__lt=end_date
            ).count()
            dynamic_data.append(count)

        return dynamic_data

    def get(self, request, format=None):
        try:
            primary_year = int(request.query_params.get('primary_year', 2026))
            comparison_year = int(request.query_params.get('comparison_year', 2025))
        except (ValueError, TypeError):
            return ApiResponse.failed(
                code=400,
                message="年份参数格式错误，请传入有效的年份数字。"
            )

        # 响应数据的主体结构
        response_customers = []

        # 遍历固定的客户列表
        for customer_db_name in self.TARGET_CUSTOMERS:
            # 获取客户的显示名称
            customer_display_name = self.CUSTOMER_MAPPING.get(customer_db_name, customer_db_name)

            # --- 处理对比年份的数据 ---
            if comparison_year == 2025:
                # 2025年 = 固定数据 + 动态10-12月
                fixed_part = self.FIXED_DATA.get(2025, {}).get(customer_db_name, [0] * 9)
                dynamic_part = self._get_dynamic_monthly_data(2025, customer_db_name, self.DYNAMIC_MONTHS_2025)
                comparison_series_data = fixed_part + dynamic_part
            elif comparison_year in self.FIXED_DATA:
                # 其他有固定数据的年份
                comparison_series_data = self.FIXED_DATA.get(comparison_year, {}).get(customer_db_name, [0] * 12)
            else:
                # 没有固定数据的年份，全量动态查询
                comparison_series_data = self._get_dynamic_monthly_data(comparison_year, customer_db_name, self.ALL_MONTHS)

            comparison_series = {
                "label": str(comparison_year),
                "data": comparison_series_data
            }

            # --- 处理主年份的数据 ---
            if primary_year == 2025:
                # 2025年 = 固定数据 + 动态10-12月
                fixed_part = self.FIXED_DATA.get(2025, {}).get(customer_db_name, [0] * 9)
                dynamic_part = self._get_dynamic_monthly_data(2025, customer_db_name, self.DYNAMIC_MONTHS_2025)
                primary_series_data = fixed_part + dynamic_part
            elif primary_year in self.FIXED_DATA:
                # 其他有固定数据的年份
                primary_series_data = self.FIXED_DATA.get(primary_year, {}).get(customer_db_name, [0] * 12)
            else:
                # 没有固定数据的年份（如2026），全量动态查询
                primary_series_data = self._get_dynamic_monthly_data(primary_year, customer_db_name, self.ALL_MONTHS)

            primary_series = {
                "label": str(primary_year),
                "data": primary_series_data
            }

            # --- 组装单个客户的完整数据 ---
            customer_data = {
                "name": customer_display_name,
                "series": [comparison_series, primary_series]
            }
            response_customers.append(customer_data)

        return ApiResponse.success(
            data={
                "customers": response_customers
            },
            message="成功获取珠海重要客户订单量统计。"
        )

# --- 上海重要客户统计 ---
class ShanghaiImportantCustomerAPI(APIView):
    TARGET_CUSTOMERS = ["五角场", "中科路", "洋山港", "新场镇"]

    # 客户名称映射关系
    CUSTOMER_MAPPING = {
        "五角场": "五角场",
        "中科路": "中科路（格科）",
        "洋山港": "洋山港（ZW）",
        "新场镇": "新场镇（昕原）"
    }

    # 需要动态查询的月份
    DYNAMIC_MONTHS_2025 = [11, 12]
    ALL_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # 写死的数据
    FIXED_DATA = {
        2024: {
            "五角场": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "中科路": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "洋山港": [520, 261, 380, 388, 201, 127, 207, 214, 230, 214, 134, 103],
            "新场镇": [0, 0, 0, 0, 0, 40, 53, 59, 50, 17, 23, 57],
        },
        2025: {
            # 2025年1-10月的数据
            "五角场": [0, 0, 0, 0, 231, 379, 491, 357, 363, 201],
            "中科路": [0, 0, 0, 274, 22, 145, 146, 276, 366, 201],
            "洋山港": [43, 79, 135, 536, 691, 415, 363, 433, 519, 629],
            "新场镇": [27, 41, 52, 71, 27, 36, 75, 51, 36, 27],
        }
    }

    def _get_dynamic_monthly_data(self, year, customer_name, months):
        """动态查询指定年份、指定客户在指定月份中的订单样品数量总和"""
        dynamic_data = []
        for month in months:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            # aggregate 和 Sum 计算 sample_quantity 的总和
            result = Order.objects.filter(
                customer=customer_name,
                execution_place__icontains='上海',
                requirement_confirm_date__gte=start_date,
                requirement_confirm_date__lt=end_date
            ).aggregate(total=Sum('sample_quantity'))

            # 如果 total 是 None (没有订单)，则取 0
            total_quantity = result['total'] or 0
            dynamic_data.append(total_quantity)

        return dynamic_data

    def get(self, request, format=None):
        try:
            primary_year = int(request.query_params.get('primary_year', 2026))
            comparison_year = int(request.query_params.get('comparison_year', 2025))
        except (ValueError, TypeError):
            return ApiResponse.failed(
                code=400,
                message="年份参数格式错误，请传入有效的年份数字。"
            )

        response_customers = []

        # 遍历固定的客户列表
        for customer_db_name in self.TARGET_CUSTOMERS:
            # 获取客户的显示名称
            customer_display_name = self.CUSTOMER_MAPPING.get(customer_db_name, customer_db_name)

            # --- 处理对比年份的数据 ---
            if comparison_year == 2025:
                # 2025年 = 固定数据 + 动态11-12月
                fixed_part = self.FIXED_DATA.get(2025, {}).get(customer_db_name, [0] * 10)
                dynamic_part = self._get_dynamic_monthly_data(2025, customer_db_name, self.DYNAMIC_MONTHS_2025)
                comparison_series_data = fixed_part + dynamic_part
            elif comparison_year in self.FIXED_DATA:
                # 其他有固定数据的年份
                comparison_series_data = self.FIXED_DATA.get(comparison_year, {}).get(customer_db_name, [0] * 12)
            else:
                # 没有固定数据的年份，全量动态查询
                comparison_series_data = self._get_dynamic_monthly_data(comparison_year, customer_db_name, self.ALL_MONTHS)

            comparison_series = {
                "label": str(comparison_year),
                "data": comparison_series_data
            }

            # --- 处理主年份的数据 ---
            if primary_year == 2025:
                # 2025年 = 固定数据 + 动态11-12月
                fixed_part = self.FIXED_DATA.get(2025, {}).get(customer_db_name, [0] * 10)
                dynamic_part = self._get_dynamic_monthly_data(2025, customer_db_name, self.DYNAMIC_MONTHS_2025)
                primary_series_data = fixed_part + dynamic_part
            elif primary_year in self.FIXED_DATA:
                # 其他有固定数据的年份
                primary_series_data = self.FIXED_DATA.get(primary_year, {}).get(customer_db_name, [0] * 12)
            else:
                # 没有固定数据的年份（如2026），全量动态查询
                primary_series_data = self._get_dynamic_monthly_data(primary_year, customer_db_name, self.ALL_MONTHS)

            primary_series = {
                "label": str(primary_year),
                "data": primary_series_data
            }

            # --- 组装单个客户的完整数据 ---
            customer_data = {
                "name": customer_display_name,
                "series": [comparison_series, primary_series]
            }
            response_customers.append(customer_data)

        return ApiResponse.success(
            data={
                "customers": response_customers
            },
            message="成功获取上海重要客户订单样品数量统计。"
        )

# --- 上海订单统计(月度) ---
class ShanghaiOrderStatisticsAPI(APIView):
    TARGET_YEARS = [2024, 2025, 2026]
    MONTHS_LABELS = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    # 需要动态计算的月份
    DYNAMIC_MONTHS_2025 = [11, 12]
    ALL_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # 死数据
    FIXED_DATA_2024 = [610, 292, 429, 459, 276, 287, 311, 430, 320, 348, 244, 264]
    FIXED_DATA_2025 = [160, 211, 515, 866, 1309, 1115, 1347, 1263, 1563, 1440]

    def _calculate_dynamic_data(self, year, months):
        """计算指定年份中指定月份列表的动态数据。"""
        dynamic_data = []
        for month in months:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            result = Order.objects.filter(
                execution_place__icontains='上海',
                requirement_confirm_date__gte=start_date,
                requirement_confirm_date__lt=end_date
            ).aggregate(total=Sum('sample_quantity'))

            total_quantity = result['total'] or 0
            dynamic_data.append(total_quantity)

        return dynamic_data

    def get(self, request):
        series = []
        for year in self.TARGET_YEARS:
            if year == 2024:
                series.append({'name': str(year), 'data': self.FIXED_DATA_2024})

            elif year == 2025:
                # 2025年数据 = 前10个月写死数据 + 后2个月动态计算数据
                dynamic_data = self._calculate_dynamic_data(year, self.DYNAMIC_MONTHS_2025)
                full_data = self.FIXED_DATA_2025 + dynamic_data
                series.append({'name': str(year), 'data': full_data})

            elif year == 2026:
                # 2026年数据 = 全部动态计算
                full_data = self._calculate_dynamic_data(year, self.ALL_MONTHS)
                series.append({'name': str(year), 'data': full_data})

        response_data = {
            'months': self.MONTHS_LABELS,
            'series': series
        }

        return ApiResponse.success(data=response_data, message="获取上海样点统计数据成功")



