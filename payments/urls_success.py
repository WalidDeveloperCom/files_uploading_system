from django.urls import path
from .views import PaymentSuccessAPIView

urlpatterns = [
    path('', PaymentSuccessAPIView.as_view(), name='payment-success'),
]
