from datetime import datetime

from django.db import transaction
from django.db.models import Q, Sum, Count
from django.utils import timezone
from rest_framework.views import APIView
from apps.machine.models import MachineUsageRecord, MachineExternal
from apps.machine.serializers import MachineUsageRecordSerializer, MachineUsageRecordCreateSerializer, \
    MachineUsageRecordUpdateSerializer
from utils import Response

"""设备编码查找机台耗时记录"""
class MachineRecordByDeviceCode(APIView):
    def get(self, request, id):
        print(id)
        try:
            machine_usage_record = MachineUsageRecord.objects.get(record_id=id)
        except MachineUsageRecord.DoesNotExist:
            # 机台耗时记录不存在
            return Response.ApiResponse.failed(message=f"机台耗时记录「{id}」不存在")
        except Exception as e:
            return Response.ApiResponse.failed(message=f"查询失败：{str(e)}")

        serializer = MachineUsageRecordSerializer(machine_usage_record)
        return Response.ApiResponse.success(
            data=serializer.data,
            message=f"机台耗时记录「{id}」查询成功"
        )

"""机台耗时列表（支持分页）"""
class MachineListAPIView1(APIView):
    def get(self, request):
        # 获取分页参数（默认第一页，每页10条）
        page_index = int(request.query_params.get('index',1))
        page_size = int(request.query_params.get('size', 10))
        offset = (page_index - 1) * page_size

        # 查询数据库（分页查询 + 按接收时间倒序）
        queryset = MachineUsageRecord.objects.all().order_by('-creation_time')
        # 分页截取：跳过offset条，取page_size条
        paginated = queryset[offset: offset + page_size]
        # 获取总条数
        total = queryset.count()
        serializer = MachineUsageRecordSerializer(paginated, many=True)

        response_data = {
            "data": serializer.data,
            "total": total
        }
        return Response.ApiResponse.success(data=response_data, message="获取机台耗时列表成功")

"""根据id删除机台耗时"""
class MachineUsageRecordDeleteAPIView(APIView):
    def delete(self, request, id):
        if not id:
            return Response.ApiResponse.failed(message="缺少机台耗时Id参数（process_id）")

        try:
            record = MachineUsageRecord.objects.get(record_id=id)
            record.delete()
            return Response.ApiResponse.success(
                message=f"机台耗时{id}的记录已成功删除"
            )
        except MachineUsageRecord.DoesNotExist:
            return Response.ApiResponse.failed(
                message=f"未找到机台耗时{id}的记录"
            )
        except Exception as e:
            return Response.ApiResponse.failed(
                message=f"删除失败：{str(e)}"
            )

"""新增机台耗时"""
class MachineUsageRecordCreateAPIView(APIView):
    def post(self, request):
        serializer = MachineUsageRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response.ApiResponse.success(
                data=serializer.data,
                message="创建机台耗时成功"
            )
        else:
            print(serializer.errors)
            return Response.ApiResponse.failed(
                message="参数验证失败",
                data=serializer.errors
            )

"""更新机台耗时"""
class MachineUsageRecordUpdateAPIView(APIView):
    def put(self, request,id):
        update_data = request.data
        # 查询机台耗时是否存在
        try:
            record = MachineUsageRecord.objects.get(process_id=id)
        except MachineUsageRecord.DoesNotExist:
            return Response.ApiResponse.failed(message=f"机台耗时ID「{id}」不存在")
        except Exception as e:
            return Response.ApiResponse.failed(message=f"查询机台耗时失败：{str(e)}")

        # 序列化器验证并更新数据（partial=True 允许部分字段更新）
        serializer = MachineUsageRecordUpdateSerializer(record, data=update_data, partial=True) # 更新已有对象
        if not serializer.is_valid():
            print(serializer.errors)
            return Response.ApiResponse.failed(message=f"数据验证失败：{serializer.errors}")

        try:
            serializer.save()
            return Response.ApiResponse.success(
                message=f"机台耗时ID「{id}」更新成功",
                data=serializer.data
            )
        except Exception as e:
            return Response.ApiResponse.failed(message=f"更新工序失败：{str(e)}")

"""机台耗时列表（支持分页和多条件查询）"""
class MachineListAPIView(APIView):
    # 支持的查询字段
    SUPPORTED_FIELDS = ['creator_name', 'device_code']

    def get(self, request):
        try:
            page_index = int(request.query_params.get('index', 1))
            page_size = int(request.query_params.get('size', 10))
            offset = (page_index - 1) * page_size
            # 处理查询条件（单条件/多条件）
            query_conditions = self._handle_query_conditions(request)
            # 数据库查询（带条件过滤和排序）
            queryset = MachineUsageRecord.objects.all().order_by('-creation_time')
            if query_conditions:
                queryset = queryset.filter(query_conditions)
            # 分页处理
            paginated = queryset[offset: offset + page_size]
            total = queryset.count()
            # 序列化并返回
            serializer = MachineUsageRecordSerializer(paginated, many=True)
            response_data = {
                "data": serializer.data,
                "total": total,
                "page_index": page_index,
                "page_size": page_size
            }
            return Response.ApiResponse.success(data=response_data, message="获取机台耗时列表成功")

        except ValueError as e:
            # 仅捕获参数转换失败的错误（如前端传非数字的index/size）
            return Response.ApiResponse.failed(code=2, message=f"参数错误：{str(e)}")
        except Exception as e:
            # 捕获其他未知错误（如数据库异常）
            return Response.ApiResponse.http_error(500, message=f"服务器内部错误：{str(e)}")

    def _handle_query_conditions(self, request):
        """处理查询条件，支持多字段AND组合"""
        query_conditions = Q()
        for field in self.SUPPORTED_FIELDS:
            value = request.query_params.get(field)
            if value:
                if field in ['device_code']:  # 设备编码精确匹配
                    query_conditions &= Q(**{field: value})
                else:  # 其他字段模糊匹配
                    query_conditions &= Q(**{f"{field}__icontains": value})
        return query_conditions

"""批量删除"""
class BatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data.get('ids', [])

        if not ids or not isinstance(ids, list):
            return Response.ApiResponse.failed(
                message="请提供有效的机台耗时记录ID列表",
                data={"ids": ids})

        try:
            # 事务确保批量删除的原子性
            with transaction.atomic():
                # 批量查询存在的机台耗时
                machine_usage_records = MachineUsageRecord.objects.filter(record_id__in=ids)
                deleted_ids = list(machine_usage_records.values_list('order_id', flat=True))  # 实际删除的ID

                if not deleted_ids:
                    return Response.ApiResponse.http_error(
                        status_code=404,
                        message="未找到任何匹配的机台耗时记录（所有ID均不存在）"
                    )
                machine_usage_records.delete()

            return Response.ApiResponse.success(
                message=f"成功删除 {len(deleted_ids)} 个机台耗时记录",
                data={
                    "deleted_machine_usage_records_ids": deleted_ids,
                    "count": len(deleted_ids),
                    "total_requested": len(ids)
                }
            )
        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"删除失败：{str(e)}"
            )

class DurationMinutesSumAPIView1(APIView):
    # 6. 定义GET请求处理方法（前端通过GET请求获取数据）
    def get(self, request):
        # 新增1：获取前端传递的时间范围参数（支持两种常见日期格式）
        # 前端可通过 ?start_time=2025-01-01&end_time=2025-12-31 传递参数
        start_time_str = request.query_params.get('start_time')  # 起始时间字符串（如"2025-01-01"）
        end_time_str = request.query_params.get('end_time')      # 结束时间字符串（如"2025-12-31"）

        # 新增2：解析时间参数，处理默认值和格式错误
        # 初始化时间范围（默认无限制，若前端传参则过滤）
        start_time = None
        end_time = None

        if start_time_str:
            try:
                # 解析时间格式（支持 "YYYY-MM-DD" 或 "YYYY-MM-DD HH:MM:SS"）
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d')
                # 转换为 timezone -aware 时间（适配Django的DateTimeField）
                start_time = timezone.make_aware(start_time)
            except ValueError:
                # 时间格式错误时返回400响应
                return Response.ApiResponse.http_error(
                    status_code=500
                )

        if end_time_str:
            try:
                end_time = datetime.strptime(end_time_str, '%Y-%m-%d')
                # 结束时间默认设为当天23:59:59，避免只传日期时过滤不到当天数据
                end_time = timezone.make_aware(end_time.replace(hour=23, minute=59, second=59))
            except ValueError:
                return Response.ApiResponse.http_error(
                    status_code=500
                )

        # 7. 筛选MachineExternal中类别为'tem'的设备编码（原有逻辑不变）
        tem_process_equipment_codes = MachineExternal.objects.filter(
            category='tem'  # 8. 过滤条件：category字段值等于'tem'（大小写敏感）
        ).values_list('process_equipment_code', flat=True)  # 9. 提取设备编码，返回扁平列表

        # 10. 计算匹配设备的duration_minutes总和（新增时间范围筛选）
        # 先初始化查询集
        usage_record_queryset = MachineUsageRecord.objects.filter(
            device_code__in=tem_process_equipment_codes  # 11. 设备编码匹配（原有逻辑）
        )

        # 新增3：根据解析后的时间参数添加过滤条件
        if start_time:
            # end_time >= 起始时间（大于等于起始时间的记录）
            usage_record_queryset = usage_record_queryset.filter(end_time__gte=start_time)
        if end_time:
            # end_time <= 结束时间（小于等于结束时间的记录）
            usage_record_queryset = usage_record_queryset.filter(end_time__lte=end_time)

        # 12. 聚合查询：求和duration_minutes字段（原有逻辑不变）
        total_duration = usage_record_queryset.aggregate(total=Sum('duration_minutes'))
        ['total'] or 0  # 13. 处理None值，默认返回0

        # 14. 返回JSON响应，包含总耗时和筛选的时间范围（新增时间范围说明）
        response_data = {
            'total_duration_minutes': total_duration,
            'filter_condition': {
                'category': 'tem',
                'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else '无',
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S') if end_time else '无'
            }
        }
        return Response.ApiResponse.success(data=response_data)

class DurationMinutesSumAPIView(APIView):
    def get(self, request):
        # 1. 获取并解析前端时间参数（原有逻辑不变）
        start_time_str = request.query_params.get('start_time')
        end_time_str = request.query_params.get('end_time')
        start_time = None
        end_time = None

        if start_time_str:
            try:
                start_time = datetime.strptime(start_time_str, '%Y-%m-%d')
                start_time = timezone.make_aware(start_time)
            except ValueError:
                return Response.ApiResponse.http_error(
                    status_code=500
                )

        if end_time_str:
            try:
                end_time = datetime.strptime(end_time_str, '%Y-%m-%d')
                end_time = timezone.make_aware(end_time.replace(hour=23, minute=59, second=59))
            except ValueError:
                return Response.ApiResponse.http_error(
                    status_code=500
                )

        # 2. 筛选MachineExternal中类别为'tem'的所有设备编码（原有逻辑不变）
        tem_process_equipment_codes = MachineExternal.objects.filter(
            category='tem'
        ).values_list('process_equipment_code', flat=True)

        # 3. 构建MachineUsageRecord查询集（含设备编码+时间筛选）
        usage_record_queryset = MachineUsageRecord.objects.filter(
            device_code__in=tem_process_equipment_codes
        )
        if start_time:
            usage_record_queryset = usage_record_queryset.filter(end_time__gte=start_time)
        if end_time:
            usage_record_queryset = usage_record_queryset.filter(end_time__lte=end_time)

        # 4. 新增：统计「有使用记录的设备编码数量」（去重）
        # distinct()：确保同一设备编码多次使用只算1个
        used_device_count = usage_record_queryset.aggregate(
            count=Count('device_code', distinct=True)
        )['count'] or 0  # 无匹配设备时返回0

        # 5. 计算总耗时（原有逻辑不变）
        total_duration = usage_record_queryset.aggregate(
            total=Sum('duration_minutes')
        )['total'] or 0

        # 6. 新增：计算平均耗时（总耗时 / 有使用记录的设备数）
        # 避免除以0：无使用设备时平均耗时为0
        average_duration = total_duration / used_device_count if used_device_count != 0 else 0

        # 7. 优化响应：返回总耗时、设备数、平均耗时及筛选条件
        response_data = {
            'filter_condition': {
                'category': 'tem',
                'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else '无',
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S') if end_time else '无'
            },
            'total_duration_minutes': total_duration,  # 总耗时（分钟）
            'used_device_count': used_device_count,    # 有使用记录的设备数量（去重）
            'average_duration_minutes': round(average_duration, 2)  # 平均耗时（保留2位小数）
        }

        return Response.ApiResponse.success(data=response_data)
# "更新机台耗时记录"
# class MachineUsageRecordUpdateAPIView(APIView):
#     def put(self, request):
#         """
#         更新机台使用记录接口（支持全量/部分字段更新）
#         - 通过 record_id 定位记录
#         """
#         # 获取记录ID和更新数据（JSON）
#         record_id = request.data.get('record_id')
#         update_data = request.data.copy()  # 复制数据避免修改原始request.data
#
#         # 校验record_id是否存在
#         if not record_id:
#             return ResponseMessage.MachineResponse.failed("缺少记录ID（record_id）")
#
#         # 3. 查询记录是否存在
#         try:
#             record = MachineUsageRecord.objects.get(record_id=record_id)
#         except MachineUsageRecord.DoesNotExist:
#             return ResponseMessage.MachineResponse.failed(f"记录ID「{record_id}」不存在")
#         except Exception as e:
#             return ResponseMessage.MachineResponse.failed("查询记录失败，请稍后重试")
#
#         # 序列化器验证并更新数据
#         serializer = MachineUsageRecordsSerializer(
#             record,
#             data=update_data,
#             partial=True  # 允许部分字段更新
#         )
#         if not serializer.is_valid():
#             return ResponseMessage.MachineResponse.failed(f"数据验证失败：{serializer.errors}")
#
#         # 保存更新
#         try:
#
#             updated_record = serializer.save()
#             return ResponseMessage.MachineResponse.success(MachineUsageRecordsSerializer(updated_record).data  # 返回更新后的数据
#             )
#         except Exception as e:
#             return ResponseMessage.MachineResponse.failed("更新记录失败，请稍后重试")

