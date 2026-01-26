from django.urls import path
from apps.order.views import OrderDeleteAPIView, OrderCreateAPIView, OrderUpdateAPIView, OrderListAPIView, \
    OrderByIdAPIView, OrderBatchDeleteAPIView

urlpatterns = [
    path("list", OrderListAPIView.as_view()),
    path("detail/<str:id>", OrderByIdAPIView.as_view()),
    path("delete/<str:id>", OrderDeleteAPIView.as_view()),
    path("batch-delete", OrderBatchDeleteAPIView.as_view()),
    path("create", OrderCreateAPIView.as_view()),
    path("update/<str:id>", OrderUpdateAPIView.as_view()),
]
