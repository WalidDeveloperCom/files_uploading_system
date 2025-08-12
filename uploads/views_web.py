from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from payments.models import PaymentTransaction
from .models import FileUpload
from activity.models import ActivityLog
from .tasks import process_file_word_count

@login_required
def dashboard_view(request):
    user = request.user
    files = FileUpload.objects.filter(user=user).order_by('-upload_time')
    activities = ActivityLog.objects.filter(user=user).order_by('-timestamp')
    transactions = PaymentTransaction.objects.filter(user=user).order_by('-timestamp')
    has_paid = PaymentTransaction.objects.filter(user=user, status='completed').exists()

    if request.method == 'POST' and 'file' in request.FILES:
        if not has_paid:
            return render(request, 'dashboard.html', {'files': files, 'activities': activities, 'transactions': transactions, 'has_paid': has_paid, 'error': 'Payment required.'})
        file_obj = request.FILES['file']
        instance = FileUpload.objects.create(user=user, file=file_obj, filename=file_obj.name, status='processing')
        process_file_word_count.delay(instance.id)
        return redirect('dashboard')

    return render(request, 'dashboard.html', {'files': files, 'activities': activities, 'transactions': transactions, 'has_paid': has_paid})
