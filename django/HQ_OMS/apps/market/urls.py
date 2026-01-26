from django.urls import path
from apps.market.views import ZhuhaiOrderStatisticsAPI, ZhuhaiCustomerStatisticsAPI, ZhuhaiMachineUtilizationAPI, \
    ZhuhaiOrderWeeklyStatsAPI, ShanghaiCustomerStatisticsAPI, ZhuhaiImportantCustomerAPI, ShanghaiImportantCustomerAPI, \
    ShanghaiOrderStatisticsAPI

urlpatterns = [
    path("zhuhai/monthly", ZhuhaiOrderStatisticsAPI.as_view()),
    path("zhuhai/weekly", ZhuhaiOrderWeeklyStatsAPI.as_view()),
    path("zhuhai/machine-utilization", ZhuhaiMachineUtilizationAPI.as_view()),
    path("zhuhai/order-sample", ZhuhaiCustomerStatisticsAPI.as_view()),
    path("zhuhai/key-customers", ZhuhaiImportantCustomerAPI.as_view()),
    path("shanghai/order-sample", ShanghaiCustomerStatisticsAPI.as_view()),
    path("shanghai/key-customers", ShanghaiImportantCustomerAPI.as_view()),
    path("shanghai/monthly", ShanghaiOrderStatisticsAPI.as_view()),

]
