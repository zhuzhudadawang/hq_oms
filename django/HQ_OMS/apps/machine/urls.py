from django.urls import path
from apps.machine.views import (MachineListAPIView, MachineRecordByDeviceCode, MachineUsageRecordDeleteAPIView,
                                MachineUsageRecordCreateAPIView, MachineUsageRecordUpdateAPIView, BatchDeleteAPIView,
                                DurationMinutesSumAPIView)

urlpatterns = [
    path("list", MachineListAPIView.as_view()),
    path("detail/<str:id>", MachineRecordByDeviceCode.as_view()),
    path("delete/<str:id>", MachineUsageRecordDeleteAPIView.as_view()),
    path("batch-delete", BatchDeleteAPIView.as_view()),
    path("create", MachineUsageRecordCreateAPIView.as_view()),
    path("update/<str:id>", MachineUsageRecordUpdateAPIView.as_view()),
    path("test", DurationMinutesSumAPIView.as_view()),
]
