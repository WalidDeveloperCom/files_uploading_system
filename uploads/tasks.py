from celery import shared_task
from .models import FileUpload
import docx

@shared_task
def process_file_word_count(file_upload_id):
    try:
        file_upload = FileUpload.objects.get(id=file_upload_id)
        file_path = file_upload.file.path
        word_count = 0

        if file_upload.filename.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                word_count = len(content.split())
        elif file_upload.filename.lower().endswith('.docx'):
            doc = docx.Document(file_path)
            word_count = sum(len(p.text.split()) for p in doc.paragraphs)
        else:
            file_upload.status = 'failed'
            file_upload.save()
            return

        file_upload.word_count = word_count
        file_upload.status = 'completed'
        file_upload.save()

        from activity.models import ActivityLog
        ActivityLog.objects.create(
            user=file_upload.user,
            action='File processed',
            metadata={'filename': file_upload.filename, 'word_count': word_count}
        )
    except Exception as e:
        try:
            file_upload.status = 'failed'
            file_upload.save()
        except Exception:
            pass
