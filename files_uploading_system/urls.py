from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (web)
    path('accounts/', include('accounts.urls')),

    # API endpoints (match spec)
    path('api/initiate-payment/', include('payments.urls_initiate')),
    path('api/payment/success/', include('payments.urls_success')),
    path('api/transactions/', include('payments.urls_transactions')),

    path('api/upload/', include('uploads.urls_upload')),
    path('api/files/', include('uploads.urls_files')),

    path('api/activity/', include('activity.urls')),

    # dashboard and web upload (web view)
    path('', include('uploads.urls_web')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
