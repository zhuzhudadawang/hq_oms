from datetime import datetime, timedelta, time
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from rest_framework.views import APIView
from apps.analysis.models import Process, MachineUsageRecord
from utils import Response

"""FIB人员完成率(月度)"""
class FibEngineerProjectCountAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["415", "414", "413", "412", "411", "410", "409", "408", "407", "406", "383"]
        test_item = ["TEM样品制备（平面、倒切、侧切_孔洞完整）",
                           "TEM样品制备（平面、倒切、侧切_单一完整）", "TEM样品制备（正切_孔洞完整）",
                           "TEM样品制备（正切_单一完整）", "TEM制样_细修（深度＞5um）", "TEM制样_细修（深度≤5um）",
                           "TEM样品制备（机械研磨）", "TEM样品制备（平面、倒切、侧切_分步）", "TEM样品制备（正切_分步）",
                           "TEM样品制备（clean）", "SEM/EDS分析服务","PFIB大尺寸切割"]
        failed_status = ["失败", "内部失败", "外部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]

        month_param = request.query_params.get("month", None)
        try:
            if month_param:
                year, month = map(int, month_param.split("-"))
                start_date = datetime(year, month, 1)
                end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
            else:
                now = datetime.now()
                start_date = datetime(now.year, now.month, 1)
                end_date = datetime(now.year + 1, 1, 1) if now.month == 12 else datetime(now.year, now.month + 1, 1)
            query_month = start_date.strftime("%Y-%m")
        except (ValueError, TypeError):
            return Response.ApiResponse.failed(
                code=400,
                message="月份参数格式错误，请传入YYYY-MM格式（如2024-05）",
                data={"valid_example": "2024-05", "invalid_param": month_param}
            )

        try:
            common_filter = {
                "test_item__in": test_item,
                "testing_engineer__isnull": False,
                "process_start_date__gte": start_date,
                "process_start_date__lt": end_date
            }
            actual_total_completed = 0
            actual_total_success = 0
            # 一次性查询该月份内所有符合条件的（工程师、样本ID、状态）原始记录
            engineer_sample_records = Process.objects.filter(
                **common_filter,
                status__in=completed_statuses
            ).exclude(
                testing_engineer__in=["", "樊佳博"]
            ).exclude(
                testing_engineer__icontains="外援"
            ).values("testing_engineer", "sample_id", "status")

            # 创建字典，用于存储每个（工程师, 样本ID）组合的最终状态
            engineer_sample_final_status = {}
            for record in engineer_sample_records:
                # 构建复合键：(工程师, 样本ID)，确保每个工程师处理的每个样本只被评估一次
                key = (record["testing_engineer"], record["sample_id"])
                current_status = record["status"]

                if key not in engineer_sample_final_status:
                    # 首次出现：如果当前状态是失败，则初始化为失败，否则为非失败
                    engineer_sample_final_status[key] = "失败" if current_status in failed_status else "非失败"
                else:
                    # 非首次出现：应用“失败优先”原则
                    # 如果当前记录是失败状态，且之前记录的状态是非失败，则将最终状态更新为失败
                    if current_status in failed_status and engineer_sample_final_status[key] == "非失败":
                        engineer_sample_final_status[key] = "失败"

            # 聚合统计每个工程师的完成量和失败量
            engineer_stats = {}
            for (engineer, sample_id), final_status in engineer_sample_final_status.items():
                if engineer not in engineer_stats:
                    engineer_stats[engineer] = {"completed": 0, "failed": 0}
                engineer_stats[engineer]["completed"] += 1
                if final_status == "失败":
                    engineer_stats[engineer]["failed"] += 1

            # 按“样本ID”分组，判定每个样本在整个月份的最终状态（失败优先）
            monthly_sample_final_status = {}
            for record in engineer_sample_records:
                sample_id = record["sample_id"]
                current_status = record["status"]

                if sample_id not in monthly_sample_final_status:
                    # 首次出现：初始化样本状态
                    monthly_sample_final_status[
                        sample_id] = "失败" if current_status in failed_status else "非失败"
                else:
                    # 非首次出现：失败优先（只要有一次失败，整个样本就判定为失败）
                    if current_status in failed_status and monthly_sample_final_status[sample_id] == "非失败":
                        monthly_sample_final_status[sample_id] = "失败"

            # 统计月度总计：完成总量、成功总量
            if monthly_sample_final_status:
                actual_total_completed = len(monthly_sample_final_status)  # 完成总量=不重复样本数（字典长度）
                actual_total_success = 0
                for status in monthly_sample_final_status.values():
                    if status == "非失败":  # 成功总量=非失败状态的样本数
                        actual_total_success += 1

            # 按完成量降序排序
            all_engineers = sorted(engineer_stats.keys(), key=lambda x: engineer_stats[x]["completed"], reverse=True)
            engineer_names = []
            success_counts = []
            completed_counts = []
            success_rates = []

            for engineer in all_engineers:
                stats = engineer_stats[engineer]
                completed_num = stats["completed"]
                failed_num = stats["failed"]
                success_num = completed_num - failed_num
                success_rate = round((success_num / completed_num) * 100, 2) if completed_num != 0 else 0.00

                engineer_names.append(engineer)
                success_counts.append(success_num)
                completed_counts.append(completed_num)
                success_rates.append(success_rate)

            return Response.ApiResponse.success(
                data={
                    "engineer_names": engineer_names,
                    "success_counts": success_counts,
                    "completed_counts": completed_counts,
                    "success_rates": success_rates,
                    "actual_total_completed": actual_total_completed,  # 全月实际完成总量（去重后）
                    "actual_total_success": actual_total_success  # 全月实际成功总量（去重后）
                },
                message=f"{query_month} 月份统计成功"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"{query_month} 月份统计失败：{str(e)}",
            )
"""FIB人员绩效工时统计（月度）"""
class FibEngineerPerformanceHoursAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["415", "414", "413", "412", "411", "410", "409", "408", "407", "406", "383"]
        test_item = ["TEM样品制备（平面、倒切、侧切_孔洞完整）",
                     "TEM样品制备（平面、倒切、侧切_单一完整）", "TEM样品制备（正切_孔洞完整）",
                     "TEM样品制备（正切_单一完整）", "TEM制样_细修（深度＞5um）", "TEM制样_细修（深度≤5um）",
                     "TEM样品制备（机械研磨）", "TEM样品制备（平面、倒切、侧切_分步）", "TEM样品制备（正切_分步）",
                     "TEM样品制备（clean）", "SEM/EDS分析服务","PFIB大尺寸切割"]
        month_param = request.query_params.get("month", None)
        try:
            if month_param:
                year, month = map(int, month_param.split("-"))
                start_date = datetime(year, month, 1)
                end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
            else:
                now = datetime.now()
                start_date = datetime(now.year, now.month, 1)
                end_date = datetime(now.year + 1, 1, 1) if now.month == 12 else datetime(now.year, now.month + 1, 1)
            query_month = start_date.strftime("%Y-%m")
        except (ValueError, TypeError):
            return Response.ApiResponse.failed(
                code=400,
                message="月份参数格式错误，请传入YYYY-MM格式（如2024-05）",
                data={"valid_example": "2024-05", "invalid_param": month_param}
            )

        try:
            common_filter = {
                "test_item__in": test_item,
                "testing_engineer__isnull": False,
                "process_start_date__gte": start_date,
                "process_start_date__lt": end_date,
                "is_calculate_performance": "是"
            }

            # 按工程师分组，统计绩效工时总和
            engineer_performance = Process.objects.filter(
                **common_filter
            ).exclude(
                testing_engineer__in=["", "樊佳博"]
            ).exclude(
                testing_engineer__icontains="外援"
            ).values("testing_engineer").annotate(
                total_performance_hours=Sum("performance_working_hours")
            ).order_by("-total_performance_hours")

            engineer_names = []
            performance_hours = []
            total_hours = 0

            for record in engineer_performance:
                engineer_names.append(record["testing_engineer"])
                hours = float(record["total_performance_hours"] or 0)
                performance_hours.append(round(hours, 2))
                total_hours += hours

            return Response.ApiResponse.success(
                data={
                    "engineer_names": engineer_names,
                    "performance_hours": performance_hours,
                    "total_performance_hours": round(total_hours, 2)
                },
                message=f"{query_month} 月份绩效工时统计成功"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"{query_month} 月份绩效工时统计失败：{str(e)}",
            )
"""TEM人员完成率（月度）"""
class TemEngineerProjectCountAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["427", "405", "404", "403", "402", "401", "400", "399", "398", "397", "396", "S12","S13"]
        test_item = ["PED测试", "非球差TEM-EDS点分析服务", "球差TEM-EDS点分析服务", "非球差TEM-EDS线分析服务",
                     "球差TEM-EDS线分析服务", "非球差TEM-EDS面分析服务", "球差TEM-EDS面分析服务",
                     "非球差TEM-EELS分析服务", "球差TEM-EELS分析服务", "非球差TEM分析服务", "球差TEM分析服务",
                     "STEM分析服务", "TEM补拍","粉末样品TEM制样"]  # 目标检测项目
        failed_status = ["失败", "内部失败", "外部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]  # 所有完成状态

        month_param = request.query_params.get("month", None)
        try:
            if month_param:
                year, month = map(int, month_param.split("-"))
                start_date = datetime(year, month, 1)
                end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
            else:
                now = datetime.now()
                start_date = datetime(now.year, now.month, 1)
                end_date = datetime(now.year + 1, 1, 1) if now.month == 12 else datetime(now.year, now.month + 1, 1)
            query_month = start_date.strftime("%Y-%m")
        except (ValueError, TypeError):
            return Response.ApiResponse.failed(
                code=400,
                message="月份参数格式错误，请传入YYYY-MM格式（如2024-05）",
                data={"valid_example": "2024-05", "invalid_param": month_param}
            )

        try:
            common_filter = {
                "test_item__in": test_item,
                "testing_engineer__isnull": False,
                "process_start_date__gte": start_date,
                "process_start_date__lt": end_date
            }
            actual_total_completed = 0
            actual_total_success = 0
            # 一次性查询该月份内所有符合条件的（工程师、样本ID、状态）原始记录
            engineer_sample_records = Process.objects.filter(
                **common_filter,
                status__in=completed_statuses
            ).values("testing_engineer", "sample_id", "status")

            # 创建字典，用于存储每个（工程师, 样本ID）组合的最终状态
            engineer_sample_final_status = {}
            for record in engineer_sample_records:
                # 构建复合键：(工程师, 样本ID)，确保每个工程师处理的每个样本只被评估一次
                key = (record["testing_engineer"], record["sample_id"])
                current_status = record["status"]

                if key not in engineer_sample_final_status:
                    # 首次出现：如果当前状态是失败，则初始化为失败，否则为非失败
                    engineer_sample_final_status[key] = "失败" if current_status in failed_status else "非失败"
                else:
                    # 非首次出现：应用“失败优先”原则
                    # 如果当前记录是失败状态，且之前记录的状态是非失败，则将最终状态更新为失败
                    if current_status in failed_status and engineer_sample_final_status[key] == "非失败":
                        engineer_sample_final_status[key] = "失败"

            # 聚合统计每个工程师的完成量和失败量
            engineer_stats = {}
            for (engineer, sample_id), final_status in engineer_sample_final_status.items():
                if engineer not in engineer_stats:
                    engineer_stats[engineer] = {"completed": 0, "failed": 0}
                engineer_stats[engineer]["completed"] += 1
                if final_status == "失败":
                    engineer_stats[engineer]["failed"] += 1

            # 按“样本ID”分组，判定每个样本在整个月份的最终状态（失败优先）
            monthly_sample_final_status = {}
            for record in engineer_sample_records:
                sample_id = record["sample_id"]
                current_status = record["status"]

                if sample_id not in monthly_sample_final_status:
                    # 首次出现：初始化样本状态
                    monthly_sample_final_status[
                        sample_id] = "失败" if current_status in failed_status else "非失败"
                else:
                    # 非首次出现：失败优先（只要有一次失败，整个样本就判定为失败）
                    if current_status in failed_status and monthly_sample_final_status[sample_id] == "非失败":
                        monthly_sample_final_status[sample_id] = "失败"

            # 统计月度总计：完成总量、成功总量
            if monthly_sample_final_status:
                actual_total_completed = len(monthly_sample_final_status)  # 完成总量=不重复样本数（字典长度）
                actual_total_success = 0
                for status in monthly_sample_final_status.values():
                    if status == "非失败":  # 成功总量=非失败状态的样本数
                        actual_total_success += 1

            # 按完成量降序排序
            all_engineers = sorted(engineer_stats.keys(), key=lambda x: engineer_stats[x]["completed"], reverse=True)
            engineer_names = []
            success_counts = []
            completed_counts = []
            success_rates = []

            for engineer in all_engineers:
                stats = engineer_stats[engineer]
                completed_num = stats["completed"]
                failed_num = stats["failed"]
                success_num = completed_num - failed_num
                success_rate = round((success_num / completed_num) * 100, 2) if completed_num != 0 else 0.00

                engineer_names.append(engineer)
                success_counts.append(success_num)
                completed_counts.append(completed_num)
                success_rates.append(success_rate)

            return Response.ApiResponse.success(
                data={
                    "engineer_names": engineer_names,
                    "success_counts": success_counts,
                    "completed_counts": completed_counts,
                    "success_rates": success_rates,
                    "actual_total_completed": actual_total_completed,  # 全月实际完成总量（去重后）
                    "actual_total_success": actual_total_success  # 全月实际成功总量（去重后）
                },
                message=f"{query_month} 月份统计成功"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"{query_month} 月份统计失败：{str(e)}",
            )
"""TEM人员绩效工时统计（月度）"""
class TemEngineerPerformanceHoursAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["427", "405", "404", "403", "402", "401", "400", "399", "398", "397", "396", "S12","S13"]
        test_item = ["PED测试", "非球差TEM-EDS点分析服务", "球差TEM-EDS点分析服务", "非球差TEM-EDS线分析服务",
                     "球差TEM-EDS线分析服务", "非球差TEM-EDS面分析服务", "球差TEM-EDS面分析服务",
                     "非球差TEM-EELS分析服务", "球差TEM-EELS分析服务", "非球差TEM分析服务", "球差TEM分析服务",
                     "STEM分析服务", "TEM补拍","粉末样品TEM制样"]  # 目标检测项目
        failed_status = ["失败", "内部失败", "外部失败"]
        month_param = request.query_params.get("month", None)
        try:
            if month_param:
                year, month = map(int, month_param.split("-"))
                start_date = datetime(year, month, 1)
                end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
            else:
                now = datetime.now()
                start_date = datetime(now.year, now.month, 1)
                end_date = datetime(now.year + 1, 1, 1) if now.month == 12 else datetime(now.year, now.month + 1, 1)
            query_month = start_date.strftime("%Y-%m")
        except (ValueError, TypeError):
            return Response.ApiResponse.failed(
                code=400,
                message="月份参数格式错误，请传入YYYY-MM格式（如2024-05）",
                data={"valid_example": "2024-05", "invalid_param": month_param}
            )

        try:
            common_filter = {
                "test_item__in": test_item,
                "testing_engineer__isnull": False,
                "process_start_date__gte": start_date,
                "process_start_date__lt": end_date,
                "is_calculate_performance": "是"
            }

            # 按工程师分组，统计绩效工时总和
            engineer_performance = Process.objects.filter(
                **common_filter
            ).exclude(
                testing_engineer__in=[""]
            ).values("testing_engineer").annotate(
                total_performance_hours=Sum("performance_working_hours")
            ).order_by("-total_performance_hours")

            engineer_names = []
            performance_hours = []
            total_hours = 0

            for record in engineer_performance:
                engineer_names.append(record["testing_engineer"])
                hours = float(record["total_performance_hours"] or 0)
                performance_hours.append(round(hours, 2))
                total_hours += hours

            return Response.ApiResponse.success(
                data={
                    "engineer_names": engineer_names,
                    "performance_hours": performance_hours,
                    "total_performance_hours": round(total_hours, 2)
                },
                message=f"{query_month} 月份绩效工时统计成功"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"{query_month} 月份绩效工时统计失败：{str(e)}",
            )


"""FIB周每日成功率（周度）"""
class FibEngineerDailyProjectCountAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["415", "414", "413", "412", "411", "410", "409", "408", "407", "406", "383"]  # 目标检测项目
        test_item = ["TEM样品制备（平面、倒切、侧切_孔洞完整）",
                     "TEM样品制备（平面、倒切、侧切_单一完整）", "TEM样品制备（正切_孔洞完整）",
                     "TEM样品制备（正切_单一完整）", "TEM制样_细修（深度＞5um）", "TEM制样_细修（深度≤5um）",
                     "TEM样品制备（机械研磨）", "TEM样品制备（平面、倒切、侧切_分步）", "TEM样品制备（正切_分步）",
                     "TEM样品制备（clean）", "SEM/EDS分析服务","PFIB大尺寸切割"]
        failed_status = ["失败", "内部失败", "外部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]  # 所有完成状态
        excluded_engineers = ["", "樊佳博"]

        # 日期范围
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        # 验证日期
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if start_date > end_date:
                return Response.ApiResponse.failed(
                    code=400,
                    message="日期范围错误：开始日期不能晚于结束日期"
                )
        except ValueError:
            return Response.ApiResponse.failed(
                code=400,
                message="日期参数格式错误，请传入YYYY-MM-DD格式（如2025-08-01）",
            )
        except TypeError:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少日期参数：请传入 start_date 和 end_date（格式YYYY-MM-DD）"
            )

        try:
            # 可复用筛选条件
            common_filter = {
                "test_item__in": test_item,
                "process_start_date__gte": datetime.combine(start_date, datetime.min.time()),
                "process_start_date__lte": datetime.combine(end_date, datetime.max.time())
            }

            # 查询所有符合条件的记录（日期+样本+状态）
            daily_sample_records = Process.objects.filter(
                **common_filter,
                status__in=completed_statuses
            ).exclude(
                testing_engineer__in=excluded_engineers
            ).exclude(
                testing_engineer__icontains="外援"
            ).annotate(
                daily_date=TruncDate("process_start_date")
            ).values("daily_date", "sample_id", "status")

            # 第一步：找出每个样本的最早出现日期和最终状态（失败优先）
            sample_first_date = {}  # 样本ID -> 最早出现日期
            sample_final_status = {}  # 样本ID -> 最终状态

            for record in daily_sample_records:
                sample_id = record["sample_id"]
                daily_date = record["daily_date"]
                status = record["status"]

                # 记录最早出现日期
                if sample_id not in sample_first_date:
                    sample_first_date[sample_id] = daily_date
                else:
                    if daily_date < sample_first_date[sample_id]:
                        sample_first_date[sample_id] = daily_date

                # 判定最终状态（失败优先）
                if sample_id not in sample_final_status:
                    sample_final_status[sample_id] = "失败" if status in failed_status else "非失败"
                else:
                    if sample_final_status[sample_id] == "非失败" and status in failed_status:
                        sample_final_status[sample_id] = "失败"

            # 计算总体统计值
            actual_total_completed = len(sample_final_status)  # 去重后的总样本数
            actual_total_success = list(sample_final_status.values()).count("非失败")  # 成功的样本数

            # 第二步：将每个样本归属到最早出现的那天
            completed_result = {}
            failed_result = {}

            for sample_id, first_date in sample_first_date.items():
                final_status = sample_final_status[sample_id]

                # 统计完成量（归属到最早出现日期）
                completed_result[first_date] = completed_result.get(first_date, 0) + 1

                # 统计失败量（归属到最早出现日期）
                if final_status == "失败":
                    failed_result[first_date] = failed_result.get(first_date, 0) + 1

            # 日期列表
            date_list = []
            current_date = start_date
            while current_date <= end_date:
                date_list.append(current_date)
                current_date += timedelta(days=1)

            # 数据集整理（成功量=完成量-失败量）
            dates = []
            daily_completed = []
            daily_failed = []
            daily_success = []
            daily_success_rate = []

            for date_obj in date_list:
                date_str = date_obj.strftime("%Y-%m-%d")
                completed = completed_result.get(date_obj, 0)
                failed = failed_result.get(date_obj, 0)
                success = completed - failed  # 成功量=完成量-失败量

                # 计算成功率（避免除零）
                success_rate = round((success / completed) * 100, 2) if completed != 0 else 0.00

                dates.append(date_str)
                daily_completed.append(completed)
                daily_failed.append(failed)
                daily_success.append(success)
                daily_success_rate.append(success_rate)

            stat_days = len(dates)
            return Response.ApiResponse.success(
                data={
                    "dates": dates,
                    "daily_completed_counts": daily_completed,
                    "daily_failed_counts": daily_failed,
                    "daily_success_counts": daily_success,
                    "daily_success_rates": daily_success_rate,
                    "actual_total_completed": actual_total_completed,
                    "actual_total_success": actual_total_success
                },
                message=f"{start_date_str} 至 {end_date_str} 每日统计完成（共{stat_days}天）"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"每日统计失败：{str(e)}",
            )
"""FIB内部周每日成功率（周度）"""
class FibInternalEngineerDailyProjectCountAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["415", "414", "413", "412", "411", "410", "409", "408", "407", "406", "383"]  # 目标检测项目
        test_item = ["TEM样品制备（平面、倒切、侧切_孔洞完整）",
                     "TEM样品制备（平面、倒切、侧切_单一完整）", "TEM样品制备（正切_孔洞完整）",
                     "TEM样品制备（正切_单一完整）", "TEM制样_细修（深度＞5um）", "TEM制样_细修（深度≤5um）",
                     "TEM样品制备（机械研磨）", "TEM样品制备（平面、倒切、侧切_分步）", "TEM样品制备（正切_分步）",
                     "TEM样品制备（clean）", "SEM/EDS分析服务","PFIB大尺寸切割"]
        failed_status = ["内部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]  # 所有完成状态
        excluded_engineers = ["", "樊佳博"]

        # 日期范围
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        # 验证日期
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if start_date > end_date:
                return Response.ApiResponse.failed(
                    code=400,
                    message="日期范围错误：开始日期不能晚于结束日期"
                )
        except ValueError:
            return Response.ApiResponse.failed(
                code=400,
                message="日期参数格式错误，请传入YYYY-MM-DD格式（如2025-08-01）",
            )
        except TypeError:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少日期参数：请传入 start_date 和 end_date（格式YYYY-MM-DD）"
            )

        try:
            # 可复用筛选条件
            common_filter = {
                "test_item__in": test_item,
                "process_start_date__gte": datetime.combine(start_date, datetime.min.time()),
                "process_start_date__lte": datetime.combine(end_date, datetime.max.time())
            }

            # 查询当天内符合条件的所有（日期+样本+状态）记录
            daily_sample_records = Process.objects.filter(
                **common_filter,
                status__in=completed_statuses
            ).exclude(
                testing_engineer__in=excluded_engineers
            ).exclude(
                testing_engineer__icontains="外援"
            ).annotate(
                daily_date=TruncDate("process_start_date")
            ).values("daily_date", "sample_id", "status")

            # 第一步：找出每个样本的最早出现日期和最终状态（失败优先）
            sample_first_date = {}  # 样本ID -> 最早出现日期
            sample_final_status = {}  # 样本ID -> 最终状态

            for record in daily_sample_records:
                sample_id = record["sample_id"]
                daily_date = record["daily_date"]
                status = record["status"]

                # 记录最早出现日期
                if sample_id not in sample_first_date:
                    sample_first_date[sample_id] = daily_date
                else:
                    if daily_date < sample_first_date[sample_id]:
                        sample_first_date[sample_id] = daily_date

                # 判定最终状态（失败优先）
                if sample_id not in sample_final_status:
                    sample_final_status[sample_id] = "失败" if status in failed_status else "非失败"
                else:
                    if sample_final_status[sample_id] == "非失败" and status in failed_status:
                        sample_final_status[sample_id] = "失败"

            # 计算总体统计值
            actual_total_completed = len(sample_final_status)  # 去重后的总样本数
            actual_total_success = list(sample_final_status.values()).count("非失败")  # 成功的样本数

            # 第二步：将每个样本归属到最早出现的那天
            completed_result = {}
            failed_result = {}

            for sample_id, first_date in sample_first_date.items():
                final_status = sample_final_status[sample_id]

                # 统计完成量（归属到最早出现日期）
                completed_result[first_date] = completed_result.get(first_date, 0) + 1

                # 统计失败量（归属到最早出现日期）
                if final_status == "失败":
                    failed_result[first_date] = failed_result.get(first_date, 0) + 1

            # 日期列表
            date_list = []
            current_date = start_date
            while current_date <= end_date:
                date_list.append(current_date)
                current_date += timedelta(days=1)

            # 数据集整理（成功量=完成量-失败量）
            dates = []
            daily_completed = []
            daily_failed = []
            daily_success = []
            daily_success_rate = []

            for date_obj in date_list:
                date_str = date_obj.strftime("%Y-%m-%d")
                completed = completed_result.get(date_obj, 0)
                failed = failed_result.get(date_obj, 0)
                success = completed - failed  # 成功量=完成量-失败量

                # 计算成功率（避免除零）
                success_rate = round((success / completed) * 100, 2) if completed != 0 else 0.00

                dates.append(date_str)
                daily_completed.append(completed)
                daily_failed.append(failed)
                daily_success.append(success)
                daily_success_rate.append(success_rate)

            stat_days = len(dates)
            return Response.ApiResponse.success(
                data={
                    "dates": dates,
                    "daily_completed_counts": daily_completed,
                    "daily_failed_counts": daily_failed,  # 新增：每日失败量
                    "daily_success_counts": daily_success,  # 成功量=完成量-失败量
                    "daily_success_rates": daily_success_rate,
                    "actual_total_completed": actual_total_completed,  # 整个日期范围内的实际完成总量（去重后）
                    "actual_total_success": actual_total_success  # 整个日期范围内的实际成功总量（去重后）
                },
                message=f"{start_date_str} 至 {end_date_str} 每日统计完成（共{stat_days}天）"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"每日统计失败：{str(e)}",
            )
"""FIB外部周每日成功率（周度）"""
class FibExternalEngineerDailyProjectCountAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["415", "414", "413", "412", "411", "410", "409", "408", "407", "406", "383"]  # 目标检测项目
        test_item = ["TEM样品制备（平面、倒切、侧切_孔洞完整）",
                     "TEM样品制备（平面、倒切、侧切_单一完整）", "TEM样品制备（正切_孔洞完整）",
                     "TEM样品制备（正切_单一完整）", "TEM制样_细修（深度＞5um）", "TEM制样_细修（深度≤5um）",
                     "TEM样品制备（机械研磨）", "TEM样品制备（平面、倒切、侧切_分步）", "TEM样品制备（正切_分步）",
                     "TEM样品制备（clean）", "SEM/EDS分析服务","PFIB大尺寸切割"]
        failed_status = ["外部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]  # 所有完成状态
        excluded_engineers = ["", "樊佳博"]

        # 日期范围
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        # 验证日期
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if start_date > end_date:
                return Response.ApiResponse.failed(
                    code=400,
                    message="日期范围错误：开始日期不能晚于结束日期"
                )
        except ValueError:
            return Response.ApiResponse.failed(
                code=400,
                message="日期参数格式错误，请传入YYYY-MM-DD格式（如2025-08-01）",
            )
        except TypeError:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少日期参数：请传入 start_date 和 end_date（格式YYYY-MM-DD）"
            )

        try:
            # 可复用筛选条件
            common_filter = {
                "test_item__in": test_item,
                "process_start_date__gte": datetime.combine(start_date, datetime.min.time()),
                "process_start_date__lte": datetime.combine(end_date, datetime.max.time())
            }

            # 查询当天内符合条件的所有（日期+样本+状态）记录
            daily_sample_records = Process.objects.filter(
                **common_filter,
                status__in=completed_statuses
            ).exclude(
                testing_engineer__in=excluded_engineers
            ).exclude(
                testing_engineer__icontains="外援"
            ).annotate(
                daily_date=TruncDate("process_start_date")
            ).values("daily_date", "sample_id", "status")

            # 第一步：找出每个样本的最早出现日期和最终状态（失败优先）
            sample_first_date = {}  # 样本ID -> 最早出现日期
            sample_final_status = {}  # 样本ID -> 最终状态

            for record in daily_sample_records:
                sample_id = record["sample_id"]
                daily_date = record["daily_date"]
                status = record["status"]

                # 记录最早出现日期
                if sample_id not in sample_first_date:
                    sample_first_date[sample_id] = daily_date
                else:
                    if daily_date < sample_first_date[sample_id]:
                        sample_first_date[sample_id] = daily_date

                # 判定最终状态（失败优先）
                if sample_id not in sample_final_status:
                    sample_final_status[sample_id] = "失败" if status in failed_status else "非失败"
                else:
                    if sample_final_status[sample_id] == "非失败" and status in failed_status:
                        sample_final_status[sample_id] = "失败"

            # 计算总体统计值
            actual_total_completed = len(sample_final_status)  # 去重后的总样本数
            actual_total_success = list(sample_final_status.values()).count("非失败")  # 成功的样本数

            # 第二步：将每个样本归属到最早出现的那天
            completed_result = {}
            failed_result = {}

            for sample_id, first_date in sample_first_date.items():
                final_status = sample_final_status[sample_id]

                # 统计完成量（归属到最早出现日期）
                completed_result[first_date] = completed_result.get(first_date, 0) + 1

                # 统计失败量（归属到最早出现日期）
                if final_status == "失败":
                    failed_result[first_date] = failed_result.get(first_date, 0) + 1

            # 日期列表
            date_list = []
            current_date = start_date
            while current_date <= end_date:
                date_list.append(current_date)
                current_date += timedelta(days=1)

            # 数据集整理（成功量=完成量-失败量）
            dates = []
            daily_completed = []
            daily_failed = []
            daily_success = []
            daily_success_rate = []

            for date_obj in date_list:
                date_str = date_obj.strftime("%Y-%m-%d")
                completed = completed_result.get(date_obj, 0)
                failed = failed_result.get(date_obj, 0)
                success = completed - failed  # 成功量=完成量-失败量

                # 计算成功率（避免除零）
                success_rate = round((success / completed) * 100, 2) if completed != 0 else 0.00

                dates.append(date_str)
                daily_completed.append(completed)
                daily_failed.append(failed)
                daily_success.append(success)
                daily_success_rate.append(success_rate)

            stat_days = len(dates)
            return Response.ApiResponse.success(
                data={
                    "dates": dates,
                    "daily_completed_counts": daily_completed,
                    "daily_failed_counts": daily_failed,  # 新增：每日失败量
                    "daily_success_counts": daily_success,  # 成功量=完成量-失败量
                    "daily_success_rates": daily_success_rate,
                    "actual_total_completed": actual_total_completed,  # 整个日期范围内的实际完成总量（去重后）
                    "actual_total_success": actual_total_success  # 整个日期范围内的实际成功总量（去重后）
                },
                message=f"{start_date_str} 至 {end_date_str} 每日统计完成（共{stat_days}天）"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"每日统计失败：{str(e)}",
            )

"""TEM周每日成功率（周度）"""
class TemEngineerDailyProjectCountAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects_projects = ["427", "405", "404", "403", "402", "401", "400", "399", "398", "397", "396", "S12","S13"]  # 目标检测项目
        test_item = ["PED测试", "非球差TEM-EDS点分析服务", "球差TEM-EDS点分析服务", "非球差TEM-EDS线分析服务",
                     "球差TEM-EDS线分析服务", "非球差TEM-EDS面分析服务", "球差TEM-EDS面分析服务",
                     "非球差TEM-EELS分析服务", "球差TEM-EELS分析服务", "非球差TEM分析服务", "球差TEM分析服务",
                     "STEM分析服务", "TEM补拍","粉末样品TEM制样"]  # 目标检测项目
        failed_status = ["失败", "内部失败", "外部失败"]
        failed_status = ["失败", "内部失败", "外部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]  # 所有完成状态

        # 日期范围
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        # 验证日期
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if start_date > end_date:
                return Response.ApiResponse.failed(
                    code=400,
                    message="日期范围错误：开始日期不能晚于结束日期"
                )
        except ValueError:
            return Response.ApiResponse.failed(
                code=400,
                message="日期参数格式错误，请传入YYYY-MM-DD格式（如2025-08-01）",
            )
        except TypeError:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少日期参数：请传入 start_date 和 end_date（格式YYYY-MM-DD）"
            )

        try:
            # 可复用筛选条件
            common_filter = {
                "test_item__in": test_item,
                "process_start_date__gte": datetime.combine(start_date, datetime.min.time()),
                "process_start_date__lte": datetime.combine(end_date, datetime.max.time())
            }

            # 查询当天内符合条件的所有（日期+样本+状态）记录
            daily_sample_records = Process.objects.filter(
                **common_filter,
                status__in=completed_statuses
            ).annotate(
                daily_date=TruncDate("process_start_date")
            ).values("daily_date", "sample_id", "status")

            # 第一步：找出每个样本的最早出现日期和最终状态（失败优先）
            sample_first_date = {}  # 样本ID -> 最早出现日期
            sample_final_status = {}  # 样本ID -> 最终状态

            for record in daily_sample_records:
                sample_id = record["sample_id"]
                daily_date = record["daily_date"]
                status = record["status"]

                # 记录最早出现日期
                if sample_id not in sample_first_date:
                    sample_first_date[sample_id] = daily_date
                else:
                    if daily_date < sample_first_date[sample_id]:
                        sample_first_date[sample_id] = daily_date

                # 判定最终状态（失败优先）
                if sample_id not in sample_final_status:
                    sample_final_status[sample_id] = "失败" if status in failed_status else "非失败"
                else:
                    if sample_final_status[sample_id] == "非失败" and status in failed_status:
                        sample_final_status[sample_id] = "失败"

            # 计算总体统计值
            actual_total_completed = len(sample_final_status)  # 去重后的总样本数
            actual_total_success = list(sample_final_status.values()).count("非失败")  # 成功的样本数

            # 第二步：将每个样本归属到最早出现的那天
            completed_result = {}
            failed_result = {}

            for sample_id, first_date in sample_first_date.items():
                final_status = sample_final_status[sample_id]

                # 统计完成量（归属到最早出现日期）
                completed_result[first_date] = completed_result.get(first_date, 0) + 1

                # 统计失败量（归属到最早出现日期）
                if final_status == "失败":
                    failed_result[first_date] = failed_result.get(first_date, 0) + 1

            # 日期列表
            date_list = []
            current_date = start_date
            while current_date <= end_date:
                date_list.append(current_date)
                current_date += timedelta(days=1)

            # 数据集整理（成功量=完成量-失败量）
            dates = []
            daily_completed = []
            daily_failed = []
            daily_success = []
            daily_success_rate = []

            for date_obj in date_list:
                date_str = date_obj.strftime("%Y-%m-%d")
                completed = completed_result.get(date_obj, 0)
                failed = failed_result.get(date_obj, 0)
                success = completed - failed  # 成功量=完成量-失败量

                # 计算成功率（避免除零）
                success_rate = round((success / completed) * 100, 2) if completed != 0 else 0.00

                dates.append(date_str)
                daily_completed.append(completed)
                daily_failed.append(failed)
                daily_success.append(success)
                daily_success_rate.append(success_rate)

            stat_days = len(dates)
            return Response.ApiResponse.success(
                data={
                    "dates": dates,
                    "daily_completed_counts": daily_completed,
                    "daily_failed_counts": daily_failed,  # 新增：每日失败量
                    "daily_success_counts": daily_success,  # 成功量=完成量-失败量
                    "daily_success_rates": daily_success_rate,
                    "actual_total_completed": actual_total_completed,  # 整个日期范围内的实际完成总量（去重后）
                    "actual_total_success": actual_total_success  # 整个日期范围内的实际成功总量（去重后）
                },
                message=f"{start_date_str} 至 {end_date_str} 每日统计完成（共{stat_days}天）"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"每日统计失败：{str(e)}",
            )
"""TEM内部周每日成功率（周度）"""
class TemInternalEngineerDailyProjectCountAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["427", "405", "404", "403", "402", "401", "400", "399", "398", "397", "396", "S12","S13"]  # 目标检测项目
        test_item = ["PED测试", "非球差TEM-EDS点分析服务", "球差TEM-EDS点分析服务", "非球差TEM-EDS线分析服务",
                     "球差TEM-EDS线分析服务", "非球差TEM-EDS面分析服务", "球差TEM-EDS面分析服务",
                     "非球差TEM-EELS分析服务", "球差TEM-EELS分析服务", "非球差TEM分析服务", "球差TEM分析服务",
                     "STEM分析服务", "TEM补拍","粉末样品TEM制样"]  # 目标检测项目
        failed_status = ["失败", "内部失败", "外部失败"]
        failed_status = ["内部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]  # 所有完成状态

        # 日期范围
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        # 验证日期
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if start_date > end_date:
                return Response.ApiResponse.failed(
                    code=400,
                    message="日期范围错误：开始日期不能晚于结束日期"
                )
        except ValueError:
            return Response.ApiResponse.failed(
                code=400,
                message="日期参数格式错误，请传入YYYY-MM-DD格式（如2025-08-01）",
            )
        except TypeError:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少日期参数：请传入 start_date 和 end_date（格式YYYY-MM-DD）"
            )

        try:
            # 可复用筛选条件
            common_filter = {
                "test_item__in": test_item,
                "process_start_date__gte": datetime.combine(start_date, datetime.min.time()),
                "process_start_date__lte": datetime.combine(end_date, datetime.max.time())
            }

            # 查询当天内符合条件的所有（日期+样本+状态）记录
            daily_sample_records = Process.objects.filter(
                **common_filter,
                status__in=completed_statuses
            ).annotate(
                daily_date=TruncDate("process_start_date")
            ).values("daily_date", "sample_id", "status")

            # 第一步：找出每个样本的最早出现日期和最终状态（失败优先）
            sample_first_date = {}  # 样本ID -> 最早出现日期
            sample_final_status = {}  # 样本ID -> 最终状态

            for record in daily_sample_records:
                sample_id = record["sample_id"]
                daily_date = record["daily_date"]
                status = record["status"]

                # 记录最早出现日期
                if sample_id not in sample_first_date:
                    sample_first_date[sample_id] = daily_date
                else:
                    if daily_date < sample_first_date[sample_id]:
                        sample_first_date[sample_id] = daily_date

                # 判定最终状态（失败优先）
                if sample_id not in sample_final_status:
                    sample_final_status[sample_id] = "失败" if status in failed_status else "非失败"
                else:
                    if sample_final_status[sample_id] == "非失败" and status in failed_status:
                        sample_final_status[sample_id] = "失败"

            # 计算总体统计值
            actual_total_completed = len(sample_final_status)  # 去重后的总样本数
            actual_total_success = list(sample_final_status.values()).count("非失败")  # 成功的样本数

            # 第二步：将每个样本归属到最早出现的那天
            completed_result = {}
            failed_result = {}

            for sample_id, first_date in sample_first_date.items():
                final_status = sample_final_status[sample_id]

                # 统计完成量（归属到最早出现日期）
                completed_result[first_date] = completed_result.get(first_date, 0) + 1

                # 统计失败量（归属到最早出现日期）
                if final_status == "失败":
                    failed_result[first_date] = failed_result.get(first_date, 0) + 1

            # 日期列表
            date_list = []
            current_date = start_date
            while current_date <= end_date:
                date_list.append(current_date)
                current_date += timedelta(days=1)

            # 数据集整理（成功量=完成量-失败量）
            dates = []
            daily_completed = []
            daily_failed = []
            daily_success = []
            daily_success_rate = []

            for date_obj in date_list:
                date_str = date_obj.strftime("%Y-%m-%d")
                completed = completed_result.get(date_obj, 0)
                failed = failed_result.get(date_obj, 0)
                success = completed - failed  # 成功量=完成量-失败量

                # 计算成功率（避免除零）
                success_rate = round((success / completed) * 100, 2) if completed != 0 else 0.00

                dates.append(date_str)
                daily_completed.append(completed)
                daily_failed.append(failed)
                daily_success.append(success)
                daily_success_rate.append(success_rate)

            stat_days = len(dates)
            return Response.ApiResponse.success(
                data={
                    "dates": dates,
                    "daily_completed_counts": daily_completed,
                    "daily_failed_counts": daily_failed,  # 新增：每日失败量
                    "daily_success_counts": daily_success,  # 成功量=完成量-失败量
                    "daily_success_rates": daily_success_rate,
                    "actual_total_completed": actual_total_completed,  # 整个日期范围内的实际完成总量（去重后）
                    "actual_total_success": actual_total_success  # 整个日期范围内的实际成功总量（去重后）
                },
                message=f"{start_date_str} 至 {end_date_str} 每日统计完成（共{stat_days}天）"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"每日统计失败：{str(e)}",
            )
"""TEM外部周每日成功率（周度）"""
class TemExternalEngineerDailyProjectCountAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["427", "405", "404", "403", "402", "401", "400", "399", "398", "397", "396", "S12","S13"]  # 目标检测项目
        test_item = ["PED测试", "非球差TEM-EDS点分析服务", "球差TEM-EDS点分析服务", "非球差TEM-EDS线分析服务",
                     "球差TEM-EDS线分析服务", "非球差TEM-EDS面分析服务", "球差TEM-EDS面分析服务",
                     "非球差TEM-EELS分析服务", "球差TEM-EELS分析服务", "非球差TEM分析服务", "球差TEM分析服务",
                     "STEM分析服务", "TEM补拍","粉末样品TEM制样"]  # 目标检测项目
        failed_status = ["失败", "内部失败", "外部失败"]
        failed_status = ["外部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]  # 所有完成状态

        # 日期范围
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        # 验证日期
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if start_date > end_date:
                return Response.ApiResponse.failed(
                    code=400,
                    message="日期范围错误：开始日期不能晚于结束日期"
                )
        except ValueError:
            return Response.ApiResponse.failed(
                code=400,
                message="日期参数格式错误，请传入YYYY-MM-DD格式（如2025-08-01）",
            )
        except TypeError:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少日期参数：请传入 start_date 和 end_date（格式YYYY-MM-DD）"
            )

        try:
            # 可复用筛选条件
            common_filter = {
                "test_item__in": test_item,
                "process_start_date__gte": datetime.combine(start_date, datetime.min.time()),
                "process_start_date__lte": datetime.combine(end_date, datetime.max.time())
            }

            # 查询当天内符合条件的所有（日期+样本+状态）记录
            daily_sample_records = Process.objects.filter(
                **common_filter,
                status__in=completed_statuses
            ).annotate(
                daily_date=TruncDate("process_start_date")
            ).values("daily_date", "sample_id", "status")

            # 第一步：找出每个样本的最早出现日期和最终状态（失败优先）
            sample_first_date = {}  # 样本ID -> 最早出现日期
            sample_final_status = {}  # 样本ID -> 最终状态

            for record in daily_sample_records:
                sample_id = record["sample_id"]
                daily_date = record["daily_date"]
                status = record["status"]

                # 记录最早出现日期
                if sample_id not in sample_first_date:
                    sample_first_date[sample_id] = daily_date
                else:
                    if daily_date < sample_first_date[sample_id]:
                        sample_first_date[sample_id] = daily_date

                # 判定最终状态（失败优先）
                if sample_id not in sample_final_status:
                    sample_final_status[sample_id] = "失败" if status in failed_status else "非失败"
                else:
                    if sample_final_status[sample_id] == "非失败" and status in failed_status:
                        sample_final_status[sample_id] = "失败"

            # 计算总体统计值
            actual_total_completed = len(sample_final_status)  # 去重后的总样本数
            actual_total_success = list(sample_final_status.values()).count("非失败")  # 成功的样本数

            # 第二步：将每个样本归属到最早出现的那天
            completed_result = {}
            failed_result = {}

            for sample_id, first_date in sample_first_date.items():
                final_status = sample_final_status[sample_id]

                # 统计完成量（归属到最早出现日期）
                completed_result[first_date] = completed_result.get(first_date, 0) + 1

                # 统计失败量（归属到最早出现日期）
                if final_status == "失败":
                    failed_result[first_date] = failed_result.get(first_date, 0) + 1

            # 日期列表
            date_list = []
            current_date = start_date
            while current_date <= end_date:
                date_list.append(current_date)
                current_date += timedelta(days=1)

            # 数据集整理（成功量=完成量-失败量）
            dates = []
            daily_completed = []
            daily_failed = []
            daily_success = []
            daily_success_rate = []

            for date_obj in date_list:
                date_str = date_obj.strftime("%Y-%m-%d")
                completed = completed_result.get(date_obj, 0)
                failed = failed_result.get(date_obj, 0)
                success = completed - failed  # 成功量=完成量-失败量

                # 计算成功率（避免除零）
                success_rate = round((success / completed) * 100, 2) if completed != 0 else 0.00

                dates.append(date_str)
                daily_completed.append(completed)
                daily_failed.append(failed)
                daily_success.append(success)
                daily_success_rate.append(success_rate)

            stat_days = len(dates)
            return Response.ApiResponse.success(
                data={
                    "dates": dates,
                    "daily_completed_counts": daily_completed,
                    "daily_failed_counts": daily_failed,  # 新增：每日失败量
                    "daily_success_counts": daily_success,  # 成功量=完成量-失败量
                    "daily_success_rates": daily_success_rate,
                    "actual_total_completed": actual_total_completed,  # 整个日期范围内的实际完成总量（去重后）
                    "actual_total_success": actual_total_success  # 整个日期范围内的实际成功总量（去重后）
                },
                message=f"{start_date_str} 至 {end_date_str} 每日统计完成（共{stat_days}天）"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"每日统计失败：{str(e)}",
            )


"""FIB人员产出饱和度（周度）"""
class FibEngineerSuccessByDateRangeAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["415", "414", "413", "412", "411", "410", "409", "408", "407", "406", "383"]  # 目标检测项目
        test_item = ["TEM样品制备（平面、倒切、侧切_孔洞完整）",
                     "TEM样品制备（平面、倒切、侧切_单一完整）", "TEM样品制备（正切_孔洞完整）",
                     "TEM样品制备（正切_单一完整）", "TEM制样_细修（深度＞5um）", "TEM制样_细修（深度≤5um）",
                     "TEM样品制备（机械研磨）", "TEM样品制备（平面、倒切、侧切_分步）", "TEM样品制备（正切_分步）",
                     "TEM样品制备（clean）", "SEM/EDS分析服务","PFIB大尺寸切割"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]
        day_required_count = 3.5  # 每日应当数量

        # 日期范围参数
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        # 验证日期参数
        try:
            # 解析日期字符串为 datetime 对象
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            # 确保开始日期 <= 结束日期
            if start_date > end_date:
                return Response.ApiResponse.failed(
                    code=400,
                    message="日期范围错误：开始日期不能晚于结束日期"
                )

        except ValueError:
            return Response.ApiResponse.failed(
                code=400,
                message="日期参数格式错误，请传入YYYY-MM-DD格式（如2025-08-01）",
            )
        except TypeError:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少日期参数：请传入 start_date 和 end_date（格式YYYY-MM-DD）"
            )

        try:
            # 筛选目标项目+成功状态+日期范围+有效工程师
            success_queryset = (Process.objects.filter(
                test_item__in=test_item,
                status__in=completed_statuses,
                testing_engineer__isnull=False,
                process_start_date__gte=datetime.combine(start_date, datetime.min.time()),
                process_start_date__lte=datetime.combine(end_date, datetime.max.time())
            ).exclude(
                testing_engineer__in=["", "樊佳博"]
            ).exclude(
                testing_engineer__icontains="外援"
            ).values("testing_engineer").annotate(
                success_count=Count("process_id")  # 按工程师分组，统计成功数量
            ).order_by("-success_count"))  # 按成功数量降序排列

            # 返回数据集
            engineer_names = []
            success_counts = []
            saturation_rates = []
            required_counts = []

            # 日期范围内总应当数量
            date_diff_days = (end_date - start_date).days + 1
            required_count = day_required_count * date_diff_days

            for item in success_queryset:
                engineer = item["testing_engineer"]
                actual_success = item["success_count"]
                # 计算饱和度
                saturation = round((actual_success / required_count) * 100, 2) if required_count != 0 else 0.00

                engineer_names.append(engineer)
                success_counts.append(actual_success)
                saturation_rates.append(saturation)
                required_counts.append(required_count)

            return Response.ApiResponse.success(
                data={
                    "engineer_names": engineer_names,
                    "success_counts": success_counts,
                    "saturation_rates": saturation_rates,
                    "required_counts": required_counts,
                },
                message=f"{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 成功数量+饱和度统计完成"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"统计失败：{str(e)}",
            )
"""TEM人员产出饱和度（周度）"""
class TemEngineerSuccessByDateRangeAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["427", "405", "404", "403", "402", "401", "400", "399", "398", "397", "396", "S12","S13"]  # 目标检测项目
        test_item = ["PED测试", "非球差TEM-EDS点分析服务", "球差TEM-EDS点分析服务", "非球差TEM-EDS线分析服务",
                     "球差TEM-EDS线分析服务", "非球差TEM-EDS面分析服务", "球差TEM-EDS面分析服务",
                     "非球差TEM-EELS分析服务", "球差TEM-EELS分析服务", "非球差TEM分析服务", "球差TEM分析服务",
                     "STEM分析服务", "TEM补拍","粉末样品TEM制样"]  # 目标检测项目
        failed_status = ["失败", "内部失败", "外部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]
        day_required_count = 10  # 每日应当数量

        # 日期范围参数
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        # 验证日期参数
        try:
            # 解析日期字符串为 datetime 对象
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            # 确保开始日期 <= 结束日期
            if start_date > end_date:
                return Response.ApiResponse.failed(
                    code=400,
                    message="日期范围错误：开始日期不能晚于结束日期"
                )
        except ValueError:
            return Response.ApiResponse.failed(
                code=400,
                message="日期参数格式错误，请传入YYYY-MM-DD格式（如2025-08-01）",
            )
        except TypeError:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少日期参数：请传入 start_date 和 end_date（格式YYYY-MM-DD）"
            )

        try:
            # 筛选目标项目+成功状态+日期范围+有效工程师
            success_queryset = Process.objects.filter(
                test_item__in=test_item,
                status__in=completed_statuses,
                testing_engineer__isnull=False,
                process_start_date__gte=datetime.combine(start_date, datetime.min.time()),
                process_start_date__lte=datetime.combine(end_date, datetime.max.time())
            ).values("testing_engineer").annotate(
                success_count=Sum("performance_working_hours")  # 按工程师分组，统计绩效工时总和
            ).order_by("-success_count")  # 按绩效工时降序排列

            # 返回数据集
            engineer_names = []
            success_counts = []
            saturation_rates = []
            required_counts = []

            # 日期范围内总应当数量
            date_diff_days = (end_date - start_date).days + 1
            required_count = day_required_count * date_diff_days

            for item in success_queryset:
                engineer = item["testing_engineer"]
                actual_success = float(item["success_count"] or 0)
                # 计算饱和度
                saturation = round((actual_success / required_count) * 100, 2) if required_count != 0 else 0.00

                engineer_names.append(engineer)
                success_counts.append(actual_success)
                saturation_rates.append(saturation)
                required_counts.append(required_count)

            return Response.ApiResponse.success(
                data={
                    "engineer_names": engineer_names,
                    "success_counts": success_counts,
                    "saturation_rates": saturation_rates,
                    "required_counts": required_counts,
                },
                message=f"{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 成功数量+饱和度统计完成"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"统计失败：{str(e)}",
            )
"""FIB人员平均饱和度（周度）"""
class FibEngineerSuccessCoreIndexAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["415", "414", "413", "412", "411", "410", "409", "408", "407", "406", "383"]  # 目标检测项目
        test_item = ["TEM样品制备（平面、倒切、侧切_孔洞完整）",
                     "TEM样品制备（平面、倒切、侧切_单一完整）", "TEM样品制备（正切_孔洞完整）",
                     "TEM样品制备（正切_单一完整）", "TEM制样_细修（深度＞5um）", "TEM制样_细修（深度≤5um）",
                     "TEM样品制备（机械研磨）", "TEM样品制备（平面、倒切、侧切_分步）", "TEM样品制备（正切_分步）",
                     "TEM样品制备（clean）", "SEM/EDS分析服务","PFIB大尺寸切割"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]
        day_required_count = 3.5

        # 日期范围
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            if start_date > end_date:
                return Response.ApiResponse.failed(code=400, message="开始日期不能晚于结束日期")
        except ValueError:
            return Response.ApiResponse.failed(code=400, message="日期格式错误，需为YYYY-MM-DD",
                                               data={"valid_example": "start_date=2025-08-01&end_date=2025-08-31"})
        except TypeError:
            return Response.ApiResponse.failed(code=400, message="缺少 start_date 或 end_date")

        try:
            # 统计总成功数量
            total_success = Process.objects.filter(
                test_item__in=test_item,
                status__in=completed_statuses,
                process_start_date__gte=datetime.combine(start_date, datetime.min.time()),
                process_start_date__lte=datetime.combine(end_date, datetime.max.time())
            ).exclude(
                testing_engineer__in=["", "樊佳博"]  # 新增：排除目标工程师和空值
            ).exclude(
                testing_engineer__icontains="外援"
            ).count()

            # 统计参与的工程师总数（去重：同一工程师多次成功只算1人）
            involved_engineers = (Process.objects.filter(
                test_item__in=test_item,
                status__in=completed_statuses,
                testing_engineer__isnull=False,
                process_start_date__gte=datetime.combine(start_date, datetime.min.time()),
                process_start_date__lte=datetime.combine(end_date, datetime.max.time())
            ).exclude(
                testing_engineer__in=["", "樊佳博"]  # 新增：排除目标工程师
            ).exclude(
                testing_engineer__icontains="外援"
            ).values("testing_engineer").distinct().count())

            # 日期范围内总应当数量
            date_diff_days = (end_date - start_date).days + 1
            required_count = day_required_count * date_diff_days
            # 计算核心指标（保留2位小数，处理除数为0）
            if required_count != 0 and involved_engineers != 0:
                core_index = round((total_success / required_count) / involved_engineers * 100, 2)
            else:
                core_index = 0.00  # 无数据时核心指标为 0

            return Response.ApiResponse.success(
                data={
                    "statistics": {
                        "total_success_count": total_success,  # 总成功数量
                        "involved_engineer_count": involved_engineers,  # 参与工程师总数
                        "core_index": core_index,  # 核心指标（总成功数÷24.5×工程师总数）
                        "date_diff_days": date_diff_days,
                        "required_count": required_count,
                    }
                },
                message=f"{start_date_str} 至 {end_date_str} 核心指标统计完成"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"统计失败：{str(e)}"
            )
"""TEM人员平均饱和度（周度）"""
class TemEngineerSuccessCoreIndexAPI(APIView):
    def get(self, request):
        # 固定配置
        # target_projects = ["427", "405", "404", "403", "402", "401", "400", "399", "398", "397", "396", "S12","S13"]  # 目标检测项目
        test_item = ["PED测试", "非球差TEM-EDS点分析服务", "球差TEM-EDS点分析服务", "非球差TEM-EDS线分析服务",
                     "球差TEM-EDS线分析服务", "非球差TEM-EDS面分析服务", "球差TEM-EDS面分析服务",
                     "非球差TEM-EELS分析服务", "球差TEM-EELS分析服务", "非球差TEM分析服务", "球差TEM分析服务",
                     "STEM分析服务", "TEM补拍","粉末样品TEM制样"]  # 目标检测项目
        failed_status = ["失败", "内部失败", "外部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]
        day_required_count = 10  # 每日应当数量

        # 日期范围
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            if start_date > end_date:
                return Response.ApiResponse.failed(code=400, message="开始日期不能晚于结束日期")
        except ValueError:
            return Response.ApiResponse.failed(code=400, message="日期格式错误，需为YYYY-MM-DD",
                                               data={"valid_example": "start_date=2025-08-01&end_date=2025-08-31"})
        except TypeError:
            return Response.ApiResponse.failed(code=400, message="缺少 start_date 或 end_date")

        try:
            # 统计绩效工时总和
            total_success_raw = Process.objects.filter(
                test_item__in=test_item,
                status__in=completed_statuses,
                process_start_date__gte=datetime.combine(start_date, datetime.min.time()),
                process_start_date__lte=datetime.combine(end_date, datetime.max.time())
            ).aggregate(total=Sum("performance_working_hours"))["total"]
            total_success = float(total_success_raw) if total_success_raw else 0

            # 统计参与的工程师总数（去重：同一工程师多次成功只算1人）
            involved_engineers = Process.objects.filter(
                test_item__in=test_item,
                status__in=completed_statuses,
                testing_engineer__isnull=False,
                process_start_date__gte=datetime.combine(start_date, datetime.min.time()),
                process_start_date__lte=datetime.combine(end_date, datetime.max.time())
            ).values("testing_engineer").distinct().count()

            # 日期范围内总应当数量
            date_diff_days = (end_date - start_date).days + 1
            required_count = day_required_count * date_diff_days
            # 计算核心指标（保留2位小数，处理除数为0）
            if required_count != 0 and involved_engineers != 0:
                core_index = round((total_success / required_count) / involved_engineers * 100, 2)
            else:
                core_index = 0.00  # 无数据时核心指标为 0

            return Response.ApiResponse.success(
                data={
                    "statistics": {
                        "total_success_count": total_success,  # 绩效工时总和
                        "involved_engineer_count": involved_engineers,  # 参与工程师总数
                        "core_index": core_index  # 核心指标（绩效工时总和÷应当数量÷工程师总数）
                    }
                },
                message=f"{start_date_str} 至 {end_date_str} 核心指标统计完成"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"统计失败：{str(e)}"
            )


"""FIB内部机台平均使用率（周度）"""
class FIBInternalMachineTotalHoursAPI(APIView):
    TARGET_EQUIPMENT_CODES = ["ZFIBE01", "ZFIBC01", "ZFIBJ01"]
    DAILY_AVAILABLE_DURATION = 24
    TARGET_USAGE_TYPE = "utilization"
    DOWNTIME_USAGE_TYPES = ["scheduled downtime", "unscheduled"]

    def _calculate_theoretical_duration(self, start_date, end_date):
        """计算单台机台在指定日期范围内的理论总时长"""
        date_diff_days = (end_date - start_date).days + 1  # +1 是为了包含首尾两天
        return date_diff_days * self.DAILY_AVAILABLE_DURATION

    def _calculate_downtime_duration(self, device_code, start_datetime, end_datetime):
        """计算单台机台在指定时间范围内的总停机时长（小时）。"""
        downtime_records = MachineUsageRecord.objects.filter(
            device_code=device_code,
            usage_type__in=self.DOWNTIME_USAGE_TYPES,
            start_time__lt=end_datetime,
            end_time__gt=start_datetime
        )

        total_downtime_seconds = 0
        for record in downtime_records:
            actual_start = max(record.start_time, start_datetime)
            actual_end = min(record.end_time, end_datetime)

            # 如果实际开始时间在实际结束时间之前，说明有有效交集
            if actual_start < actual_end:
                downtime_delta = actual_end - actual_start
                total_downtime_seconds += downtime_delta.total_seconds()

        return total_downtime_seconds / 3600  # 3600秒 = 1小时

    def _calculate_available_duration_for_machine(self, device_code, start_date, end_date):
        """计算单台机台在指定日期范围内的最终可用时长"""
        theoretical_duration = self._calculate_theoretical_duration(start_date, end_date)
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
        # 计算总停机时长
        downtime_duration = self._calculate_downtime_duration(device_code, start_datetime, end_datetime)
        available_duration = max(theoretical_duration - downtime_duration, 0)
        return available_duration

    def get(self, request):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date > end_date:
                return Response.ApiResponse.failed(code=400, message="开始日期不能晚于结束日期")
        except ValueError:
            return Response.ApiResponse.failed(code=400, message="日期格式错误，需为YYYY-MM-DD")
        except TypeError:
            return Response.ApiResponse.failed(code=400, message="缺少 start_date 或 end_date 参数")

        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

            # 捕获所有与统计期有交集的记录
            usage_records = MachineUsageRecord.objects.filter(
                device_code__in=self.TARGET_EQUIPMENT_CODES,
                usage_type=self.TARGET_USAGE_TYPE,
                # 记录的开始时间 < 统计的结束时间，并且记录的结束时间 > 统计的开始时间
                start_time__lt=end_datetime,
                end_time__gt=start_datetime
            )

            # 遍历每条记录，精确计算其在统计范围内的有效时长
            total_seconds = 0
            active_device_codes = set() # 统计实际机台数量

            for record in usage_records:
                actual_start = max(record.start_time, start_datetime)
                actual_end = min(record.end_time, end_datetime)

                if actual_start < actual_end:
                    work_delta = actual_end - actual_start
                    total_seconds += work_delta.total_seconds()
                    active_device_codes.add(record.device_code)

            total_hours = round(total_seconds / 3600, 2)
            distinct_device_count = len(active_device_codes)
            # --- 计算总可用时长 ---
            total_available_duration = 0.0
            machine_details = []  # 用于存储每台机台的详细信息

            for device_code in self.TARGET_EQUIPMENT_CODES:
                available_hours = self._calculate_available_duration_for_machine(device_code, start_date, end_date)
                total_available_duration += available_hours

                # 收集详细信息
                machine_details.append({
                    'device_code': device_code,
                    'available_hours': round(available_hours, 2)
                })

            # --- 计算平均利用率 ---
            average_utilization = 0.0
            if total_available_duration > 0:
                average_utilization = (total_hours / total_available_duration) * 100

            average_utilization_str = f"{average_utilization:.2f}"

            return Response.ApiResponse.success(
                data={
                    'date_range': f"{start_date_str} 至 {end_date_str}",
                    'date_diff_days': (end_date - start_date).days + 1,
                    'distinct_device_count': distinct_device_count, # 实际工作机台数
                    'total_hours': total_hours,
                    'total_available_duration': round(total_available_duration, 2),
                    'average_utilization_rate': average_utilization_str,
                },
                message=f"{start_date_str} 至 {end_date_str} FIB内部机台使用统计成功"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"FIB内部机台统计失败：{str(e)}"
            )
"""FIB外部机台平均使用率（周度）"""
class FIBExternalMachineTotalHoursAPI(APIView):
    DAILY_AVAILABLE_DURATION = 11  # 单日可用时长（小时）
    TARGET_USAGE_TYPE = "utilization"  # 仅统计该类型的记录
    DOWNTIME_USAGE_TYPES = ["scheduled downtime", "unscheduled"]  # 停机类型

    def _calculate_theoretical_duration(self, start_date, end_date):
        """计算单台机台在指定日期范围内的理论总时长（小时）。"""
        date_diff_days = (end_date - start_date).days + 1
        return date_diff_days * self.DAILY_AVAILABLE_DURATION

    def _calculate_downtime_duration(self, device_code, start_datetime, end_datetime):
        """计算单台机台在指定时间范围内的总停机时长（小时）。"""
        downtime_records = MachineUsageRecord.objects.filter(
            device_code=device_code,
            usage_type__in=self.DOWNTIME_USAGE_TYPES,
            start_time__lt=end_datetime,
            end_time__gt=start_datetime
        )

        total_downtime_seconds = 0
        for record in downtime_records:
            actual_start = max(record.start_time, start_datetime)
            actual_end = min(record.end_time, end_datetime)
            if actual_start < actual_end:
                downtime_delta = actual_end - actual_start
                total_downtime_seconds += downtime_delta.total_seconds()
        return total_downtime_seconds / 3600

    def _calculate_available_duration_for_machine(self, device_code, start_date, end_date):
        """计算单台机台在指定日期范围内的最终可用时长（小时）。"""
        theoretical_duration = self._calculate_theoretical_duration(start_date, end_date)
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
        downtime_duration = self._calculate_downtime_duration(device_code, start_datetime, end_datetime)
        available_duration = max(theoretical_duration - downtime_duration, 0)
        return available_duration

    def get(self, request):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date > end_date:
                return Response.ApiResponse.failed(code=400, message="开始日期不能晚于结束日期")
        except ValueError:
            return Response.ApiResponse.failed(code=400, message="日期格式错误，需为YYYY-MM-DD")
        except TypeError:
            return Response.ApiResponse.failed(code=400, message="缺少 start_date 或 end_date 参数")

        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

            usage_records = MachineUsageRecord.objects.filter(
                device_code__contains="FIB",
                device_code__regex=r'^[^Z]',
                usage_type=self.TARGET_USAGE_TYPE,
                # 记录的开始时间 < 统计的结束时间，并且记录的结束时间 > 统计的开始时间
                start_time__lt=end_datetime,
                end_time__gt=start_datetime
            )

            # 遍历每条记录，精确计算其在统计范围内的有效时长
            total_seconds = 0  # 改用秒来计算，以提高精度
            device_work_details = {}  # 用于存储每台设备的工作记录，以便后续去重

            for record in usage_records:
                # 计算记录与统计范围的交集
                actual_start = max(record.start_time, start_datetime)
                actual_end = min(record.end_time, end_datetime)

                if actual_start < actual_end:
                    work_delta = actual_end - actual_start
                    total_seconds += work_delta.total_seconds()

                    # 同时，收集该设备的编码，用于后续计算可用时长
                    device_code = record.device_code
                    if device_code not in device_work_details:
                        device_work_details[device_code] = True

            total_hours = round(total_seconds / 3600, 2)

            # --- 计算总可用时长 ---

            # 从工作记录中提取所有不重复的设备编码
            distinct_device_codes = list(device_work_details.keys())
            distinct_device_count = len(distinct_device_codes)

            # 遍历机台列表，计算每台机的可用时长并累加
            total_available_duration = 0.0
            machine_details = []

            for device_code in distinct_device_codes:
                available_hours = self._calculate_available_duration_for_machine(device_code, start_date, end_date)
                total_available_duration += available_hours

                machine_details.append({
                    'device_code': device_code,
                    'available_hours': round(available_hours, 2)
                })

            # --- 计算平均利用率  ---
            average_utilization = 0.0
            # 分母是动态计算出的总可用时长
            if total_available_duration > 0:
                average_utilization = (total_hours / total_available_duration) * 100
            average_utilization_str = f"{average_utilization:.2f}"

            response_data = {
                'date_range': f"{start_date_str} 至 {end_date_str}",
                'date_diff_days': (end_date - start_date).days + 1,
                'distinct_device_count': distinct_device_count,  # 机台数
                'total_hours': total_hours,
                'average_utilization_rate': average_utilization_str,
                'total_available_duration': round(total_available_duration, 2),  # 动态计算的总可用时长
            }


            return Response.ApiResponse.success(
                data=response_data,
                message=f"{start_date_str} 至 {end_date_str} FIB外部机台使用统计成功"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"FIB外部机台统计失败：{str(e)}"
            )
"""TEM内部机台平均使用率（周度）"""
class TEMInternalMachineTotalHoursAPI(APIView):
    TARGET_EQUIPMENT_CODES = ["ZTEMC01"]  # 内部目标机台编码
    DAILY_AVAILABLE_DURATION = 24  # 单日可用时长（小时）
    TARGET_USAGE_TYPE = "utilization"
    DOWNTIME_USAGE_TYPES = ["scheduled downtime", "unscheduled"]

    def _calculate_theoretical_duration(self, start_date, end_date):
        """计算单台机台在指定日期范围内的理论总时长"""
        date_diff_days = (end_date - start_date).days + 1  # +1 是为了包含首尾两天
        return date_diff_days * self.DAILY_AVAILABLE_DURATION

    def _calculate_downtime_duration(self, device_code, start_datetime, end_datetime):
        """计算单台机台在指定时间范围内的总停机时长"""
        downtime_records = MachineUsageRecord.objects.filter(
            device_code=device_code,
            usage_type__in=self.DOWNTIME_USAGE_TYPES,
            start_time__lt=end_datetime,
            end_time__gt=start_datetime
        )

        total_downtime_seconds = 0
        for record in downtime_records:
            actual_start = max(record.start_time, start_datetime)
            actual_end = min(record.end_time, end_datetime)

            if actual_start < actual_end:
                downtime_delta = actual_end - actual_start
                total_downtime_seconds += downtime_delta.total_seconds()

        return total_downtime_seconds / 3600  # 3600秒 = 1小时

    def _calculate_available_duration_for_machine(self, device_code, start_date, end_date):
        """计算单台机台在指定日期范围内的最终可用时长（小时）。"""
        theoretical_duration = self._calculate_theoretical_duration(start_date, end_date)
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
        # 计算总停机时长
        downtime_duration = self._calculate_downtime_duration(device_code, start_datetime, end_datetime)
        available_duration = max(theoretical_duration - downtime_duration, 0)
        return available_duration

    def get(self, request):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date > end_date:
                return Response.ApiResponse.failed(code=400, message="开始日期不能晚于结束日期")
        except ValueError:
            return Response.ApiResponse.failed(code=400, message="日期格式错误，需为YYYY-MM-DD")
        except TypeError:
            return Response.ApiResponse.failed(code=400, message="缺少 start_date 或 end_date 参数")

        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

            # 捕获所有与统计期有交集的记录
            usage_records = MachineUsageRecord.objects.filter(
                device_code__in=self.TARGET_EQUIPMENT_CODES,
                usage_type=self.TARGET_USAGE_TYPE,
                # 记录的开始时间 < 统计的结束时间，并且记录的结束时间 > 统计的开始时间
                start_time__lt=end_datetime,
                end_time__gt=start_datetime
            )

            # 遍历每条记录，精确计算其在统计范围内的有效时长
            total_seconds = 0
            active_device_codes = set()

            for record in usage_records:
                actual_start = max(record.start_time, start_datetime)
                actual_end = min(record.end_time, end_datetime)

                if actual_start < actual_end:
                    work_delta = actual_end - actual_start
                    total_seconds += work_delta.total_seconds()
                    active_device_codes.add(record.device_code)

            total_hours = round(total_seconds / 3600, 2)
            distinct_device_count = len(active_device_codes)
            # --- 计算总可用时长 ---
            total_available_duration = 0.0
            machine_details = []  # 用于存储每台机台的详细信息

            for device_code in self.TARGET_EQUIPMENT_CODES:
                available_hours = self._calculate_available_duration_for_machine(device_code, start_date, end_date)
                total_available_duration += available_hours

                machine_details.append({
                    'device_code': device_code,
                    'available_hours': round(available_hours, 2)
                })

            # --- 计算平均利用率 ---
            average_utilization = 0.0
            if total_available_duration > 0:
                average_utilization = (total_hours / total_available_duration) * 100

            average_utilization_str = f"{average_utilization:.2f}"

            return Response.ApiResponse.success(
                data={
                    'date_range': f"{start_date_str} 至 {end_date_str}",
                    'date_diff_days': (end_date - start_date).days + 1,
                    'distinct_device_count': distinct_device_count,
                    'total_hours': total_hours,
                    'total_available_duration': round(total_available_duration, 2),
                    'average_utilization_rate': average_utilization_str,
                },
                message=f"{start_date_str} 至 {end_date_str} FIB内部机台使用统计成功"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"TEM内部机台统计失败：{str(e)}"
            )
"""TEM外部机台平均使用率（周度）"""
class TEMExternalMachineTotalHoursAPI(APIView):
    DAILY_AVAILABLE_DURATION = 11  # 单日可用时长（小时）
    TARGET_USAGE_TYPE = "utilization"  # 目标使用类型
    DOWNTIME_USAGE_TYPES = ["scheduled downtime", "unscheduled"]  # 停机类型

    def _calculate_theoretical_duration(self, start_date, end_date):
        """计算单台机台在指定日期范围内的理论总时长（小时）。"""
        date_diff_days = (end_date - start_date).days + 1
        return date_diff_days * self.DAILY_AVAILABLE_DURATION

    def _calculate_downtime_duration(self, device_code, start_datetime, end_datetime):
        """计算单台机台在指定时间范围内的总停机时长（小时）。"""
        downtime_records = MachineUsageRecord.objects.filter(
            device_code=device_code,
            usage_type__in=self.DOWNTIME_USAGE_TYPES,
            start_time__lt=end_datetime,
            end_time__gt=start_datetime
        )

        total_downtime_seconds = 0
        for record in downtime_records:
            actual_start = max(record.start_time, start_datetime)
            actual_end = min(record.end_time, end_datetime)
            if actual_start < actual_end:
                downtime_delta = actual_end - actual_start
                total_downtime_seconds += downtime_delta.total_seconds()
        return total_downtime_seconds / 3600

    def _calculate_available_duration_for_machine(self, device_code, start_date, end_date):
        """计算单台机台在指定日期范围内的最终可用时长（小时）。"""
        theoretical_duration = self._calculate_theoretical_duration(start_date, end_date)
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
        downtime_duration = self._calculate_downtime_duration(device_code, start_datetime, end_datetime)
        available_duration = max(theoretical_duration - downtime_duration, 0)
        return available_duration

    def get(self, request):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date > end_date:
                return Response.ApiResponse.failed(code=400, message="开始日期不能晚于结束日期")
        except ValueError:
            return Response.ApiResponse.failed(code=400, message="日期格式错误，需为YYYY-MM-DD")
        except TypeError:
            return Response.ApiResponse.failed(code=400, message="缺少 start_date 或 end_date 参数")

        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)

            usage_records = MachineUsageRecord.objects.filter(
                device_code__contains="TEM",
                device_code__regex=r'^[^Z]',
                usage_type=self.TARGET_USAGE_TYPE,
                # 记录的开始时间 < 统计的结束时间，并且记录的结束时间 > 统计的开始时间
                start_time__lt=end_datetime,
                end_time__gt=start_datetime
            )

            # 遍历每条记录，精确计算其在统计范围内的有效时长
            total_seconds = 0  # 改用秒来计算，以提高精度
            device_work_details = {}  # 用于存储每台设备的工作记录，以便后续去重

            for record in usage_records:
                # 计算记录与统计范围的交集
                actual_start = max(record.start_time, start_datetime)
                actual_end = min(record.end_time, end_datetime)

                if actual_start < actual_end:
                    work_delta = actual_end - actual_start
                    total_seconds += work_delta.total_seconds()

                    # 同时，收集该设备的编码，用于后续计算可用时长
                    device_code = record.device_code
                    if device_code not in device_work_details:
                        device_work_details[device_code] = True

            total_hours = round(total_seconds / 3600, 2)

            # --- 计算总可用时长 ---
            # 从工作记录中提取所有不重复的设备编码
            distinct_device_codes = list(device_work_details.keys())
            distinct_device_count = len(distinct_device_codes)

            # 遍历机台列表，计算每台机的可用时长并累加
            total_available_duration = 0.0
            machine_details = []

            for device_code in distinct_device_codes:
                available_hours = self._calculate_available_duration_for_machine(device_code, start_date, end_date)
                total_available_duration += available_hours

                machine_details.append({
                    'device_code': device_code,
                    'available_hours': round(available_hours, 2)
                })

            # --- 计算平均利用率 ---
            average_utilization = 0.0
            # 分母是动态计算出的总可用时长
            if total_available_duration > 0:
                average_utilization = (total_hours / total_available_duration) * 100
            average_utilization_str = f"{average_utilization:.2f}"

            response_data = {
                'date_range': f"{start_date_str} 至 {end_date_str}",
                'date_diff_days': (end_date - start_date).days + 1,
                'distinct_device_count': distinct_device_count,  # 机台数
                'total_hours': total_hours,
                'average_utilization_rate': average_utilization_str,
                'total_available_duration': round(total_available_duration, 2),  # 新增：动态计算的总可用时长
            }
            return Response.ApiResponse.success(
                data=response_data,
                message=f"{start_date_str} 至 {end_date_str} FIB外部机台使用统计成功"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"TEM外部机台统计失败：{str(e)}"
            )


"""内部机台工作时间饱和度"""
class InternalMachineWorkSaturationAPI(APIView):
    """
    内部机台工作时间饱和度统计API
    - 统计指定日期范围内，各目标机台的工作时长和饱和度。
    - 饱和度 = (机台总运行时长 / 机台总可用时长) * 100%
    - 机台总可用时长 = 理论总时长(天数×24) - 该台机的停机总时长
    - 停机总时长包括 "scheduled downtime" 和 "unscheduled" 类型的记录。
    """
    # --- 常量定义 ---
    TARGET_PROCESS_EQUIPMENT_CODES = [
        "ZFIBE01", "ZFIBC01", "ZFIBJ01", "ZTEMC01", "ZTEMH01"  # 目标机台编码列表
    ]
    DAILY_AVAILABLE_DURATION = 24  # 单日理论可用时长
    TARGET_USAGE_TYPE = "utilization"  # 目标类型
    DOWNTIME_USAGE_TYPES = ["scheduled downtime", "unscheduled"] # 停机类型

    def _calculate_theoretical_duration(self, start_date, end_date):
        """计算单台机台在指定日期范围内的理论总时长（小时）。"""
        date_diff_days = (end_date - start_date).days + 1
        return date_diff_days * self.DAILY_AVAILABLE_DURATION

    def _calculate_downtime_duration(self, device_code, start_datetime, end_datetime):
        """计算单台机台在指定时间范围内的总停机时长（小时）。"""
        downtime_records = MachineUsageRecord.objects.filter(
            device_code=device_code,
            usage_type__in=self.DOWNTIME_USAGE_TYPES,
            start_time__lt=end_datetime,
            end_time__gt=start_datetime
        )

        total_downtime_seconds = 0
        for record in downtime_records:
            actual_start = max(record.start_time, start_datetime)
            actual_end = min(record.end_time, end_datetime)
            if actual_start < actual_end:
                downtime_delta = actual_end - actual_start
                total_downtime_seconds += downtime_delta.total_seconds()
        return total_downtime_seconds / 3600

    def _calculate_available_duration_for_machine(self, device_code, start_date, end_date):
        """计算单台机台在指定日期范围内的最终可用时长（小时）。"""
        theoretical_duration = self._calculate_theoretical_duration(start_date, end_date)
        start_datetime = datetime.combine(start_date, datetime.min.time())
        # 将结束时间设置为结束日期的次日零点
        end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
        downtime_duration = self._calculate_downtime_duration(device_code, start_datetime, end_datetime)
        return max(theoretical_duration - downtime_duration, 0)

    def get(self, request):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if start_date > end_date:
                return Response.ApiResponse.failed(code=400, message="开始日期不能晚于结束日期")
        except ValueError:
            return Response.ApiResponse.failed(code=400, message="日期格式错误，需为YYYY-MM-DD")
        except TypeError:
            return Response.ApiResponse.failed(code=400, message="缺少 start_date 或 end_date 参数")

        try:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            # 将结束时间设置为结束日期的次日零点
            end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
            saturation_rates = []
            total_hours_list = []
            total_available_duration_list = []

            # 在循环内为每台机单独计算 ---
            for code in self.TARGET_PROCESS_EQUIPMENT_CODES:
                # --- 为当前机台查询所有相关的工作记录 ---
                machine_usage_records = MachineUsageRecord.objects.filter(
                    device_code=code,
                    usage_type=self.TARGET_USAGE_TYPE,
                    # 使用更宽泛的条件，确保捕获所有交集
                    start_time__lt=end_datetime,
                    end_time__gt=start_datetime
                )
                # 计算当前机台的总工作时长 ---
                total_work_seconds = 0
                for record in machine_usage_records:
                    actual_start = max(record.start_time, start_datetime) # 最大开始
                    actual_end = min(record.end_time, end_datetime) # 最小结束
                    if actual_start < actual_end:
                        work_delta = actual_end - actual_start
                        total_work_seconds += work_delta.total_seconds()

                # 将秒转换为小时
                total_hours = round(total_work_seconds / 3600, 2)
                total_hours_list.append(total_hours)

                # --- 计算可用时长 ---
                machine_available_hours = self._calculate_available_duration_for_machine(code, start_date, end_date)
                total_available_duration_list.append(round(machine_available_hours, 2))

                # --- 计算饱和度 ---
                if machine_available_hours < 1e-9:  # 使用一个极小值避免浮点数精度问题
                    saturation = "0.00"
                else:
                    saturation_val = round((total_hours / machine_available_hours) * 100, 2)
                    saturation = f"{saturation_val:.2f}"
                saturation_rates.append(saturation)

            date_diff_days = (end_date - start_date).days + 1

            return Response.ApiResponse.success(
                data={
                    "date_range": f"{start_date_str} 至 {end_date_str}",
                    "date_diff_days": date_diff_days,
                    "target_machine_count": len(self.TARGET_PROCESS_EQUIPMENT_CODES),
                    "saturation_rates": saturation_rates, # 饱和度
                    "total_hours_list": total_hours_list, # 每台机的实际时长列表
                    "total_available_duration_list": total_available_duration_list, # 每台机的可用时长列表
                },
                message=f"{start_date_str} 至 {end_date_str} 内部机台工作时间饱和度统计成功"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"内部机台工作时间饱和度统计失败：{str(e)}"
            )

"""FIB外部客户每日成功率统计（周度）"""
class FibCustomerExternalDailyProjectCountAPI(APIView):
    def get(self, request):
        # 固定配置
        test_item = ["TEM样品制备（平面、倒切、侧切_孔洞完整）",
                     "TEM样品制备（平面、倒切、侧切_单一完整）", "TEM样品制备（正切_孔洞完整）",
                     "TEM样品制备（正切_单一完整）", "TEM制样_细修（深度＞5um）", "TEM制样_细修（深度≤5um）",
                     "TEM样品制备（机械研磨）", "TEM样品制备（平面、倒切、侧切_分步）", "TEM样品制备（正切_分步）",
                     "TEM样品制备（clean）", "SEM/EDS分析服务","PFIB大尺寸切割"]
        failed_status = ["外部失败"]
        completed_statuses = ["成功", "等待质审核工序", "检测中", "返工工序", "失败", "内部失败", "外部失败"]

        # 获取参数
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        customer = request.query_params.get("customer")

        # 验证customer参数
        if not customer:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少客户参数：请传入 customer"
            )

        # 验证日期
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            if start_date > end_date:
                return Response.ApiResponse.failed(
                    code=400,
                    message="日期范围错误：开始日期不能晚于结束日期"
                )
        except ValueError:
            return Response.ApiResponse.failed(
                code=400,
                message="日期参数格式错误，请传入YYYY-MM-DD格式（如2025-01-01）",
            )
        except TypeError:
            return Response.ApiResponse.failed(
                code=400,
                message="缺少日期参数：请传入 start_date 和 end_date（格式YYYY-MM-DD）"
            )

        try:
            # 筛选条件：按客户 + 检测项目筛选
            common_filter = {
                "customer": customer,
                "test_item__in": test_item,
                "process_start_date__gte": datetime.combine(start_date, datetime.min.time()),
                "process_start_date__lte": datetime.combine(end_date, datetime.max.time())
            }

            # 查询符合条件的所有（日期+样本+状态）记录
            daily_sample_records = Process.objects.filter(
                **common_filter,
                status__in=completed_statuses
            ).annotate(
                daily_date=TruncDate("process_start_date")
            ).values("daily_date", "sample_id", "status")

            # 第一步：找出每个样本的最早出现日期和最终状态（失败优先）
            sample_first_date = {}
            sample_final_status = {}

            for record in daily_sample_records:
                sample_id = record["sample_id"]
                daily_date = record["daily_date"]
                status = record["status"]

                # 记录最早出现日期
                if sample_id not in sample_first_date:
                    sample_first_date[sample_id] = daily_date
                else:
                    if daily_date < sample_first_date[sample_id]:
                        sample_first_date[sample_id] = daily_date

                # 判定最终状态（失败优先）
                if sample_id not in sample_final_status:
                    sample_final_status[sample_id] = "失败" if status in failed_status else "非失败"
                else:
                    if sample_final_status[sample_id] == "非失败" and status in failed_status:
                        sample_final_status[sample_id] = "失败"

            # 计算总体统计值
            actual_total_completed = len(sample_final_status)
            actual_total_success = list(sample_final_status.values()).count("非失败")

            # 第二步：将每个样本归属到最早出现的那天
            completed_result = {}
            failed_result = {}

            for sample_id, first_date in sample_first_date.items():
                final_status = sample_final_status[sample_id]

                completed_result[first_date] = completed_result.get(first_date, 0) + 1

                if final_status == "失败":
                    failed_result[first_date] = failed_result.get(first_date, 0) + 1

            # 日期列表
            date_list = []
            current_date = start_date
            while current_date <= end_date:
                date_list.append(current_date)
                current_date += timedelta(days=1)

            # 数据集整理
            dates = []
            daily_completed = []
            daily_failed = []
            daily_success = []
            daily_success_rate = []

            for date_obj in date_list:
                date_str = date_obj.strftime("%Y-%m-%d")
                completed = completed_result.get(date_obj, 0)
                failed = failed_result.get(date_obj, 0)
                success = completed - failed

                success_rate = round((success / completed) * 100, 2) if completed != 0 else 0.00

                dates.append(date_str)
                daily_completed.append(completed)
                daily_failed.append(failed)
                daily_success.append(success)
                daily_success_rate.append(success_rate)

            stat_days = len(dates)
            return Response.ApiResponse.success(
                data={
                    "dates": dates,
                    "daily_completed_counts": daily_completed,
                    "daily_failed_counts": daily_failed,
                    "daily_success_counts": daily_success,
                    "daily_success_rates": daily_success_rate,
                    "actual_total_completed": actual_total_completed,
                    "actual_total_success": actual_total_success
                },
                message=f"{start_date_str} 至 {end_date_str} {customer} 每日统计完成（共{stat_days}天）"
            )

        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"每日统计失败：{str(e)}",
            )



