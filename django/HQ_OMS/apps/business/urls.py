from django.urls import path
from .views import FibTemEstimatedRevenueAPI, ZhuhaiEstimatedRevenueAPI

urlpatterns = [
    path("fib-tem-estimated-revenue", FibTemEstimatedRevenueAPI.as_view()),
    path("zhuhai-estimated-revenue", ZhuhaiEstimatedRevenueAPI.as_view()),
]
