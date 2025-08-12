from django.contrib import admin
from .models import FileUpload

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in FileUpload._meta.fields]

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
