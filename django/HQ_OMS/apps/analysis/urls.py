from django.urls import path
from apps.analysis.views import FibEngineerProjectCountAPI, FibEngineerSuccessByDateRangeAPI, \
    FibEngineerDailyProjectCountAPI, FibEngineerSuccessCoreIndexAPI, TemEngineerSuccessCoreIndexAPI, \
    TemEngineerDailyProjectCountAPI, TemEngineerSuccessByDateRangeAPI, TemEngineerProjectCountAPI, \
    FIBInternalMachineTotalHoursAPI, FIBExternalMachineTotalHoursAPI, InternalMachineWorkSaturationAPI, \
    TEMInternalMachineTotalHoursAPI, TEMExternalMachineTotalHoursAPI, FibInternalEngineerDailyProjectCountAPI, \
    FibExternalEngineerDailyProjectCountAPI, TemInternalEngineerDailyProjectCountAPI, \
    TemExternalEngineerDailyProjectCountAPI, FibEngineerPerformanceHoursAPI, TemEngineerPerformanceHoursAPI, \
    FibCustomerExternalDailyProjectCountAPI

urlpatterns = [
    # Fib相关
    path("fib-completion",FibEngineerProjectCountAPI.as_view()),
    path("fib-performance",FibEngineerPerformanceHoursAPI.as_view()),
    path("fib-output",FibEngineerSuccessByDateRangeAPI.as_view()),
    path("fib-sample-success",FibEngineerDailyProjectCountAPI.as_view()),
    path("fib-internal-sample-success",FibInternalEngineerDailyProjectCountAPI.as_view()),
    path("fib-external-sample-success",FibExternalEngineerDailyProjectCountAPI.as_view()),
    path("fib-saturation",FibEngineerSuccessCoreIndexAPI.as_view()),
    path("fib-customer/daily-stats", FibCustomerExternalDailyProjectCountAPI.as_view()),
    # tem相关
    path("tem-completion", TemEngineerProjectCountAPI.as_view()),
    path("tem-performance",TemEngineerPerformanceHoursAPI.as_view()),
    path("tem-output", TemEngineerSuccessByDateRangeAPI.as_view()),
    path("tem-sample-success", TemEngineerDailyProjectCountAPI.as_view()),
    path("tem-internal-sample-success", TemInternalEngineerDailyProjectCountAPI.as_view()),
    path("tem-external-sample-success", TemExternalEngineerDailyProjectCountAPI.as_view()),
    path("tem-saturation", TemEngineerSuccessCoreIndexAPI.as_view()),
    # 机台相关
    path("fib-utilization-internal", FIBInternalMachineTotalHoursAPI.as_view()),
    path("tem-utilization-internal", TEMInternalMachineTotalHoursAPI.as_view()),
    path("fib-utilization-external", FIBExternalMachineTotalHoursAPI.as_view()),
    path("tem-utilization-external", TEMExternalMachineTotalHoursAPI.as_view()),
    path("machine-saturation", InternalMachineWorkSaturationAPI.as_view()),

]
