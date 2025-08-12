from django.urls import path
from .views_api import FileUploadAPIView

urlpatterns = [
    path('', FileUploadAPIView.as_view(), name='api-upload'),
]
