from django.urls import path
from .views import InitiatePaymentAPIView

urlpatterns = [
    path('', InitiatePaymentAPIView.as_view(), name='initiate-payment'),
]
