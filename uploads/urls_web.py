from django.urls import path
from .views_web import dashboard_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
]
