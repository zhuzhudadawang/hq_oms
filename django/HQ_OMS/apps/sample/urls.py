from django.urls import path
from apps.sample.views import (SampleUpdateAPIView, SampleByIdAPIView,
                               DeleteSampleAPIView, SampleCreateAPIView, SampleListAPIView, SampleCountView)

urlpatterns = [
    path("detail/<str:id>", SampleByIdAPIView.as_view()),
    path("list", SampleListAPIView.as_view()),
    path("create", SampleCreateAPIView.as_view()),
    path("delete/<str:id>", DeleteSampleAPIView.as_view()),
    path("update/<str:id>", SampleUpdateAPIView.as_view()),

    path("count", SampleCountView.as_view()),


]
