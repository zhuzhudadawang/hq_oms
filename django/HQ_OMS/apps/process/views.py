from datetime import datetime, timedelta
from django.db import transaction
from django.db.models import Q
from rest_framework.views import APIView
from apps.process.models import Process
from apps.process.serializers import ProcessSerializer, ProcessListSerializer, ProcessCreateSerializer, \
    ProcessUpdateSerializer
from utils import Response

"""工序编号查询"""
class ProcessByIdAPIView(APIView):
    def get(self, request,id):
        try:
            process = Process.objects.get(process_id=id)
            print(process)
        except Process.DoesNotExist:
            # 工序不存在
            return Response.ApiResponse.failed(message=f"工序编号「{id}」不存在")
        except Exception as e:
            return Response.ApiResponse.failed(message=f"查询失败：{str(e)}")

        serializer = ProcessSerializer(process)
        return Response.ApiResponse.success(
            data=serializer.data,
            message=f"工序「{id}」查询成功"
        )

"""工序列表（支持分页）"""
class ProcessListAPIView1(APIView):
    def get(self, request):
        # 获取分页参数（默认第一页，每页10条）
        page_index = int(request.query_params.get('index',1))
        page_size = int(request.query_params.get('size', 10))
        offset = (page_index - 1) * page_size

        # 查询数据库（分页查询 + 按接收时间倒序）
        process_queryset = Process.objects.all().order_by('-create_time')
        # 分页截取：跳过offset条，取page_size条
        paginated_processes = process_queryset[offset: offset + page_size]
        # 获取总条数
        total = process_queryset.count()
        serializer = ProcessListSerializer(paginated_processes, many=True)

        response_data = {
            "data": serializer.data,
            "total": total
        }
        return Response.ApiResponse.success(data=response_data, message="获取工序列表成功")

"""根据编号删除"""
class ProcessDeleteAPIView(APIView):
    def delete(self, request, id):
        if not id:
            return Response.ApiResponse.failed(message="缺少工序编号参数（process_id）")

        try:
            process = Process.objects.get(process_id=id)
            process.delete()
            return Response.ApiResponse.success(
                message=f"工序编号{id}的记录已成功删除"
            )
        except Process.DoesNotExist:
            return Response.ApiResponse.failed(
                message=f"未找到工序编号{id}的记录"
            )
        except Exception as e:
            return Response.ApiResponse.failed(
                message=f"删除失败：{str(e)}"
            )

"""新增工序"""
class ProcessCreateAPIView(APIView):
    def post(self, request):
        process_id = request.data.get('process_id')
        if Process.objects.filter(process_id=process_id).exists():
            return Response.ApiResponse.failed(
                message="工序编号已存在",
                data={"order_id": [f"process_id: {process_id} 已存在"]}
            )

        serializer = ProcessCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response.ApiResponse.success(
                data=serializer.data,
                message="新增工序成功"
            )
        else:
            print(serializer.errors)
            return Response.ApiResponse.failed(
                message="参数验证失败",
                data=serializer.errors
            )

"""更新工序"""
class ProcessUpdateAPIView(APIView):
    def put(self, request,id):
        update_data = request.data
        # 查询工序是否存在
        try:
            process = Process.objects.get(process_id=id)
        except Process.DoesNotExist:
            return Response.ApiResponse.failed(message=f"工序ID「{id}」不存在")
        except Exception as e:
            return Response.ApiResponse.failed(message=f"查询工序失败：{str(e)}")

        # 序列化器验证并更新数据（partial=True 允许部分字段更新）
        serializer = ProcessUpdateSerializer(process, data=update_data, partial=True) # 更新已有对象
        if not serializer.is_valid():
            print(serializer.errors)
            return Response.ApiResponse.failed(message=f"数据验证失败：{serializer.errors}")

        try:
            serializer.save()
            return Response.ApiResponse.success(
                message=f"工序ID「{id}」更新成功",
                data=serializer.data
            )
        except Exception as e:
            return Response.ApiResponse.failed(message=f"更新工序失败：{str(e)}")

"""测试：工序列表（支持分页和多条件查询）"""
class ProcessListAPIView(APIView):
    # 支持的查询字段
    SUPPORTED_FIELDS = ['customer', 'process_id', 'status']

    def get(self, request):
        try:
            page_index = int(request.query_params.get('index', 1))
            page_size = int(request.query_params.get('size', 10))
            offset = (page_index - 1) * page_size
            # 处理查询条件（单条件/多条件）
            query_conditions = self._handle_query_conditions(request)
            # 数据库查询（带条件过滤和排序）
            queryset = Process.objects.all().order_by('-create_time')
            if query_conditions:
                queryset = queryset.filter(query_conditions)
            # 分页处理
            paginated = queryset[offset: offset + page_size]
            total = queryset.count()
            # 序列化并返回
            serializer = ProcessListSerializer(paginated, many=True)
            response_data = {
                "data": serializer.data,
                "total": total,
                "page_index": page_index,
                "page_size": page_size
            }
            return Response.ApiResponse.success(data=response_data, message="获取工序列表成功")

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
                if field in ['process_id']:  # 工序编号精确匹配
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
                # 批量查询存在的工序
                processes = Process.objects.filter(record_id__in=ids)
                deleted_ids = list(processes.values_list('process_id', flat=True))  # 实际删除的ID

                if not deleted_ids:
                    return Response.ApiResponse.http_error(
                        status_code=404,
                        message="未找到任何匹配的机台耗时记录（所有ID均不存在）"
                    )
                processes.delete()

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

