from rest_framework import serializers
from .models import FileUpload
import os

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'filename', 'file', 'upload_time', 'status', 'word_count']
        read_only_fields = ['status', 'word_count', 'upload_time']

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in ['.txt', '.docx']:
            raise serializers.ValidationError('Unsupported file extension.')
        return value
