from django.urls import path
from .views import ActivityListAPIView

urlpatterns = [
    path('', ActivityListAPIView.as_view(), name='api-activity'),
]
