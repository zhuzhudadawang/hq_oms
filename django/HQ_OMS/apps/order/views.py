from django.db import transaction
from django.db.models import Q
from rest_framework.views import APIView
from apps.order.models import Order
from apps.order.serializers import OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer
from utils import Response

"""订单号查询"""
class OrderByIdAPIView(APIView):
    def get(self, request,id):
        try:
            order = Order.objects.get(order_id=id)
        except Order.DoesNotExist:
            # 订单不存在
            return Response.ApiResponse.failed(message=f"订单编号「{id}」不存在")
        except Exception as e:
            return Response.ApiResponse.failed(message=f"查询失败：{str(e)}")

        serializer = OrderDetailSerializer(order)
        return Response.ApiResponse.success(
            data=serializer.data,
            message=f"订单「{id}」查询成功"
        )

"""订单列表（支持分页）"""
class OrderListAPIView1(APIView):
    def get(self, request):
        # 获取分页参数（默认第一页，每页10条）
        page_index = int(request.query_params.get('index',1))
        page_size = int(request.query_params.get('size', 10))
        offset = (page_index - 1) * page_size

        # 查询数据库（分页查询 + 按创建时间倒序）
        order_queryset = Order.objects.all().order_by('-create_time')
        # 分页截取：跳过offset条，取page_size条
        paginated_orders = order_queryset[offset: offset + page_size]
        # 获取总条数
        total = order_queryset.count()
        serializer = OrderListSerializer(paginated_orders, many=True)

        response_data = {
            "data": serializer.data,
            "total": total
        }
        return Response.ApiResponse.success(data=response_data, message="获取订单列表成功")

"""根据订单号删除"""
class OrderDeleteAPIView(APIView):
    def delete(self, request, id):
        try:
            order = Order.objects.get(order_id=id)
        except Order.DoesNotExist:
            return Response.ApiResponse.http_error(404, "订单不存在")

        order.delete()
        return Response.ApiResponse.success(
            message=f"订单ID: {id} 已成功删除",
            data={"deleted_order_id": id}
        )

"""新增订单"""
class OrderCreateAPIView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        if Order.objects.filter(order_id=order_id).exists():
            return Response.ApiResponse.failed(
                message="订单编号已存在",
                data={"order_id": [f"order_id: {order_id} 已存在"]}
            )

        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response.ApiResponse.success(
                data=serializer.data,
                message="订单创建成功"
            )
        else:
            return Response.ApiResponse.failed(
                message="参数验证失败",
                data=serializer.errors
            )

"""更新订单"""
class OrderUpdateAPIView(APIView):
    def put(self, request,id):
        update_data = request.data
        # 查询订单是否存在
        try:
            order = Order.objects.get(order_id=id)
        except Order.DoesNotExist:
            return Response.ApiResponse.failed(message=f"订单ID「{id}」不存在")
        except Exception as e:
            return Response.ApiResponse.failed(message=f"查询订单失败：{str(e)}")

        # 序列化器验证并更新数据（partial=True 允许部分字段更新）
        serializer = OrderCreateSerializer(order, data=update_data, partial=True)
        if not serializer.is_valid():
            return Response.ApiResponse.failed(message=f"数据验证失败：{serializer.errors}")

        try:
            serializer.save()
            return Response.ApiResponse.success(
                message=f"订单ID「{id}」更新成功",
                data=serializer.data
            )
        except Exception as e:
            return Response.ApiResponse.failed(message=f"更新订单失败：{str(e)}")

"""测试：订单列表（支持分页和多条件查询）"""
class OrderListAPIView(APIView):
    # 支持的查询字段
    SUPPORTED_FIELDS = ['customer', 'order_id', 'order_status']

    def get(self, request):
        try:
            page_index = int(request.query_params.get('index', 1))
            page_size = int(request.query_params.get('size', 10))
            offset = (page_index - 1) * page_size
            print(request.query_params)
            # 处理查询条件（单条件/多条件）
            query_conditions = self._handle_query_conditions(request)
            # 数据库查询（带条件过滤和排序）
            order_queryset = Order.objects.all().order_by('-create_time')
            if query_conditions:
                order_queryset = order_queryset.filter(query_conditions)
            # 分页处理
            paginated_orders = order_queryset[offset: offset + page_size]
            total = order_queryset.count()
            # 序列化并返回
            serializer = OrderListSerializer(paginated_orders, many=True)
            response_data = {
                "data": serializer.data,
                "total": total,
                "page_index": page_index,
                "page_size": page_size
            }
            return Response.ApiResponse.success(data=response_data, message="获取订单列表成功")

        except ValueError as e:
            # 仅捕获参数转换失败的错误
            return Response.ApiResponse.failed(code=2, message=f"参数错误：{str(e)}")
        except Exception as e:
            # 捕获其他未知错误
            return Response.ApiResponse.http_error(500, message=f"服务器内部错误：{str(e)}")

    def _handle_query_conditions(self, request):
        """处理查询条件，支持多字段AND组合"""
        query_conditions = Q()  # 初始为空条件
        for field in self.SUPPORTED_FIELDS:
            value = request.query_params.get(field)
            if value:
                if field in ['order_id']:  # 订单号精确匹配
                    query_conditions &= Q(**{field: value})
                else:  # 其他字段模糊匹配
                    query_conditions &= Q(**{f"{field}__icontains": value})
        return query_conditions

"""批量删除"""
class OrderBatchDeleteAPIView(APIView):
    def post(self, request):
        ids = request.data.get('ids', [])

        if not ids or not isinstance(ids, list):
            return Response.ApiResponse.failed(
                message="请提供有效的订单ID列表",
                data={"ids": ids})

        try:
            # 事务确保批量删除的原子性
            with transaction.atomic():
                # 批量查询存在的订单
                orders = Order.objects.filter(order_id__in=ids)
                deleted_ids = list(orders.values_list('order_id', flat=True))  # 实际删除的ID

                if not deleted_ids:
                    return Response.ApiResponse.http_error(
                        status_code=404,
                        message="未找到任何匹配的订单（所有ID均不存在）"
                    )
                orders.delete()

            return Response.ApiResponse.success(
                message=f"成功删除 {len(deleted_ids)} 个订单",
                data={
                    "deleted_order_ids": deleted_ids,
                    "count": len(deleted_ids),
                    "total_requested": len(ids)
                }
            )
        except Exception as e:
            return Response.ApiResponse.http_error(
                status_code=500,
                message=f"删除失败：{str(e)}"
            )


