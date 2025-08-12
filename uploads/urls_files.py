from django.urls import path
from .views_api import FileListAPIView

urlpatterns = [
    path('', FileListAPIView.as_view(), name='api-files'),
]
