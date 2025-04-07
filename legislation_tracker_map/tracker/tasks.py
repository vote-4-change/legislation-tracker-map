from celery import shared_task
from django.conf import settings
from .models import UploadedFile
import os
import tarfile
import zipfile
import shutil

@shared_task
def process_uploads():
    upload_base_dir = f'{settings.MEDIA_ROOT}/uploads/'
    temp_dir = f'{settings.MEDIA_ROOT}/temp/'

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for uploaded_file in UploadedFile.objects.filter(processed=False):
        file_path = os.path.join(upload_base_dir, uploaded_file.user.username, uploaded_file.filename)
        if os.path.exists(file_path):
            if file_path.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            elif file_path.endswith(('.tar', '.tar.gz', '.tgz')):
                with tarfile.open(file_path, 'r:*') as tar_ref:
                    tar_ref.extractall(temp_dir)

            # Mark the file as processed
            uploaded_file.processed = True
            uploaded_file.save()

            # Clean up the temporary directory
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)