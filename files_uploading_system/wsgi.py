import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'files_uploading_system.settings')

application = get_wsgi_application()
