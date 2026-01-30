from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from rest_framework.views import APIView
from decimal import Decimal

from utils.Response import ApiResponse
from .models import Orderitem, Order

"FIB/TEM检测暂估收入（月度）- 上海+珠海"
class FibTemEstimatedRevenueAPI(APIView):
    """
    FIB/TEM检测暂估收入（月度）- 上海+珠海
    计算逻辑：
    1. 从 Orderitem 表获取数据，用 validity_start_date 按月分组
    2. 通过 order_id 关联 Order 表，筛选 execution_place 包含'上海'或'珠海'
    3. 累加 amount_after_tax，转换为万元
    """
    
    # 2025年写死数据（单位：万元）
    FIXED_DATA_2025 = [34.80, 52.25, 107.63, 207.67, 234.89, 251.33, 267.98, 249.03, 285.60, 306.74, 262.50, 252.13]
    ALL_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def _calculate_year_data(self, year):
        """
        计算指定年份每月的暂估收入
        返回：12个月的数据列表（单位：万元）
        """
        # 1. 获取执行地包含上海或珠海的订单ID集合
        from django.db.models import Q
        target_order_ids = set(
            Order.objects.filter(
                Q(execution_place__icontains='上海') | Q(execution_place__icontains='珠海')
            ).values_list('order_id', flat=True)
        )
        
        # 2. 查询该年份的 Orderitem，筛选上海或珠海订单，按月汇总
        monthly_data = (
            Orderitem.objects
            .filter(
                validity_start_date__year=year,
                order_id__in=target_order_ids
            )
            .exclude(order_id__isnull=True)
            .exclude(order_id='')
            .annotate(month=ExtractMonth('validity_start_date'))
            .values('month')
            .annotate(total=Sum('amount_after_tax'))
            .order_by('month')
        )
        
        # 3. 转换为12个月的列表（单位：万元）
        result = [0.0] * 12
        for item in monthly_data:
            month = item['month']
            total = item['total'] or Decimal('0')
            # 转换为万元，保留2位小数
            result[month - 1] = round(float(total) / 10000, 2)
        
        return result

    def get(self, request):
        # 2025年数据（写死）
        data_2025 = self.FIXED_DATA_2025
        total_2025 = round(sum(data_2025), 2)
        
        # 2026年数据（从数据库计算）
        data_2026 = self._calculate_year_data(2026)
        total_2026 = round(sum(data_2026), 2)
        
        response_data = {
            'months': self.ALL_MONTHS,
            'series': [
                {'name': '2025', 'data': data_2025},
                {'name': '2026', 'data': data_2026}
            ],
            'totals': {
                '2025': total_2025,
                '2026': total_2026
            }
        }
        
        return ApiResponse.success(data=response_data, message="获取FIB/TEM检测暂估收入数据成功")

"珠海检测暂估收入（月度）"
class ZhuhaiEstimatedRevenueAPI(APIView):
    """
    珠海检测暂估收入（月度）
    计算逻辑：
    1. 从 Orderitem 表获取数据，用 validity_start_date 按月分组
    2. 通过 order_id 关联 Order 表，筛选 execution_place='珠海'
    3. 累加 amount_after_tax，转换为万元
    """
    
    # 2025年写死数据（单位：万元）- 总计
    FIXED_DATA_2025 = [11.52, 7.17, 19.06, 21.49, 30.39, 16.17, 16.68, 15.35, 12.01, 20.54, 30.14, 24.4]
    ALL_MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    def _calculate_year_data(self, year):
        """
        计算指定年份每月的暂估收入
        返回：12个月的数据列表（单位：万元）
        """
        # 1. 获取执行地为珠海的订单ID集合
        zhuhai_order_ids = set(
            Order.objects.filter(
                execution_place='珠海'
            ).values_list('order_id', flat=True)
        )
        
        # 2. 查询该年份的 Orderitem，筛选珠海订单，按月汇总
        monthly_data = (
            Orderitem.objects
            .filter(
                validity_start_date__year=year,
                order_id__in=zhuhai_order_ids
            )
            .exclude(order_id__isnull=True)
            .exclude(order_id='')
            .annotate(month=ExtractMonth('validity_start_date'))
            .values('month')
            .annotate(total=Sum('amount_after_tax'))
            .order_by('month')
        )
        
        # 3. 转换为12个月的列表（单位：万元）
        result = [0.0] * 12
        for item in monthly_data:
            month = item['month']
            total = item['total'] or Decimal('0')
            # 转换为万元，保留2位小数
            result[month - 1] = round(float(total) / 10000, 2)
        
        return result

    def get(self, request):
        # 2025年数据（写死）
        data_2025 = self.FIXED_DATA_2025
        total_2025 = round(sum(data_2025), 2)
        
        # 2026年数据（从数据库计算）
        data_2026 = self._calculate_year_data(2026)
        total_2026 = round(sum(data_2026), 2)
        
        response_data = {
            'months': self.ALL_MONTHS,
            'series': [
                {'name': '2025', 'data': data_2025},
                {'name': '2026', 'data': data_2026}
            ],
            'totals': {
                '2025': total_2025,
                '2026': total_2026
            }
        }
        
        return ApiResponse.success(data=response_data, message="获取珠海检测暂估收入数据成功")
