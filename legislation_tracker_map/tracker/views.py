from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def prefs(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'prefs.html', {'form': form})

@login_required
def manage_uploads(request):
    upload_dir = f'{settings.MEDIA_ROOT}/uploads/{request.user.username}/'

    # Ensure the directory exists
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        allowed_extensions = ['.zip', '.tar', '.tar.gz', '.tgz']
        file_extension = os.path.splitext(upload.name)[1].lower()

        if file_extension not in allowed_extensions:
            return render(request, 'manage_uploads.html', {
                'error': 'Invalid file type. Only zip, tar, tar.gz, and tgz files are allowed.',
                'files': os.listdir(upload_dir)
            })

        fs = FileSystemStorage(location=upload_dir)
        fs.save(upload.name, upload)
        return redirect('manage_uploads')

    files = os.listdir(upload_dir)
    return render(request, 'manage_uploads.html', {'files': files})