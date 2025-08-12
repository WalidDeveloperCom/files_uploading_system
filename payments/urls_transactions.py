from django.urls import path
from .views import TransactionListAPIView

urlpatterns = [
    path('', TransactionListAPIView.as_view(), name='payment-transactions'),
]
