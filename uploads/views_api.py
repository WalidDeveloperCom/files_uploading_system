from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .models import FileUpload
from .serializers import FileUploadSerializer
from payments.models import PaymentTransaction
from .tasks import process_file_word_count

class FileUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # check payment
        has_paid = PaymentTransaction.objects.filter(user=request.user, status='completed').exists()
        if not has_paid:
            return Response({'error': 'Payment required before uploading files.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']
            instance = FileUpload.objects.create(
                user=request.user,
                file=file_obj,
                filename=file_obj.name,
                status='processing'
            )
            process_file_word_count.delay(instance.id)
            return Response(FileUploadSerializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileUploadSerializer

    def get_queryset(self):
        return FileUpload.objects.filter(user=self.request.user).order_by('-upload_time')
