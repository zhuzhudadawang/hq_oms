from django.urls import path
from apps.process.views import ProcessCreateAPIView, ProcessUpdateAPIView, \
    ProcessDeleteAPIView, ProcessByIdAPIView, ProcessListAPIView

urlpatterns = [
    path('create', ProcessCreateAPIView.as_view()),
    path('update/<str:id>', ProcessUpdateAPIView.as_view()),
    path('detail/<str:id>', ProcessByIdAPIView.as_view()),
    path('list', ProcessListAPIView.as_view()),
    path('delete/<str:id>', ProcessDeleteAPIView.as_view()),
]
