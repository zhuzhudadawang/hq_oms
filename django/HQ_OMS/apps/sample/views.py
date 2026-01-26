from django.db.models import Q
from django.utils.dateparse import parse_date
from rest_framework.views import APIView
from apps.sample.models import Sample
from apps.sample.serializers import SampleListSerializer, SampleDetailSerializer, \
    SampleCreateSerializer
from utils import Response

"""样点编号查询"""
class SampleByIdAPIView(APIView):
    def get(self, request,id):
        print(id)
        try:
            print(id)
            sample = Sample.objects.get(sample_id=id)
        except Sample.DoesNotExist:
            # 样点不存在
            return Response.ApiResponse.failed(message=f"样点编号「{id}」不存在")
        except Exception as e:
            return Response.ApiResponse.failed(message=f"查询失败：{str(e)}")

        serializer = SampleDetailSerializer(sample)
        return Response.ApiResponse.success(
            data=serializer.data,
            message=f"样点「{id}」查询成功"
        )

"""订单列表（支持分页）"""
class SampleListAPIView1(APIView):
    def get(self, request):
        # 分页参数（默认第一页，每页10条）
        page_index = int(request.query_params.get('index',1))
        page_size = int(request.query_params.get('size', 10))
        offset = (page_index - 1) * page_size

        # 查询数据库（分页查询 + 按接收时间倒序）
        sample_queryset = Sample.objects.all().order_by('-receive_time')
        # 分页截取：跳过offset条，取page_size条
        paginated_samples = sample_queryset[offset: offset + page_size]
        # 获取总条数
        total = sample_queryset.count()
        serializer = SampleListSerializer(paginated_samples, many=True)

        response_data = {
            "data": serializer.data,
            "total": total
        }
        return Response.ApiResponse.success(data=response_data, message="获取样点列表成功")

"""根据编号删除"""
class DeleteSampleAPIView(APIView):
    def delete(self, request, id):
        if not id:
            return Response.ApiResponse.failed(message="缺少样点编号参数（sample_id）")

        try:
            sample = Sample.objects.get(sample_id=id)
            sample.delete()
            return Response.ApiResponse.success(
                message=f"样点编号{id}的记录已成功删除"
            )
        except Sample.DoesNotExist:
            return Response.ApiResponse.failed(
                message=f"未找到样点编号{id}的记录"
            )
        except Exception as e:
            return Response.ApiResponse.failed(
                message=f"删除失败：{str(e)}"
            )

"""新增样点"""
class SampleCreateAPIView(APIView):
    def post(self, request):
        sample_id = request.data.get('sample_id')
        if Sample.objects.filter(sample_id=sample_id).exists():
            return Response.ApiResponse.failed(
                message="样点编号已存在",
                data={"sample_id": [f"sample_id: {sample_id} 已存在"]}
            )

        serializer = SampleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response.ApiResponse.success(
                data=serializer.data,
                message="样点创建成功"
            )
        else:
            print(serializer.errors)
            return Response.ApiResponse.failed(
                message="参数验证失败",
                data=serializer.errors
            )

"""更新样点"""
class SampleUpdateAPIView(APIView):
    def put(self, request,id):
        update_data = request.data
        # 查询样点是否存在
        try:
            sample = Sample.objects.get(sample_id=id)
        except Sample.DoesNotExist:
            return Response.ApiResponse.failed(message=f"样点ID「{id}」不存在")
        except Exception as e:
            return Response.ApiResponse.failed(message=f"查询样点失败：{str(e)}")

        # 序列化器验证并更新数据（partial=True 允许部分字段更新）
        serializer = SampleCreateSerializer(sample, data=update_data, partial=True) # 更新已有对象
        if not serializer.is_valid():
            print(serializer.errors)
            return Response.ApiResponse.failed(message=f"数据验证失败：{serializer.errors}")

        try:
            serializer.save()
            return Response.ApiResponse.success(
                message=f"样点ID「{id}」更新成功",
                data=serializer.data
            )
        except Exception as e:
            return Response.ApiResponse.failed(message=f"更新样点失败：{str(e)}")

"""测试：样点列表（支持分页和多条件查询）"""
class SampleListAPIView(APIView):
    # 支持的查询字段
    SUPPORTED_FIELDS = ['customer_name', 'sample_id', 'status']

    def get(self, request):
        try:
            page_index = int(request.query_params.get('index', 1))
            page_size = int(request.query_params.get('size', 10))
            offset = (page_index - 1) * page_size
            # 处理查询条件（单条件/多条件）
            query_conditions = self._handle_query_conditions(request)
            # 数据库查询（带条件过滤和排序）
            queryset = Sample.objects.all().order_by('-receive_time')
            if query_conditions:
                queryset = queryset.filter(query_conditions)
            # 分页处理
            paginated = queryset[offset: offset + page_size]
            total = queryset.count()
            # 序列化并返回
            serializer = SampleListSerializer(paginated, many=True)
            response_data = {
                "data": serializer.data,
                "total": total,
                "page_index": page_index,
                "page_size": page_size
            }
            return Response.ApiResponse.success(data=response_data, message="获取样点列表成功")

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
                if field in ['sample_id']:  # 样点编号精确匹配
                    query_conditions &= Q(**{field: value})
                else:  # 其他字段模糊匹配
                    query_conditions &= Q(**{f"{field}__icontains": value})
        return query_conditions

"""样点数量"""
class SampleCountView(APIView):
    """
    按接收时间范围查询样点数量
    请求参数：start_date（开始日期，格式YYYY-MM-DD）、end_date（结束日期，格式YYYY-MM-DD）
    """
    def get(self, request):
        # 获取请求参数（支持 GET 方法的查询参数）
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        # 校验日期参数
        if not (start_date_str and end_date_str):
            return Response.ApiResponse.failed(message="请提供 start_date 和 end_date 参数（格式：YYYY-MM-DD）")

        # 解析日期（Django 内置的 parse_date 可处理 YYYY-MM-DD 格式）
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            return Response.ApiResponse.failed(message="日期格式错误，请使用 YYYY-MM-DD")

        if start_date > end_date:
            return Response.ApiResponse.failed(message="开始日期不能晚于结束日期")

        # 按接收时间范围筛选样点并统计数量
        # 注意：DateTimeField 需用 date() 提取日期部分进行筛选
        sample_count = Sample.objects.filter(
            receive_time__date__gte=start_date,  # 大于等于开始日期
            receive_time__date__lte=end_date     # 小于等于结束日期
        ).count()

        # 返回结果（使用自定义的 ApiResponse）
        return Response.ApiResponse.success(
            data={
                "start_date": start_date_str,
                "end_date": end_date_str,
                "count": sample_count
            },
            message="样点数量查询成功"
        )


# "根据样点编号删除(单条/多条)"
# class DeleteSample(APIView):
#     def delete(self, request):
#         # 从URL参数或请求体获取sample_id（支持单值或数组）
#         # 优先从请求体获取（批量删除时数组更适合放请求体），其次从URL参数获取
#         sample_ids = request.data.get('sample_ids') or request.GET.get('sample_ids')
#
#         # 校验参数是否存在
#         if not sample_ids:
#             return ResponseMessage.SampleResponse.failed("缺少样点编号参数（sample_ids，支持单值或数组）")
#
#         # 统一转换为列表格式（处理单值情况）
#         if not isinstance(sample_ids, list):
#             # 若为字符串，尝试按逗号分割（支持URL参数传递多个值，如?sample_ids=id1,id2）
#             if isinstance(sample_ids, str):
#                 sample_ids = [id.strip() for id in sample_ids.split(',') if id.strip()]
#             else:
#                 sample_ids = [sample_ids]  # 非列表非字符串类型（如数字）直接转为单元素列表
#
#         # 校验处理后的列表不为空
#         if not sample_ids:
#             return ResponseMessage.SampleResponse.failed("样点编号列表不能为空")
#
#         try:
#             # 查询所有待删除的记录
#             queryset = Sample.objects.filter(sample_id__in=sample_ids)
#             existing_ids = list(queryset.values_list('sample_id', flat=True))  # 实际存在的ID
#             non_existing_ids = [id for id in sample_ids if id not in existing_ids]  # 不存在的ID
#
#             # 执行删除
#             deleted_count = queryset.delete()[0]  # delete()返回元组：(删除条数, {模型: 条数})
#
#             # 构建响应信息
#             response_data = {
#                 "message": f"成功删除{deleted_count}条样点记录",
#                 "deleted_ids": existing_ids,
#                 "total_deleted": deleted_count
#             }
#
#             # 若存在不存在的ID，补充提示
#             if non_existing_ids:
#                 response_data["warning"] = f"以下样点编号不存在：{', '.join(non_existing_ids)}"
#
#             return ResponseMessage.SampleResponse.success(response_data)
#
#         except Exception as e:
#             return ResponseMessage.SampleResponse.failed(f"删除失败：{str(e)}")


