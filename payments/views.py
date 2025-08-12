import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.utils import timezone
from .models import PaymentTransaction
from activity.models import ActivityLog
from django.conf import settings

try:
    from aamarpay.aamarpay import aamarPay
except Exception:
    aamarPay = None

class InitiatePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # create a transaction id
        transaction_id = f"{request.user.id}-{int(time.time())}"

        # create a pending record
        PaymentTransaction.objects.create(
            user=request.user,
            transaction_id=transaction_id,
            amount=100.00,
            status='pending',
            gateway_response={'initiated': True},
        )

        # try to use aamarpay package if available
        if aamarPay:
            pay = aamarPay(
                isSandbox=True,
                store_id='aamarpaytest',
                signature_key='dbb74894e82415a2f7ff0ec3a97e4183',
                transactionAmount=100,
                transactionId=transaction_id,
                returnUrl=request.build_absolute_uri('/api/payment/success/')
            )
            try:
                payment_url = pay.payment()
                return Response({'payment_url': payment_url})
            except Exception:
                # fallback
                return Response({'payment_url': f'https://sandbox.aamarpay.com/paynow.php?track={transaction_id}'})

        # fallback URL (user can open manually)
        return Response({'payment_url': f'https://sandbox.aamarpay.com/paynow.php?track={transaction_id}'})

class PaymentSuccessAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        track = request.GET.get('track') or request.GET.get('tran_id') or request.GET.get('transaction_id')
        if not track:
            return Response({'error': 'Missing track parameter'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tx = PaymentTransaction.objects.get(transaction_id=track)
            tx.status = 'completed'
            tx.gateway_response = tx.gateway_response or {}
            tx.gateway_response['verified_at'] = timezone.now().isoformat()
            tx.save()

            ActivityLog.objects.create(
                user=tx.user,
                action='Payment completed',
                metadata={'transaction_id': tx.transaction_id, 'amount': float(tx.amount)},
            )
            return Response({'message': 'Payment marked completed. You can now upload files.'})
        except PaymentTransaction.DoesNotExist:
            return Response({'error': 'Invalid transaction id'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.generics import ListAPIView
from .serializers import PaymentTransactionSerializer
class TransactionListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentTransactionSerializer

    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user).order_by('-timestamp')
